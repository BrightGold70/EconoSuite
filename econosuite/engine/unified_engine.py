"""Unified Engine — orchestrates strategy → scaffold → DAG → triad → quality → compile.

Design Ref: §2.5 — Main orchestrator (FR-10, FR-14).
Thread-safe per-section execution via DAGResolver.execute().
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from engine.block_store import BlockStore
from engine.dag import DAGResolver, SectionNode
from engine.double_lock import AnchorSet, AuditResult, DoubleLockAuditor
from engine.plugin import PipelinePlugin, resolve_plugin
from engine.strategy import StrategyConfig, StrategyLoader

logger = logging.getLogger(__name__)


# ── Data Types ────────────────────────────────────────────────────────────────

@dataclass
class EngineConfig:
    """Input configuration for a unified engine run."""

    document_type: str
    project_dir: str | Path
    llm_provider: Any = None
    pico: Any = None
    design: Any = None
    evidence_articles: list[dict[str, Any]] = field(default_factory=list)
    dataset_path: str | Path | None = None  # FR-14: CSA R script input dataset
    max_workers: int = 4
    quality_threshold: int = 85
    nlm_context: str = ""


@dataclass
class SectionResult:
    """Per-section outcome from engine execution."""

    section_id: str
    content: str
    accepted: bool
    iterations: int = 1
    anchor_set: AnchorSet | None = None
    audit_result: AuditResult | None = None
    evidence_tags: dict[str, int] = field(default_factory=lambda: {"lit": 0, "csa": 0, "flag": 0})
    error: str | None = None


@dataclass
class EngineResult:
    """Final output from a complete engine run."""

    docx_path: str | None
    quality_score: float
    quality_passed: bool
    block_manifest: dict[str, dict]
    section_results: dict[str, SectionResult] = field(default_factory=dict)
    evidence_stats: dict[str, Any] = field(default_factory=dict)


# ── Engine ────────────────────────────────────────────────────────────────────

class UnifiedEngine:
    """Orchestrates the full document generation pipeline.

    Pipeline stages:
        1. Strategy load
        2. Block scaffold
        3. DAG resolve
        4. Per-section: [pre_anchor → plugin.build_context → plugin.enrich_prompt →
           triad loop → plugin.post_validate → post_audit → block_store.write]
        5. Quality scoring + refinement
        6. plugin.post_compile (tables/figures/CRF)
        7. DOCX assembly (preamble + DocxRenderer)
    """

    def __init__(
        self,
        config: EngineConfig,
        strategy_loader: StrategyLoader | None = None,
    ) -> None:
        self._config = config
        self._project_dir = Path(config.project_dir)
        self._loader = strategy_loader or StrategyLoader()

    def run(self) -> EngineResult:
        """Execute the full pipeline and return EngineResult."""
        cfg = self._config

        # 1. Strategy load
        strategy = self._loader.load(cfg.document_type)
        logger.info("Loaded strategy: %s (%d sections)", strategy.display_name, len(strategy.sections))

        # 2. Resolve plugin
        plugin = self._resolve_and_instantiate_plugin(strategy.plugin)

        # 3. Block scaffold
        block_store = BlockStore(self._project_dir)
        block_store.scaffold(strategy)

        # 4. Separate CSA nodes from content nodes
        csa_sections = [sec for sec in strategy.sections if sec.kind == "csa"]
        content_sections = [sec for sec in strategy.sections if sec.kind != "csa"]

        # 5. Execute CSA tasks first (FR-14: first-class R integration)
        csa_results: dict[str, Any] = {}
        if csa_sections and cfg.dataset_path:
            from engine.plugins.csa_plugin import CSAPlugin
            csa_plugin = CSAPlugin(dataset_path=cfg.dataset_path)
            for csa_node in csa_sections:
                csa_result = csa_plugin.run_task(csa_node.id)
                if csa_result.success:
                    csa_results[csa_node.id] = csa_result.output_data
                    logger.info("CSA task %s completed", csa_node.id)
                else:
                    logger.warning("CSA task %s failed: %s", csa_node.id, csa_result.error)
        elif csa_sections:
            logger.info("CSA sections found but no dataset_path — skipping R execution")

        # 6. DAG resolve (content nodes only — CSA already executed)
        dag = DAGResolver()
        nodes = [
            SectionNode(id=sec.id, depends_on=[
                dep for dep in sec.depends_on if not dep.startswith("csa:")
            ])
            for sec in content_sections
        ]
        layers = dag.resolve(nodes)
        logger.info("DAG resolved: %d layers (%d content sections, %d CSA tasks done)",
                     len(layers), len(content_sections), len(csa_results))

        # 7. Create triad orchestrator (domain-specific or base)
        triad = plugin.create_triad(cfg.llm_provider)

        # 8. Create auditor and build anchor set once (avoids N+1 PubMed calls)
        auditor = DoubleLockAuditor()
        shared_anchor = auditor.pre_anchor(cfg.evidence_articles, cfg.document_type)

        # 7. Execute sections via DAG
        section_results: dict[str, SectionResult] = {}
        section_contents: dict[str, str] = {}
        section_map = {sec.id: sec for sec in strategy.sections}

        def run_section(section_id: str) -> SectionResult:
            return self._run_section(
                section_id=section_id,
                section_config=section_map[section_id],
                strategy=strategy,
                plugin=plugin,
                block_store=block_store,
                auditor=auditor,
                triad=triad,
                all_sections=section_contents,
                anchor_set=shared_anchor,
                csa_results=csa_results,
            )

        raw_results = dag.execute(layers, run_section, max_workers=cfg.max_workers)

        for sid, result in raw_results.items():
            if isinstance(result, Exception):
                section_results[sid] = SectionResult(
                    section_id=sid, content="", accepted=False,
                    error=str(result),
                )
            else:
                section_results[sid] = result
                if result.accepted:
                    section_contents[sid] = result.content

        # 8. Quality scoring + refinement loop
        max_refinements = strategy.quality.max_refinement_iterations
        quality_score = self._compute_quality(section_results, strategy)
        quality_passed = quality_score >= cfg.quality_threshold

        refinement_round = 0
        while not quality_passed and refinement_round < max_refinements:
            refinement_round += 1
            logger.info("Refinement round %d/%d (score: %.1f, threshold: %d)",
                         refinement_round, max_refinements, quality_score, cfg.quality_threshold)

            # Re-run only failed sections
            for sid, sr in list(section_results.items()):
                if sr.accepted or sr.error:
                    continue
                try:
                    rerun = self._run_section(
                        section_id=sid,
                        section_config=section_map[sid],
                        strategy=strategy,
                        plugin=plugin,
                        block_store=block_store,
                        auditor=auditor,
                        triad=triad,
                        all_sections=section_contents,
                        anchor_set=shared_anchor,
                        csa_results=csa_results,
                    )
                    section_results[sid] = rerun
                    if rerun.accepted:
                        section_contents[sid] = rerun.content
                except Exception as exc:
                    logger.warning("Refinement failed for %s: %s", sid, exc)

            quality_score = self._compute_quality(section_results, strategy)
            quality_passed = quality_score >= cfg.quality_threshold

        logger.info("Quality score: %.1f (threshold: %d, passed: %s, refinements: %d)",
                     quality_score, cfg.quality_threshold, quality_passed, refinement_round)

        # 9. Plugin post-compile (tables, figures, CRF, SAP)
        plugin.post_compile(cfg, block_store, strategy)

        # 10. DOCX assembly
        docx_path = self._assemble_docx(block_store, plugin, cfg, strategy)

        # 11. Evidence stats
        evidence_stats = self._compute_evidence_stats(section_results)

        return EngineResult(
            docx_path=docx_path,
            quality_score=quality_score,
            quality_passed=quality_passed,
            block_manifest=block_store.get_manifest(),
            section_results=section_results,
            evidence_stats=evidence_stats,
        )

    # ── Per-Section Runner (thread-safe) ──────────────────────────────────────

    def _run_section(
        self,
        section_id: str,
        section_config: Any,
        strategy: StrategyConfig,
        plugin: PipelinePlugin,
        block_store: BlockStore,
        auditor: DoubleLockAuditor,
        triad: Any,
        all_sections: dict[str, str],
        anchor_set: AnchorSet | None = None,
        csa_results: dict[str, Any] | None = None,
    ) -> SectionResult:
        """Run a single section through the pipeline (thread-safe)."""
        cfg = self._config
        evidence = cfg.evidence_articles

        # Use pre-built anchor set (batched once) or build per-section as fallback
        if anchor_set is None:
            anchor_set = auditor.pre_anchor(evidence, section_id)

        # Plugin: build domain context
        context = plugin.build_context(section_id, strategy, evidence)

        # FR-14: Inject CSA results into context for sections that depend on CSA tasks
        if csa_results:
            deps = getattr(section_config, "depends_on", [])
            for dep in deps:
                if dep.startswith("csa:") and dep in csa_results:
                    context.setdefault("csa_stats", {}).update(csa_results[dep])
                    logger.info("Injected CSA output %s into context for %s", dep, section_id)

        # Build base prompt from strategy hint
        base_prompt = getattr(section_config, "llm_prompt_hint", "") or ""

        # Plugin: enrich prompt with domain rules
        prompt = plugin.enrich_prompt(section_id, base_prompt, context)

        # Generate content via UniversalTriadOrchestrator (Phase I integration)
        gen_result = self._generate_content(
            section_id, prompt, triad, cfg,
            context=context,
            existing_sections=all_sections,
        )
        content = gen_result.content

        # Plugin: post-validate
        issues = plugin.post_validate(section_id, content, evidence)

        # Post-Audit: verify citations
        audit_result = auditor.post_audit(section_id, content, anchor_set)

        # Determine acceptance (triad + plugin + audit must all pass)
        accepted = gen_result.accepted and len(issues) == 0 and audit_result.passed

        # Merge evidence tags from triad result
        lit_count = audit_result.total_citations
        flag_count = audit_result.flag_count

        # Write to block store
        block_store.write(section_id, content, {
            "status": "validated" if accepted else "draft",
            "score": audit_result.grounding_ratio,
            "grounding_coverage": audit_result.grounding_ratio,
            "grounding_flags": audit_result.flag_count,
            "title": getattr(section_config, "title", section_id),
            "iteration": gen_result.iterations,
        })

        return SectionResult(
            section_id=section_id,
            content=content,
            accepted=accepted,
            iterations=gen_result.iterations,
            anchor_set=anchor_set,
            audit_result=audit_result,
            evidence_tags=gen_result.evidence_tags or {"lit": lit_count, "csa": 0, "flag": flag_count},
        )

    # ── Content Generation ────────────────────────────────────────────────────

    def _generate_content(
        self,
        section_id: str,
        prompt: str,
        triad: Any,
        config: EngineConfig,
        *,
        context: dict[str, Any] | None = None,
        existing_sections: dict[str, str] | None = None,
    ) -> SectionResult:
        """Generate section content via UniversalTriadOrchestrator or direct LLM.

        Design Ref: §3.7 — UnifiedEngine wires UniversalTriadOrchestrator from Phase I.
        Returns a SectionResult with content, iterations, evidence_tags.
        """
        # Phase I integration: use UniversalTriadOrchestrator with SectionConfig
        if config.llm_provider is not None:
            try:
                from tools.triad.section_config import build_default_registry
                from tools.triad.universal_orchestrator import UniversalTriadOrchestrator

                registry = build_default_registry()
                # Map plugin name to section type for registry lookup
                section_type = self._plugin_to_section_type(triad)
                if registry.has(section_type, section_id):
                    section_config = registry.get(section_type, section_id)
                else:
                    section_config = registry.get(section_type, "_default") if registry.has(section_type, "_default") else None

                if section_config:
                    orchestrator = UniversalTriadOrchestrator(
                        llm_provider=config.llm_provider,
                        config=section_config,
                        evidence_articles=config.evidence_articles,
                        existing_sections=existing_sections or {},
                        design=config.design,
                        nlm_context=context.get("nlm_context", config.nlm_context) if context else config.nlm_context,
                    )
                    triad_ctx = context or {}
                    triad_ctx["evidence"] = config.evidence_articles
                    triad_ctx["nlm_context"] = context.get("nlm_context", config.nlm_context) if context else config.nlm_context
                    triad_ctx["design"] = config.design
                    triad_ctx["existing_sections"] = existing_sections or {}

                    base_result = orchestrator.run_section(section_id, triad_ctx)
                    return SectionResult(
                        section_id=section_id,
                        content=base_result.final_draft,
                        accepted=base_result.accepted,
                        iterations=base_result.iterations,
                        evidence_tags=base_result.evidence_tags,
                    )
            except Exception as exc:
                logger.warning("UniversalTriadOrchestrator failed for %s: %s, falling back", section_id, exc)

        # Legacy triad fallback
        if triad is not None and hasattr(triad, "run_section"):
            result = triad.run_section(section_id, prompt)
            content = result.content if hasattr(result, "content") else str(result)
            return SectionResult(section_id=section_id, content=content, accepted=True)

        # Direct LLM fallback
        llm = config.llm_provider
        if llm is not None and hasattr(llm, "chat"):
            content = llm.chat(
                system="You are a clinical document writer. Follow the prompt instructions precisely.",
                user=prompt,
            )
            return SectionResult(section_id=section_id, content=content, accepted=True)

        # No LLM available — return placeholder
        return SectionResult(
            section_id=section_id,
            content=f"[Placeholder for {section_id}: {prompt[:100]}]",
            accepted=False,
        )

    @staticmethod
    def _plugin_to_section_type(triad: Any) -> str:
        """Map plugin/triad to section type for SectionConfigRegistry lookup."""
        if triad is not None:
            type_name = type(triad).__name__
            if "Protocol" in type_name:
                return "protocol"
            if "Manuscript" in type_name:
                return "manuscript"
        return "protocol"  # default

    # ── Quality Scoring ───────────────────────────────────────────────────────

    @staticmethod
    def _compute_quality(
        results: dict[str, SectionResult],
        strategy: StrategyConfig,
    ) -> float:
        """Compute overall quality score from section results."""
        if not results:
            return 0.0
        accepted = sum(1 for r in results.values() if r.accepted)
        total = len(results)
        # Base score from acceptance ratio
        acceptance_ratio = accepted / total
        # Weighted by grounding ratios
        grounding_sum = sum(
            r.audit_result.grounding_ratio
            for r in results.values()
            if r.audit_result is not None
        )
        grounding_avg = grounding_sum / total if total else 0.0
        # Combined: 60% acceptance + 40% grounding
        return round((acceptance_ratio * 60 + grounding_avg * 40), 1)

    # ── DOCX Assembly ─────────────────────────────────────────────────────────

    def _assemble_docx(
        self,
        block_store: BlockStore,
        plugin: PipelinePlugin,
        config: EngineConfig,
        strategy: StrategyConfig,
    ) -> str | None:
        """Assemble final DOCX from block store with plugin preamble."""
        if strategy.compilation.format != "docx":
            return None

        output_path = self._project_dir / f"{config.document_type}.docx"
        preamble = plugin.get_preamble_renderers(config, strategy)

        try:
            return block_store.assemble_docx(output_path, preamble_renderers=preamble)
        except Exception as exc:
            logger.error("DOCX assembly failed: %s", exc)
            return None

    # ── Evidence Stats ────────────────────────────────────────────────────────

    @staticmethod
    def _compute_evidence_stats(results: dict[str, SectionResult]) -> dict[str, Any]:
        """Aggregate evidence statistics across all sections."""
        total_lit = sum(r.evidence_tags.get("lit", 0) for r in results.values())
        total_flags = sum(r.evidence_tags.get("flag", 0) for r in results.values())
        total_verified = sum(
            r.audit_result.verified_count
            for r in results.values()
            if r.audit_result is not None
        )
        total_orphans = sum(
            len(r.audit_result.orphan_pmids)
            for r in results.values()
            if r.audit_result is not None
        )
        return {
            "total_citations": total_lit,
            "total_verified": total_verified,
            "total_orphans": total_orphans,
            "total_flags": total_flags,
        }

    # ── Plugin Resolution ─────────────────────────────────────────────────────

    @staticmethod
    def _resolve_and_instantiate_plugin(plugin_name: str) -> PipelinePlugin:
        """Resolve and instantiate a plugin by name."""
        cls = resolve_plugin(plugin_name)
        return cls()
