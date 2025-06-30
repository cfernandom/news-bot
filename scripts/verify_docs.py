#!/usr/bin/env python3
"""
Documentation Verification Script
Automatically verifies all links in docs/README.md and updates status indicators.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class DocVerifier:
    def __init__(self, repo_root: str = None):
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).parent.parent
        self.docs_root = self.repo_root / "docs"
        self.readme_path = self.docs_root / "README.md"

    def extract_links(self, content: str) -> List[Tuple[str, str, str]]:
        """Extract markdown links from content.
        Returns: List of (title, path, description) tuples
        """
        # Pattern: [Title](path) - Description  or  [Title](path) - ✅/❌ Description
        pattern = r"\[([^\]]+)\]\(([^)]+)\)(?:\s*-\s*(?:✅|❌|\(Pendiente\))?\s*(.+))?"
        matches = re.findall(pattern, content)
        return [
            (title.strip(), path.strip(), desc.strip() if desc else "")
            for title, path, desc in matches
        ]

    def check_file_exists(self, relative_path: str) -> bool:
        """Check if a file exists relative to docs directory."""
        if relative_path.startswith("#"):  # Skip anchors
            return True
        if relative_path.startswith("http"):  # Skip external links
            return True

        full_path = self.docs_root / relative_path
        return full_path.exists()

    def get_status_indicator(self, exists: bool) -> str:
        """Get status indicator for file."""
        return "✅" if exists else "(Pendiente)"

    def update_readme_content(self, content: str) -> str:
        """Update README content with current status indicators."""
        lines = content.split("\n")
        updated_lines = []

        for line in lines:
            # Find lines with markdown links
            link_matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", line)
            if link_matches:
                updated_line = line
                for title, path in link_matches:
                    if not path.startswith("#") and not path.startswith("http"):
                        exists = self.check_file_exists(path)
                        status = self.get_status_indicator(exists)

                        # Remove existing status indicators
                        updated_line = re.sub(
                            r"\s*-\s*(?:✅|\(Pendiente\))\s*", " - ", updated_line
                        )

                        # Add new status indicator
                        if " - " in updated_line:
                            updated_line = updated_line.replace(
                                " - ", f" - {status} ", 1
                            )
                        else:
                            # If no description, add status
                            updated_line = updated_line.replace(
                                f"]({path})", f"]({path}) - {status}"
                            )

                updated_lines.append(updated_line)
            else:
                updated_lines.append(line)

        return "\n".join(updated_lines)

    def generate_metrics(self, links: List[Tuple[str, str, str]]) -> Dict:
        """Generate documentation metrics."""
        total_files = 0
        existing_files = 0
        missing_files = []
        existing_files_list = []

        for title, path, desc in links:
            if not path.startswith("#") and not path.startswith("http"):
                total_files += 1
                if self.check_file_exists(path):
                    existing_files += 1
                    existing_files_list.append(f"{path}")
                else:
                    missing_files.append(f"{path}")

        completion_rate = (existing_files / total_files * 100) if total_files > 0 else 0

        return {
            "total_files": total_files,
            "existing_files": existing_files,
            "missing_files": missing_files,
            "existing_files_list": existing_files_list,
            "completion_rate": completion_rate,
        }

    def update_metrics_section(self, content: str, metrics: Dict) -> str:
        """Update the documentation status section in README."""
        # Find the documentation status section
        status_start = content.find("## 📋 Estado de la Documentación")
        if status_start == -1:
            return content

        # Find the end of the section (next ## or end of file)
        next_section = content.find("\n## ", status_start + 1)
        if next_section == -1:
            next_section = content.find("\n---", status_start + 1)

        if next_section == -1:
            # Section goes to end of file
            before_section = content[:status_start]
            after_section = ""
        else:
            before_section = content[:status_start]
            after_section = content[next_section:]

        # Generate new metrics section
        new_section = f"""## 📋 Estado de la Documentación

### ✅ **Documentación Completada ({metrics['existing_files']} archivos)**
Archivos existentes y verificados:
{chr(10).join(f'- `{path}`' for path in sorted(metrics['existing_files_list']))}

### 📋 **Documentación Pendiente ({len(metrics['missing_files'])} archivos)**
Archivos pendientes de crear:
{chr(10).join(f'- `{path}`' for path in sorted(metrics['missing_files']))}

### 📊 **Métricas de Completitud**
- **Total archivos referenciados**: {metrics['total_files']}
- **Archivos existentes**: {metrics['existing_files']}
- **Archivos pendientes**: {len(metrics['missing_files'])}
- **Completitud**: {metrics['completion_rate']:.1f}%

### 🎯 **Próxima Prioridad**
Para FASE 3, se recomienda completar:
1. **Docker Setup** y **Environment Variables** (setup crítico)
2. **Data Flow** y **Tech Stack** (arquitectura)
3. **FastAPI Analytics API** (implementación)

---

**Última verificación**: {self.get_current_date()}
**Estado**: FASE 2 Completada ✅ | Documentación: {metrics['completion_rate']:.1f}% completada
**Mantenedores**: Claude (Director Técnico), cfernandom (Ingeniero Senior)"""

        return before_section + new_section + after_section

    def get_current_date(self) -> str:
        """Get current date in YYYY-MM-DD format."""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d")

    def verify_and_update(self, dry_run: bool = False) -> Dict:
        """Main verification and update process."""
        if not self.readme_path.exists():
            raise FileNotFoundError(f"README.md not found at {self.readme_path}")

        # Read current content
        with open(self.readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract links and generate metrics
        links = self.extract_links(content)
        metrics = self.generate_metrics(links)

        # Update content
        updated_content = self.update_readme_content(content)
        updated_content = self.update_metrics_section(updated_content, metrics)

        # Write back if not dry run
        if not dry_run:
            with open(self.readme_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"✅ Updated {self.readme_path}")
        else:
            print("🔍 Dry run - no files modified")

        return metrics


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Verify documentation links and update status"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be updated without making changes",
    )
    parser.add_argument("--repo-root", help="Path to repository root")

    args = parser.parse_args()

    try:
        verifier = DocVerifier(args.repo_root)
        metrics = verifier.verify_and_update(dry_run=args.dry_run)

        # Print report
        print("\n📊 Documentation Verification Report")
        print("=" * 40)
        print(f"Total files referenced: {metrics['total_files']}")
        print(f"Existing files: {metrics['existing_files']}")
        print(f"Missing files: {len(metrics['missing_files'])}")
        print(f"Completion rate: {metrics['completion_rate']:.1f}%")

        if metrics["missing_files"]:
            print(f"\n📋 Missing files ({len(metrics['missing_files'])}):")
            for file in sorted(metrics["missing_files"]):
                print(f"  - {file}")

        print(f"\n✅ Verification completed successfully!")
        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
