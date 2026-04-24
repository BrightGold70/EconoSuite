# EconoSuite Platform: Master Architecture & Technical Specification

**Objective**: This document serves as the foundational master specification for **EconoSuite**, an automated, high-fidelity orchestration pipeline designed explicitly for drafting, analyzing, and formatting top-tier economic research manuscripts. It outlines the core subsystems, econometric requirements, typography rules, and data orchestration modules necessary to operate EconoSuite as an independent, premier platform.

---

## 1. System Overview & Core Orchestration

EconoSuite operates on a unified, state-machine-driven **Orchestration Engine**, executing tasks through multi-phase Directed Acyclic Graphs (DAGs). The system guarantees end-to-end consistency, moving autonomously from literature ingestion to executable code generation and final manuscript compilation.

### The Master Synopsis (The Core Blueprint)
A fundamental concept of EconoSuite is that the system is heavily front-loaded. Rather than expecting the user to manually micromanage every stage, Phase 1 autonomously generates a highly detailed **Master Synopsis** (`Synopsis.md`). 
This AI-generated Synopsis locks in the research topic, theoretical background, causal endpoints, required datasets, and the exact econometric identification strategy. **Every subsequent phase of the pipeline is strictly guided by, and validated against, this single Master Synopsis.**

### The 10-Phase Pipeline
The engine navigates a strict sequence governed by the Synopsis:
1. **Ideation & Master Synopsis Generation** (EconoSuite drafts the blueprint).
2. **Literature Ingestion & Synthesis** (RAG queries strictly scoped to the Synopsis).
3. **Identification Strategy Formalization** (Mathematical lockdown of the Synopsis).
4. **Data Preprocessing & Harmonization** (Fetching specific variables dictated by the Synopsis).
5. **Econometric Analysis (ESA execution)** (Blueprint converted to Jinja2 R templates).
6. **Robustness & Falsification Testing** (Testing validity threats defined in the Synopsis).
7. **Manuscript Drafting** (The narrative must reflect the original Synopsis endpoints).
8. **Mathematical Typography & Table Compilation**
9. **Constitutional Formatting Validation (AEA/QJE Guidelines)**
10. **Final Compilation & Replication Package (PDF/HWPX/Makefiles)**

### Identification Strategy Design (Phase 3)
Before touching data, EconoSuite translates the Master Synopsis into a strict mathematical approach:
*   **Formalizing the Counterfactual**: Clearly defining the experimental or quasi-experimental ideal based on the endpoints in the Synopsis.
*   **Identifying Assumptions**: Explicitly documenting and validating the relevance and exogeneity of instruments (for IV), or proving the parallel trends assumption (for DiD) via simulation or pre-trend data.
*   **Threats to Validity Parsing**: The RAG architecture actively researches known threats to the chosen strategy and mandates robust counter-arguments to preempt reviewer critiques.

---

## 2. The Unified Engine: Comprehensive Submission Pathways

The text generation process in EconoSuite is far more rigorous than standard prompt-completion. It utilizes a **Unified Engine** built upon a high-fidelity Retrieval-Augmented Generation (RAG) architecture. At initialization, the user explicitly declares the manuscript's underlying methodology and formal submission category. This categorizes the graph execution into a **Five-Tier Pipeline Architecture**:

