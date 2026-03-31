import asyncio
import os
from pathlib import Path
from notebooklm import NotebookLMClient

async def sync_project_async(project_name: str, base_dir: Path, notebook_id: str = None) -> str:
    """Syncs the current project files to a Google Notebook."""
    async with await NotebookLMClient.from_storage() as client:
        # Create or verify notebook
        if notebook_id:
            try:
                # Try to get it to ensure it exists
                # notebooklm-py might not have an elegant "get" right now, but we can list and check
                notebooks = await client.notebooks.list()
                if not any(nb.id == notebook_id for nb in notebooks):
                    raise ValueError(f"Notebook ID {notebook_id} not found in your account.")
            except Exception:
                # Fallback: create new
                nb = await client.notebooks.create(project_name)
                notebook_id = nb.id
        else:
            nb = await client.notebooks.create(project_name)
            notebook_id = nb.id

        # Find all sources
        notes_dir = base_dir / "notes"
        results_dir = base_dir / "results"
        
        all_files = []
        if notes_dir.exists():
            for f in notes_dir.iterdir():
                if f.is_file() and not f.name.startswith('.'):
                    all_files.append(f)
                    
        if results_dir.exists():
            for f in results_dir.iterdir():
                if f.is_file() and f.suffix in ['.csv', '.txt', '.md'] and not f.name.startswith('.'):
                    all_files.append(f)

        # Upload files
        for f in all_files:
            try:
                print(f"Uploading {f.name}...")
                await client.sources.add_file(notebook_id, f, wait=False)
            except Exception as e:
                print(f"Failed to upload {f.name}: {e}")

        return notebook_id

async def ask_notebook_async(notebook_id: str, query: str) -> str:
    """Queries the specified notebook."""
    if not notebook_id:
        raise ValueError("No Notebook ID provided. Please run 'econosuite notebook sync' first.")
        
    async with await NotebookLMClient.from_storage() as client:
        result = await client.chat.ask(notebook_id, query)
        return result.answer

def sync_project(project_name: str, base_dir: Path, notebook_id: str = None) -> str:
    return asyncio.run(sync_project_async(project_name, base_dir, notebook_id))

def ask_notebook(notebook_id: str, query: str) -> str:
    return asyncio.run(ask_notebook_async(notebook_id, query))
