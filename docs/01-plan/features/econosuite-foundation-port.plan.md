---
template: plan
version: 1.0
feature: econosuite-foundation-port
date: 2026-04-28
author: Claude Code (Opus 4.7)
project: EconoSuite
status: Draft
supersedes: ~/.gemini/antigravity/brain/81f6874c-db7f-41fc-a1d4-7bc841f3cadc/implementation_plan.md.resolved (Antigravity-resolved scratch plan)
references:
  - /Users/kimhawk/Coding/EconoSuite/EconoSuite_Master_Architecture.md (target spec)
  - /Users/kimhawk/Coding/HemaSuite/HemaSuite_Architecture_Note.md (source-of-truth, 781 lines, §1–§14)
---

# EconoSuite Foundation Port — Planning Document

> **Summary**: Port HemaSuite's matured orchestration architecture (Unified Engine + KnowledgeOrchestrator + Daemon HTTP transport + Four-Axis Knowledge Model + Content-Integrity / NLM-Health pipelines + Asymmetric LightRAG) into EconoSuite, transforming the source-domain assumptions (clinical RCTs, biostatistics, HIPAA-aware aggregates) into the target domain (retrospective observational economics, identification-strategy-driven causal inference, AEA/QJE replication-package compliance, OMML math rendering). This is a 4-phase port, not a rewrite — every HemaSuite invariant has an EconoSuite analog except where the domain genuinely diverges (CRF → eliminated; CTCAE grading → replaced with AEA reporting checklists; clinical safety endpoints → replaced with parallel-trends and RDD validity tests). The "completed" status of the prior plan in `.pdca-status.json` reflected the Master Architecture spec only; this is the actionable porting plan that drives the Design and Do phases.

---

## Executive Summary

| Perspective | Content |
|---|---|
| **Problem** | EconoSuite needs HemaSuite's hardened orchestration foundation (Phase 0 daemon HTTP transport, KO single-source gateway, four-axis grounding, asymmetric LightRAG, NLM hard-dependency, content-integrity, scaffold-echo-guard, unified engines for tables/figures/references), but with seven cross-disciplinary translations applied: epistemology (RCT → identification-strategy), data (HIPAA aggregates → administrative panels with anonymization), statistics (Cox/KM → TWFE/IV/DiD/RDD), standard errors (independent → clustered/multi-way), graphics (KM/Forest → Event Study/McCrary), theory-first mandate (none → required structural model preamble), publication standards (CONSORT → AEA/QJE/JEL). |
| **Solution** | Forked port of HemaSuite at `~/Coding/HemaSuite` into `~/Coding/EconoSuite`, executed in 4 phases. Phase 1 ports the daemon + invariants verbatim (HTTP `:8021`, KO gateway, four-axis model, NLM-Health, Content-Integrity), then layers EconoSuite-specific surfaces (`HardwareHealthGuard`, `ESA Bridge`, dynamic Mellel-style sectioning, EconoSyntax math rendering, AEA replication packager, anonymizer scrubber). Asymmetric LightRAG (compile on 192GB Mac Studio, query on 16GB MacBook) is treated as a hard runtime invariant from day 1, not a deployment afterthought. |
| **Function/UX Effect** | Operator runs `econosuite draft "topic"` (or feeds a Master Synopsis) and gets a fully-assembled, AEA/QJE-formatted DOCX manuscript with: (1) NLM-grounded literature synthesis, (2) ESA-engine-generated Stata regressions with multi-way clustered SEs, (3) Event Study / McCrary plots with mandatory alt-text, (4) OMML-rendered math under EconoSyntax conventions, (5) one-command-replicable Makefiles, (6) per-author disclosure PDFs, (7) double-blind anonymized submission package — with the same orchestration reliability that HemaSuite already delivers for clinical trials. |
| **Core Value** | Avoid 6+ months of independent reinvention by treating EconoSuite as a "domain reskin" of HemaSuite's invariant stack, while honoring the structural differences with first-class translations rather than after-the-fact patches. The asymmetric hardware design (192GB compile / 16GB query) is the unlock that makes the architecture viable on consumer hardware where Stata + LightRAG + LLM cannot coexist in RAM. |

---

## Architectural Decisions (Locked-In)

These three decisions are settled by the Antigravity-resolved scratch plan and are **not** revisitable inside this plan. Any change requires editing the Master Architecture first and re-deriving downstream FRs.

1. **Daemon Architecture Upgrade — HTTP, not Unix Socket.** Port HemaSuite's resilient FastAPI + uvicorn transport on `:8021` to the EconoSuite Antigravity Daemon. This replaces fragile Unix Socket IPC and guarantees stable, long-running NotebookLM polling under sustained ingest. Headless isolation enforced by routing STDIN to `/dev/null` so the daemon cannot be wedged by orphaned terminal reads.
2. **Asymmetric LightRAG.** Graph compilation runs **off-device** on a 192 GB Mac Studio using a high-precision indexing model (`qwen3.6:35b-a3b-mlx-bf16` or larger). The compiled artifact (entity / relationship / chunk vectors + `graph_chunk_entity_relation.graphml`) ships to the **16 GB MacBook**, where EconoSuite queries it with a sub-10 GB generation model (`qwen2.5:7b-q4_K_M`) plus a small embedding model. This is the only architecture that survives the 16 GB RAM ceiling alongside Stata.
3. **Active Stata Integration — `pystata` First.** EconoSuite does not just *generate* Stata code. It actively executes it via `pystata` (preferred) or subprocess `stata-mp` (fallback), captures coefficient matrices and clustered standard errors, and feeds them into `UnifiedTableEngine` for automated table compilation. Independent-observation SEs are forbidden in `manuscript_type=empirical`; multi-way clustered or 2-way CGM SEs are the default.

---

## Context Anchor

