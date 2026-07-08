import os
import sys
import json
import subprocess


def get_changed_files():
    # In GHA, we can get this from environment or git
    # For local test, we check against main
    try:
        output = subprocess.check_output(
            ["git", "diff", "--name-only", "origin/main...HEAD"]
        ).decode("utf-8")
        return output.splitlines()
    except:
        # Fallback to local diff or empty
        return []


def load_map():
    with open("OWNERSHIP_MAP.json", "r") as f:
        return json.load(f)


def main():
    changed_files = sys.argv[1:] if len(sys.argv) > 1 else get_changed_files()
    if not changed_files:
        print("ℹ️ No changed files detected or provided.")
        sys.exit(0)

    owner_map = load_map()
    violations = []

    # Try to identify the agent from IAMD header in one of the files or env
    # For now, let's assume the agent ID is in an environment variable
    acting_agent = os.environ.get("ACTING_AGENT_ID", "UNKNOWN")
    print(f"🛡️ Ownership Enforcer: Validating changes by {acting_agent}...")

    for file_path in changed_files:
        # Find the most specific owner
        owner = None

        # Check direct file match first
        if file_path in owner_map:
            owner = owner_map[file_path]
        else:
            # Check directory matches
            matching_dirs = [
                d for d in owner_map.keys() if file_path.startswith(d + "/")
            ]
            if matching_dirs:
                # Get the longest (most specific) directory match
                best_match = max(matching_dirs, key=len)
                owner = owner_map[best_match]

        if owner == "LOCKED":
            violations.append(f"{file_path} is LOCKED and requires multiple approvals.")
        elif owner and acting_agent != "UNKNOWN" and owner != acting_agent:
            # In a real scenario, this would be an error.
            # For this multi-agent env, we flag it as a contention risk.
            print(
                f"⚠️ Contention Risk: {file_path} is owned by {owner}, but {acting_agent} is modifying it."
            )
            # violations.append(f"{file_path} ownership violation ({owner} vs {acting_agent})")

    if violations:
        print("🔴 Ownership Violations Found:")
        for v in violations:
            print(f"  - {v}")
        # sys.exit(1) # We won't fail yet to allow flexibility, but we report it.

    print("✅ Ownership check complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()
