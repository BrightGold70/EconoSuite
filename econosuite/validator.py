import yaml
from pathlib import Path
import re

def check_document(base_dir):
    errors = []
    config_path = base_dir / "config.yaml"
    
    if not config_path.exists():
        errors.append("config.yaml not found. Please run 'init'.")
        return errors
        
    with open(config_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except Exception as e:
            errors.append(f"Invalid YAML config: {str(e)}")
            return errors
            
    # Check Abstract
    abstract = config.get("abstract", "")
    max_ab_words = config.get("max_abstract_words", 250)
    word_count = len(abstract.split())
    if word_count > max_ab_words:
        errors.append(f"Abstract is too long ({word_count} words). Keep under {max_ab_words} words for this template.")
    if word_count < 50:
        errors.append("Abstract is too short or missing.")
        
    # Check JEL codes
    jel_codes = config.get("jel_codes", [])
    if not jel_codes:
        errors.append("Missing JEL (Journal of Economic Literature) classification codes in config.")
        
    # Check Introduction Structure (Basic Heuristics)
    # Could be named 01_introduction.md or 01_background.md
    intro_path = base_dir / "01_introduction.md"
    if not intro_path.exists():
        intro_path = base_dir / "01_background.md"
        
    if intro_path.exists():
        with open(intro_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            if "contribution" not in content and "contribute" not in content:
                # Some AER templates may just not use the word contribution but we warn anyway.
                errors.append("First section lacks a clear 'contribution' statement.")
            if "methodology" not in content and "strategy" not in content and "model" not in content:
                errors.append("First section lacks a clear methodology or strategy outline.")
                
    # Check table and figure references exist
    table_pattern = re.compile(r"\{\{table:\s*(.+?)\}\}")
    figure_pattern = re.compile(r"\{\{figure:\s*(.+?)\}\}")
    
    for md_file in base_dir.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            # tables
            for m in table_pattern.findall(content):
                table_path = base_dir / m.strip()
                if not table_path.exists():
                    errors.append(f"Table reference '{m.strip()}' in {md_file.name} points to a missing file.")
            # figures
            for m in figure_pattern.findall(content):
                fig_path = base_dir / m.strip()
                if not fig_path.exists():
                    errors.append(f"Figure reference '{m.strip()}' in {md_file.name} points to a missing file.")
                    
    # Check total manuscript word limit
    max_words = config.get("max_words", 10000)
    total_words = 0
    for md_file in base_dir.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            total_words += len(f.read().split())
            
    if total_words > max_words:
        errors.append(f"Manuscript total word count ({total_words} words) exceeds the strict {max_words}-word limit for this journal.")
        
    return errors