| Dimension | Content |
|---|---|
| **WHY** | HemaSuite has 7+ months of operational hardening (HTTP transport upgrade, NLM-Health pipeline, Content-Integrity guard, four-axis grounding, asymmetric LightRAG, single-source gateway). Re-deriving these invariants for EconoSuite from scratch would burn the same operator-hours, hit the same dead ends (silent NLM degradation, scaffold-token leakage, KV-slot crashes under sustained ingest, GPU contention across runners). Port the invariants; reskin the domain. |
| **WHO** | EconoSuite operator (researcher drafting an AEA/QJE submission); EconoSuite daemon (background orchestrator on `:8021`); the off-device Mac Studio compiling LightRAG indices nightly; Stata-mp running on the operator's MacBook for econometric estimation. |
| **RISK** | (1) **Domain leakage**: porting HemaSuite Python verbatim risks importing clinical-trial assumptions into econometric workflows (e.g., assuming `manuscript_type ∈ {clinical_trial, systematic_review, narrative_review}` instead of `{empirical, theoretical, review, short_comms, proposal}`). (2) **Hardware ceiling**: Stata is RAM-greedy; running a 27B+ parameter LLM in-process while Stata is doing covariance matrix work will OOM. The HardwareHealthGuard is a hard precondition, not a "nice to have". (3) **Math rendering correctness**: AEA reviewers will reject manuscripts with mis-typeset $\hat{\beta}$ or italic Roman operators ($Var$ instead of $\text{Var}$). Self-healing compilation loop is non-optional. (4) **Anonymization**: a single leaked author identifier in compiled PDF metadata blows the double-blind review. Pre-flight scrubber is a hard gate, not a warning. |
| **SUCCESS** | (a) `econosuite draft "topic"` produces a complete AEA-formatted DOCX with $\geq$ 3 ESA-generated regression tables, $\geq$ 2 Event Study / McCrary figures with mandated alt-text, JEL codes, AEA RCT registry footnote (where applicable), per-author disclosure PDFs, and a working `make all` replication Makefile, in $\leq$ 30 minutes wall-clock on the 16GB MacBook with the LightRAG index pre-shipped from Mac Studio. (b) Zero regressions vs HemaSuite's existing test suite for the ported invariants (NLM-Health, KO single-source gateway, four-axis grounding, scaffold-echo-guard, content-integrity). (c) HardwareHealthGuard hard-fails any attempt to load a generation LLM in-process on the 16GB machine. (d) AnonymizerScrubber strips author metadata from the compiled DOCX/PDF before the submission package is sealed. |
| **SCOPE** | `~/Coding/EconoSuite/` (entire repo). Touches: `econosuite/engine/`, `econosuite/phases/`, `econosuite/cli.py`, new modules under `econosuite/tools/`, new modules under `econosuite/protocol/` (replacing HemaSuite's CRF subsystem), `templates/`, `data/guidelines/` (econ-side: AEA + ICH + Stata reference docs), `scripts/compile_guidelines_db.py` (Mac Studio target). Out of scope for this plan: actual ESA estimator code (deferred to a v2 plan once the foundation lands), Tauri desktop UI (deferred indefinitely). |

---

## 1. Overview

### 1.1 Purpose

Establish the EconoSuite orchestration foundation by porting HemaSuite's invariant stack (§§1–14 of `HemaSuite_Architecture_Note.md`) under explicit translation discipline. After this plan ships, EconoSuite will have parity with HemaSuite on every cross-cutting concern (daemon HTTP, single-source gateway, four-axis grounding, NLM-Health, Content-Integrity, asymmetric LightRAG, unified engines for tables/figures/references), plus six EconoSuite-specific additions that have no HemaSuite analog (HardwareHealthGuard, ESA Bridge, EconoSyntax math rendering, dynamic Mellel-style sectioning, AnonymizerScrubber, Replication Packager).

### 1.2 Background

The Antigravity-resolved scratch plan (`implementation_plan.md.resolved`) and the EconoSuite Master Architecture together specify the *what*. This plan is the *how* — a phased, FR-tracked, success-criteria-bound execution roadmap that future-you can pick up at any phase and continue without re-deriving the design choices. It also surfaces non-obvious failure modes (hardware ceiling, math typesetting, anonymization) and codifies their mitigations as hard architectural invariants from day 1.

### 1.3 Relationship to Master Architecture

`EconoSuite_Master_Architecture.md` is the spec; this plan is the execution. Where the Master Architecture says "EconoSuite must do X", this plan says "we ship X via FR-N in Phase M, verified by SC-K, with risks R1/R2 mitigated by..." Both documents must agree at the FR/spec level. If a conflict surfaces during execution, edit the Master Architecture first (it's the spec) and revise this plan to match.

---

## 2. Scope

### 2.1 In Scope (4 Phases)

#### Phase 1 — Core Foundation & Daemon Porting

- [ ] **FR-01** Port HemaSuite daemon HTTP transport (FastAPI + uvicorn on `:8021`) → `econosuite/engine/agent_daemon.py`. Inherit DaemonLock, `GET /health`, AgentConfig with `http_port` env override (`ECONOSUITE_DAEMON_PORT`). **Headless isolation**: route STDIN to `/dev/null` at startup so terminal-detached daemons cannot wedge on orphaned reads (`EOFError`-on-read is the assertion). Verified by `tests/test_daemon_isolation.py`.
- [ ] **FR-02** Port `KnowledgeOrchestrator` (KO) → `econosuite/engine/knowledge_orchestrator.py`. KO is the **sole** evidence query gateway (per §11 of HemaSuite Note). Lazy accessors `_pubmed`, `_nlm`, `_lightrag`. Regression test `tests/test_ko_sole_query_gateway.py` ports verbatim from HemaSuite.
- [ ] **FR-03** Port the **Four-Axis Knowledge Model** (§12 of HemaSuite Note) with EconoSuite-specific axis renames:
  - **Evidence** axis → unchanged (NLM + PubMed + LightRAG econometric textbook KG)
  - **Data** axis → unchanged in semantics; producer changes from R-script (CSA) to ESA Bridge (R + Stata via `pystata`)
  - **Protocol** axis → renamed **Identification-Strategy** axis (`[IDENT-CONSISTENCY]` guard) — covers DiD/IV/RDD/Event Study choices, parallel-trends pre-tests, instrument exclusion-restriction declarations
  - **Interpretation** axis → unchanged (per-sentence routing of `<evidence>`/`<data>`/`<identification>` clauses)
- [ ] **FR-04** Port `[NLM-HEALTH]` Hard-Dependency Pipeline (§10) → `econosuite/engine/nlm_health.py`. `guard_nlm_call`, `attempt_maintenance`, `format_remediation`. `NLMHardFailure` raised on auth lapse / empty response.
- [ ] **FR-05** Port `[SCAFFOLD-GUARD]` Content-Integrity Pipeline (§9) → `econosuite/engine/triad/content_integrity.py`. Same 4 layers (daemon cleanup → triad iteration → best-of-N → KO-reservoir fallback). Same scaffold regex (`{feature}`, `{section}`, etc.) — invariant is domain-independent.
- [ ] **FR-06** Port `UnifiedEngine` orchestrator (§1.2 of Master Arch) → `econosuite/engine/unified_engine.py`. Composes the sub-engines (Table/Figure/Reference/Tri). Implements the **Five-Tier Execution Pipeline** — one DAG per `manuscript_type` ∈ `{empirical, theoretical, review, short_comms, proposal}` — with **Phase-level Checkpointing via `StateAdapter`** so the daemon can resume a partially-completed manuscript after a crash without re-running NLM polls or Stata fits. Checkpoint granularity: per-phase per-section, persisted as `.econosuite/checkpoints/{manuscript_id}/{phase}.json`.
- [ ] **FR-07** **NEW (no HemaSuite analog): Hardware Health Guard** → `econosuite/engine/hardware_health.py`. Public surface (locked-in by Antigravity-resolved plan §3.1.1):
  - `class HardwareHardFailure(Exception)` — raised on memory ceiling violation; never caught silently.
  - `def _get_system_memory_gb() -> float` — wraps `psutil.virtual_memory()` (`sysctl hw.memsize` on macOS).
  - `def _detect_loaded_generation_models() -> bool` — probes Ollama (`/api/ps`) and MLX runtime for resident generation-class models (`*:7b+` or larger).
  - `def ensure_hardware_safe_execution(strict: bool = True) -> None` — refuses to start the daemon if the 16 GB ceiling is violated AND a heavy generation model is loaded; `strict=False` downgrades to a warning for advanced operators on >32 GB machines.

  This is a precondition for the Asymmetric LightRAG architecture (§Phase 3) to operate within the operator's RAM budget.
- [ ] **FR-07a** **Orthogonal Guards module** → `econosuite/engine/orthogonal_guards.py`. Public surface:
  - `def guard_data_integrity(...)` — enforces the `[DATA-INTEGRITY]` axis (no fabricated cell values, no hallucinated sample sizes, no claims unbacked by the materialized Stata output).
  - `def guard_protocol_consistency(...)` — enforces the `[IDENT-CONSISTENCY]` axis (DiD/IV/RDD identification claims match the executed estimator; parallel-trends pre-test mention required when `EstimatorChoice == DiD`; instrument exclusion-restriction declared when `EstimatorChoice == IV_2SLS`).
  These two guards run *orthogonally* per the four-axis grounding model (§12 HemaSuite Note) — every claim in a synthesis section is routed through both, regardless of which axis primarily owns the section.
- [ ] **FR-28** **Mellel-style Section Manager** → `econosuite/tools/section_manager.py`. Public surface:
  - `class SectionManager` — manages dynamic section routing (Mellel-inspired tagged section-slicing, see Master Arch §1.3).
  - `def parse_mellel_tags(self, synopsis_text: str) -> list[str]` — extracts tags like `[SECTION: INTRO]`, `[SECTION: IDENTIFICATION]`, `[SECTION: ROBUSTNESS]` from the Master Synopsis. Returned in deterministic insertion order; the `UnifiedEngine` dispatches each tag through the Five-Tier Pipeline's section-grounding profile. This is the artifact that makes EconoSuite's manuscript assembly *dynamic* (not IMRaD-locked) — it is the structural translation of HemaSuite's fixed-section pipeline.
- [ ] **FR-08** **Manuscript-type extension**: `EngineConfig.manuscript_type: Literal["empirical", "theoretical", "review", "short_comms", "proposal"]` (replaces HemaSuite's clinical-trial-flavored enum). Section grounding profiles (§12.2 HemaSuite Note) re-keyed for econ:
  - `empirical`: Background = `EVIDENCE_ONLY`; Identification = `IDENT_PRIMARY`; Empirical Analysis = `DATA_ONLY`; Robustness = `DATA_ONLY` ($+$ identification);  Discussion = `SYNTHESIS` (per-sentence)
  - `theoretical`: Background = `EVIDENCE_ONLY`; Model = `IDENT_PRIMARY` (formal proofs); Comparative Statics = `DATA_ONLY` (analytical); Discussion = `SYNTHESIS`
  - `review`: All sections = `EVIDENCE_ONLY`
  - `short_comms`: condensed `empirical` profile
  - `proposal` (Korean grant): `IDENT_PRIMARY` + `EVIDENCE_ONLY` mix; HWPX output

#### Phase 2 — ESA Engine Implementation & Stata Integration

- [ ] **FR-09** `econosuite/tools/esa_bridge.py` — replaces HemaSuite's `tools/csa_bridge.py`. Sole entry for empirical analysis. Generates Jinja2-templated R + Stata scripts.
- [ ] **FR-10** **DGP (Data Generating Process) selector**: input `EngineConfig.dgp_hint` (or auto-detect from variable types) → output `EstimatorChoice` $\in$ `{OLS, FE_TWO_WAY, IV_2SLS, DiD, EVENT_STUDY, RDD_LOCAL_LINEAR, LOGIT, PROBIT, CENSORED, HAZARD, HECKMAN_SELECTION}` with associated `pystata` code template. Default heuristic (Antigravity-resolved): Continuous outcome → OLS / FE; Binary → Logit / Probit; Censored → Tobit / Censored Regression; Time-to-event → Hazard. The selector also covers **Extremum Estimators** (GMM, M-estimators) and **Nonparametric** computations (kernel density for McCrary, local-linear for RDD) as first-class branches — these are not "advanced extras," they are required for AEA-grade robustness sections.
- [ ] **FR-11** **Multi-way clustered standard errors enforced**: every regression output through ESA Bridge defaults to `vce(cluster <unit>)` or 2-way CGM (Cameron-Gelbach-Miller) clustering when panel structure is detected. Independent-observation SEs are explicitly forbidden in the `empirical` manuscript_type.
- [ ] **FR-12** **`pystata` subprocess execution layer** with timeout / retry / output-parsing primitives. Capture coefficient matrices, standard errors, and execution logs. Surface them as `RScriptResults`-equivalent objects (`StataExecResults`) for the Data axis.
- [ ] **FR-13** **Synthetic Data Generator** (§4.1 Master Arch hard requirement): `econosuite/tools/synthetic_data_generator.py` produces a mock matrix with matched distributional properties when proprietary data is used. Replication package builds against the synthetic; reviewers can run `make all` without the proprietary data.
- [ ] **FR-14** **Supplemental Appendix Auto-Router**: when robustness-check tables exceed the main-text quota, route to `online_appendix.docx`. Auto-link from main text via cross-reference.

#### Phase 3 — Asymmetric LightRAG Implementation

- [ ] **FR-15** **Off-device compile script** `scripts/compile_guidelines_db.py` (Mac Studio target). Ingests AEA Author Style Guide + econometric textbooks (Wooldridge, Cameron-Trivedi, Angrist-Pischke, Hansen) + ICH/FDA guidance for RCT-flavored econ. Uses high-precision indexing model (`qwen3.6:35b-a3b-mlx-bf16` or larger). Output: portable `data/guideline_db/` artifact (MANIFEST.yaml + vdb_*.json + graph_chunk_entity_relation.graphml).
- [ ] **FR-16** **On-device query daemon** `econosuite/engine/lightrag_client.py` reads the pre-shipped artifact, queries with a tiny embedding model (`qwen3-embedding:latest`, ~14 GB) and a small generation model (`qwen2.5:7b-q4_K_M`, ~5 GB) — total $\leq$ 19 GB, leaves $\geq$ 13 GB for Stata on a 32 GB machine and tightly within budget on 16 GB.
- [ ] **FR-17** **Knowledge routing separation** (Master Arch §9.2): empirical/literature queries → NotebookLM (cloud); methodology/identification-strategy queries → local LightRAG. Hard-coded routing in `KO.populate_corpus_store` vs `KO.populate_methodology_store`. Routing is an SSD-swap-prevention measure too: the lightweight on-device query model never holds enough RAM to compete with a running Stata estimation, which is what kills the pipeline on consumer hardware when routing is left to a single heavyweight model.
- [ ] **FR-18** **Guideline-category facet (ported from HemaSuite, see HemaSuite plan)**: Extend `DocumentRef.category: Literal["aea_style", "econometrics_textbook", "fda_guidance", "ich", "stata_manual", "stat_methods"]`. Ports the additivity-with-default pattern.

#### Phase 4 — Typographic, Output & Strictness Engines

- [ ] **FR-19** **`UnifiedTableEngine` ported + extended for econ rules** (Master Arch §5.1):
  - Hard 9-column max — tables exceeding split into Panels A/B
  - Vertical lines stripped
  - Significance-asterisk stripping (regression tables show coefficient + SE in parens, no `***`)
  - Decimal-fraction leading-zero enforcement (`0.357`, never `.357`)
  - Standard-error parenthesization
- [ ] **FR-20** **`UnifiedFigureEngine` ported + extended**:
  - Mandatory `Alt text:` line below every figure caption
  - Native rendering of Event Study / McCrary plot helpers (replaces HemaSuite's KM/Forest helpers)
  - Coefficient-stability plot helper (econ-specific)
- [ ] **FR-21** **EconoSyntax Math Rendering** (Master Arch §5.2): `econosuite/tools/docx_renderer.py` detects `$inline$` and `$$display$$` LaTeX, converts to OMML. Enforces:
  - Italic scalars; **bold** vectors/matrices; script set notation; blackboard-bold number sets
  - Roman operators (`\text{Var}`, `\text{Cov}`, `\text{Pr}`, `\log`, `\ln`)
  - Hat / tilde for estimators
  - Italic indexing subscripts, Roman descriptive subscripts (`X_{\text{max}}` not `X_{max}`)
  - Vertical fractions in display, solidus in inline
  - Auto-numbered display equations
  - Native mapping for the EconoSyntax Reference Table (TWFE, IV first/second stage, DiD, Event Study, etc.) per Master Arch §5.2.1
- [ ] **FR-22** **Self-Healing LaTeX Compilation Loop** (Master Arch §5.2.3): `/tmp/`-sandboxed `xelatex -halt-on-error` invocations bounded by a max-iterations counter, supervised by a dedicated **Debugger Agent** that parses `*.log` error messages, classifies the failure (undefined macro, mismatched environment, encoding fault, theorem-numbering collision), and patches the source for the next attempt. Required for theoretical-pipeline papers with novel proof syntax. Native template support shipped: Taylor & Francis `interact.cls` (`templates/aea_interact.cls.j2`) is the reference template, with the Debugger Agent's correction rules tuned to its constraints.
- [ ] **FR-23** **`UnifiedReferenceEngine` ported + extended**:
  - JEL-code injection (≥3 codes after abstract)
  - AEA RCT registry footnote when `EngineConfig.has_rct = True`
  - JEL bibliography style (vs HemaSuite's Vancouver)
- [ ] **FR-24** **AnonymizerScrubber** (Master Arch §6.3): pre-flight pass over compiled DOCX/PDF strips author names, affiliations, and metadata fields (`<dc:creator>`, `<cp:lastModifiedBy>`, EXIF-equivalent). Hard-fails the submission package build if any author identifier survives.
- [ ] **FR-25** **AI-Disclosure Generator** (Master Arch §6.2): produces per-author `_disclosure.pdf` files (one per coauthor, formal "nothing to disclose" if no conflicts). Generates AI-usage declaration block placed immediately before References.
- [ ] **FR-26** **Replication Packager** (Master Arch §4.3): one-click `make all` Makefile, `.csv`/`.txt` ASCII data alongside `.dta`, ASCII filenames (no spaces, no symbols), seed hardening across R + Stata.
- [ ] **FR-27** **HWPX/OWPML Generator** for Korean grant proposals (Master Arch §6.1): Python `zipfile` + `lxml` writes `section0.xml` into `.hwpx` archive structure. Triggered by `manuscript_type == "proposal"`.

### 2.2 Out of Scope

- Actual estimator implementation beyond template generation. ESA Bridge ships templates; v2 plan handles estimator-by-estimator validation (TWFE has clean-controls, IV has weak-instrument F-stats, RDD has manipulation tests, etc.).
- Tauri desktop UI. EconoSuite ships CLI + daemon only in this plan; UI is a deferred v3.
- NLM corpus seeding strategy (which papers to seed for which topic). That's an operator concern; the orchestration plumbing is what this plan delivers.
- CRF subsystem from HemaSuite §13 — econometrics has no Case Report Form analog. Eliminate, do not port. Closest econ analog is the Replication Codebook, which is covered by FR-26.

---

## 3. Requirements

### 3.1 Functional Requirements

(See Phase tables in §2.1 — FR-01 through FR-27, 27 total.)

### 3.2 Non-Functional Requirements

| ID | Requirement | Verification |
|---|---|---|
| **NFR-01** | Daemon cold start $\leq$ 10s from `econosuite daemon start` to `GET /health` returning 200. | `tests/test_daemon_cold_start.py` |
| **NFR-02** | Full `empirical` manuscript draft completion $\leq$ 30 min on 16GB MacBook with pre-shipped LightRAG, given a populated NLM notebook. | E2E smoke test on a reference topic. |
| **NFR-03** | Per-section content-integrity guard $\leq$ 50ms overhead vs unguarded path. | Microbenchmark; matches HemaSuite §9. |
| **NFR-04** | Multi-way clustered SE generation succeeds via `pystata` for $\geq$ 95% of well-formed panel datasets up to 1M observations. | Synthetic-data smoke + 3 real-world archetype datasets. |
| **NFR-05** | OMML math rendering correct on EconoSyntax Reference Table (Master Arch §5.2.1) and General Math Reference Table (§5.2.2) — all 18 examples render without manual fixup in MS Word 2024+. | Visual diff against reference DOCX. |
| **NFR-06** | AnonymizerScrubber removes 100% of author identifiers from a compiled DOCX with metadata baked in by Word's track-changes; regression test corpus of 5 manuscripts. | `tests/test_anonymizer_zero_leakage.py` |
| **NFR-07** | Replication Makefile completes `make all` on a fresh machine with only R + Stata + the synthetic dataset, in $\leq$ 15 min. | E2E reproducibility test. |
| **NFR-08** | LightRAG query latency on 16GB MacBook: p50 $\leq$ 2s, p95 $\leq$ 8s for a hybrid query against the Wooldridge+Angrist-Pischke pre-compiled index. | Load test post-Phase-3. |
| **NFR-09** | Surface delta vs HemaSuite baseline $\leq$ 30% LOC growth (foundation port should be $\sim$70% reuse from HemaSuite). | `cloc` diff at end of Phase 1. |

### 3.3 Inherited Invariants (Non-negotiable)

These are **ported as hard runtime invariants**, not optional features. Any implementation that violates them is a regression from HemaSuite:

| Invariant | HemaSuite §ref | EconoSuite anchor |
|---|---|---|
| KO is sole evidence query gateway | §11 | `econosuite/engine/knowledge_orchestrator.py` + `tests/test_ko_sole_query_gateway.py` |
| NLM-grounding is hard, not soft (NLMHardFailure halts pipeline; no silent PubMed fallback claiming NLM) | §10 | `econosuite/engine/nlm_health.py` |
| Scaffold tokens never reach saved files | §9 | `econosuite/engine/triad/content_integrity.py` |
| Four-axis grounding routing applies per-sentence in synthesis sections | §12 | Per-section grounding profile in `engine/strategies/*.json` |
| Daemon HTTP transport (`:8021`), not Unix socket | §3.4 + §7 Phase 0 | `econosuite/engine/agent_daemon.py` |
| LightRAG asymmetric: compile off-device, query on-device | HemaSuite §3.5 + §3.6 + §7 Phase 1.6 | Phase 3 of this plan |
| Single sub-engine per concern (no parallel reference manager, no parallel table renderer) | §1.2 Master Arch | All `Unified*Engine` classes |

---

## 4. Risks and Mitigation

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Hardware ceiling: Stata + LightRAG + LLM exceed 16GB RAM, causing SSD swap thrash and cascading timeouts | High | Critical | `HardwareHealthGuard` (FR-07) hard-fails any attempt to load a generation LLM in-process on $\leq$ 32 GB machines. Added OS-level memory-pressure polling to detect stealth-loads. Since the Mac Studio is offline, execution relies solely on the manually synced local LightRAG DB artifact being present on the MacBook. |
| Domain leakage: HemaSuite clinical assumptions leak, or causal inference assumptions (e.g. DiD parallel trends) are hallucinated as met by the LLM | High | Critical | Phase 1 ports invariants, not clinical specifics. Introduce deterministic rule-based pre-filters in `[IDENT-CONSISTENCY]` (e.g., regex requirements for "parallel trends" or "exclusion restriction") *before* LLM synthesis is allowed to proceed. |
| Math typesetting incorrectness: AEA reviewers reject manuscripts with mis-typeset equations, or the `xelatex` self-healing loop gets stuck in an infinite recursion | High | High | EconoSyntax (FR-21) is a hard-coded rendering pipeline. Cap the `xelatex` Debugger Agent at `MAX_RETRIES=3` to prevent infinite loops, falling back to high-res PNG rendering instead of halting compilation. |
| Anonymization gap: a single leaked author identifier in compiled PDF/DOCX metadata blows the double-blind submission | Low | Critical | `AnonymizerScrubber` (FR-24) mandates `zipfile`-level XML scrubbing and `exiftool` OS-metadata stripping. Synthetic "honey-token" authors injected into test suite to ensure deep-nesting removal. Failure mode is `ValueError`, not warning. |
| Stata licensing & Output Parsing Fragility: `pystata` bindings fail, and `subprocess stata-mp` regex parsing misaligns standard errors | Medium | High | ESA Bridge ships dual-mode. Impose strict regex boundaries on subprocess parsing. Add an R-based `fixest` fast sanity check to cross-validate Stata coefficients (flag output as corrupted if divergence >1%). |
| Phase-Level Checkpointing Corruption: JSON state checkpoint is interrupted, leading to corrupted manuscript resumption | Medium | Medium | Implement a Two-Phase Commit protocol for `.json` state checkpoints. Write to a `.tmp` file, verify JSON schema validity using a strict `pydantic` model, and perform an atomic rename to `.json`. |
| LightRAG index drift: AEA style guide v2027 lands; the pre-shipped index is stale | Low | Medium | Compile script (FR-15) ships with versioned MANIFEST.yaml. Operator re-runs on offline Mac Studio; deploys via manual artifact swap (no on-device re-indexing). |
| Korean HWPX/OWPML schema drift: government schema changes break `section0.xml` generator | Low | Low | HWPX generator is feature-flagged behind `manuscript_type == "proposal"`; failures don't impact main pipeline. Schema validation against a pinned reference `.hwpx` in `tests/fixtures/`. |
| OMML rendering inconsistency across Word versions (2019 vs 2024 vs LibreOffice) | Medium | Medium | Test rendering against MS Word 2024 (gold standard) + LibreOffice 24 (sanity). Document known divergences. Pin operator-side Word version in `docs/02-design/features/econosyntax-rendering.design.md`. |

---

## 5. Architecture Considerations

### 5.1 Directory Layout (post-Phase-1)

```
EconoSuite/
├── econosuite/
│   ├── cli.py                              # CLI entry (existing, extend)
│   ├── builder.py / validator.py / ...     # existing, refactor
│   ├── engine/
│   │   ├── unified_engine.py               # NEW (port from HemaSuite §1.2)
│   │   ├── knowledge_orchestrator.py       # NEW (port §11 — sole gateway)
│   │   ├── nlm_health.py                   # NEW (port §10 — hard-fail)
│   │   ├── hardware_health.py              # NEW (econ-specific FR-07)
│   │   ├── agent_daemon.py                 # NEW (port HTTP :8021)
│   │   ├── lightrag_client.py              # NEW (Phase 3)
│   │   ├── strategies/                     # JSON section profiles per manuscript_type
│   │   ├── data_integrity.py               # NEW (port §12 [DATA-INTEGRITY])
│   │   ├── identification_consistency.py   # NEW (econ analog of [PROTOCOL-CONSISTENCY])
│   │   ├── orthogonal_guards.py            # NEW FR-07a (guard_data_integrity + guard_protocol_consistency dispatch)
│   │   └── parallel.py                     # NEW (port UnifiedParallelEngine)
│   ├── triad/
│   │   ├── content_integrity.py            # NEW (port §9 scaffold-echo-guard)
│   │   ├── universal_orchestrator.py       # NEW (port triad)
│   │   └── contrastive_validator.py
│   ├── tools/
│   │   ├── esa_bridge.py                   # NEW (Phase 2 — econ analog of csa_bridge)
│   │   ├── section_manager.py              # NEW FR-28 (Mellel-style dynamic sectioning)
│   │   ├── synthetic_data_generator.py     # NEW (FR-13)
│   │   ├── docx_renderer.py                # NEW (FR-21 EconoSyntax)
│   │   ├── unified_table_engine.py         # NEW (FR-19)
│   │   ├── unified_figure_engine.py        # NEW (FR-20)
│   │   ├── unified_reference_engine.py     # NEW (FR-23 — JEL/AEA)
│   │   ├── anonymizer_scrubber.py          # NEW (FR-24)
│   │   ├── ai_disclosure.py                # NEW (FR-25)
│   │   ├── replication_packager.py         # NEW (FR-26)
│   │   ├── hwpx_generator.py               # NEW (FR-27)
│   │   └── pubmed_searcher.py              # NEW (port; econ uses Semantic Scholar peer-equivalent + RePEc/NBER)
│   └── phases/                             # 10-phase manuscript workflow (existing scaffold, extend)
├── data/
│   ├── guidelines/                         # Pre-shipped LightRAG sources
│   │   ├── aea_style/                      # AEA Author Style Guide
│   │   ├── econometrics_textbook/          # Wooldridge, Angrist-Pischke, Cameron-Trivedi
│   │   ├── stata_manual/                   # Stata reference docs
│   │   ├── fda_guidance/                   # ICH E9, RWE for econ-flavored RCTs
│   │   └── ich/
│   └── guideline_db/                       # Pre-compiled (Mac Studio output)
│       ├── MANIFEST.yaml
│       ├── corpus_plan.yaml
│       ├── vdb_entities.json
│       ├── vdb_relationships.json
│       ├── vdb_chunks.json
│       └── graph_chunk_entity_relation.graphml
├── scripts/
│   ├── compile_guidelines_db.py            # Mac Studio target (FR-15)
│   ├── verify_corpus_integrity.py          # Port from HemaSuite
│   └── migrate_category.py                 # Port from HemaSuite (idempotent)
├── templates/
│   ├── aea_interact.cls.j2                 # AEA LaTeX template
│   ├── qje.docx.j2                         # QJE Word template
│   └── hwpx_section0.xml.j2                # Korean grant template
├── tests/
│   ├── test_ko_sole_query_gateway.py       # Ported from HemaSuite
│   ├── test_nlm_hard_dependency.py         # Ported
│   ├── test_scaffold_guard.py              # Ported
│   ├── test_four_axis_grounding.py         # Ported with econ axes
│   ├── test_hardware_health.py             # NEW Session A gate (≡ test_hardware_health_guard.py from §5.1)
│   ├── test_daemon_isolation.py            # NEW Session B gate (FastAPI :8021 + STDIN /dev/null)
│   ├── test_section_manager.py             # NEW Session D gate (Mellel-tag parsing)
│   ├── test_econosyntax_rendering.py       # NEW
│   ├── test_anonymizer_zero_leakage.py     # NEW
│   └── test_replication_makefile.py        # NEW
└── docs/
    ├── 01-plan/features/
    │   └── econosuite-foundation-port.plan.md  # this file
    ├── 02-design/features/
    │   ├── esa-bridge.design.md            # to be written in Design phase
    │   ├── econosyntax-rendering.design.md
    │   ├── asymmetric-lightrag.design.md
    │   └── anonymizer-scrubber.design.md
    └── handoffs/
```

### 5.2 Translation Table — HemaSuite → EconoSuite

| HemaSuite concept | EconoSuite analog | Notes |
|---|---|---|
| `manuscript_type ∈ {clinical_trial, systematic_review, narrative_review, case_report, protocol}` | `manuscript_type ∈ {empirical, theoretical, review, short_comms, proposal}` | Different enum, same dispatch pattern |
| `CSA bridge` (Clinical Statistics Analyzer, R-only) | `ESA Bridge` (Economic-Statistic-Analysis, R + Stata) | Strict superset; Stata is the new addition |
| `[PROTOCOL-CONSISTENCY]` guard (clinical study design) | `[IDENT-CONSISTENCY]` guard (identification strategy) | Same axis, renamed |
| ELN/ICC/WHO-HAEM guideline corpus | AEA Style + Wooldridge/Angrist-Pischke textbook + Stata manual + ICH/FDA RWE corpus | Different sources, same LightRAG ingestion pattern |
| CTCAE grading scale | (eliminated; no econ analog) | Out of scope |
| CRF Engine (§13) | (eliminated; closest analog is Replication Packager FR-26) | Out of scope |
| Vancouver citation style | JEL + AEA bibliography style | `UnifiedReferenceEngine` style swap |
| KM / Forest plot helpers | Event Study / McCrary / Coefficient Stability plot helpers | `UnifiedFigureEngine` helper swap |
| HemaSuite Project YAML (`hemasuite_projects.yaml`) | `econosuite_project.yaml` (already designed in Master Arch §7) | Same registry pattern |
| Vancouver numbered citations in body | AEA `(Author, Year)` parenthetical citations | `UnifiedReferenceEngine` style swap |
| `hpw research "topic"` CLI | `econosuite draft "topic"` CLI | Same UX pattern |
| HemaSuite triad (draft → validate → revise) | EconoSuite triad (prove → write → verify) | Same loop, different validation primitives (econ requires identification-strategy validation step) |

### 5.3 Decision Records (architectural)

1. **Asymmetric LightRAG is non-optional.** On 16 GB hardware, running Stata + LightRAG node-extraction LLM in-process exceeds RAM. The compile/query split is the only viable architecture. Documented in `docs/02-design/features/asymmetric-lightrag.design.md` (to be written in Design phase).
2. **`pystata` over subprocess `stata-mp`.** When available, `pystata` is preferred for return-code + matrix capture without parsing log files. Subprocess fallback exists for environments where `pystata` install fails.
3. **CRF subsystem eliminated, not ported.** Replication Packager (FR-26) covers the closest econ-equivalent need (one-click reproducibility).
4. **`manuscript_type == "clinical_trial"` is renamed to `"empirical"`** with extended semantics for both observational and experimental designs. Keeping the HemaSuite name would invite leakage of clinical-trial assumptions.
5. **Daemon HTTP transport on `:8021`** matches HemaSuite's port registry to avoid collision when both stacks run on the same machine. LightRAG on `:8020`. Ollama on `:11434`.
6. **EconoSyntax rendering is enforced at the `UnifiedTableEngine` / `UnifiedFigureEngine` boundary**, not in the LLM prompt. LLMs occasionally drift on math typesetting; deterministic post-processing is the only correctness guarantee.

---

## 6. Convention Prerequisites

- HemaSuite repo accessible at `~/Coding/HemaSuite/` (read-only) for invariant porting reference.
- Python 3.14 + virtual environment (`.venv/`) — same as HemaSuite.
- Ollama installed with `qwen3-embedding:latest`, `qwen2.5:7b-q4_K_M` for on-device; `qwen3.6:35b-a3b-mlx-bf16` available on Mac Studio for off-device compile.
- Stata-mp installed locally (or `pystata` Python wrapper).
- R 4.4+ with `fixest`, `data.table`, `did`, `rdrobust`, `RDHonest`, `ivmodelBoot` packages.
- LaTeX distribution (TeX Live 2024+) with `xelatex` for self-healing compilation loop.
- MS Word 2024+ on the operator's MacBook for OMML render verification.
- Git remote configured for EconoSuite repo with push access for CI integration.

---

## 7. Success Criteria

| SC | Target | Verification |
|---|---|---|
| **SC-01** | Daemon HTTP `:8021` health check responds 200 within 10s of cold start | `tests/test_daemon_cold_start.py` |
| **SC-02** | KO single-source gateway: zero direct `LightRAGClient` / `NotebookLM` / `PubMed` imports outside `KnowledgeOrchestrator` | `tests/test_ko_sole_query_gateway.py` (ported) |
| **SC-03** | NLM Hard-Dependency: synthetic NLM auth failure raises `NLMHardFailure`, halts pipeline, no silent PubMed fallback claiming NLM grounding | `tests/test_nlm_hard_dependency.py` |
| **SC-04** | Scaffold-echo-guard: `{feature}`/`{section}`-style tokens never reach saved DOCX | `tests/test_scaffold_guard.py` |
| **SC-05** | Four-axis grounding: `Empirical Analysis` section under `manuscript_type=empirical` runs `[DATA-INTEGRITY]` guard, NOT `guard_nlm_call`; `Background` section runs `guard_nlm_call`, NOT `[DATA-INTEGRITY]` | `tests/test_four_axis_grounding.py` |
| **SC-06** | HardwareHealthGuard hard-fails on a synthetic 16 GB RAM machine when Ollama has `qwen3.6:35b` loaded | `tests/test_hardware_health_guard.py` |
| **SC-07** | ESA Bridge generates a TWFE Stata script with 2-way clustered SE for a synthetic panel; `pystata` execution returns coefficient matrix | `tests/test_esa_bridge_twfe.py` |
| **SC-08** | EconoSyntax: all 18 reference-table examples render OMML correctly in MS Word 2024 (italic scalars, bold vectors, Roman operators, leading-zero decimals) | Visual diff against `tests/fixtures/econosyntax_reference.docx` |
| **SC-09** | AnonymizerScrubber removes 100% of author identifiers from a corpus of 5 reference manuscripts (DOCX + PDF) | `tests/test_anonymizer_zero_leakage.py` |
| **SC-10** | `make all` Replication Makefile completes on a fresh machine with R + Stata + synthetic dataset, in $\leq$ 15 min | `tests/test_replication_makefile.py` |
| **SC-11** | LightRAG hybrid query latency on 16 GB MacBook: p50 $\leq$ 2s, p95 $\leq$ 8s | Load test post-Phase-3 |
| **SC-12** | E2E smoke: `econosuite draft "topic"` produces a complete AEA-formatted DOCX in $\leq$ 30 min, with $\geq$ 3 regression tables, $\geq$ 2 figures with alt-text, JEL codes, disclosure PDFs | E2E test on a reference topic |

**Exit criteria** (all must hold to declare the foundation port complete):
- All 12 SCs pass
- All 29 FRs (FR-01..FR-27 + FR-07a + FR-28) implemented or explicitly deferred with reason captured in this plan's `Incomplete / Deferred Items` section
- HemaSuite invariant tests (KO gateway, NLM-Health, Scaffold-Guard, Four-Axis) pass with EconoSuite axis renames
- Zero `grep -rn` hits for `clinical|CTCAE|CRF|hematology|patient` in production code (acceptable in test fixtures and porting comments)

### 7.1 Antigravity Verification Plan (Automated + Manual)

Carried over verbatim from the resolved scratch plan as the minimum bar before the foundation port can be declared shipped. These are *complementary* to the SC table above, not a replacement.

**Automated:**
- Feed `UnifiedTableEngine` a 12-column Stata regression output containing significance asterisks. Assert: table is split into Panel A / Panel B, asterisks stripped, standard errors enclosed in parentheses, leading-zero decimals enforced.
- Run `synthetic_data_generator` against a mock dataset; assert output preserves the input's distributional properties (mean / variance / quantile parity within tolerance) so reviewers running `make all` against the synthetic see equivalent regression coefficients.
- Verify `pystata` and the subprocess `stata-mp` fallback both correctly capture return codes and parse coefficient matrices for the same input script.

**Manual:**
- Generate a full EconoSuite manuscript draft and verify by inspection: Keith Head 5-step Introduction structure, QJE/AER abstract length compliance, JEL codes present, AEA RCT-registry footnote when applicable.
- Inspect the output Replication Package: `make all` Makefile present, ASCII-only filenames, per-author `_disclosure.pdf` files generated, anonymizer scrubber removed all author identifiers from compiled DOCX/PDF metadata.

---

## 8. Phased Execution Sequence

| Phase | Scope | Dependencies | Estimated FR count |
|---|---|---|---|
| **Phase 1 — Foundation & Daemon** | FR-01..08 + Hardware Health Guard | None (start here) | 8 FRs |
| **Phase 2 — ESA Engine** | FR-09..14 | Phase 1 (KO + four-axis ready) | 6 FRs |
| **Phase 3 — Asymmetric LightRAG** | FR-15..18 | Phase 1 (KO ready); Mac Studio access for compile | 4 FRs |
| **Phase 4 — Typography & Output** | FR-19..27 | Phase 1 (UnifiedEngine ready); Phase 2 (ESA outputs to format); Phase 3 (LightRAG queries for stylistic guidance) | 9 FRs |

Phases are sequential **for review purposes** (the plan ships in 4 reviewable units), but Phases 2/3/4 can overlap during execution since they depend only on Phase 1.

### 8.1 Phase 1 Implementation Sessions (Locked-In)

The Antigravity-resolved scratch plan settles Phase 1 into four sequential coding sessions, each with a hard gate. Sessions ship in order; a session does not start until its predecessor's gate is green.

| Session | Module(s) | Gate (Definition of Done) |
|---|---|---|
| **Session A** | `econosuite/engine/hardware_health.py` + `tests/test_hardware_health.py` | `test_hardware_health.py` asserts `ensure_hardware_safe_execution(strict=True)` raises `HardwareHardFailure` when mocked memory ≤ 16.5 GB AND a heavy generation model is reported loaded. |
| **Session B** | `econosuite/engine/agent_daemon.py` + `tests/test_daemon_isolation.py` | Daemon binds to `:8021` headlessly under `econosuite daemon start`; STDIN reads raise `EOFError`; `GET /health` returns 200 within 10s of cold start (matches NFR-01). |
| **Session C** | `econosuite/engine/orthogonal_guards.py` + `econosuite/engine/knowledge_orchestrator.py` (port) | HemaSuite invariants pass on EconoSuite axes: KO sole-gateway (`tests/test_ko_sole_query_gateway.py`), four-axis grounding (`tests/test_four_axis_grounding.py`), `[DATA-INTEGRITY]` + `[IDENT-CONSISTENCY]` orthogonal routing. |
| **Session D** | `econosuite/engine/unified_engine.py` + `econosuite/tools/section_manager.py` + `tests/test_section_manager.py` | Five-Tier Pipeline DAG executes for every `manuscript_type`; `parse_mellel_tags` correctly slices a custom-section synopsis bypassing IMRaD; phase-level checkpoint roundtrip (write → kill → restart → resume) succeeds via `StateAdapter`. |

Sessions A and B do not depend on each other in principle, but the resolved plan keeps them serial so a Session A regression cannot mask a Session B isolation bug.

---

## 9. Out of Scope / Deferred to v2

- ESA estimator implementation beyond template generation (TWFE clean-controls verification, IV weak-instrument F-stats, RDD manipulation tests, Heckman first-stage diagnostics).
- Tauri desktop UI / browser-based authoring interface.
- AEA Data and Code Availability Policy (DCAP) full automation — Phase 4's Replication Packager is a foundation, but the policy compliance check is its own v2 plan.
- Korean HWPX export beyond `section0.xml` skeleton — full schema coverage is a v2 plan.
- `[IDENT-CONSISTENCY]` guard's deep validation (e.g., automated parallel-trends pre-test verification, instrument F-stat threshold enforcement). Phase 1 ships the guard *boundary*; deep semantics are v2.
- Antigravity Brain integration. The `~/.gemini/antigravity/brain/` integration was the source of the resolved scratch plan, but EconoSuite ships the daemon HTTP transport from day 1 and does not depend on Antigravity at runtime.

---

## 10. Next Steps (Operator-driven)

1. **Review this plan** end-to-end. Mark FRs you want to descope, retarget, or add. Write a comment block at the bottom of the plan rather than editing inline.
2. **Update `.pdca-status.json`** to reflect the new feature: `"active_feature": "econosuite-foundation-port.plan.md"`, `"current_phase": "design"`.
3. **Phase 1 Design doc** kickoff: `docs/02-design/features/econosuite-foundation-port.design.md`. Use HemaSuite's `lightrag-qwen36-upgrade.design.md` as a structural template; the design phase nails down module signatures, class hierarchies, and test fixtures.
4. **Snapshot the HemaSuite invariant test suite** that will be ported (KO gateway, NLM Hard-Dependency, Scaffold-Guard, Four-Axis Grounding) — verify they all pass on the current HemaSuite main branch before porting, so any failure during port is unambiguously a port-side bug.
5. **Pre-flight Mac Studio access** for the off-device LightRAG compile job. Confirm `qwen3.6:35b-a3b-mlx-bf16` available; confirm $\geq$ 192 GB unified memory; confirm Ollama installed.
6. **Decide on `pystata` vs subprocess** strategy for the operator's primary machine. Document in design phase.

---

## 11. Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2026-04-28 | Claude Code (Opus 4.7) | Initial draft. Synthesizes Antigravity-resolved scratch plan + EconoSuite Master Architecture + HemaSuite Architecture Note (§§1–14) into actionable 4-phase, 27-FR, 12-SC porting plan with explicit HemaSuite→EconoSuite translation table. |
| 1.1 | 2026-04-28 | Claude Code (Opus 4.7) | Reconciled with the Antigravity-resolved scratch plan: added "Architectural Decisions (Locked-In)" §; spelled out Phase 1 module signatures (`HardwareHardFailure`, `_get_system_memory_gb`, `_detect_loaded_generation_models`, `ensure_hardware_safe_execution`); added FR-07a (orthogonal_guards module) and FR-28 (`SectionManager` for Mellel-style dynamic sectioning); amended FR-01 (STDIN→/dev/null isolation), FR-06 (Five-Tier Execution Pipeline + Phase-level Checkpointing via `StateAdapter`), FR-10 (Extremum + Nonparametric estimators), FR-17 (SSD-swap-thrash routing rationale), FR-22 (named Debugger Agent + Taylor & Francis `interact.cls`); added §8.1 Phase 1 Implementation Sessions A–D with gates; added §7.1 Antigravity Verification Plan (automated + manual); updated directory layout and test file roster; FR count 27 → 29. |
| 1.2 | 2026-04-30 | Antigravity | Updated Risks and Mitigation section to incorporate robust architectural solutions for 6 key risks, strictly enforcing the offline-only Mac Studio constraint for LightRAG execution. |

---

## 12. Related Documents

- **Spec**: `EconoSuite_Master_Architecture.md` (target, lives at repo root)
- **Source-of-truth invariants**: `~/Coding/HemaSuite/HemaSuite_Architecture_Note.md` §§1–14
- **Antigravity-resolved scratch plan** (superseded by this doc): `~/.gemini/antigravity/brain/81f6874c-db7f-41fc-a1d4-7bc841f3cadc/implementation_plan.md.resolved`
- **HemaSuite reference plans** (templates for design phase):
  - `~/Coding/HemaSuite/docs/archive/2026-04/lightrag-qwen36-upgrade/lightrag-qwen36-upgrade.plan.md`
  - `~/Coding/HemaSuite/docs/01-plan/features/lightrag-qwen36-mlx-upgrade.plan.md`
  - `~/Coding/HemaSuite/hematology-paper-writer/docs/01-plan/features/guideline-category-facet.plan.md`
- **HemaSuite invariant test suite** (templates for porting):
  - `tests/test_ko_sole_query_gateway.py` (HPW)
  - `tests/test_nlm_hard_dependency.py` (HPW)
  - `tests/test_scaffold_guard.py` (HPW)
- **HemaSuite tech note** for operational gotchas (parallel-slot crash, GPU contention, MLX backend, model identity decoupling): `~/Coding/HemaSuite/hematology-paper-writer/.claude/rules/hpw-lightrag.md` v5.2

---
