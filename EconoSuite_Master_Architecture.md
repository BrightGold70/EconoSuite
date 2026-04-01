# EconoSuite Platform: Master Architecture & Technical Specification

**Objective**: This document serves as the foundational master specification for **EconoSuite**, an automated, high-fidelity orchestration pipeline designed explicitly for drafting, analyzing, and formatting top-tier economic research manuscripts. It outlines the core subsystems, econometric requirements, typography rules, and data orchestration modules necessary to operate EconoSuite as an independent, premier platform.

---

## 1. System Overview & Core Orchestration

EconoSuite operates on a unified, state-machine-driven **Orchestration Engine**, executing tasks through multi-phase Directed Acyclic Graphs (DAGs). The system guarantees end-to-end consistency, moving autonomously from literature ingestion to executable code generation and final manuscript compilation.

### The 10-Phase Pipeline
The engine navigates a strict 10-phase sequence:
1. **Ideation & Hypothesis Formulation**
2. **Literature Ingestion & Synthesis**
3. **Identification Strategy Design**
4. **Data Preprocessing & Validation**
5. **Econometric Analysis (ESA execution)**
6. **Robustness & Falsification Testing**
7. **Manuscript Drafting (Gatekeeping & Methodologies)**
8. **Mathematical Typography & Table Generation**
9. **Constitutional Formatting Validation (AEA/QJE Guidelines)**
10. **Final Compilation & Replication Package (PDF/HWPX/Makefiles)**

### Identification Strategy Design (Phase 3)
EconoSuite formalizes the economic approach *before* any data is touched. Through the Orchestration Engine, it enforces a strict sequence:
*   **Formalizing the Counterfactual**: Clearly defining the experimental or quasi-experimental ideal before writing the empirical specification.
*   **Identifying Assumptions**: Explicitly documenting and validating the relevance and exogeneity of instruments (for IV), or proving the parallel trends assumption (for DiD) via simulation or pre-trend data.
*   **Threats to Validity Parsing**: The RAG architecture actively researches known threats to the chosen strategy (e.g., anticipation effects, spillover, or sorting around the threshold in RDD) and drafts robust counter-arguments or falsification tests to preempt reviewer critiques.

---

## 2. The Unified Engine: High-Fidelity Text Generation

The text generation process in EconoSuite is far more rigorous than standard prompt-completion. It utilizes a **Unified Engine** (a complete refactoring and merging of the legacy Protocol and Manuscript Triad Orchestrators) built upon a high-fidelity Retrieval-Augmented Generation (RAG) architecture.

### 2.1 Cross-Section Consistency & Auditing
Economic manuscripts require absolute mathematical and narrative synchronization between the theory, the identification strategy, and the empirical results. The Unified Engine achieves this through:
*   **Constitutional Validation**: Before any drafted section is finalized, an autonomous critic agent audits the text against the original hypotheses and theoretical models. The engine strictly avoids the "history of the trial-and-error process," ensuring the text is a precisely engineered argument.
*   **Statistical Auditing**: The text generator dynamically reads the output artifacts from the ESA Engine. It injects valid coefficients directly into the text, neutralizing hallucinated values.
*   **Concrete vs. Abstract Lexicon**: Based on NLP reviews of desk-rejected AER papers, the engine forces "concrete and descriptive" terminology, actively scoring and rejecting overly abstract linguistic framing.

### 2.2 Iterative RAG Drafting Pipeline
1.  **Ingestion & Mapping**: The engine pulls specifically tagged chunks from the Semantic Scholar/RePEc vector database.
2.  **Constraint Enforcement**: The text generation prompt is layered with AEA/QJE journal-specific constraints (e.g., abstract length limits, tone, specific vocabulary).
3.  **Section Drafting (DAG Execution)**: Text is drafted in a non-linear Directed Acyclic Graph. For instance, the "Data & Methodology" section is drafted *simultaneously* with the "Robustness Checks" once the ESA engine concludes, but the "Introduction" is locked until all empirical results are finalized and validated.

