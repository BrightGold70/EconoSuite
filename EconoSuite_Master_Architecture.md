# EconoSuite Platform: Master Architecture & Technical Specification

**Objective**: This document serves as the foundational master specification for **EconoSuite**, an automated, high-fidelity orchestration pipeline designed explicitly for drafting, analyzing, and formatting top-tier economic research manuscripts. It outlines the core subsystems, econometric requirements, typography rules, and data orchestration modules necessary to operate EconoSuite as an independent, premier platform.

---

## 1. System Overview & The HemaSuite Lineage

### 1.1 The HemaSuite Lineage & Cross-Disciplinary Translation
EconoSuite is a direct clone and architectural fork of **HemaSuite**, inheriting its robust manuscript drafting and statistical compilation structures originally designed for hematology. Because the many Unified Systems governing this process are extensively documented in the `HemaSuite_Architecture_Note.md` file, **EconoSuite must closely review that reference document** when designing the architecture and structure for the porting plan.

Porting this system to economics requires navigating significant cross-disciplinary friction points. The architecture addresses these fundamental differences through a precise anatomic translation across seven major axes:

*   **1. Epistemological Approach (Trial Design vs. Identification Strategy)**: 
    *   *Hematology*: Relies heavily on prospective Randomized Controlled Trials (RCTs), blinding, and cohort assignments as the gold standard.
    *   *Economics*: Relies heavily on retrospective observational data, requiring rigorous "Identification Strategies" (Natural Experiments, Instrumental Variables, Regression Discontinuity) to isolate causal counterfactuals from endogenous noise.
*   **2. Data Paradigms & Privacy Models**: 
    *   *Hematology*: Patient-level data governed by strict clinical privacy laws (HIPAA, patient consent), often with smaller, highly controlled sample sizes subject to loss-to-follow-up.
    *   *Economics*: Massive administrative, geographic, or macro-level panel datasets (often millions of rows) requiring complex harmonizations. Missing data is often treated as an endogenous selection bias (e.g., Heckman models) rather than random attrition.
*   **3. Statistical Engines (Biostatistics vs. Econometrics)**: 
    *   *Hematology (HemaSuite)*: Biostatistical core focusing on survival analysis (Kaplan-Meier, Cox proportional hazards), incidence rates, odds ratios, and adverse event toxicity.
    *   *Economics (EconoSuite)*: Econometric core battling Unobserved Heterogeneity and Endogeneity. Requires high-dimensional Fixed Effects (Two-Way/Multi-Way), Staggered Difference-in-Differences (Bacon decomposition), and Instrumental Variables.
*   **4. Standard Error Architecture**:
    *   *Hematology*: Often assumes independence of observations within a trial or simple trial stratifications.
    *   *Economics*: Enforces strict clustering assumptions. EconoSuite must default to Heteroskedasticity-Robust and Multi-Way Clustered Standard Errors (e.g., clustered by state or industry) to prevent false-positive significance in panel data.
*   **5. Graphical Evidence Requirements**:
    *   *Hematology*: Emphasizes Kaplan-Meier survival curves, Forest plots, and PRISMA flow diagrams.
    *   *Economics*: Demands Event Study plots (to prove parallel pre-trends for DiD), McCrary density plots (to prove no manipulation of the running variable in RDD), and coefficient stability plots.
*   **6. Structural Theory vs. Pure Empirics**:
    *   *Hematology*: Largely empirically driven, focusing directly on clinical outcomes and physiological efficacy.
    *   *Economics*: Frequently mandates a formal mathematical "Structural Model" or utility-maximizing theoretical framework *before* empirical testing can begin, to justify the economic mechanism.
*   **7. Publication Standards & Terminology**: 
    *   *Hematology*: Strict adherence to medical terminology (SNOMED/ICD-10), PubMed/MeSH indexing, and clinical reporting guidelines (CONSORT, STROBE).
    *   *Economics*: Strict adherence to McCloskey/Keith Head writing structures, JEL (Journal of Economic Literature) indexing, RePEc/NBER working paper reliance, and mandatory reproducible data/code packages for AEA/QJE submission.

