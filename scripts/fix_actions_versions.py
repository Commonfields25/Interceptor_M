import os
import re

replacements = {
    r'actions/checkout(@v\d+)?': 'actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332',  # v4.1.7
    r'actions/setup-python(@v\d+)?': 'actions/setup-python@f677139bee7f93243e0b99e2f95b4e1b3c527f31', # v5.1.1
    r'actions/setup-node(@v\d+)?': 'actions/setup-node@1d11996622869ed6e68393b21c46a932bc0b2981', # v4.0.3
    r'actions/upload-artifact(@v\d+)?': 'actions/upload-artifact@0b2256b8c012f0828bd1d899d584e2667d165322', # v4.3.4
    r'actions/github-script(@v\d+)?': 'actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea', # v7.0.1
    r'actions/attest-build-provenance(@v\d+(\.\d+\.\d+)?)?': 'actions/attest-build-provenance@520d128f1d5917a808f0292c07522e8f520ca521', # v1.4.3
    r'github/codeql-action/init(@v\d+)?': 'github/codeql-action/init@afb1ef2944391e0bc6880430d9fd9d6f300ce711', # v3.25.15
    r'github/codeql-action/analyze(@v\d+)?': 'github/codeql-action/analyze@afb1ef2944391e0bc6880430d9fd9d6f300ce711', # v3.25.15
    r'actions/configure-pages(@v\d+)?': 'actions/configure-pages@1f0e5c648dc9a96e959419036d00ec64b0b8c67a', # v5.0.0
    r'actions/jekyll-build-pages(@v\d+)?': 'actions/jekyll-build-pages@1a0628771b7b7f6ce02049d2024b6f671c068302', # v1.0.12
    r'actions/upload-pages-artifact(@v\d+)?': 'actions/upload-pages-artifact@56afc609e74202658d3ffba0e8f6dee434047195', # v3.0.1
    r'actions/deploy-pages(@v\d+)?': 'actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e', # v4.0.5
    r'tj-actions/changed-files(@v\d+)?': 'tj-actions/changed-files@84815234ad467ca051e710ca8b999c06d3d99f8e', # v44.5.7
}

folder = '.github/workflows'
for filename in os.listdir(folder):
    if filename.endswith('.yml') or filename.endswith('.yml.disabled'):
        path = os.path.join(folder, filename)
        with open(path, 'r') as f:
            content = f.read()

        new_content = content
        for pattern, replacement in replacements.items():
            new_content = re.sub(pattern, replacement, new_content)

        if new_content != content:
            with open(path, 'w') as f:
                f.write(new_content)
            print(f"✅ Fixed {filename}")
