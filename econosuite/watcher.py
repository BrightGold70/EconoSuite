import time
import click
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .builder import build_document
from .validator import check_document

class EconoSuiteWatcher(FileSystemEventHandler):
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.last_built = time.time()
        
    def _is_relevant_file(self, event):
        if event.is_directory:
            return False
            
        path = Path(event.src_path)
        
        # Don't rebuild if the docx itself changed
        if path.suffix == '.docx':
            return False
            
        # Rebuild if markdown changes or results change
        if path.suffix in ['.md', '.csv', '.png', '.jpg']:
            return True
            
        return False

    def on_modified(self, event):
        if self._is_relevant_file(event):
            # Debounce rapid save events (common in IDEs)
            current = time.time()
            if current - self.last_built < 2.0:
                return
                
            self.last_built = current
            click.secho(f"\n[Watcher] Detected changes in {Path(event.src_path).name}. Rebuilding...", fg="cyan")
            try:
                # Optional: check validation before building
                errors = check_document(self.base_dir)
                if errors:
                    click.secho(f"[Watcher] Manuscript has structural issues: {errors[0]}", fg="yellow")
                    
                output_file = build_document(self.base_dir)
                click.secho(f"[Watcher] Successfully built {output_file} at {time.strftime('%H:%M:%S')}", fg="green")
            except Exception as e:
                click.secho(f"[Watcher] Error building document: {e}", fg="red")

def start_watcher(base_dir: Path):
    """Starts the endless watchdog daemon to monitor for manuscript changes."""
    click.secho(f"Starting EconoSuite Daemon in {base_dir}", fg="blue")
    click.echo("Monitoring .md drafts and results/ outputs. Press Ctrl+C to stop.")
    
    event_handler = EconoSuiteWatcher(base_dir)
    observer = Observer()
    observer.schedule(event_handler, str(base_dir), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\nStopping daemon...")
        observer.stop()
    observer.join()