### 1.2 Core Architectural Principles (The Two Pillars)
To overcome these translation challenges and operate autonomously, EconoSuite relies on two unshakeable pillars:

1.  **The Unified Principle (Most Important)**: All functions across the pipeline are integrated and centralized by the overarching **`UnifiedEngine`**. This master engine controls the whole process of text generation, preventing disjointed formatting and ensuring global continuity. The `UnifiedEngine` governs several specialized sub-engines:
    *   **`KnowledgeOrchestrator`**: The singular, centralized control mechanism responsible for all evidence collection, validation, and fetching of strict economic evidence.
    *   **`UnifiedTriOrchestrator`**: The specialized tripartite logic engine responsible for the strict "prove/write/verify" drafting cycle, ensuring that every generated claim is mathematically and theoretically verified before being committed to the manuscript.
    *   **`UnifiedTableEngine`**: The centralized system controlling all table-related formatting, compilation, constraints, and alignment.
    *   **`UnifiedFigureEngine`**: The centralized system controlling all figure-related operations, layout, rendering, and accessibility compliance.
    *   **`UnifiedReferenceEngine`**: The centralized engine controlling all EndNote tagging, citation formatting, and the generation of the final bibliographic library.
2.  **End-to-End NotebookLM (NLM) Integration (Most Important)**: Throughout the entire lifecycle of EconoSuite, general sources and comprehensive text generation must be maintained and routed through NotebookLM integration. This integration is explicitly powered by the **`notebooklm-py`** library (`https://github.com/teng-lin/notebooklm-py.git`). NLM acts as the master knowledge synthesis engine, dictating the truth for the drafting process.

---

## 2. Advanced Mellel-Inspired Section System & DOCX Assembly

Rather than treating the manuscript as a monolithic text block with a fixed flow, EconoSuite adopts an advanced, tag-based "Section-Slicing" methodology inspired by Mellel. 

### 2.1 Dynamic Tag-Based Sectioning
The document is divided into modular, isolated sections. Every section is assigned a unique, isolated structural tag (e.g., `[SECTION: INTRO]`, `[SECTION: ROBUSTNESS]`). This allows sections to be drafted, revised, and validated completely independently of one another.

### 2.2 NLM-Generated Local Section Corpus (Truth Reservoir)
Each tagged section is backed by its own dedicated "Truth Reservoir". **While these corpora are stored physically in the local project folder, 100% of their content is generated by querying NotebookLM via the `KnowledgeOrchestrator`.** This ensures that the local files contain pristine, NLM-validated text that acts as the isolated evidence base for that specific section tag, avoiding cross-contamination of facts.

### 2.3 Adjustable Assembly & Template-Based DOCX Compilation
The combination of sections is **not bound by a fixed order**. The DOCX Template Compiler reads a dynamic assembly configuration, allowing authors to instantly shuffle, reorder, or omit sections on the fly during compilation without breaking the document's flow. 
The Template Compiler stitches these dynamically ordered tags and local reservoirs together into a unified **DOCX document**, autonomously resolving continuous mathematical numbering, cross-references, and global formatting across the isolated slices.

---

## 3. Orchestration: The Five-Tier Execution Pipeline
EconoSuite extends beyond a standard linear draft by orchestrating a **Five-Tier Execution Pipeline** capable of adapting to any formal journal submission classification:
1. **Empirical Pipeline**: Full ESA Engine activation mapping structural/reduced-form analytics.
2. **Theoretical Pipeline**: Couples the drafting engine strictly to the LaTeX Math Compiler for pure theory, proofs, and estimations.
3. **Review Pipeline**: Literature syntheses and PRISMA Flow Diagram scoping reviews.
4. **Short Communications**: Ultra-concise layouts for notes and replies.
5. **Proposal Protocol (Korean Standard)**: Direct XML translation into Korean government `.hwpx` standard templates, utilizing RAG to draft methodologies entirely in the Korean language.

