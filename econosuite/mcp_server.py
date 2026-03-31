import os
import yaml
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from econosuite.builder import build_document
from econosuite.validator import check_document
from econosuite.notebook import sync_project, ask_notebook

# Determine the workspace path. When running as an MCP server,
# it executes in the context of the user's workspace, so Path.cwd() is perfect.
mcp = FastMCP("econosuite")

def _get_workspace() -> Path:
    return Path.cwd()

@mcp.tool()
def econosuite_init(template: str = 'aer') -> str:
    """Initializes a new EconoSuite paper project in the current working directory."""
    from click.testing import CliRunner
    from econosuite.cli import init
    
    # We invoke the CLI directly utilizing click test mechanisms to reuse scaffold logic 
    # without duplicating it. Or we can just call the underlying logic if we had decoupled it.
    runner = CliRunner()
    result = runner.invoke(init, ['--template', template])
    if result.exit_code == 0:
        return f"Successfully initialized EconoSuite project with '{template}' template."
    return f"Failed to initialize: {result.output}"

@mcp.tool()
def econosuite_check() -> str:
    """Validates the current manuscript against submission standards."""
    errors = check_document(_get_workspace())
    if not errors:
        return "Manuscript validation passed perfectly!"
    else:
        return "Validation failed with the following issues:\n" + "\n".join(f"- {e}" for e in errors)

@mcp.tool()
def econosuite_build() -> str:
    """Builds the final .docx manuscript dynamically."""
    try:
        output = build_document(_get_workspace())
        return f"Successfully generated manuscript docx: {output}"
    except Exception as e:
        return f"Error building manuscript: {str(e)}"

@mcp.tool()
def econosuite_notebook_sync() -> str:
    """Syncs the current project notes and results directly into the user's Google NotebookLM cloud."""
    config_path = _get_workspace() / "config.yaml"
    if not config_path.exists():
        return "Error: config.yaml not found. Please run econosuite_init first."
        
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        params_nb_id = config.get("notebook_id")
        project_name = f"EconoSuite - {config.get('title', 'Project')}"
        
        # NOTE: If notebooklm login hasn't been run by the user locally, this fails.
        new_id = sync_project(project_name, _get_workspace(), params_nb_id)
        
        if new_id and new_id != params_nb_id:
            config["notebook_id"] = new_id
            with open(config_path, "w") as f:
                yaml.dump(config, f, sort_keys=False)
                
        return f"Successfully synced project to Google NotebookLM. Notebook ID: {new_id}"
    except Exception as e:
        return f"Failed to sync to NotebookLM: {str(e)}. \nPlease advise the user to run 'notebooklm login' in their console to authenticate."

@mcp.tool()
def econosuite_notebook_ask(query: str) -> str:
    """Ask your Google NotebookLM source agent an analytical question based on your notes."""
    config_path = _get_workspace() / "config.yaml"
    if not config_path.exists():
        return "Error: config.yaml not found."
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    notebook_id = config.get("notebook_id")
    if not notebook_id:
        return "Error: No Notebook connected. Run econosuite_notebook_sync first."
        
    try:
        answer = ask_notebook(notebook_id, query)
        return answer
    except Exception as e:
        return f"Failed to query NotebookLM: {str(e)}"

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
