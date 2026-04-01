"""Shared adapter logic for routing CLI commands through UnifiedEngine."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def run_via_engine(
    document_type: str,
    project_dir: str | Path,
    llm_provider: Any = None,
    pico: Any = None,
    design: Any = None,
    evidence_articles: list[dict[str, Any]] | None = None,
    nlm_context: str = "",
    max_workers: int = 4,
    dataset_path: str | Path | None = None,
) -> Any:
    """Run document generation through UnifiedEngine.

    Shared by protocol_adapter and manuscript_adapter.

    Returns:
        EngineResult with docx_path, quality_score, block_manifest, etc.
    """
    from engine.unified_engine import EngineConfig, UnifiedEngine

    config = EngineConfig(
        document_type=document_type,
        project_dir=str(project_dir),
        llm_provider=llm_provider,
        pico=pico,
        design=design,
        evidence_articles=evidence_articles or [],
        max_workers=max_workers,
        nlm_context=nlm_context,
        dataset_path=str(dataset_path) if dataset_path else None,
    )

    engine = UnifiedEngine(config)
    result = engine.run()

    logger.info(
        "%s generated via unified engine: %s (quality: %.1f, passed: %s)",
        document_type, result.docx_path, result.quality_score, result.quality_passed,
    )
    return result