1.  **The Empirical (Data-Driven) Pipeline**: The flagship EconoSuite pathway for *Original Research*. Expects distinct tabular data. Triggers the ESA Engine (Data Profiler, Method Heuristic), generates Stata Repliation Packages, and distinguishes implicitly between Structural vs. Reduced-Form models depending on the title intent.
2.  **The Pure Theoretical Pipeline**: Handles *Theoretical Papers* and *Methodological / Econometric Papers*. Entirely bypasses Data Profiling and Stata. Instead, tightly couples the RAG engine directly to the `LaTeXMathCompiler` to continuously validate and render pure economic theory, proofs, and internal consistency checks using EconoSyntax without waiting for dataset parameters.
3.  **The Comprehensive Review Pipeline**: Designed for *Review Articles, Essays, Book Reviews, Editorials*, and *Interviews*. Maximizes Semantic Scholar API timeouts for exhaustive literature digestion and critical evaluation. Retains the capability to generate PRISMA Flow Diagrams for rigid scoping submissions.
4.  **The Short Communications Pipeline**: Tailored for *Notes, Miscellanea, and Replies*. Truncates the Keith Head introduction constraints and strips vast literature digests in favor of ultra-concise, single-innovation reporting frameworks.
5.  **The Proposal / Protocol Pipeline**: Exclusively tailored for domestic funding. Suppresses all LaTeX compilation. The RAG outputs are mandated to be drafted entirely in **Korean language** to align with domestic standards. The generated Korean text blocks are securely mapped into the **HWPX/OWPML Protocol Generator** to compile into formatting-strict Korean government templates (e.g., NRF or KDI grant `.hwpx` files).

### 2.1 Cross-Section Consistency & Auditing
Economic manuscripts require absolute mathematical and narrative synchronization between the theory, the identification strategy, and the empirical results. The Unified Engine achieves this natively across all pipelines through:
*   **Constitutional Validation**: Before any drafted section is finalized, an autonomous critic agent audits the text against the original hypotheses and theoretical models. The engine strictly avoids the "history of the trial-and-error process," ensuring the text is a precisely engineered argument.
*   **Statistical Auditing**: The text generator dynamically reads the output artifacts from the ESA Engine. It injects valid coefficients directly into the text, neutralizing hallucinated values.
*   **Mandatory Structural Guidelines (The "Unwritten Rules")**:
    *   **The "Keith Head" Introduction Formula:** The engine enforces a rigid 5-step introduction: Hook, Question, Antecedents, Value-Added, and Roadmap.
    *   **The "John Cochrane" Rule (No Suspense):** The drafting agent is constrained to state the primary empirical findings on page one, actively preventing "mystery novel" structures.
*   **Concrete vs. Abstract Lexicon (McCloskey Constraints)**: Based on Deirdre McCloskey's *Economical Writing*, the engine forces active voice and "concrete and descriptive" terminology, actively scoring and rejecting overly abstract linguistic framing or passive phrasing (e.g., rejecting "it should be noted that").
*   **Trade Terminology Enforcement**: When the `JELClassifier.py` tags the paper as International Trade (e.g., F10, F14), the engine strictly maps concepts to formal trade nomenclature: enforcing distinctions between *Intensive/Extensive Margins*, defining shipping frictions strictly as *Iceberg Transport Costs*, and requiring *Multilateral Resistance Terms* in any Gravity Model discussion.

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
*   **Local LightRAG Architecture (Offline Engine)**:
    *   To ensure strict compliance with mathematical syntaxes and editorial constraints without internet dependency, EconoSuite deploys a local **LightRAG** (Graph-Enhanced Retrieval-Augmented Generation) system.
    *   **Guideline Index (`data/guideline/`)**: Indexes the Cochrane, McCloskey, Keith Head, and WTO structural constraints. The drafting agent queries this graph to validate tone, structure, and terminology during the writing phase.
    *   **Statistical Manual Index (`data/statistics/`)**: Indexes the dense PDF manuals of R packages (e.g., `MCMCpack`, `np`, `did`). The ESA Engine queries this database to extract exact, hallucination-free code parameters and default assumptions during script generation.
*   **Intelligent JEL Classification**:
    *   The specialized `JELClassifier.py` autonomously parses abstract content and assigns highly precise Journal of Economic Literature (JEL) indexing codes. EconoSuite enforces the inclusion of at least three relevant codes (e.g., C: Quantitative Methods, D: Microeconomics) to map into the granular subfields required by top journals.

---

## 4. The ESA (Economic-Statistic-Analysis) Engine

The analytical core of EconoSuite bypasses traditional biostatistics in favor of rigorous, modern theoretical econometrics capable of executing and diagnosing modern empirical designs. 

