"""Strategy loading for the unified pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, model_validator


class SectionConfig(BaseModel):
    """Configuration for a single pipeline section."""

    id: str
    title: str
    mode: Literal["llm", "hybrid", "structured"]
    kind: str = "body"
    word_target: int = 0
    depends_on: list[str] = Field(default_factory=list)
    quality_category: str | None = None
    llm_prompt_hint: str | None = None


class QualityConfig(BaseModel):
    """Quality thresholds for a strategy."""

    pass_threshold: int = 85
    max_refinement_iterations: int = 3
    categories: list[str] = Field(default_factory=list)


class CompilationConfig(BaseModel):
    """Compilation settings for final document assembly."""

    format: str = "docx"
    renderer: str
    preamble: list[str] = Field(default_factory=list)
    postprocess: list[str] = Field(default_factory=list)


class StrategyConfig(BaseModel):
    """Top-level strategy configuration loaded from JSON."""

    document_type: str
    display_name: str
    plugin: str
    sections: list[SectionConfig]
    quality: QualityConfig = Field(default_factory=QualityConfig)
    compilation: CompilationConfig

    @model_validator(mode="after")
    def validate_sections(self) -> "StrategyConfig":
        section_ids = [section.id for section in self.sections]
        unique_ids = set(section_ids)
        if len(unique_ids) != len(section_ids):
            duplicates: list[str] = []
            seen: set[str] = set()
            for section_id in section_ids:
                if section_id in seen and section_id not in duplicates:
                    duplicates.append(section_id)
                seen.add(section_id)
            raise ValueError(f"Duplicate section IDs: {', '.join(duplicates)}")

        unknown_dependencies = sorted(
            {
                dependency
                for section in self.sections
                for dependency in section.depends_on
                if dependency not in unique_ids
            }
        )
        if unknown_dependencies:
            raise ValueError(
                "Unknown depends_on references: "
                + ", ".join(unknown_dependencies)
            )
        return self


class StrategyLoader:
    """Loads strategy JSON files from the engine strategies directory."""

    def __init__(self, strategies_dir: str | Path | None = None):
        if strategies_dir is None:
            strategies_dir = Path(__file__).with_name("strategies")
        self._strategies_dir = Path(strategies_dir)

    @property
    def strategies_dir(self) -> Path:
        return self._strategies_dir

    def load(self, doc_type: str) -> StrategyConfig:
        path = self._strategies_dir / f"{doc_type}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        return StrategyConfig.model_validate(payload)

    def list_available(self) -> list[str]:
        if not self._strategies_dir.exists():
            return []
        return sorted(path.stem for path in self._strategies_dir.glob("*.json"))