---

## 3. Literature Ingestion & Knowledge Base

EconoSuite integrates specialized data ingestion APIs to ensure the research is grounded in the latest economic theory and working papers.

*   **API & Database Integrations**:
    *   **Semantic Scholar Graph API**: For deep citation networks and influential paper tracking.
    *   **RePEc (Research Papers in Economics)**: The definitive repository for economics working papers.
    *   **NBER Working Papers Indexer**: Continuous scraping of National Bureau of Economic Research publications to ensure state-of-the-art methodology adherence.
*   **Intelligent JEL Classification**:
    *   The specialized `JELClassifier.py` autonomously parses abstract content and assigns highly precise Journal of Economic Literature (JEL) indexing codes. EconoSuite enforces the inclusion of at least three relevant codes (e.g., C: Quantitative Methods, D: Microeconomics) to map into the granular subfields required by top journals.

---

## 4. The ESA (Economic-Statistic-Analysis) Engine

The analytical core of EconoSuite bypasses traditional biostatistics in favor of rigorous, causal inference methodologies.

### Core Causal Inference Capabilities
The engine natively selects, processes, and validates:
*   **Instrumental Variables (IV / 2SLS)**: Validating relevance and exogeneity assumptions.
*   **Difference-in-Differences (DiD)**: Executing parallel trends testing and dynamic treatment effect plotting.
*   **Regression Discontinuity Design (RDD)**: McCrary density sorting and bandwidth optimization.
*   **Synthetic Control Methods (SCM)**: Placebo testing in space and time.
*   **Heckman Selection Models**: Controlling for non-random sample selection.

### Reproducibility & Code Generation
*   **Stata Script Auto-generation**: The engine automatically translates Python DataFrames and model logic into highly commented, executable Stata `.do` scripts.
*   **Replication Package Mandate**: EconoSuite natively complies with the strict AEA/RES Data and Code Availability Policy. For every simulation or empirical run, the orchestrator:
    1.  Generates a master `makefile`.
    2.  Hardcodes the pseudo-random generator `seed` for Monte Carlos.
    3.  Writes comprehensive `README` documentation (including software versions like Stata 17, R 4.2).
    4.  Outputs proprietary datasets in dual formats (e.g., `.dta` and `.csv`/ASCII).

### Robustness Checks & Falsification
The orchestrator enforces strict falsification testing categorized by a standard taxonomy: Sub-sample Splits, Alternative Specifications, Moment Selection, Functional Forms, and Out-of-sample Testing.
*   **Linguistic Precision**: When drafting robustness results, the Unified Engine physically prevents vagueness. Phrases like *"the results are qualitatively the same"* are flagged; the generator must explicitly state which features (sign and relative magnitude) remained constant.

---

## 5. Typography, Formatting & Structural Adherence

Top-tier economic journals (e.g., *American Economic Review* (AEA), *Quarterly Journal of Economics* (QJE)) enforce extremely rigid stylistic guidelines. EconoSuite hardcodes these rules to prevent desk rejections.

### Dynamically Injected Journal Templates
To eliminate formatting friction, EconoSuite natively parses and adheres to specific journal typesetting templates (`.cls`, `.sty`, or `.bst` files):
*   **Taylor & Francis 'Interact' Class**: Official routing for the `interact.cls` LaTeX class, ensuring compliance with **Journal of Applied Economics**, **The International Trade Journal**, and **Global Economic Review**. This handles bespoke `natbib` integration for author-year versus APA styles depending on the specific Routledge journal requirements.
*   **AER / AEJ Styles**: Automated configuration of `aea.cls`, ensuring perfect adherence to frontmatter layout and JEL codes placement.
*   **Econometrica / QJE Styles**: Dynamic swapping of margin sizes, inter-line spacing, and proof environment formatting.
*   **Automated Bibliographies**: Native handling of `.bib` database extraction and formatting according to the specific journal's `bibliographystyle`.

