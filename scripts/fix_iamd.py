#!/usr/bin/env python3
import os
import datetime

HEADER = """---
agent: Jules
action: Fix
timestamp: {timestamp}
status: Validated
---
"""

def fix_iamd(root_dir="."):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    for root, dirs, files in os.walk(root_dir):
        if any(d in root for d in ['.git', 'node_modules', 'venv', '__pycache__', 'legacy']):
            continue
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if not content.strip().startswith('---'):
                    print(f"Fixing IAMD header for {path}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(HEADER.format(timestamp=timestamp) + "\n" + content)

if __name__ == "__main__":
    fix_iamd()