Regardless of the tier, the baseline execution sequence utilizes **Phase-level Checkpointing & Run Adapters**, enabling instantaneous DAG state resumption after API timeouts without data loss.

### 3.1 The Baseline 10-Phase Sequence
The empirical engine navigates a strict sequence governed by the Master Synopsis (`Synopsis.md`):
1. **Ideation & Master Synopsis Generation** (EconoSuite drafts the blueprint).
2. **Literature Ingestion & Synthesis** (NLM queries via the KnowledgeOrchestrator).
3. **Identification Strategy Formalization** (Mathematical lockdown).
4. **Data Preprocessing & Harmonization** (Fetching specific variables dictated by the Synopsis).
5. **Econometric Analysis (ESA execution)** (Blueprint converted to Jinja2 R templates).
6. **Robustness & Falsification Testing** (Testing validity threats defined in the Synopsis).
7. **Modular Drafting (Section-Slicing)** (Drafting tagged sections backed by NLM Truth Reservoirs).
8. **Unified Assembly** (`UnifiedTableEngine` and `UnifiedFigureEngine` execution).
9. **Constitutional Formatting Validation (AEA/QJE Guidelines)**
10. **Final Compilation & Replication Package (DOCX/Makefiles/PDFs)**

---

## 4. The ESA (Economic-Statistic-Analysis) Engine & Data Ingestion

### 4.1 Data Ingestion & Profiling Protocol
Because EconoSuite autonomously dictates the statistical pipeline, data collection is executed only *after* the theoretical architecture dictates the exact variables required. EconoSuite supports two ingestion pathways:

1.  **Autonomous API Data Deduction (Preferred)**: The `KnowledgeOrchestrator` deduces variables and fetches data directly via APIs (e.g., Comtrade, WDI).
2.  **The Manual Supply Mandate (For Proprietary Data)**: The user supplies the raw data matrix and a `ResearchSchema.yaml`.
    *   **Synthetic Data Generation Mandate**: If proprietary data is used, the system **must autonomously generate a script that produces a synthetic/mock dataset** mirroring the distributional properties of the raw data. This is a hard requirement to ensure that the generated replication code can run without crashing during peer review when the actual data is restricted.

### 4.2 Automated Method Selection & Execution
EconoSuite dynamically selects the optimal estimator and CRAN/Stata package via an intelligent DGP (Data Generating Process) selection parser:
*   **Distributional Mapping**: Continuous $\to$ OLS/FE; Binary $\to$ Logit/Probit/MLE; Censored $\to$ Censored Regression; Duration $\to$ Hazard Models; Selected $\to$ Endogenous Selection (Heckman).
*   **Intent Mapping**: Impact intent $\to$ IV Causal Isolation; Policy intent $\to$ Structural Modeling.
*   **Advanced Compute**: Support for Extremum Estimators (GMM, QML), Nonparametric Modules (Method of Sieves, Kernel estimators), and Simulation Compute (MCMC/Metropolis-Hastings, Bootstrap variance estimation).

R and Stata scripts are auto-generated via Jinja2 templates, ensuring dual-language compliance.

### 4.3 Reproducibility & Replication Packages
To achieve 100% compliance with top economics journals, the replication packager enforces the following:
*   **File Naming Protocol**: All generated replication files, datasets, and scripts must use short, simple string names without spaces, symbols (like `&`), or special characters.
*   **"Makefiles" for One-Click Replication**: Generates a master `makefile` ensuring all results and tables can be reproduced with a single command execution.
*   **Universal File Accessibility (ASCII formatting)**: If proprietary formats like Stata's `.dta` are used, the engine automatically generates and includes plain-text ASCII versions (`.csv` or `.txt`) of the data for long-term accessibility.
*   **Seed Setting**: All simulations strictly enforce pseudo-random generator `seed` hardening across both R and Stata environments.

---

## 5. Typography, Formatting & Structural Adherence

Top-tier economic journals enforce extremely rigid stylistic guidelines. EconoSuite hardcodes these rules into the DOCX Template Compiler, `UnifiedTableEngine`, and `UnifiedFigureEngine`.

