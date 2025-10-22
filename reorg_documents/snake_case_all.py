#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Define the root directory
root = Path.home() / "Documents"

# Regex to identify technical/system files to skip
TECHNICAL_PATTERNS = [
    r"^\.",             # hidden files or folders (.git, .DS_Store)
    r"^~",              # temp/backup files
    r".*\.DS_Store$",   # macOS system files
    r".*Thumbs\.db$",   # Windows thumbnail cache
    r".*\.tmp$",        # temp files
]

def is_technical(name: str) -> bool:
    """Return True if file/folder name looks like a system or temp file."""
    return any(re.match(p, name) for p in TECHNICAL_PATTERNS)

def to_snake_case(name: str) -> str:
    """Convert a string to snake_case, preserving file extension."""
    if "." in name and not name.startswith("."):
        stem, ext = os.path.splitext(name)
    else:
        stem, ext = name, ""

    # Replace spaces, dashes, and camelCase
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", stem)
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s)
    s = s.strip("_").lower()
    return s + ext.lower()

def is_rename_without_asking(name, extensions_to_rename) -> bool:
	_, ext = os.path.splitext(name)
	return ext.lower() in extensions_to_rename

# Walk bottom-up so folders are renamed after their contents
for path, dirs, files in os.walk(root, topdown=False):
    # Rename files
    for name in files:
        if is_technical(name):
            continue
        old_path = Path(path) / name
        new_name = to_snake_case(name)
        if new_name != name:
            rel = old_path.relative_to(root)
            if is_rename_without_asking(name, [".jpg", ".jpeg", ".png", ".gif", ".txt", ".md", ".pdf", ".docx", ".xlsx", ".pptx", ".mp3", ".mp4", ".avi"]):
                confirm = "y"
            else:
                confirm = input(f"Rename file '{rel}' → '{new_name}' ? [y/N]: ").strip().lower()
                
            if confirm == "y":
                new_path = Path(path) / new_name
                try:
                    old_path.rename(new_path)
                    print(f"✅ Renamed: {rel} → {new_name}")
                except Exception as e:
                    print(f"⚠️ Could not rename {rel}: {e}")

    # Rename folders
    for name in dirs:
        if is_technical(name):
            continue
        old_path = Path(path) / name
        new_name = to_snake_case(name)
        if new_name != name:
            rel = old_path.relative_to(root)
            confirm = input(f"Rename folder '{rel}' → '{new_name}' ? [y/N]: ").strip().lower()
            if confirm == "y":
                new_path = Path(path) / new_name
                try:
                    old_path.rename(new_path)
                    print(f"📁 Renamed folder: {rel} → {new_name}")
                except Exception as e:
                    print(f"⚠️ Could not rename folder {rel}: {e}")
