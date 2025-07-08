#!/usr/bin/env python3
"""
Simple conventional commit validator script.
Validates commit messages against conventional commit format.
"""

import re
import sys
from pathlib import Path


def check_conventional_commit(commit_msg_file: str) -> bool:
    """
    Check if commit message follows conventional commit format.

    Args:
        commit_msg_file: Path to commit message file

    Returns:
        True if valid, False otherwise
    """
    try:
        with open(commit_msg_file, "r", encoding="utf-8") as f:
            commit_msg = f.read().strip()
    except FileNotFoundError:
        print(f"❌ Error: Commit message file not found: {commit_msg_file}")
        return False

    if not commit_msg:
        print("❌ Error: Empty commit message")
        return False

    # Define allowed types (including our custom ones)
    allowed_types = [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "test",
        "chore",
        "migration",
        "scraper",
        "nlp",
        "analytics",
        "legal",
    ]

    # Conventional commit regex pattern
    # Format: type(scope): description
    # Scope is optional
    pattern = rf"^({'|'.join(allowed_types)})(\(.+\))?: .+"

    if re.match(pattern, commit_msg):
        return True

    # Print helpful error message
    print("❌ Commit message does not follow conventional commit format")
    print(f"📝 Your message: {commit_msg}")
    print(f"✅ Required format: type(scope): description")
    print(f"✅ Valid types: {', '.join(allowed_types)}")
    print("📖 Examples:")
    print("   feat: add new feature")
    print("   fix(api): resolve authentication issue")
    print("   docs: update README")
    return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_conventional_commit.py <commit_msg_file>")
        sys.exit(1)

    commit_msg_file = sys.argv[1]

    if check_conventional_commit(commit_msg_file):
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure
