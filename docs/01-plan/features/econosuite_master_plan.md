# PDCA Feature Plan: EconoSuite Platform Transformation

## 1. Feature Specifications

### 1.1 Core Orchestration & Unified Engine
*   **Objective**: Establish a massive multi-pipeline orchestrator capable of intelligently accepting every formal submission classification inherent to top-tier economic journal standards.
*   **Key Deliverables**: 
    1. A multi-phase DAG orchestrator spanning a **Five-Tier Execution Pipeline**:
       *   **Empirical Pipeline**: Full ESA Engine activation mapping structural/reduced-form analytics.
       *   **Theoretical Pipeline**: Coupling the Drafting Engine strictly to the `LaTeXMathCompiler` for pure theory, proofs, and methodological estimations.
       *   **Review Pipeline**: Literature syntheses, book reviews, editorials, and PRISMA Flow Diagram scoping reviews.
       *   **Short Communications**: Ultra-concise layouts for notes and replies.
       *   **Proposal Protocol**: Direct XML translation routing into Korean govt. `.hwpx` standard templates, mandating the RAG text generator to draft the methodology and goals entirely in the **Korean language**.
    2. Constitutional validation mapping the drafting engine strictly to the Keith Head Introduction formula (25-30% result summary, concrete lexicon).
    3. **Phase-level Checkpointing & Run Adapters**: A unified entry logic module managing persistent DAG states, allowing instantaneous resumption after API timeouts without data loss.
    4. **Strict No-Fallback Mode & NLM Connects**: Complete removal of silent degradation pathways; the pipeline enforces a hard-stop for human or Debugger Agent intervention upon econometric failure, as well as upon NotebookLM extraction failures. EconoSuite enforces a 600s padded connection stack (`NOTEBOOKLM_QUERY_TIMEOUT=600`) to guarantee deep-literature queries don't trigger fallback modes.
    5. **Exclusive Daemon Routing**: Direct terminal execution is disabled; the framework *always* forces execution through the Antigravity daemon wrapper, except when utilizing the native Tauri or Streamlit graphical interfaces.
       *   **Antigravity Token-Optimized Logging**: Implementation of condensed JSON-logging rather than human-readable text to preserve the agent's context window.
       *   **STDIN Isolation**: Native routing of `STDIN` to `/dev/null` to enforce fully headless execution without blocking prompts.
    6. **Agent Delegation & IPC Upgrades**:
       *   **Unix Socket IPC Migration**: High-priority architectural shift replacing file-based handshake delegation with Unix sockets to natively support DAG parallelism and eliminate file-based race conditions.
       *   **Directory Auto-Detection**: Implementation of project-scoped agent directory tracking (`ECONOSUITE_AGENT_DIR`) to isolate daemon protocol runs from extraneous file watcher events and stale data.

### 1.2 ESA (Economic-Statistic-Analysis) Engine
*   **Objective**: Establish a rigorous causal inference analysis and data presentation backend spanning the full taxonomy of modern econometrics, guided by an intelligent DGP selection parser.
*   **Key Deliverables**: 
    1. **Data Ingestion & Profiler Node**: A module designed to parse `.csv`/`.dta` files alongside a `ResearchSchema.yaml` to extract the Working Title and isolate the Dependent ($Y$) variable. Includes autonomous distribution testing (e.g., checking for censoring boundaries, binary 0/1 distributions).
    2. **Automated Method Selection Heuristic**: A pre-analyzer that maps theoretical models based on Dependent Variable types (Continuous $\to$ OLS; Binary $\to$ Logit/Probit; Censored $\to$ Censored Regression; Duration $\to$ Hazard Models; Selected $\to$ Endogenous Selection) and Research Title Intent (Impact $\to$ IV Causal Isolation; Policy $\to$ Structural Modeling).
    3. **Causal Inference Handlers**: Integration of RCTs, IV/2SLS, DiD, RDD, Regression Kinks, Synthetic Controls, and precise targeting estimators (ATE, ATT, LATE, MTE, QTE).
    2. **Extremum Estimator Pipeline**: Functionality for OLS, Fixed Effects, MLE/QML, GMM, and Limited Dependent Variables (Logit/Probit/Censored).
    3. **Robust/Nonparametric Modules**: Implementations for Method of Sieves (splines/wavelets), semiparametric endogenous sample selection, kernel/nearest-neighbor estimators, and dynamic enforcement of Heteroskedasticity-Consistent Standard Errors.
    4. **Simulation & Resampling Compute**: Markov Chain Monte Carlo (MCMC/Metropolis-Hastings), Method of Simulated Moments (MSM), and Bootstrap routines for variance estimation.
    5. A Replication Package Generator that natively outputs fully commented Stata `.do` scripts, `Makefiles`, predetermined simulation seeds, and AEA-compliant `README` configurations.
    6. An automated econometric falsification suite spanning Sub-sample splits, Alternative Specifications, and Functional Forms.
    7. **Supplemental Appendix Auto-Router**: Diverts the excessive robustness check tables into an autonomous, clearly labeled appendix document to preserve main-text brevity.

