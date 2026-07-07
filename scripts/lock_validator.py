import os
import sys


def main():
    print("🔐 Checking for Agent Concurrency Locks...")

    locks = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".lock"):
                locks.append(os.path.join(root, file))

    if not locks:
        print("✅ No active file locks found. Parallel execution safe.")
        sys.exit(0)

    print(f"⚠️ Found {len(locks)} active locks:")
    for lock in locks:
        try:
            with open(lock, "r") as f:
                owner = f.read().strip()
            print(f"  - {lock} (Held by: {owner})")
        except:
            print(f"  - {lock} (Unknown owner)")

    # In a CI context, we would check if the current PR touches any of these locked files
    # For now, we just report them.
    sys.exit(0)


if __name__ == "__main__":
    main()
