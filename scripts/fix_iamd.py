import os
import yaml
import re
from datetime import datetime

REQUIRED_FIELDS = ['agent', 'action', 'timestamp', 'related_gate', 'status']

def get_iamd_header(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)), content[match.end():]
        except:
            return None, content
    return None, content

def fix_iamd_header(file_path):
    header, body = get_iamd_header(file_path)

    # Guess agent from path
    agent = "E3"
    if "agents/" in file_path:
        parts = file_path.split('/')
        agent_dir = next((p for p in parts if p.startswith(('D', 'E', 'AC')) and len(p) <= 3), "E3")
        agent = agent_dir

    if header is None or not isinstance(header, dict):
        header = {}

    # Fill missing fields
    if 'agent' not in header: header['agent'] = agent
    if 'action' not in header: header['action'] = "Audit/Fix"
    if 'timestamp' not in header: header['timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    if 'related_gate' not in header: header['related_gate'] = "G2"
    if 'status' not in header: header['status'] = "Validated"

    # Ensure all required fields exist
    for field in REQUIRED_FIELDS:
        if field not in header:
            header[field] = "N/A"

    yaml_header = "---\n" + yaml.dump(header, default_flow_style=False) + "---\n\n"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(yaml_header + body.lstrip())

def main():
    directories = ['docs', 'engineering', 'governance', 'agents']
    for d in directories:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d):
                if '.git' in dirs: dirs.remove('.git')
                for file in files:
                    if file.endswith('.md'):
                        fix_iamd_header(os.path.join(root, file))

if __name__ == "__main__":
    main()
