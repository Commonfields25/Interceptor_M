import os
import re
import sys


def find_tags(directory, pattern):
    tags = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".md", ".json", ".yml")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        matches = re.findall(pattern, content)
                        for match in matches:
                            if match not in tags:
                                tags[match] = []
                            tags[match].append(path)
                except:
                    continue
    return tags


def main():
    print("🔍 Running ISO/AS9100 Traceability Audit...")

    # REQ-XXX tags
    req_pattern = r"REQ-[A-Z0-9]+"

    code_tags = find_tags(".", req_pattern)

    if not code_tags:
        print("ℹ️ No traceability tags (REQ-XXX) found in the codebase.")
        sys.exit(0)

    print(f"✅ Found {len(code_tags)} unique requirements referenced.")
    for req, paths in code_tags.items():
        print(f"  - {req}: {len(paths)} references")
        for p in paths[:3]:  # Show first 3
            print(f"    - {p}")

    # In a real scenario, we'd compare this against a requirements master list
    sys.exit(0)


if __name__ == "__main__":
    main()
