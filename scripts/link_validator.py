import os
import re
import sys


def main():
    print("🔗 Validating Markdown Link Integrity...")

    md_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))

    broken_links = []
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Find markdown links: [text](path)
            links = re.findall(r"\[.*?\]\((.*?)\)", content)

            base_dir = os.path.dirname(md_file)
            for link in links:
                if link.startswith(("http", "#", "mailto:")):
                    continue

                # Split anchor
                link_path = link.split("#")[0]
                if not link_path:
                    continue

                target = os.path.abspath(os.path.join(base_dir, link_path))
                if not os.path.exists(target):
                    broken_links.append((md_file, link, target))

    if broken_links:
        print(f"🔴 Found {len(broken_links)} broken internal links:")
        for source, link, abs_target in broken_links:
            print(f"  - In {source}: '{link}' (Resolved to: {abs_target})")
        sys.exit(1)
    else:
        print("✅ All internal Markdown links are valid.")
        sys.exit(0)


if __name__ == "__main__":
    main()
