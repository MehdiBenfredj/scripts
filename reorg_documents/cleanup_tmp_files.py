#!/usr/bin/env python3
"""
Script to delete all files inside ~/Documents/tmp and ~/Downloads/tmp
"""
import subprocess
from datetime import datetime, timedelta
import os
import shutil
import psycopg2 # type: ignore
from pathlib import Path
from dotenv import load_dotenv # type: ignore

def clean_tmp_directory(tmp_dir, timestamp, conn):
    """Delete all files and subdirectories in the specified tmp directory"""
    dir_path = Path(tmp_dir).expanduser()
    
    if not dir_path.exists():
        print(f"Warning: Directory {dir_path} does not exist")
        return
    
    if not dir_path.is_dir():
        print(f"Warning: {dir_path} is not a directory")
        return
    
    # Get all items in the directory
    items = list(dir_path.iterdir())
    
    if not items:
        print(f"Directory {dir_path} is already empty")
        return
    
    print(f"Found {len(items)-1} item(s) in {dir_path}")
    
    deleted_count = 0
    error_count = 0
    
    for item in items:
        try:
            if (item.is_file() or item.is_symlink()) and item.name not in (".gitignore"):
                os.remove(item)
                print(f"  ✓ Deleted file: {item.name}")
                deleted_count += 1
            elif item.is_dir() and item.name not in (".git"):
                shutil.rmtree(item)
                print(f"  ✓ Deleted directory: {item.name}")
                deleted_count += 1
        except Exception as e:
            print(f"  ✗ Error deleting {item.name}: {e}")
            error_count += 1
    cur = conn.cursor()
    cur.execute("UPDATE delete_directories SET last_operation = %s WHERE directory = %s;", (timestamp, tmp_dir))
    cur.execute("COMMIT;")
    cur.close()
    print(f"Summary: {deleted_count} deleted, {error_count} errors")

def get_tmp_directories(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM delete_directories;")
    # Fetch all rows
    result = cur.fetchall()
    # Clean up
    cur.close()

    return result

def git_commit_and_push(directory, timestamp):
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=directory,
        capture_output=True,
        text=True
    )
    if result.stdout.strip(): 
        commit_message = f"Auto commit {timestamp}"
        subprocess.run(["git", "add", "."], cwd=directory, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=directory, check=True)
        subprocess.run(["git", "push"], cwd=directory, check=True)

def main():
    load_dotenv()

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    print("=" * 60)
    print("Temporary Directory Cleanup Script")
    print("=" * 60)
    
    tmp_directories = get_tmp_directories(conn)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for tmp_dir in tmp_directories:
        if datetime.now() - tmp_dir[2] > timedelta(days=tmp_dir[1]):
            print(f"\nProcessing: {tmp_dir[0]}")
            clean_tmp_directory(tmp_dir[0], timestamp, conn)
            git_commit_and_push(tmp_dir[0], timestamp)
        else:
            print(f"\nSkipping `{tmp_dir[0]}`, not old enough to delete")
    
    conn.close()
    print("\n" + "=" * 60)
    print("Cleanup completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()