### The `LaTeXMathCompiler.py` & Automated Math Generation
Generating syntactically perfect LaTeX in a high-throughput, non-interactive environment requires completely decoupling mathematical logic from raw text generation. EconoSuite solves this via a dual-engine approach:

1.  **Macro JSON Injection (Standard Empirical Models)**:
    *   For core causal inference strategies (IV, DiD, RDD, SCM), the LLM relies entirely on predefined LaTeX macros hardcoded into the template (e.g., `\DiDModel{Dependent}{Treat}{Post}{Error}`).
    *   The LLM agent only outputs validated JSON schemas (`{"model": "DiD", "dependent": "Y_{it}", ...}`). Python injects this into the preamble, mathematically guaranteeing compilation success without human input.
2.  **Self-Healing Compilation Loop (Novel Theoretical Proofs)**:
    *   When the Drafting Agent must generate custom theoretical mathematical modeling (e.g., a specific utility function or game-theoretic equilibrium), it outputs raw LaTeX.
    *   The orchestrator immediately routes this block into a `/tmp/` sandbox and executes `xelatex -halt-on-error`. If compilation fails due to hallucinated syntax (e.g., mismatched brackets or missing environments), the daemon captures the `.log` trace and autonomously feeds it to a **Debugger Critic Agent**, executing correction loops in the background until it compiles flawlessly.
3.  **Natural Language to LaTeX Translator (Revision Phase)**:
    *   While the initial pipeline is fully automated, the **Refinement Phase** allows for "human-in-the-loop" interaction. Instead of manually writing complex LaTeX code, the user provides natural language directives.
    *   **EconoSuite Shorthand Syntax (EconoSyntax)**: To reduce LLM hallucination during translation, EconoSuite provides a domain-specific pseudo-syntax. The **LaTeX Translator Agent** deterministically parses this into strict Top Five typography without guesswork.
    *   The Agent isolates the existing math block, reconstructs the precise LaTeX syntax using Econometrica typographical standards, and re-injects standard, compilable code safely into the manuscript.

#### EconoSyntax Comprehensive Mappings
*(Generated to prevent LLM hallucination and enforce strict Econometrica/AER compliance)*