### 5.1 Tables & Figures (`UnifiedTableEngine` & `UnifiedFigureEngine`)
*   **Rigid Table Constraints**: The `UnifiedTableEngine` strictly enforces a maximum width of **9 columns** (including row headings). If the ESA Engine produces more columns, the `UnifiedTableEngine` autonomously splits the table. All tables are forced into a portrait/vertical orientation.
*   **Horizontal Lines Only**: Tables must utilize top, middle, and bottom rules. Vertical dividers and shading are strictly prohibited.
*   **Abolition of Significance Asterisks**: The compilation tool actively strips "stargazing" asterisks (`*`, `**`) from regression tables, enforcing standard errors in parentheses below the coefficients.
*   **Strict Decimal Formatting**: Decimal fractions uniformly include a leading zero (e.g., 0.357, not .357).
*   **Alt Text for Figures**: The `UnifiedFigureEngine` mandates the generation of Alternative Text descriptions for all figures. These must be preceded by the exact phrase "Alt text:" and placed directly below the figure legends in the manuscript.
*   **Supplemental Appendix Auto-Router**: To preserve main-text brevity, the engine diverts excessive robustness check tables and falsification tests into an autonomously labeled and linked online appendix.

### 5.2 Mathematical Formatting & EconoSyntax
Generating syntactically perfect mathematics relies on the DOCX Template Compiler rendering equations seamlessly. EconoSyntax dictates the following strict typesetting rules:
*   **Mathematical Notation Hierarchy**: Scalar variables are italicized; vectors and matrices are **boldface** (non-italicized); sets use script fonts; number sets use Blackboard bold.
*   **Operators & Functions**: Operators like Expectation (E), Variance (Var), Covariance (Cov), Probability (Pr), and standard functions (log, ln, exp) must strictly be rendered in Roman (non-italic) font to prevent them from being misread as multiplied scalar variables.
*   **Estimators & Notation**: Estimated coefficients and fitted values must use hats (e.g., $\hat{\beta}$) or tildes (e.g., $\tilde{\beta}$). 
*   **Subscripts & Superscripts**: Indexing subscripts for entity ($i, j$) and time ($t$) are italicized. However, descriptive text labels in subscripts must be Roman (e.g., $X_{\text{max}}$, not $X_{max}$).
*   **Fractions**: Displayed block equations must use full vertical fractions, while inline paragraph equations must use the solidus ($a/b$) to preserve line spacing.
*   **Consecutive Numbering**: Block equations must be numbered consecutively at the left margin (or right margin depending on the specific journal template) using Arabic numerals in parentheses, autonomously managed by the DOCX Template Compiler across the modular slices.

### 5.2.1 EconoSyntax Reference Table
To guarantee consistency across manuscripts, EconoSuite relies on the following standard LaTeX formulations for common econometric identification strategies. Users and internal agents should adhere to these baseline syntaxes:

