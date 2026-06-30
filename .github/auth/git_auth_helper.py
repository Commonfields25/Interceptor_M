#!/usr/bin/env python3
# coding: utf-8
"""
Git Authentication Helper Script
Automates Git operations (clone, push, PR) using environment variables or config files.
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path


def load_config(config_path: str = ".github/auth/.git_credentials_config.json") -> dict:
    """Load GitHub credentials from config file or environment variables."""
    config = {}

    # Try to load from config file
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config file: {e}")
            sys.exit(1)

    # Override with environment variables if they exist
    if "GITHUB_TOKEN" in os.environ:
        config["github"] = config.get("github", {})
        config["github"]["token"] = os.environ["GITHUB_TOKEN"]
    if "GITHUB_USERNAME" in os.environ:
        config["github"] = config.get("github", {})
        config["github"]["username"] = os.environ["GITHUB_USERNAME"]
    if "GIT_USER_NAME" in os.environ:
        config["github"] = config.get("github", {})
        config["github"]["user_name"] = os.environ["GIT_USER_NAME"]
    if "GIT_USER_EMAIL" in os.environ:
        config["github"] = config.get("github", {})
        config["github"]["user_email"] = os.environ["GIT_USER_EMAIL"]

    return config


def validate_config(config: dict) -> bool:
    """Validate the configuration."""
    github_config = config.get("github", {})
    required_keys = ["token", "username", "user_name", "user_email"]
    missing_keys = [key for key in required_keys if key not in github_config or not github_config[key]]

    if missing_keys:
        print(f"Error: Missing required configuration keys: {', '.join(missing_keys)}")
        return False
    return True


def run_command(command: list, cwd: str = None) -> bool:
    """Run a shell command and return True if successful."""
    try:
        subprocess.run(command, cwd=cwd, check=True, shell=False)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(command)}\n{e}")
        return False


def test_config():
    """Test the GitHub configuration."""
    config = load_config()
    if validate_config(config):
        print("✅ Configuration is valid.")
        return True
    else:
        print("❌ Configuration is invalid.")
        return False


def clone_repo(repo_url: str, target_dir: str = None):
    """Clone a Git repository."""
    if not target_dir:
        target_dir = Path(repo_url).stem
    command = ["git", "clone", repo_url, target_dir]
    return run_command(command)


def create_branch(branch_name: str, base_branch: str = "main"):
    """Create and checkout a new branch."""
    commands = [
        ["git", "fetch", "origin"],
        ["git", "checkout", base_branch],
        ["git", "pull", "origin", base_branch],
        ["git", "checkout", "-b", branch_name]
    ]
    return all(run_command(cmd) for cmd in commands)


def push_branch(branch_name: str):
    """Push a branch to the remote repository."""
    commands = [
        ["git", "push", "-u", "origin", branch_name]
    ]
    return all(run_command(cmd) for cmd in commands)


def create_pr(title: str, body: str, base: str, head: str):
    """Create a Pull Request using GitHub API."""
    config = load_config()
    if not validate_config(config):
        return False

    token = config["github"]["token"]
    repo = "Interceptor_M"
    api_url = f"https://api.github.com/repos/Commonfields25/{repo}/pulls"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }

    try:
        import requests
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 201:
            pr_url = response.json()["html_url"]
            print(f"✅ Pull Request created: {pr_url}")
            return True
        else:
            print(f"❌ Failed to create PR: {response.json().get('message', 'Unknown error')}")
            return False
    except ImportError:
        print("Error: 'requests' library is required. Install it with: pip install requests")
        return False


def main():
    parser = argparse.ArgumentParser(description="Git Authentication Helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Test config
    subparsers.add_parser("test-config", help="Test the GitHub configuration")

    # Clone repo
    clone_parser = subparsers.add_parser("clone-repo", help="Clone a Git repository")
    clone_parser.add_argument("repo_url", help="URL of the repository to clone")
    clone_parser.add_argument("--target", help="Target directory", default=None)

    # Create PR
    pr_parser = subparsers.add_parser("create-pr", help="Create a Pull Request")
    pr_parser.add_argument("--title", required=True, help="Title of the PR")
    pr_parser.add_argument("--body", required=True, help="Body of the PR")
    pr_parser.add_argument("--base", default="main", help="Base branch for the PR")
    pr_parser.add_argument("--head", required=True, help="Head branch for the PR")

    args = parser.parse_args()

    if args.command == "test-config":
        success = test_config()
        sys.exit(0 if success else 1)
    elif args.command == "clone-repo":
        success = clone_repo(args.repo_url, args.target)
        sys.exit(0 if success else 1)
    elif args.command == "create-pr":
        success = create_pr(args.title, args.body, args.base, args.head)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()