### Data Ingestion & Profiling Protocol
Because EconoSuite autonomously dictates the statistical pipeline, data collection is executed only *after* the theoretical architecture (Phase 3) dictates the exact variables required. EconoSuite supports two distinct ingestion pathways:

#### Pathway A: Autonomous API Data Deduction (Preferred)
1.  **Topic Analysis via LightRAG**: The user submits a natural language research topic. The Orchestrator queries the local LightRAG database to deduce the necessary theoretical variables (e.g., Gravity models require Bilateral Trade, GDP, and Distance).
2.  **Parameter Inference & LLM Tool Use**: The agent autonomously maps these theoretical variables into precise API parameters. Using native function calling, it triggers predefined tools (e.g., `fetch_comtrade()`, `fetch_wdi()`, `fetch_wto()`).
3.  **Dynamic Script Execution & Harmonization**: EconoSuite dynamically writes an R/Python script to fetch the exact data vector from the internet, handling API pagination and rate limits. The raw data is automatically harmonized into a structural panel dataset before the ESA Engine triggers.

#### Pathway B: The Manual Supply Mandate (For Proprietary Data)
1.  **The Dual Supply Mandate**: For non-public data, the user must supply two assets: The Raw Data Matrix (`.csv` or `.dta`) and a `ResearchSchema.yaml` designating the Dependent ($Y$) variable.
2.  **Autonomous Matrix Profiler (Pre-Flight Phase)**: EconoSuite loads the data matrix using pandas/NumPy to scan the specific $Y$ array.
    *   If $Y \in \{0, 1\}$, it tags the data as Binary.
    *   If $Y \ge 0$ with mass accumulation at $0$, it tags the data as Censored.
    *   It runs initial Shapiro-Wilk and Breusch-Pagan testing to verify homoskedastic parameters.

### Automated Method Selection Heuristic
To operate autonomously, the ESA Engine initiates every analysis by applying a strict heuristic to the dataset and research title to map out the theoretical Data Generation Process (DGP) before running models:
1.  **Selection by Dependent Variable (Data Type):**
    *   *Continuous Data*: Routes to standard parametric linear models (Ordinary Least Squares - OLS).
    *   *Discrete/Binary Data* (e.g., Voting, Brand Choice): Routes to Limited Dependent Variable Models (Probit, Logit, Maximum Score Estimators).
    *   *Censored Data* (e.g., Capped expenditure thresholds): Routes to Censored Regression Models.
    *   *Duration/Time-to-Event Data* (e.g., Employment lags): Routes to Hazard Models (Cox proportional hazards, Weibull duration models).
    *   *Endogenously Selected Data* (e.g., Self-selected samples): Routes to Endogenous Sample Selection Models (Heckman).
2.  **Selection by Topic Title (Research Intent):**
    *   *Impact / Effect*: Titles suggesting causal relationships compel the system to prioritize exogeneity handlers (Instrumental Variables - IV) over simple descriptive correlation to control for "wrong-way" causality.
    *   *Policy / Forecasting*: Titles implying policy scenario prediction trigger Structural Modeling invariants rather than historical regression.
    *   *Topic-Specific Overrides*: Specific keywords trigger rigid mathematical paths (e.g., "Willingness-to-Pay" forces binary response contingent valuation architectures).
3.  **DGP Diagnostics (The Assumption Check):**
    *   The engine tests distribution assumptions. If errors are non-normal or heteroskedastic, it autonomously shifts away from parametric methods toward robust, nonparametric estimation (kernels, sieves).
    *   If endogeneity or unobserved heterogeneity is detected, the engine mandates structural heterogeneity parameters or robust control strategies.

### The Codebase Architecture: Autonomous Package Selection & Execution
To execute these heuristics without crashing due to LLM coding hallucinations, the ESA Engine codebase is physically structured as a deterministic pipeline:

1.  **The Blueprint Parser (LLM $\rightarrow$ JSON)**: The Orchestrator does *not* write R code directly from the natural language Synopsis. Instead, it generates a rigid `AnalysisBlueprint.json`. This JSON explicitly maps the dataset headers to theoretical variables (Dependent, Treatment, Controls).
2.  **Autonomous Package Selection (LightRAG + Profiler)**: EconoSuite dynamically selects the optimal CRAN package by fusing the dataset profile with journal guidelines.
    *   *Example*: If the topic involves staggered policy rollouts across states, LightRAG informs the Agent that standard Two-Way Fixed Effects (TWFE) is biased. The Agent autonomously ignores base R and forces the inclusion of `"recommended_packages": ["did", "bacondecomp"]` into the Blueprint JSON.
    *   *Data Trigger*: If the Profiler detects thousands of covariates but limited observations, it forces the inclusion of `"xgboost"` or `"glmnet"`.
3.  **The ESA Factory (Python Jinja2 Templating)**: Instead of "freestyling" scripts, a Python module (`esa_generator.py`) reads the `AnalysisBlueprint.json` and injects the parameters into pre-tested, hardened **Jinja2 R Templates** (e.g., `did_twfe_template.R`, `iv_regression_template.R`). This completely guarantees flawless syntax during execution.
4.  **The Falsification Loop**: Python runs the generated script via `subprocess`. If a statistical error occurs (e.g., "Matrix computationally singular"), Python feeds the error back to a Debugger LLM to alter the JSON blueprint and autonomously retry.

### Core Econometric Methodologies
The heuristic and the ESA Factory trigger computation across four major pillars:
1.  **Causal Inference & Treatment Effects**:
    *   *Handlers*: Randomized Controlled Trials (RCTs), Instrumental Variables (`AER::ivreg`), Difference-in-Differences (`did`, `bacondecomp`), Regression Discontinuity Design (`rdrobust`), Regression Kink Design, and Synthetic Controls (`Synth`).
    *   *Estimators*: Functionality explicitly targets the Average Treatment Effect (ATE), Average Treatment Effect on the Treated (ATT), Local Average Treatment Effect (LATE), Marginal Treatment Effects (MTE), and Quantile (QTE).
2.  **Parametric & Extremum Estimators**:
    *   *Linear*: OLS and Panel Data Fixed Effects via high-performance engines (`fixest`, `plm`).
    *   *Non-Linear/Moment based*: Maximum Likelihood Estimation (MLE & QML), Generalized Method of Moments (`gmm`), and Discrete Choice modeling (`mlogit`). Marginal effects are strictly translated via `marginaleffects`.
3.  **Robust, Machine Learning, & Nonparametric Methods**:
    *   *Machine Learning & XAI*: High-dimensional variable selection and forecasting via Lasso/Elastic-Net (`glmnet`) and Gradient Boosting (`xgboost`). All ML models are strictly interpreted via Explainable AI (`shapviz`) to satisfy journal transparency requirements.
    *   *Causal Forests*: Heterogeneous treatment effect discovery via Generalized Random Forests (`grf`).
    *   *Standard Errors*: Immediate fallback to Heteroskedasticity-Consistent (HC) and cluster-robust Standard Errors (`sandwich`, `lmtest`).
4.  **Simulation & Resampling**:
    *   *Compute-Intensive*: Indirect Inference, Method of Simulated Moments (MSM).
    *   *Monte Carlo*: MCMC frameworks and Metropolis-Hastings (MH) samplers for computationally intractable distributions.
    *   *Resampling*: Bootstrap handlers for finite-sample distribution variance correction.

### Reproducibility & Code Generation
*   **Dual-Language Script Auto-generation**: The engine automatically translates Python DataFrames and model logic into highly commented, executable scripts in both **R** and **Stata**.
    *   **R (Primary Analytical Engine)**: Used to execute the cutting-edge empirical methodologies (e.g., Staggered DiD, Machine Learning, Causal Forests) utilizing the pre-configured `EconoSuite` R environment.
    *   **Stata (Verification & Submission Engine)**: Stata `.do` scripts are generated simultaneously. This serves a dual purpose: providing an independent algorithmic robustness check (cross-verifying core OLS/IV/FE results against R) and fulfilling strict journal data submission mandates where Stata remains the institutional standard for replication files.