| EconoSyntax Input | Output LaTeX Rendering Objective | Econometric Context |
| :--- | :--- | :--- |
| **1. Expectations & Probabilities** |
| `E[Y | X]` | `\mathbb{E}[Y \mid X]` | Conditional Expectation (Blackboard bold). |
| `Var(X | Z)` | `\text{Var}(X \mid Z)` | Conditional Variance. |
| `Cov(X, Y)` | `\text{Cov}(X, Y)` | Covariance Operator. |
| `Pr(Y=1 | X)` | `\Pr(Y = 1 \mid X)` | Conditional Probability (Logit/Probit). |
| **2. Asymptotics & Limits** |
| `plim(X_n)` | `\text{plim}_{n \to \infty} X_n` | Probability limit. |
| `converge_d` | `\xrightarrow{d}` | Convergence in distribution. |
| `converge_p` | `\xrightarrow{p}` | Convergence in probability. |
| `normal_dist(mu, sigma^2)` | `\mathcal{N}(\mu, \sigma^2)` | Normal Distribution (Calligraphic math font). |
| **3. Linear Models & Causality** |
| `OLS(Y, X)` | `Y_{it} = \alpha + \boldsymbol{X}_{it}'\boldsymbol{\beta} + \epsilon_{it}` | Multivariate OLS (Bold vectors, proper transpose). |
| `DiD(Y, D, Post)` | `Y_{it} = \alpha + \beta_1 D_i + \beta_2 \text{Post}_t + \beta_3 (D_i \times \text{Post}_t) + \epsilon_{it}` | Difference-in-Differences. |
| `IV_1(X, Z)` | `X_{it} = \pi_0 + \boldsymbol{Z}_{it}'\boldsymbol{\pi} + \nu_{it}` | First stage IV/2SLS. |
| `IV_2(Y, X_hat)` | `Y_{it} = \alpha + \beta \hat{X}_{it} + \epsilon_{it}` | Second stage IV/2SLS. |
| `RDD_sharp(Y, X, c)` | `Y_i = \alpha + \tau \mathbb{1}\{X_i \ge c\} + f(X_i - c) + \epsilon_i` | Sharp Regression Discontinuity (Indicator function). |
| **4. Panel Data & Fixed Effects** |
| `FE_twoway(Y, X)` | `Y_{it} = \boldsymbol{X}_{it}'\boldsymbol{\beta} + \mu_i + \gamma_t + \epsilon_{it}` | Two-way Fixed Effects (Individual & Time). |
| `RE_error(u)` | `u_{it} = \mu_i + \nu_{it}` | Random Effects error decomposition. |
| **5. Advanced Estimators (MLE / GMM)** |
| `MLE_obj(theta)` | `\hat{\boldsymbol{\theta}}_{MLE} = \arg\max_{\boldsymbol{\theta}} \sum_{i=1}^n \log L(\boldsymbol{\theta} \mid y_i, \boldsymbol{x}_i)` | Maximum Likelihood Objective. |
| `GMM_obj(theta)` | `\hat{\boldsymbol{\theta}}_{GMM} = \arg\min_{\boldsymbol{\theta}} \left[ \frac{1}{n} \sum_{i=1}^n \boldsymbol{g}(y_i, \boldsymbol{x}_i, \boldsymbol{\theta}) \right]' \boldsymbol{W} \left[ \frac{1}{n} \sum_{i=1}^n \boldsymbol{g}(y_i, \boldsymbol{x}_i, \boldsymbol{\theta}) \right]` | Generalized Method of Moments. |
| **6. Matrix Algebra (Econometrica Style)** |
| `matrix_inv(X'X)` | `(\boldsymbol{X}'\boldsymbol{X})^{-1}` | OLS projection matrix inverse. |
| `trace(A)` | `\text{tr}(\boldsymbol{A})` | Trace of a matrix. |
| `rank(A)` | `\text{rk}(\boldsymbol{A})` | Rank of a matrix. |
| `kronecker(A, B)` | `\boldsymbol{A} \otimes \boldsymbol{B}` | Kronecker product. |

Economic mathematical notation strictness is enforced globally within these pipelines to signal "submission-ready" rigor:
*   **Basic Notation**: Italicized scalars; boldface vectors and matrices. Sets use script fonts, while number sets ($\mathbb{R}$, $\mathbb{Z}$, $\mathbb{N}$) use Blackboard bold font. Subscripts/superscripts are capped at 2 levels.
*   **Fractions**: Forces solidus ($x/y$) for inline fractions and reserves `\frac{}` for displayed equations.
*   **Advanced Matrix Operators**: Strict enforcement of Econometrica conventions: Transpose uses $A'$ or $A^0$ (never $A^T$), Trace uses $tr(A)$, Rank uses $rk(A)$, Kronecker uses $A \otimes B$. Distinguishes strictly between null vector ($0$) and null matrix ($O$).

### 5. Korean Government Protocol Engine (HWPX/OWPML)
Domestic Korean funding agencies (NRF, KDI, BOK) exclusively mandate grant protocols structured in `.hwp` and `.hwpx` templates (e.g., `신진연구자지원사업` - Early Career Researcher Support Program). To automate these domestic pipelines, EconoSuite shifts away from LaTeX into an autonomous XML injection framework.

