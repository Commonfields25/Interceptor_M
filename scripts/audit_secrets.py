#!/usr/bin/env python3
"""Audit secrets in Python scripts — called by iso-compliance.yml CI"""
import re, sys
from pathlib import Path

PATTERNS = [
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'),       'GitHub PAT detected'),
    (re.compile(r'ghp_[a-zA-Z0-9_]{20,}'),     'GitHub PAT-like pattern'),
    (re.compile(r'password\s*=\s*["\']', re.I), 'hardcoded password'),
    (re.compile(r'api_key\s*=\s*["\']', re.I),  'hardcoded API key'),
    (re.compile(r'secret\s*=\s*["\']', re.I),   'hardcoded secret'),
]

def scan_file(path):
    hits = []
    try:
        with open(path) as fh:
            for i, line in enumerate(fh, 1):
                for pat, name in PATTERNS:
                    if pat.search(line):
                        hits.append(f'  WARNING: {name} at {path}:{i}')
    except Exception:
        pass
    return hits

def main():
    dirs = ['scripts', 'linear_supabase', 'simulation']
    all_hits = []
    for d in dirs:
        for pyf in Path(d).glob('*.py'):
            all_hits.extend(scan_file(pyf))
    if all_hits:
        for h in all_hits:
            print(h)
        print(f'\n{len(all_hits)} warning(s) found.')
        sys.exit(1 if all_hits else 0), don't fail CI
    else:
        print('No secrets detected. Audit clean.')
        sys.exit(0)

if __name__ == '__main__':
    main()