*   **Replication Package Mandate**: EconoSuite natively complies with the strict AEA/RES Data and Code Availability Policy. For every simulation or empirical run, the orchestrator:
    1.  Generates a master `makefile` that controls both the R execution and the Stata verification protocols.
    2.  Hardcodes the pseudo-random generator `seed` across both environments for Monte Carlos.
    3.  Writes comprehensive `README` documentation (including software versions like Stata 17+, R 4.2+).
    4.  Outputs proprietary datasets in dual formats (e.g., `.dta` and `.csv`/ASCII).

### The ESA-to-Manuscript Bridge (The Anti-Hallucination Protocol)
To prevent the LLM from hallucinating standard errors, dropping decimals, or faking significance asterisks, EconoSuite completely decouples statistical execution from text generation through a rigid 3-step bridge:
1.  **The JSON Export Mandate**: R and Stata scripts are banned from outputting raw console text (e.g., `summary(model)`). Instead, scripts must utilize packages like `broom::tidy()` to extract coefficients, t-statistics, and p-values, exporting them into a strictly formatted, machine-readable `results.json` state file.
2.  **Deterministic Table Compilation**: The LLM is structurally banned from writing LaTeX tables. Instead, a deterministic Python script (`TableCompiler.py`) reads `results.json` and autonomously generates the `\begin{table}` matrix using `booktabs`, guaranteeing perfect alignment and exact numerical transcription.
3.  **The Statistical Auditor (Critic Agent)**: When the LLM drafts the "Empirical Results" narrative, it relies on the JSON state file. Before the text is committed to the manuscript, a Critic Agent runs a differential regex scan—cross-referencing every number written in the LLM's text against the `results.json` array. Any mismatch (e.g., writing "0.45" when the JSON states "0.42") triggers a fatal error and forces an immediate redraft.

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
| **1. Expectations & Probabilities** | | |
| `E[X]` | `E(X)` | Mathematical Expectation. |
| `Var(X)` | `\text{var}(X)` | Variance (enforced lowercase text). |
| `Cov(X,Y)` | `\text{cov}(X, Y)` | Covariance. |
| `Corr(X,Y)` | `\text{corr}(X, Y)` | Correlation. |
| `dist_as` | `\sim` | "Is distributed as". |
| `pdf_norm` | `\phi` | Standard normal pdf. |
| `cdf_norm` | `\Phi` | Standard normal cdf. |
| `chi_sq` | `\chi^2` | Chi-squared distribution. |
| **2. Asymptotics & Limits** | | |
| `plim(X)` | `\text{plim} X_n` | Probability limit. |
| `converge_p` | `\xrightarrow{p}` | Convergence in probability. |
| `converge_d` | `\xrightarrow{d}` | Convergence in distribution. |
| `big_Op(X)` | `O_p(X)` | Probabilistic order (bounded in probability). |
| `small_op(X)` | `o_p(X)` | Probabilistic order (converges to 0). |
| **3. Linear Models & Testing** | | |
| `OLS(y, X)` | `y = \boldsymbol{X}\boldsymbol{\beta} + \boldsymbol{\epsilon}` | Linear Regression (Bold matrix/vectors). |
| `Hypothesis(R, beta, c)` | `\boldsymbol{R}'\boldsymbol{\beta} = \boldsymbol{c}` | Linear restrictions testing. |
| `indicator(K)` | `1_K` | Indicator function for condition K. |
| **4. Advanced Estimators (MLE / GMM)** | | |
| `MLE_obj(theta)` | `\hat{\boldsymbol{\theta}}_{MLE} = \arg\max_{\boldsymbol{\theta}} \sum_{i=1}^n \log L(\boldsymbol{\theta} \mid y_i, \boldsymbol{x}_i)` | Maximum Likelihood Objective. |
| `GMM_obj(theta)` | `\hat{\boldsymbol{\theta}}_{GMM} = \arg\min_{\boldsymbol{\theta}} \left[ \frac{1}{n} \sum_{i=1}^n \boldsymbol{g}(y_i, \boldsymbol{x}_i, \boldsymbol{\theta}) \right]' \boldsymbol{W} \left[ \frac{1}{n} \sum_{i=1}^n \boldsymbol{g}(y_i, \boldsymbol{x}_i, \boldsymbol{\theta}) \right]` | Generalized Method of Moments. |
| **5. Matrix Algebra (Econometrica Style)** | | |
| `matrix(A)'` | `\boldsymbol{A}'` or `\boldsymbol{A}^0` | Transpose (strictly prevents $A^T$). |
| `matrix_inv(A)` | `\boldsymbol{A}^{-1}` | Standard inverse. |
| `matrix_pinv(A)` | `\boldsymbol{A}^{+}` | Moore-Penrose generalized inverse. |
| `det(A)` | `\lvert\boldsymbol{A}\rvert` or `\det \boldsymbol{A}` | Determinant. |
| `trace(A)` | `\text{tr}(\boldsymbol{A})` | Trace (and `\text{etr}` for exponential trace). |
| `rank(A)` | `\text{rk}(\boldsymbol{A})` | Rank of a matrix. |
| `kronecker(A,B)` | `\boldsymbol{A} \otimes \boldsymbol{B}` | Kronecker product. |
| `hadamard(A,B)` | `\boldsymbol{A} \odot \boldsymbol{B}` | Hadamard product. |
| **6. Time Series & Calculus** | | |
| `lag(x)` | `L x_t` or `B x_t` | Backward shift/lag operator. |
| `diff(x)` | `\Delta x_t` | Difference operator. |
| `diff_d(x)` | `\text{d}x` | Roman 'd' for differentials. |
| `partial(x)` | `\partial x` or `\text{D}x` | Partial derivative. |
| `grad(f)` | `\nabla f` | Gradient (transpose of derivative). |
| `hessian(f)` | `\boldsymbol{H}` | Hessian matrix. |

