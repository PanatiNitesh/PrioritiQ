import os
import glob
import re
from typing import List, Dict, Any

NOTES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "notes"))

def parse_note_file(filepath: str) -> Dict[str, Any]:
    with open(filepath, "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    metadata = {}
    content = raw_text
    
    # Check for frontmatter
    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            content = parts[2].strip()
            for line in fm_text.strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip()] = v.strip()
                    
    metadata["filename"] = os.path.basename(filepath)
    metadata["content"] = content
    return metadata

def load_all_notes() -> List[Dict[str, Any]]:
    notes = []
    for fp in glob.glob(os.path.join(NOTES_DIR, "*.txt")):
        try:
            note = parse_note_file(fp)
            notes.append(note)
        except Exception as e:
            print(f"Error reading {fp}: {e}")
    return notes
