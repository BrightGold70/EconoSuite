"""Unified Block Storage — manages document sections as individual .md files with YAML front matter.

Supports both Protocol (ICH E6) and Manuscript (IMRAD/Systematic Review) workflows
by unifying ProtocolSectionMeta and BlockMetadata into a single schema.
"""

from __future__ import annotations

import logging
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Dict, List, Tuple
from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)

# ── Pydantic Models ───────────────────────────────────────────────────────────

class BlockOutput(BaseModel):
    """Unified metadata for a document section block."""
    # Identity
    section_id: str
    title: str
    
    # Classification
    kind: str = "body"  # front_matter | body | back_matter
    mode: str = "llm"   # structured | hybrid | llm
    parent: Optional[str] = None
    template: str = ""
    guideline_item: str = ""
    
    # Status
    status: str = "pending"  # pending | scaffold | draft | validated | refined | final
    iteration: int = 0
    
    # Word Counts
    word_target: int = 0
    draft_word_target: int = 0
    actual_words: int = 0
    
    # Quality & Evidence
    score: Optional[float] = None
    synthesis_chars: int = 0
    grounding_coverage: Optional[float] = None
    grounding_flags: int = 0
    evidence_tags: Dict[str, int] = Field(default_factory=dict)
    sources: List[str] = Field(default_factory=list)
    
    # Protocol-specific
    validator_pass: bool = False
    regulatory_check: Optional[str] = None
    
    # Timestamps
    created_at: str = ""
    updated_at: str = ""

    @model_validator(mode="before")
    @classmethod
    def normalize_legacy_keys(cls, data: Any) -> Any:
        """Accept legacy keys from ProtocolBlockManager and old tools.BlockManager."""
        if not isinstance(data, dict):
            return data
        # Mapping legacy keys to new unified keys
        mappings = {
            "key": "section_id",
            "heading": "title",
            "last_updated": "updated_at",
            "created": "created_at",
            "updated": "updated_at",
        }
        for old_key, new_key in mappings.items():
            if old_key in data and new_key not in data:
                data[new_key] = data.pop(old_key)
        return data

# ── Block Store ───────────────────────────────────────────────────────────────

