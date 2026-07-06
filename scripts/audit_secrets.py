#!/usr/bin/env python3
"""Audit secrets in Python scripts — called by iso-compliance.yml CI"""
import re, sys
from pathlib import Path

# Security-focused patterns for secret detection
PATTERNS = [
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'),       'GitHub PAT detected'),
    (re.compile(r'ghp_[a-zA-Z0-9_]{20,}'),     'GitHub PAT-like pattern'),
    (re.compile(r'lin_api_[a-zA-Z0-9]{40}'),   'Linear API Key detected'),
    (re.compile(r'sbp_[a-zA-Z0-9]{40}'),       'Supabase Key pattern'),
    (re.compile(r'AKIA[0-9A-Z]{16}'),          'AWS Access Key ID'),
    (re.compile(r'password\s*=\s*["\'][^"\']{1,}["\']', re.I), 'Hardcoded password'),
    (re.compile(r'api_key\s*=\s*["\'][^"\']{1,}["\']', re.I),  'Hardcoded API key'),
    (re.compile(r'secret\s*=\s*["\'][^"\']{1,}["\']', re.I),   'Hardcoded secret'),
    (re.compile(r'-----BEGIN [A-Z ]{1,100}PRIVATE KEY-----'), 'Private Key detected'),
]

# Files or directories to exclude from scanning
EXCLUDE_FILES = {'.env.example', 'secrets.json.example'}

def scan_file(path):
    hits = []
    if path.name in EXCLUDE_FILES:
        return hits

    try:
        with open(path, 'r', encoding='utf-8') as fh:
            for i, line in enumerate(fh, 1):
                for pat, name in PATTERNS:
                    if pat.search(line):
                        # Avoid flagging environment variable lookups
                        if 'os.getenv' in line or 'os.environ' in line:
                            continue
                        hits.append(f'  [!] SECURITY WARNING: {name} at {path}:{i}')
    except Exception as e:
        # Silently skip files that can't be read (binary, etc.)
        pass
    return hits

def main():
    # Root directories to scan for Python files
    dirs = ['scripts', 'linear_supabase', 'simulation', 'api']
    all_hits = []

    for d in dirs:
        if not Path(d).exists():
            continue
        for pyf in Path(d).rglob('*.py'):
            all_hits.extend(scan_file(pyf))

    if all_hits:
        print("🛡️ Sentinel Security Audit Found Issues:")
        for h in all_hits:
            print(h)
        print(f'\nTotal issues found: {len(all_hits)}')
        print("ACTION REQUIRED: Remove hardcoded secrets and use environment variables.")
        sys.exit(1)
    else:
        print('✅ Sentinel: No hardcoded secrets detected in Python scripts.')
        sys.exit(0)

if __name__ == '__main__':
    main()