1.  **Standardization Gateway**: Due to macOS platform constraints, all legacy binary `.hwp` templates must be converted to the modern, open-standard `.hwpx` (Open Word-Processor Markup Language) format before ingestion.
2.  **OWPML Payload Injection (The `HWPXGenerator.py`)**: 
    *   Since a `.hwpx` file is inherently a ZIP archive, the generator mounts into the `Contents/section0.xml` environment.
    *   Using Python's `lxml` tree parser, the engine isolates pre-ordained mapping boundaries (e.g., `<<RESEARCH_METHODOLOGY>>`) embedded inside the XML `<hp:t>` (paragraph text) tags.
    *   The Unified Engine drafts pristine Korean text describing the causal inference strategies established in Phase 2, and the Generator injects it seamlessly into the XML DOM without breaking the rigid government formatting conventions (fonts, table paddings).
3.  **Final Compression**: The mutated XML structure is re-zipped, producing a natively readable `.hwpx` file ready for an agency portal upload.

### Tabular Standards
*   **Horizontal Lines Only**: Tables must utilize `\toprule`, `\midrule`, and `\bottomrule` (via `booktabs`). Vertical dividers are strictly prohibited.
*   **Significance & Numerics**: Complete suppression of "stargazing" (asterisks `*`, `**`). Standard errors are stated in parentheses. Decimal fractions uniformly include a leading zero (0.357, not .357).

### Structural Journal Compliance
*   **Gatekeeping Introduction Segment**: Utilizing the "Keith Head Introduction Formula." The intro (usually 5-6 pages) establishes a hook, the research question, antecedents, and the value-added. Crucially, EconoSuite allocates 25% to 30% of the introduction directly to summarizing the core results before concluding with a structural roadmap.
*   **Abstract Strictness**: EconoSuite dynamically adjusts abstract constraints based on the target:
    *   **AER**: Max 100 words, no citations, no title page.
    *   **QJE**: Max 250 words, separate title page.
    *   **Econometrica**: ~200 words, anonymous PDF structure.

### Ethics & Disclosure Injection
*   **Disclosure Statements**: Automatically generates conflict of interest paragraphs and formal AI disclosures per contemporary publisher mandates.
*   **IRB Stamping**: Forces the inclusion of Institutional Review Board protocol numbers for studies involving human data.

---

## 6. Antigravity Daemon & Agentic Orchestration

EconoSuite is fundamentally powered by the **Antigravity Daemon**, which operates as the persistent, background orchestrator driving the entire 10-phase pipeline autonomously.

### Continuous Pipeline Execution
*   **State Management & Resilience**: The daemon continuously monitors the DAG execution state. If an econometric falsification test fails or an API times out (e.g., Semantic Scholar throttling), the daemon autonomously triggers fallback mechanisms, adjusting parameters or re-routing logic without manual user intervention.
*   **Persistent Context & Memory**: The daemon maintains a rolling, persistent context of the manuscript's progression. It cross-references current drafts against the initial "Ideation & Hypothesis" constraints, ensuring the final text strictly adheres to the original Identification Strategy.
*   **Tool & MCP Coordination**: The daemon acts as the central nervous system connecting Python execution environments (ESA Engine, `LaTeXMathCompiler`) with external Model Context Protocol (MCP) servers seamlessly.

---

## 7. Multi-Agent Integration & Deep Research

> [!TIP]
> **NotebookLM MCP / Intelligent Synthesis**
> EconoSuite utilizes the `jacob-bd/notebooklm-mcp-cli` for advanced synthesis. By uploading hundreds of working papers and utilizing deep research capabilities alongside the orchestrator, the AI agents can accurately spot identification strategy flaws, literature gaps, and suggest robustness checks based on the latest NBER publications. 

---

## 8. Document Architecture & Output Handlers

*   **Native HWPX Support (Hancom OWPML)**: Aside from standard `.tex` and `.pdf` packages, EconoSuite bridges the domestic-international gap by natively supporting `.hwpx` outputs through Hancom OWPML models. This ensures seamless submissions to Korean policy institutes (e.g., KDI, BOK) and domestic journals without formatting loss.
*   **Citation Database Reliability**: The `EndNoteWriter` manages structural integrity, eliminating schema corruption in `.Data` folders during the aggressive citation mapping required for empirical literature reviews.