Economic mathematical notation strictness is enforced globally within these pipelines to signal "submission-ready" rigor:
*   **Basic Notation**: Scalar variables must be italicized. Vectors and matrices **must be designated in boldface** (lowercase bold-italic for vectors, uppercase for matrices). Sets use script fonts, while number systems ($\mathbb{R}, \mathbb{Z}, \mathbb{N}$) natively use Blackboard bold.
*   **Null Entities**: Enforces the distinct usage of the bold null vector ($\mathbf{0}$) versus the uppercase null matrix ($\mathbf{O}$).
*   **Fractions & Exponentials**: Forces solidus ($X/Y$) for inline fractions and reserves `\frac{}` for displayed equations. Power of $e$ strictly converts to `\exp(\cdot)`.
*   **Mathematical Relations**: Natively formats identity (`\equiv`), defines as (`:=`), implies (`\implies`), and asymptotic equivalence (`\sim`).

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

### Continuous Pipeline Execution & Re-Unification Engine
Drawing directly from the completed orchestration architecture, the EconoSuite Unified Engine absorbs all entry points through a singular **Run Adapter**.
*   **State Management & Resilience (Phase-level Checkpointing)**: The daemon continuously monitors the DAG execution state, strictly saving progress to a local state JSON file after every phase. If a deep API call times out (e.g., Semantic Scholar throttling) or compilation crashes, the daemon autonomously resumes the exact pipeline phase without redundant recalculations. 
*   **Persistent Context & Memory**: The daemon maintains a rolling, persistent context of the manuscript's progression. It cross-references current drafts against the initial "Ideation & Hypothesis" constraints, ensuring the final text strictly adheres to the original Identification Strategy.
*   **Strict No-Fallback Mode**: Silent degradation is permanently banned. If constitutional validation fails or an ESA econometric check throws a mismatch, the engine will halt execution and alert the Debugger Agent rather than inserting a generic "Placeholder." This ensures the integrity of the economic argument.
*   **Tool & MCP Coordination**: The daemon acts as the central nervous system connecting Python execution environments (ESA Engine, `LaTeXMathCompiler`, LLM Resolvers) with external Model Context Protocol (MCP) servers seamlessly.
*   **Exclusive Daemon Routing**: Direct, interactive terminal executions are strictly disabled. When operating via CLI, the workflow *must always* route through the isolated Antigravity daemon wrapper. The only explicit exceptions to this background-daemon requirement are when the user is operating within the visual **Tauri Desktop App** or the **Streamlit** web interface.
    *   **Headless STDIN Isolation**: To prevent pipeline hanging when executed automatically, the daemon explicitly routes `STDIN` to `/dev/null`, preventing third-party packages from requesting interactive confirmations.
    *   **Context-Aware Machine Output**: Standard output is stripped of verbose human-readable ASCII art and logs. By utilizing concise JSON-log outputs, it preserves the running LLM Agent's token context window.