### 1.3 Mathematical Typography & Typesetting (EconoSyntax)
*   **Objective**: Enforce strictly compliant "Top Five" mathematical rendering and tabular limits natively in LaTeX without human intervention.
*   **Key Deliverables**:
    1. Rigid structural enforcement for tables: 9-column portrait limits, 0 stargazing, leading zero decimals, and horizontal-only `booktabs`.
    2. A Macro JSON Extractor pipeline where LLM agents supply only variable constraints, protecting bracket syntax integrity.
    3. A `/tmp/` sandboxed Self-Healing Compilation Loop (`xelatex -halt-on-error`) managed by a Debugger Agent to recursively correct novel proofs.
    4. The Natural Language LaTeX Translator Agent driven by the hardcoded **EconoSyntax** pseudo-syntax mapping. Includes expansive vocabulary for Probability Limits ($O_p, o_p$), Time Series lags ($L, \Delta$), Calculus with roman differentials ($\text{d}$), Matrix operators (Hadamard product), and strict Null Vector ($\mathbf{0}$) / Null Matrix ($\mathbf{O}$) distinctions.

### 1.4 Native Output & Document Architecture
*   **Objective**: Package final drafts into submission-ready configurations and complex visuals. All produced files, assets, and replication packages must be explicitly routed and stored outside the active repository at `~/EconoSuite_Outputs/[topic_or_project_name]`.
*   **Key Deliverables**:
    1. Taylor & Francis `interact.cls` templating injection engine.
    2. Automated PRISMA Flow Diagram generators specifically for economic scoping reviews (e.g., *Econometrics*).
    3. Dynamic ethics and disclosure statement appending.
    4. The highly specialized **HWPX/OWPML Protocol Generator** utilizing `zipfile` and `lxml` to map texts directly into Korean government `section0.xml` configurations.

## 2. Technical Dependencies
*   Python `lxml` and `zipfile` modules for OWPML extraction.
*   Background LaTeX distributions (`xelatex`, `pdflatex` + `booktabs`).
*   Data APIs (Semantic Scholar API access keys, NBER indices).

## 3. Implementation Phasing
*   **Phase 1**: Base API transition, RAG core, and intro structural formulas.
*   **Phase 2**: Python-to-Stata ESA Engine and robust testing framework.
*   **Phase 3**: Math typographical compilers (Macro + Self-healing) and EconoSyntax mapping setup.
*   **Phase 4**: Output formatting (HWPX, `interact.cls`).

## 4. Verification Protocols
*   **Numeric Verification**: Audit auto-generated Stata outputs against Python native analysis modules.
*   **Compilability Audit**: Stress-test the background `xelatex` autocorrect loop with purposefully broken math syntax.
*   **XML Integrity**: Ensure generated `.hwpx` files open without corruption in conventional Hancom suite viewers.