| Econometric Model | LaTeX EconoSyntax | Rendered Example Focus |
| :--- | :--- | :--- |
| **Two-Way Fixed Effects (TWFE)** | `$$ Y_{it} = \alpha_i + \gamma_t + \beta D_{it} + \mathbf{X}_{it}'\mathbf{\theta} + \epsilon_{it} $$` | Italic $i, t$, bold $\mathbf{X}, \mathbf{\theta}$ |
| **Instrumental Variables (First Stage)** | `$$ D_{it} = \pi_0 + \pi_1 Z_{it} + \mathbf{X}_{it}'\mathbf{\rho} + \nu_{it} $$` | Exogenous instrument $Z_{it}$ |
| **Instrumental Variables (Second Stage)**| `$$ Y_{it} = \beta_0 + \beta_1 \hat{D}_{it} + \mathbf{X}_{it}'\mathbf{\theta} + \epsilon_{it} $$` | Hat on fitted endogenous var $\hat{D}_{it}$ |
| **Difference-in-Differences (DiD)** | `$$ Y_{it} = \beta_0 + \beta_1 (\text{Treat}_i \times \text{Post}_t) + \mathbf{X}_{it}'\mathbf{\theta} + \epsilon_{it} $$` | Roman text for $\text{Treat}$ and $\text{Post}$ |
| **Staggered Event Study** | `$$ Y_{it} = \alpha_i + \gamma_t + \sum_{k \neq -1} \beta_k \mathbb{I}(t - E_i = k) + \epsilon_{it} $$` | Blackboard bold indicator $\mathbb{I}$ |
| **Expected Value / Variance** | `$$ \text{Var}(Y_{it} \mid \mathbf{X}_{it}) = \mathbb{E}[\epsilon_{it}^2 \mid \mathbf{X}_{it}] $$` | Roman $\text{Var}$, Blackboard $\mathbb{E}$ |
| **Probability Limits** | `$$ \sqrt{N}(\hat{\beta} - \beta) = O_p(1) + o_p(1) $$` | Capital $O_p$, lowercase $o_p$ |
| **Time Series Operators** | `$$ \Delta Y_t = Y_t - L Y_t = Y_t - Y_{t-1} $$` | Lag $L$, Difference $\Delta$ |
| **Calculus / Differentials** | `$$ \frac{\text{d}y}{\text{d}x} = \int f(x) \text{d}x $$` | Roman differential $\text{d}$ |
| **Matrix Operations** | `$$ \mathbf{A} \circ \mathbf{B} $$` | Hadamard product $\circ$ |
| **Null Vectors / Matrices** | `$$ \mathbf{X}'\mathbf{\epsilon} = \mathbf{0}, \quad \mathbf{A} - \mathbf{A} = \mathbf{O} $$` | Bold zero $\mathbf{0}$, Bold O $\mathbf{O}$ |

### 5.2.2 General Mathematics Reference Table
In addition to econometric-specific strategies, the system natively supports and standardizes the following fundamental mathematical expressions to ensure the Template Compiler generates flawless OMML:

| Mathematical Concept | LaTeX Syntax | Rendered Example Focus |
| :--- | :--- | :--- |
| **Summations & Products** | `$$ \sum_{i=1}^N x_i, \quad \prod_{j=1}^K y_j $$` | Limits rendered explicitly above/below the operator |
| **Integrals & Limits** | `$$ \lim_{N \to \infty} \int_0^N f(x) \text{d}x $$` | Roman limit, arrow operator, Roman differential |
| **Fractions & Derivatives** | `$$ \frac{\partial y}{\partial x}, \quad \frac{\text{d}y}{\text{d}x} $$` | Vertical fractions, partial $\partial$ vs Roman $\text{d}$ |
| **Roots & Exponents** | `$$ \sqrt{x^2 + y^2}, \quad e^{-\lambda} $$` | Root spanning, superscript nesting |
| **Inequalities & Logic** | `$$ x \le y \implies y \ge x, \quad x \neq 0 $$` | Less than/equal $\le$, implies $\implies$, not equal $\neq$ |
| **Piecewise Functions** | `$$ f(x) = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{otherwise} \end{cases} $$` | Cases environment, Roman text conditions |
| **Greek Variables** | `$$ \alpha, \beta, \gamma, \Gamma, \Delta, \epsilon, \varepsilon, \theta, \Theta $$` | Lowercase (italicized), Uppercase (upright/Roman) |

### 5.2.3 Self-Healing Compilation Loop
For pure theory papers or complex mathematical proofs, EconoSuite utilizes a `/tmp/` sandboxed Self-Healing Compilation Loop (`xelatex -halt-on-error`). A Debugger Agent recursively parses compilation errors to autonomously correct novel proof syntax before final document generation.

### 5.3 Journal Compliance & Structure Limits
*   **The "Keith Head" Introduction Formula:** The engine enforces a 5-step introduction, allocating 25% to 30% of the space directly to summarizing core results.
*   **The "Table of Contents" Paragraph:** The introduction must conclude with a roadmap paragraph detailing the sequence of subsequent sections.
*   **Abstract Length Strictness**: Abstract word limits are rigidly enforced based on the target journal: **AER (100 words)**, **REStud (150 words)**, **JPE/Econometrica (~200 words)**, and **QJE (250 words)**.
*   **Hard Page Limits**: The engine monitors compilation length to ensure manuscripts do not exceed limits (e.g., Main manuscript < 45 typeset pages, Online Appendix < 30 pages).

