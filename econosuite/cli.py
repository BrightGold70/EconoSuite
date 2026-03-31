import click
import os
import yaml
import shutil
from pathlib import Path
from .builder import build_document
from .validator import check_document
from .notebook import sync_project, ask_notebook
from .watcher import start_watcher

@click.group()
def cli():
    """EconoSuite: Prepare economics manuscripts in .docx format."""
    pass

@cli.command()
@click.option('--template', default='aer', help='Journal template (e.g., aer, nature, generic)')
def init(template):
    """Initialize a new EconoSuite paper project."""
    base_dir = Path.cwd()
    
    # Create directories for notes and results
    (base_dir / "notes").mkdir(exist_ok=True)
    (base_dir / "results" / "figures").mkdir(parents=True, exist_ok=True)
    
    key = template.lower()
    max_words = 10000
    max_abstract_words = 250
    
    if key == "uitj":
        max_words = 8000
        max_abstract_words = 150
    elif key == "rger":
        max_words = 7000
        max_abstract_words = 200
        
    # Create config.yaml
    config_path = base_dir / "config.yaml"
    if not config_path.exists():
        default_config = {
            "title": "A New Economic Theory",
            "authors": [{"name": "Author 1", "affiliation": "University"}],
            "abstract": "This is a placeholder abstract. Word limit is usually 150-250 words.",
            "jel_codes": ["D80", "E10"],
            "journal_template": template.upper(),
            "date": "2024-01-01",
            "max_words": max_words,
            "max_abstract_words": max_abstract_words,
            "notebook_id": None
        }
        with open(config_path, "w") as f:
            yaml.dump(default_config, f, sort_keys=False)
    
    # Template scaffolding definitions
    templates = {
        "aer": [
            ("01_background.md", "# Background\n\nWrite your motivation ({Author, 2023}) here.\n"),
            ("02_method.md", "# Method\n\nExplain the econometric model.\n"),
            ("03_results.md", "# Results\n\nHere is our main result table:\n{{table: results/regression.csv}}\n\nAnd a figure:\n{{figure: results/figures/graph1.png}}\n"),
            ("04_discussion.md", "# Discussion\n\nSummary of findings and policy implications.\n")
        ],
        "nature": [
            ("01_introduction.md", "# Introduction\n\n"),
            ("02_results.md", "# Results\n\n"),
            ("03_discussion.md", "# Discussion\n\n"),
            ("04_methods.md", "# Methods\n\n")
        ],
        "generic": [
            ("01_introduction.md", "# Introduction\n\n"),
            ("02_data.md", "# Data\n\n"),
            ("03_methodology.md", "# Methodology\n\n"),
            ("04_results.md", "# Results\n\n"),
            ("05_conclusion.md", "# Conclusion\n\n")
        ],
        "uitj": [
            ("01_introduction.md", "# Introduction\n\n"),
            ("02_theoretical_background.md", "# Theoretical Background\n\n"),
            ("03_data_methods.md", "# Data & Methods\n\n"),
            ("04_results.md", "# Results\n\n{{table: results/regression.csv}}\n"),
            ("05_discussion.md", "# Discussion & Conclusions\n\n")
        ],
        "rger": [
            ("01_introduction.md", "# Introduction\n\n"),
            ("02_literature_review.md", "# Literature Review\n\n"),
            ("03_empirical_model.md", "# Empirical Model & Data\n\n"),
            ("04_results.md", "# Results\n\n{{table: results/regression.csv}}\n"),
            ("05_conclusion.md", "# Conclusion & Policy Implications\n\n")
        ]
    }
    
    if key not in templates:
        click.secho(f"Warning: Template '{template}' not found. Using generic.", fg="yellow")
        key = "generic"
        
    sections = templates[key]
    
    for filename, content in sections:
        file_path = base_dir / filename
        if not file_path.exists():
            with open(file_path, "w") as f:
                f.write(content)
                
    # Create a dummy csv in results
    dummy_csv = base_dir / "results" / "regression.csv"
    if not dummy_csv.exists():
        with open(dummy_csv, "w") as f:
            f.write("Variable,Coefficient,StdError,PValue\n")
            f.write("Income,0.45**,0.05,0.01\n")
            f.write("Education,0.12*,0.04,0.04\n")
            f.write("Age,0.01,0.02,0.50\n")
            
    # Instruct user about NotebookLM workflow
    click.echo("Initialized EconoSuite project successfully.")
    click.secho("Tip: Save your NotebookLM notes in the 'notes/' folder.", fg="cyan")
    click.secho("Tip: Use {Author, Year} for EndNote auto-formatting in Word.", fg="cyan")

@cli.command()
def check():
    """Validate the current project against economics journal standards."""
    errors = check_document(Path.cwd())
    if not errors:
        click.secho("Validation passed! Ready to build.", fg="green")
    else:
        click.secho("Validation failed with the following errors:", fg="red")
        for err in errors:
            click.echo(f" - {err}")

@cli.command()
def build():
    """Build the final .docx manuscript."""
    click.echo("Building document...")
    try:
        output_file = build_document(Path.cwd())
        click.secho(f"Successfully built {output_file}", fg="green")
    except Exception as e:
        click.secho(f"Error building document: {str(e)}", fg="red")

@cli.command()
def watch():
    """Start a background daemon to auto-build your .docx as you write."""
    try:
        start_watcher(Path.cwd())
    except Exception as e:
        click.secho(f"Error starting watcher: {e}", fg="red")

@cli.group()
def notebook():
    """NotebookLM integration commands."""
    pass

@notebook.command()
def sync():
    """Sync notes and results to Google NotebookLM."""
    base_dir = Path.cwd()
    config_path = base_dir / "config.yaml"
    if not config_path.exists():
        click.secho("Error: Not an EconoSuite project. Run 'econosuite init' first.", fg="red")
        return
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    notebook_id = config.get("notebook_id")
    project_name = f"EconoSuite - {config.get('title', 'Project')}"
    
    click.echo(f"Syncing to NotebookLM (Project: {project_name})...")
    click.echo("This may open your browser for authentication if you haven't logged in.")
    
    try:
        new_id = sync_project(project_name, base_dir, notebook_id)
        if new_id and new_id != notebook_id:
            config["notebook_id"] = new_id
            with open(config_path, "w") as f:
                yaml.dump(config, f, sort_keys=False)
        click.secho("Sync complete!", fg="green")
    except Exception as e:
        click.secho(f"Error syncing to NotebookLM: {e}\n(Make sure to run 'notebooklm login' to authenticate!)", fg="red")

@notebook.command()
@click.argument('query')
def ask(query):
    """Ask your Google NotebookLM a question."""
    base_dir = Path.cwd()
    config_path = base_dir / "config.yaml"
    if not config_path.exists():
        click.secho("Error: Not an EconoSuite project.", fg="red")
        return
        
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    notebook_id = config.get("notebook_id")
    if not notebook_id:
        click.secho("Error: No Notebook connected. Run 'econosuite notebook sync' first.", fg="red")
        return
        
    click.echo(f"Querying NotebookLM: '{query}'...")
    try:
        answer = ask_notebook(notebook_id, query)
        click.secho("\n--- NotebookLM Answer ---", fg="cyan")
        click.echo(answer)
        click.secho("-------------------------", fg="cyan")
    except Exception as e:
        click.secho(f"Error querying NotebookLM: {e}", fg="red")

if __name__ == "__main__":
    cli()
