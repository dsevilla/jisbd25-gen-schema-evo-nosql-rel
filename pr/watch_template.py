#!/usr/bin/env python3
"""
File watcher script that automatically regenerates slides when template files change.
This is an alternative to the VS Code extension approach.
"""

import time
import subprocess
from subprocess import CompletedProcess
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TemplateHandler(FileSystemEventHandler):
    """Handle file system events for template files."""

    def __init__(self, target_file="pr.md.j2"):
        self.target_file: str = target_file

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Check if the modified file is our target template
        if file_path.name == self.target_file:
            print(f"🔄 Template {self.target_file} changed, regenerating slides...")
            try:
                result: CompletedProcess[str] = subprocess.run([
                    sys.executable, "generate_slides.py"
                ], capture_output=True, text=True, cwd=file_path.parent)

                if result.returncode == 0:
                    print("✅ Slides regenerated successfully!")
                else:
                    print(f"❌ Error regenerating slides: {result.stderr}")

            except Exception as e:
                print(f"❌ Error running generation script: {e}")

def main():
    """Main function to start file watching."""
    watch_dir = Path.cwd()
    target_file = "pr.md.j2"

    if not (watch_dir / target_file).exists():
        print(f"❌ Target file {target_file} not found in {watch_dir}")
        sys.exit(1)

    # Set up file watcher
    event_handler = TemplateHandler(target_file)
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=False)

    print(f"👀 Watching {target_file} for changes...")
    print("Press Ctrl+C to stop watching")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping file watcher...")
        observer.stop()

    observer.join()
    print("👋 File watcher stopped")

if __name__ == "__main__":
    main()
