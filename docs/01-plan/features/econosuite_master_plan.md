# PDCA Feature Plan: EconoSuite Platform Transformation

## 1. Feature Specifications

### 1.1 Core Orchestration & Unified Engine
*   **Objective**: Purge HemaSuite clinical dependencies and implement the advanced RAG Unified Engine.
*   **Key Deliverables**: 
    1. A multi-phase DAG orchestrator resilient to API timeouts (Semantic Scholar / RePEc).
    2. Constitutional validation mapping the drafting engine strictly to the Keith Head Introduction formula (25-30% result summary, concrete lexicon).

### 1.2 ESA (Economic-Statistic-Analysis) Engine
*   **Objective**: Establish a rigorous causal inference analysis backend.
*   **Key Deliverables**: 
    1. Implementation of IV, DiD, RDD, and SCM models.
    2. A Replication Package Generator that natively outputs fully commented Stata `.do` scripts, `Makefiles`, predetermined simulation seeds, and AEA-compliant `README` configurations.
    3. An automated econometric falsification suite spanning Sub-sample splits and Moment Selection.

### 1.3 Mathematical Typography & Typesetting (EconoSyntax)
*   **Objective**: Enforce strictly compliant "Top Five" mathematical rendering natively in LaTeX without human intervention.
*   **Key Deliverables**:
    1. A Macro JSON Extractor pipeline where LLM agents supply only variable constraints, protecting bracket syntax integrity.
    2. A `/tmp/` sandboxed Self-Healing Compilation Loop (`xelatex -halt-on-error`) managed by a Debugger Agent to recursively correct novel proofs.
    3. The Natural Language LaTeX Translator Agent driven by the hardcoded **EconoSyntax** pseudo-syntax mapping (e.g., parsing `plim(X)` or `E[Y|X]`) for interactive refinement phases.

### 1.4 Native Output & Document Architecture
*   **Objective**: Package final drafts into submission-ready configurations spanning foreign and domestic endpoints.
*   **Key Deliverables**:
    1. Taylor & Francis `interact.cls` templating injection engine.
    2. Dynamic ethics and disclosure statement appending.
    3. The highly specialized **HWPX/OWPML Protocol Generator** utilizing `zipfile` and `lxml` to map texts directly into Korean government `section0.xml` configurations, bypassing Windows COM restrictions altogether.

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