class BlockStore:
    """Manages section-based storage for unified pipelines."""

    def __init__(self, project_dir: Path | str, subdirectory: str = "sections", partitioned: bool = False):
        self.project_dir = Path(project_dir)
        self.sections_dir = self.project_dir / subdirectory
        self.partitioned = partitioned
        self._cache: dict[str, tuple[str, "BlockOutput"]] = {}

        # Subdirectories for partitioned storage (Mellel-style)
        self.kind_dirs = {
            "front_matter": "front",
            "body": "body",
            "back_matter": "back",
        }

    def scaffold(self, strategy: Any) -> List[BlockOutput]:
        """Create initial section files based on a StrategyConfig."""
        self.sections_dir.mkdir(parents=True, exist_ok=True)
        results = []
        
        now = datetime.now(timezone.utc).isoformat()
        
        sections = getattr(strategy, "sections", [])
        for sec in sections:
            # Handle both object-based and dict-based strategies
            # SectionConfig uses 'id', legacy code may use 'section_id'
            if isinstance(sec, dict):
                sid = sec.get("section_id") or sec.get("id")
                title = sec.get("title", sid)
                mode = sec.get("mode", "llm")
                kind = sec.get("kind", "body")
            else:
                sid = getattr(sec, "section_id", None) or getattr(sec, "id", None)
                title = getattr(sec, "title", sid)
                mode = getattr(sec, "mode", "llm")
                kind = getattr(sec, "kind", "body")
            
            meta = BlockOutput(
                section_id=sid,
                title=title,
                mode=mode,
                kind=kind,
                created_at=now,
                updated_at=now,
                status="scaffold"
            )
            
            self.write(sid, f"# {title}\n\n", meta.model_dump())
            results.append(meta)
            
        logger.info("Scaffolded %d sections in %s", len(results), self.sections_dir)
        return results

    def read(self, section_id: str) -> Tuple[str, BlockOutput]:
        """Read a section file, returning (content, BlockOutput). Uses in-memory cache."""
        if section_id in self._cache:
            return self._cache[section_id]

        path = self._resolve_path(section_id)
        text = path.read_text(encoding="utf-8")
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                metadata_dict = yaml.safe_load(parts[1]) or {}
                content = parts[2].strip()
                if "section_id" not in metadata_dict and "key" not in metadata_dict:
                    metadata_dict["section_id"] = section_id
                result = (content, BlockOutput(**metadata_dict))
                self._cache[section_id] = result
                return result

        result = (text, BlockOutput(section_id=section_id, title=section_id))
        self._cache[section_id] = result
        return result

    def _resolve_path(self, section_id: str, kind: str = "body") -> Path:
        """Resolve file path for a section, using EAFP pattern."""
        path = self._get_path(section_id, kind)
        if path.exists():
            return path
        if self.partitioned:
            fallback = self.sections_dir / f"{section_id}.md"
            if fallback.exists():
                return fallback
            for kd in self.kind_dirs.values():
                p = self.sections_dir / kd / f"{section_id}.md"
                if p.exists():
                    return p
        raise FileNotFoundError(f"Section block not found: {section_id} at {path}")

    def write(self, section_id: str, content: str, metadata: Dict[str, Any] | BlockOutput) -> BlockOutput:
        """Write section content with updated YAML front matter."""
        if isinstance(metadata, BlockOutput):
            meta_obj = metadata
        else:
            # Merge with existing if available
            try:
                _, existing_meta = self.read(section_id)
                merged = {**existing_meta.model_dump(), **metadata}
                meta_obj = BlockOutput(**merged)
            except FileNotFoundError:
                # New block
                if "section_id" not in metadata:
                    metadata["section_id"] = section_id
                if "title" not in metadata:
                    metadata["title"] = section_id
                meta_obj = BlockOutput(**metadata)
        
        meta_obj.updated_at = datetime.now(timezone.utc).isoformat()
        if not meta_obj.created_at:
            meta_obj.created_at = meta_obj.updated_at
            
        # Update word count
        meta_obj.actual_words = len(content.split()) if content else 0

        path = self._get_path(section_id, meta_obj.kind)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        yaml_str = yaml.dump(meta_obj.model_dump(exclude_none=True), default_flow_style=False, sort_keys=False, allow_unicode=True)
        path.write_text(f"---\n{yaml_str}---\n\n{content}\n", encoding="utf-8")
        self._cache[section_id] = (content, meta_obj)
        return meta_obj

    def read_section(self, section_id: str) -> Dict[str, Any]:
        """Legacy-compatible read returning {'content': str, 'metadata': dict}."""
        content, meta = self.read(section_id)
        return {"content": content, "metadata": meta.model_dump()}

    def write_section(self, section_id: str, content: str, metadata: Dict[str, Any] | None = None) -> None:
        """Legacy-compatible write accepting section_id, content, metadata."""
        self.write(section_id, content, metadata or {})

    def get_manifest(self) -> Dict[str, Dict[str, Any]]:
        """Return all section metadata as a dictionary."""
        result = {}
        # Scan all .md files in sections_dir (recursive if partitioned)
        glob_pattern = "**/*.md" if self.partitioned else "*.md"
        for md_file in sorted(self.sections_dir.glob(glob_pattern)):
            if md_file.name.startswith("_"):
                continue
            section_id = md_file.stem
            try:
                _, meta = self.read(section_id)
                result[section_id] = meta.model_dump()
            except Exception as exc:
                logger.debug("Failed to read section %s: %s", section_id, exc)
        return result

    def assemble_markdown(self) -> str:
        """Concatenate all sections into a single markdown document."""
        parts = []
        manifest = self.get_manifest()
        # Order by filename for now; future: use strategy/manifest order
        for section_id in sorted(manifest.keys()):
            content, _ = self.read(section_id)
            parts.append(content)
        return "\n\n---\n\n".join(parts)

    def assemble_docx(self, output_path: Path | str, preamble_renderers: List[Any] = None) -> str:
        """Assemble DOCX from sections. Returns output path string."""
        from docx import Document
        from protocol.docx_renderer import DocxRenderer

        doc = Document()
        renderer = DocxRenderer(table_style="Table Grid")

        # Render preamble (Title Page, Synopsis, etc.)
        for renderer_fn in (preamble_renderers or []):
            if callable(renderer_fn):
                renderer_fn(doc)
            elif hasattr(renderer_fn, "render") and callable(renderer_fn.render):
                renderer_fn.render(doc)

        manifest = self.get_manifest()
        for section_id in sorted(manifest.keys()):
            content, meta = self.read(section_id)
            doc.add_heading(meta.title, level=1)
            renderer.render_markdown(doc, content)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(output_path))
        logger.info("Assembled DOCX: %s", output_path)
        return str(output_path)

    def _get_path(self, section_id: str, kind: str = "body") -> Path:
        """Resolve the file path for a section."""
        if self.partitioned:
            kind_dir = self.kind_dirs.get(kind, "body")
            return self.sections_dir / kind_dir / f"{section_id}.md"
        return self.sections_dir / f"{section_id}.md"
