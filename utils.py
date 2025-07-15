"""
Utility functions for setting up Python environment for PreventIA scripts.
This replaces the need for sys.path manipulations scattered throughout the codebase.
"""

import os
import sys
from pathlib import Path


def setup_project_path():
    """
    Add project root to Python path if not already present.
    This should be called at the beginning of scripts that need to import from services.
    """
    # Get the project root directory (parent of this file)
    project_root = Path(__file__).parent.absolute()
    project_root_str = str(project_root)

    # Add to sys.path if not already present
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

    return project_root


def get_project_root() -> Path:
    """
    Get the project root directory as a Path object.
    """
    return Path(__file__).parent.absolute()


def ensure_env_loaded():
    """
    Ensure .env file is loaded for environment variables.
    """
    try:
        from dotenv import load_dotenv

        env_file = get_project_root() / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    except ImportError:
        # dotenv not installed, skip
        pass


def setup_script_environment():
    """
    Complete setup for scripts: add to path and load environment.
    Use this as a one-liner in scripts instead of manual path manipulation.
    """
    setup_project_path()
    ensure_env_loaded()
    return get_project_root()


if __name__ == "__main__":
    # Test the utility
    root = setup_script_environment()
    print(f"Project root: {root}")
    print(f"Python path contains project: {str(root) in sys.path}")
