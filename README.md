# EconoSuite

A CLI for preparing economics manuscripts of submission-ready quality in `.docx` format.
Integrating data from R/Python regressions and enforcing strict journal structures (e.g. AER).

## Installation

```bash
pip install -e .
```

## Usage

```bash
econosuite init --template aer
econosuite watch        # Starts the auto-build file watcher daemon
econosuite check
econosuite notebook sync # Syncs to Google NotebookLM
econosuite build
```

## Live File Watcher Daemon
EconoSuite includes a continuous file watcher. Open your terminal in your paper's directory and run:
`econosuite watch`
Every time you save a markdown file in your text editor, or export a new `.csv` from your R/Stata run, EconoSuite will instantly inject the changes and rebuild your final `.docx` file in the background!

## Agent-Enhanced Workflow

EconoSuite comes pre-installed with over 30 **AI Scientific Skills** (powered by open-source K-Dense skills) inside `.gemini/skills/`. Your local AI coding assistant has the power to autonomously:
- Query economic databases like FRED directly (`database-lookup`, `usfiscaldata`).
- Fetch literature using Academic Search Ultimate or PubMed (`paper-lookup`).
- Analyze Python/Stata results and write the manuscript text (`scientific-writing`, `statistical-analysis`).

### Antigravity MCP Server Wrapper
EconoSuite itself is also managed by Antigravity via the Model Context Protocol (MCP). By installing it as an MCP Server, Antigravity natively gains tools to orchestrate EconoSuite without typing CLI commands.

**Installation for Antigravity (`mcp_config.json`):**
```json
{
  "mcpServers": {
    "econosuite": {
      "command": "d:/Coding/EconoSuite/.venv/Scripts/python.exe",
      "args": [
        "-m",
        "econosuite.mcp_server"
      ]
    }
  }
}
```
*Once added, you can simply ask your agent: "Start a new EconoSuite AER paper here and sync it to my NotebookLM!" and it will magically happen.*