---

## 6. Document Architecture & Output Handlers (Ethics, Disclosures & Submissions)

EconoSuite strictly saves all generated assets outside the active repository (e.g., `~/EconoSuite_Outputs/[project_name]`).

### 6.1 Output Templating & Native Formats
*   **Taylor & Francis / AEA Templates**: Injecting content directly into standard `interact.cls` or AEA LaTeX classes.
*   **HWPX/OWPML Protocol Generator**: Utilizing Python `zipfile` and `lxml` modules to map texts directly into Korean government `section0.xml` configurations for grant proposals.

### 6.2 The Disclosure Wizard & AI Declarations
*   **Individualized Disclosure Wizard**: The system mandates the generation of **separate PDF disclosure statements for each individual co-author**, detailing funding sources and conflicts of interest. Crucially, even if an author has no conflicts, the system generates a formal statement explicitly claiming "nothing to disclose."
*   **AI Usage Declarations**: Generative AI cannot be listed as an author. EconoSuite generates a specific declaration section immediately preceding the references, detailing the tool's name, version, and the purpose of its use (e.g., readability, translation).
*   **RCT Registry Footnotes**: If the paper involves a Randomized Controlled Trial, the system ensures the RCT is registered and explicitly cites the AEA registry ID in the acknowledgment footnote on the first page.
*   **JEL Classifications**: The manuscript is tagged with at least three relevant *Journal of Economic Literature* (JEL) codes, placed immediately after the abstract.

### 6.3 Pre-Flight Anonymization Scrubber
To preserve double-blind peer-review integrity, EconoSuite introduces an **Anonymization Scrubber**. Before generating the final submission package, this pre-flight tool securely removes all identifying author metadata, names, and affiliations from the primary compiled PDF and DOCX files.

---

## 7. Antigravity Daemon & Agentic Orchestration

The **Antigravity Daemon** operates as the persistent, background orchestrator driving the entire pipeline autonomously.
*   **State Management via `econosuite_project.yaml`**: The daemon tracks project state, metadata, and the sequence of the modular section tags. This YAML file is the definitive source of truth.
*   **Agent Delegation & IPC**: The engine relies on Unix Socket IPC and auto-detected project-scoped directories (`ECONOSUITE_AGENT_DIR`) to manage multi-agent orchestration without race conditions or stale file-watcher conflicts.
*   **NLM Connectivity Hardening Stack**: The daemon forcibly extends internal subprocess polling timeouts by 600 seconds to guarantee that the `KnowledgeOrchestrator` can process deep, high-latency literature scans without falling back to a silent degradation mode. No-Fallback is strictly enforced.
*   **Headless Execution & Isolation**: Direct terminal execution is disabled; the framework runs exclusively via the Daemon. STDIN is inherently routed to `/dev/null` to prevent blocking prompts, and the daemon implements Token-Optimized JSON-logging to preserve LLM context windows during complex DAG execution.

---

## 8. HemaSuite Unified Engine Invariants (Inherited Architecture)

Because EconoSuite is a direct fork of HemaSuite, it strictly inherits and enforces the foundational unified pipeline invariants outlined in the `HemaSuite_Architecture_Note.md`.

### 8.1 The Four-Axis Knowledge Model & Grounding Guards
EconoSuite explicitly models four orthogonal knowledge axes, preventing contamination between literature and empirical Stata results:
*   **Evidence**: External literature/guidelines. Guarded strictly by `guard_nlm_call` (`[NLM-HEALTH]`).
*   **Data**: Empirical observations and $p$-values generated by the ESA engine. Guarded by `[DATA-INTEGRITY]` to ensure exact byte-for-byte match with R/Stata output. No NLM grounding applies here.
*   **Protocol**: Methodology decisions (e.g., DiD vs IV selection). Guarded by `[PROTOCOL-CONSISTENCY]`.
*   **Interpretation**: LLM synthesis of Evidence + Data. Enforces per-sentence axis routing.