*   **Agent Delegation & IPC (Inter-Process Communication)**: To prevent race conditions in parallel DAG execution and avoid file-watcher conflicts with external handlers, EconoSuite adopts advanced daemon isolation:
    *   **Scoped Directory Auto-Detection**: The engine autonomously detects and routes communications to project-scoped agent directories (e.g., `ECONOSUITE_AGENT_DIR`), ensuring that simultaneous runs do not experience nonce mismatches or stale handshake files.
    *   **Unix Socket IPC (High Priority Migration)**: The target core architecture explicitly mandates a transition from legacy file-based LLM delegation (prompt/response text files) to robust Unix socket IPC. This upgrade fundamentally eliminates file deletion timing issues and properly enables true concurrent DAG node processing in agent mode.

---

## 7. Multi-Agent Integration & Deep Research

> [!TIP]
> **NotebookLM MCP / Intelligent Synthesis & Connectivity Hardening**
> EconoSuite utilizes the `jacob-bd/notebooklm-mcp-cli` for advanced synthesis. By uploading hundreds of working papers and utilizing deep research capabilities alongside the orchestrator, the AI agents can accurately spot identification strategy flaws, literature gaps, and suggest robustness checks based on the latest NBER publications. 
> 
> **CRITICAL ARCHITECTURE REQUIREMENT**: NLM is a hard dependency within EconoSuite—if NLM context is unavailable, the workflow must abort rather than silently degrading to fallback searches. To sustain long-running MCP connections during these deep-dive research queries, EconoSuite strictly enforces an **NLM Connectivity Hardening Stack**:
> * **Provider / CLI Buffer**: Extended localized timeouts (CLI: 120s, MCP Provider: 30s) and exponential backoff retry states.
> * **Daemon Stack Buffer**: The central orchestration daemon forcibly injects `NOTEBOOKLM_QUERY_TIMEOUT=600` into agent subprocess environments and extends its internal subprocess polling timeout by an additional 600 seconds, guaranteeing that the MCP component processes deep literature scans without premature term signals.

---

## 8. Document Architecture & Output Handlers

*   **Global Output Directory**: To prevent repository pollution, EconoSuite strictly saves all generated assets (LaTeX manuscripts, compiled PDFs, Stata replication packages, Makefiles, data extracts, and PRISMA diagrams) outside the active repository. All outputs are explicitly routed to `~/EconoSuite_Outputs/[topic_or_project_name]`.
*   **Native HWPX Support (Hancom OWPML)**: Aside from standard `.tex` and `.pdf` packages, EconoSuite bridges the domestic-international gap by natively supporting `.hwpx` outputs through Hancom OWPML models. This ensures seamless submissions to Korean policy institutes (e.g., KDI, BOK) and domestic journals without formatting loss. All compiled HWPX protocols are pushed to the global output directory.
*   **Citation Database Reliability**: The `EndNoteWriter` manages structural integrity, eliminating schema corruption in `.Data` folders during the aggressive citation mapping required for empirical literature reviews.
