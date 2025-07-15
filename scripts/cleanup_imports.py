#!/usr/bin/env python3
"""
Cleanup script to remove sys.path manipulations and standardize imports.
Run this script to clean up all files that use manual sys.path manipulation.
"""

import re
import sys
from pathlib import Path

# Setup project environment
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment

setup_script_environment()


def cleanup_file(file_path: Path) -> bool:
    """
    Clean up sys.path manipulations in a Python file.
    Returns True if file was modified, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Pattern to match common sys.path manipulations
        patterns_to_remove = [
            r"# Add project root to path\n.*?\n.*?sys\.path\.append\(.*?\)\n",
            r"project_root = os\.path\.dirname\(os\.path\.dirname\(os\.path\.abspath\(__file__\)\)\)\n",
            r"sys\.path\.append\(project_root\)\n",
            r"sys\.path\.append\(str\(project_root\)\)\n",
            r"project_root = Path\(__file__\)\.parent\.parent\n",
            r"sys\.path\.append\(str\(project_root\)\)\n",
        ]

        # Remove the patterns
        for pattern in patterns_to_remove:
            content = re.sub(pattern, "", content, flags=re.MULTILINE | re.DOTALL)

        # Remove standalone sys.path.append lines
        content = re.sub(
            r"^sys\.path\.append\(.*?\)\n", "", content, flags=re.MULTILINE
        )

        # Add our standardized import if we removed sys.path manipulation
        if (
            "sys.path.append" in original_content
            and "from utils import setup_script_environment" not in content
        ):
            # Find where to insert the new import
            import_section = re.search(r"(import .*?\n)+", content)
            if import_section:
                end_pos = import_section.end()
                new_import = """
# Setup project environment (replaces manual sys.path manipulation)
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import setup_script_environment
setup_script_environment()
"""
                content = content[:end_pos] + new_import + content[end_pos:]

                # Make sure we have Path imported
                if "from pathlib import Path" not in content:
                    content = re.sub(
                        r"(import sys\n)", r"\1from pathlib import Path\n", content
                    )

        # Remove extra blank lines
        content = re.sub(r"\n\n\n+", "\n\n", content)

        # Write back if changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

    return False


def main():
    """Main cleanup function"""

    # Find all Python files that contain sys.path.append
    files_to_clean = []
    project_root = Path(__file__).parent.parent

    for pattern in ["**/*.py"]:
        for file_path in project_root.glob(pattern):
            if "venv" in str(file_path) or "__pycache__" in str(file_path):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "sys.path.append" in content:
                        files_to_clean.append(file_path)
            except Exception:
                continue

    print(f"Found {len(files_to_clean)} files with sys.path.append:")
    for file_path in files_to_clean:
        print(f"  - {file_path.relative_to(project_root)}")

    print("\nCleaning up files...")
    modified_count = 0

    for file_path in files_to_clean:
        if cleanup_file(file_path):
            print(f"✅ Cleaned: {file_path.relative_to(project_root)}")
            modified_count += 1
        else:
            print(f"⏭️  Skipped: {file_path.relative_to(project_root)}")

    print(f"\n🎯 Cleanup complete! Modified {modified_count} files.")
    print("\nNext steps:")
    print("1. Test that all scripts still work correctly")
    print("2. Consider adding more __init__.py files for better package structure")
    print("3. Run tests to ensure imports still work")


if __name__ == "__main__":
    main()