### 8.2 The Universal 4-Step Orchestration Pattern
All NLM literature interactions must follow the 4-Step pattern:
1. **Pre-flight Auth & Discovery**: `ensure_nlm_auth` execution.
2. **Verification & Creation**: Fuzzy matching to topic notebooks.
3. **Persistent Mapping**: Caching the Topic $\to$ Notebook ID binding.
4. **Corpus Updating (PubMed/Semantic Scholar Injection)**: Diffing and appending only missing abstracts to the notebook.

### 8.3 The Single-Source Gateway Rule
The `KnowledgeOrchestrator` (KO) acts as the **sole query gateway** for all evidence. Downstream consumers (Triad, ESA Engine) read only from KO-owned stores. No direct calls to `LightRAGClient` or `NotebookLMIntegration` are permitted outside the orchestrator.

### 8.4 Unified Content-Integrity & NLM Health Pipelines
*   **Content-Integrity**: A strict stateless pipeline (`tools/triad/content_integrity.py`) that prevents LLM subprocess contamination and literal scaffold tokens (e.g., `{feature}`) from reaching saved files.
*   **NLM Health**: EconoSuite enforces NLM grounding as a runtime invariant. Any failure (auth lapse, empty response) throws an `NLMHardFailure` which attempts automated maintenance; if unrecoverable, the pipeline strictly halts to prevent silent fallback to non-grounded outputs.

### 8.5 Local Service Port Registry
EconoSuite adheres to the exact local service map to prevent daemon collisions:
*   **`8020`**: LightRAG FastAPI (Guideline/Methodology Knowledge Graph).
*   **`8021`**: Antigravity Agent Daemon FastAPI (LLM delegation proxy).
*   **`11434`**: Ollama (Local embedding/inference).

---

## 9. Dynamic LightRAG & Hardware Constraints

EconoSuite is explicitly designed to scale across hardware environments—operating efficiently on consumer hardware (e.g., a 16GB MacBook Air) via offline offloading, while unlocking full symmetric autonomous extraction on high-end workstations (e.g., a 64GB+ MacBook Pro).

### 9.1 Hardware Health Guard (Dynamic Footprint)
EconoSuite introduces a dynamic `HardwareHardFailure` guard (`engine/hardware_health.py`). During the daemon pre-flight sequence, the `ensure_hardware_safe_execution()` function queries system memory via `sysctl hw.memsize`:
*   **For 16GB Machines**: It strictly verifies that the daemon operates **without any local generation LLM loaded in RAM**. Only lightweight embedding models are permitted. Loading a generation model issues a hard halt to prevent OS freezes during Stata execution.
*   **For 64GB+ Machines**: It unlocks **High-Compute Mode**. The machine is permitted to load heavy local generation models (e.g., `qwen3.6:35b-a3b-q4_K_M` or `qwen3.6:27b-coding-mxfp8`), safely allocating up to 35GB of VRAM while leaving ample overhead for the ESA engine.

### 9.2 LightRAG Architecture (Asymmetric vs. Symmetric)
Depending on the hardware health gate, LightRAG scales its execution strategy:
*   **Asymmetric Execution (16GB Clients)**: Graph indexing is executed explicitly offline on high-memory hardware. The 16GB client runs the LightRAG FastAPI strictly in **Query-Only mode**, querying the pre-compiled `.db` artifact using only local embeddings (`qwen3-embedding:latest`).
*   **Symmetric Execution (64GB+ Clients)**: A 64GB machine can autonomously index and query local graphs on-device using a high-precision model like `qwen3.6:35b-a3b`, bypassing the need for pre-compiled external artifacts.
*   **Knowledge Routing Separation**: Regardless of hardware, empirical/literature queries are routed to the cloud via NotebookLM MCP, while structural/methodology queries hit the local LightRAG graph.
