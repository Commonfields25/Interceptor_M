import sys
import yaml
import re
import os

REQUIRED_FIELDS = ["agent", "action", "timestamp", "related_gate", "status"]


def validate_iamd_header(file_path):
    if not file_path.endswith(".md"):
        return True, None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}"

    # Search for YAML frontmatter
    # Format: --- \n (yaml) \n ---
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return False, "Missing IAMD YAML header (must start with --- and end with ---)"

    yaml_text = match.group(1)
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as e:
        return False, f"Invalid YAML syntax in header: {e}"

    if not isinstance(data, dict):
        return False, "Header content is not a valid YAML object"

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        return False, f"Missing required IAMD fields: {', '.join(missing)}"

    return True, None


def main():
    files_to_check = sys.argv[1:]
    if not files_to_check:
        print("No files to check.")
        sys.exit(0)

    failed_files = []
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"Warning: File not found: {file_path}")
            continue

        is_valid, error = validate_iamd_header(file_path)
        if not is_valid:
            failed_files.append((file_path, error))

    if failed_files:
        print("🔴 IAMD Protocol Violation found in the following files:")
        for file_path, error in failed_files:
            print(f"  - {file_path}: {error}")
        print(
            "\nPlease ensure all Markdown files start with a valid YAML header as per BOT_GUIDELINES.md:"
        )
        print("---")
        print("agent: [AgentID]")
        print("action: [Update/Create/Refactor]")
        print("timestamp: YYYY-MM-DDTHH:MM:SSZ")
        print("related_gate: [G1-G11 or N/A]")
        print("status: [Draft/Review/Validated]")
        print("---\n")
        sys.exit(1)
    else:
        print("✅ All Markdown files follow the IAMD protocol.")
        sys.exit(0)


if __name__ == "__main__":
    main()
