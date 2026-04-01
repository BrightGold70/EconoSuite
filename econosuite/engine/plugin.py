"""PipelinePlugin ABC — domain-specific hooks for the unified engine.

Design Ref: §2.6 — 4 abstract + 2 optional hooks.
Plugins adapt domain logic (protocol ICH, manuscript IMRaD) to the generic engine pipeline.
"""

from __future__ import annotations

import importlib
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable

logger = logging.getLogger(__name__)

# ── Plugin Registry ──────────────────────────────────────────────────────────

PLUGIN_REGISTRY: dict[str, str] = {
    "ProtocolPlugin": "protocol.protocol_plugin.ProtocolPlugin",
    "ManuscriptPlugin": "tools.manuscript_plugin.ManuscriptPlugin",
    "CSAPlugin": "engine.plugins.csa_plugin.CSAPlugin",
}


def resolve_plugin(name: str) -> type["PipelinePlugin"]:
    """Resolve a plugin name to its class via importlib.

    Accepts either a registry key (e.g. ``"ProtocolPlugin"``) or a
    fully-qualified dotted path (e.g. ``"protocol.protocol_plugin.ProtocolPlugin"``).
    """
    dotted = PLUGIN_REGISTRY.get(name, name)
    module_path, _, class_name = dotted.rpartition(".")
    if not module_path:
        raise ValueError(f"Cannot resolve plugin: {name!r}")
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    if not (isinstance(cls, type) and issubclass(cls, PipelinePlugin)):
        raise TypeError(f"{dotted} is not a PipelinePlugin subclass")
    return cls


# ── Abstract Base ─────────────────────────────────────────────────────────────

class PipelinePlugin(ABC):
    """Domain-specific hooks invoked by UnifiedEngine at well-defined points.

    Subclasses implement domain logic (ICH compliance, IMRAD structure, etc.)
    while the engine handles orchestration, DAG execution, and block storage.
    """

    # ── 4 Abstract Hooks (required) ──────────────────────────────────────────

    @abstractmethod
    def build_context(
        self,
        section_id: str,
        strategy: Any,
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Build domain-specific context dict for a section.

        Called before prompt construction. Returns keys consumed by
        ``enrich_prompt`` (e.g. regulatory requirements, PICO context).
        """

    @abstractmethod
    def enrich_prompt(
        self,
        section_id: str,
        base_prompt: str,
        context: dict[str, Any],
    ) -> str:
        """Inject domain rules into the LLM prompt.

        Receives the generic prompt and the context from ``build_context``.
        Returns the final prompt string sent to the triad drafter.
        """

    @abstractmethod
    def post_validate(
        self,
        section_id: str,
        content: str,
        evidence: list[dict[str, Any]],
    ) -> list[str]:
        """Run domain-specific checks after generation.

        Returns a list of issue strings (empty = no issues).
        E.g. ICH compliance checks, reporting guideline verification.
        """

    @abstractmethod
    def post_compile(
        self,
        config: Any,
        block_store: Any,
        strategy: Any,
    ) -> None:
        """Enrich assembled document with domain artifacts.

        Called after quality scoring, before DOCX assembly.
        E.g. inject tables, figures, CRF forms, SAP appendices.
        """

    # ── 2 Optional Hooks (with defaults) ─────────────────────────────────────

    def create_triad(self, llm_provider: Any) -> tuple[type, Any] | None:
        """Return (TriadClass, registry) tuple for domain-specific orchestration.

        Default returns (UniversalTriadOrchestrator, build_default_registry()).
        Plugins can override to customize triad configuration.
        Returns None if triad imports are unavailable.
        """
        try:
            from tools.triad.section_config import build_default_registry
            from tools.triad.universal_orchestrator import UniversalTriadOrchestrator
            return UniversalTriadOrchestrator, build_default_registry()
        except ImportError:
            return None

    def get_preamble_renderers(
        self,
        config: Any,
        strategy: Any,
    ) -> list[Callable]:
        """Return callables that render DOCX preamble pages.

        Default returns an empty list (no preamble — typical for manuscripts).
        Each callable receives a ``python-docx Document`` and renders in-place.
        """
        return []
