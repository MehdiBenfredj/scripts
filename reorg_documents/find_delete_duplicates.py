# write.a script that checks files in ~/Documents folder recursivelly 
# find all duplicate files based on their name and extension 
# print them all ( 2 by 2 ) with relative path from ~/Documents 
# with size and last modified date


#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime
from itertools import combinations

root = Path.home() / "Documents"
files_by_name_and_size = {}

# --- Step 1: Collect files by name and size ---
for path, _, files in os.walk(root):
    for f in files:
        full_path = Path(path) / f
        try:
            size = full_path.stat().st_size
            key = (f, size)
            files_by_name_and_size.setdefault(key, []).append(full_path)
        except FileNotFoundError:
            continue  # Skip broken symlinks or deleted files

# --- Step 2: Process duplicates ---
for (filename, size), paths in files_by_name_and_size.items():
    if len(paths) > 1:
        print(f"\n🔁 Duplicates found for: {filename} ({size/1024:.1f} KB)")
        print("-" * 70)
        for p in paths:
            stat = p.stat()
            rel = p.relative_to(root)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{rel} | modified: {modified}")
        print("-" * 70)

        # Ask user which file(s) to delete
        for p in paths[1:]:  # Keep the first by default, ask for others
            rel = p.relative_to(root)
            confirm = input(f"❓ Delete duplicate '{rel}'? [y/N]: ").strip().lower()
            if confirm == "y":
                try:
                    p.unlink()
                    print(f"🗑️ Deleted: {rel}")
                except Exception as e:
                    print(f"⚠️ Could not delete {rel}: {e}")

# --- Step 3: Clean up empty folders ---
print("\n🧹 Cleaning up empty folders...")
deleted_count = 0
for path, dirs, files in os.walk(root, topdown=False):
    folder = Path(path)
    try:
        if not any(folder.iterdir()):  # Folder is empty
            folder.rmdir()
            print(f"🧺 Removed empty folder: {folder.relative_to(root)}")
            deleted_count += 1
    except Exception:
        continue

print(f"\n✅ Done. Removed {deleted_count} empty folders.")
#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime
from itertools import combinations

root = Path.home() / "Documents"
files_by_name_and_size = {}

# --- Step 1: Collect files by name and size ---
for path, _, files in os.walk(root):
    for f in files:
        full_path = Path(path) / f
        try:
            size = full_path.stat().st_size
            key = (f, size)
            files_by_name_and_size.setdefault(key, []).append(full_path)
        except FileNotFoundError:
            continue  # Skip broken symlinks or deleted files

# --- Step 2: Process duplicates ---
for (filename, size), paths in files_by_name_and_size.items():
    if len(paths) > 1:
        print(f"\n🔁 Duplicates found for: {filename} ({size/1024:.1f} KB)")
        print("-" * 70)
        for p in paths:
            stat = p.stat()
            rel = p.relative_to(root)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{rel} | modified: {modified}")
        print("-" * 70)

        # Ask user which file(s) to delete
        for p in paths[1:]:  # Keep the first by default, ask for others
            rel = p.relative_to(root)
            confirm = input(f"❓ Delete duplicate '{rel}'? [y/N]: ").strip().lower()
            if confirm == "y":
                try:
                    p.unlink()
                    print(f"🗑️ Deleted: {rel}")
                except Exception as e:
                    print(f"⚠️ Could not delete {rel}: {e}")

# --- Step 3: Clean up empty folders ---
print("\n🧹 Cleaning up empty folders...")
deleted_count = 0
for path, dirs, files in os.walk(root, topdown=False):
    folder = Path(path)
    try:
        if not any(folder.iterdir()):  # Folder is empty
            folder.rmdir()
            print(f"🧺 Removed empty folder: {folder.relative_to(root)}")
            deleted_count += 1
    except Exception:
        continue

print(f"\n✅ Done. Removed {deleted_count} empty folders.")
