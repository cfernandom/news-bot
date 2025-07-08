#!/usr/bin/env python3
"""
Documentation Quality Check Script
Validates documentation quality, consistency, and completeness.
"""

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class QualityIssue:
    file_path: str
    line_number: int
    issue_type: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    suggestion: Optional[str] = None


class DocQualityChecker:
    def __init__(self, repo_root: str = None):
        self.repo_root = Path(repo_root) if repo_root else Path(__file__).parent.parent
        self.docs_root = self.repo_root / "docs"
        self.issues: List[QualityIssue] = []

        # Quality rules configuration
        self.language_rules = {
            "technical_docs": ["architecture/", "api/", "development/standards/"],
            "team_docs": ["decisions/", "implementation/", "conversations/"],
            "mixed_docs": ["development/setup/", "development/guides/"],
        }

        self.required_sections = {
            "api": ["Overview", "Usage", "Examples", "References"],
            "architecture": ["Overview", "Components", "References"],
            "standards": ["Overview", "Guidelines", "Examples", "References"],
            "setup": ["Prerequisites", "Installation", "Verification"],
            "adr": ["Context", "Decision", "Consequences"],
        }

    def check_all_docs(self) -> List[QualityIssue]:
        """Run all quality checks on documentation."""
        self.issues = []

        for md_file in self.docs_root.rglob("*.md"):
            relative_path = md_file.relative_to(self.docs_root)
            self._check_single_file(md_file, str(relative_path))

        return self.issues

    def _check_single_file(self, file_path: Path, relative_path: str):
        """Check quality of a single documentation file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Run individual checks
            self._check_metadata_presence(relative_path, content)
            self._check_language_consistency(relative_path, content)
            self._check_required_sections(relative_path, content)
            self._check_link_format(relative_path, lines)
            self._check_code_block_format(relative_path, lines)
            self._check_heading_structure(relative_path, lines)
            self._check_line_length(relative_path, lines)
            self._check_security_patterns(relative_path, content)

        except Exception as e:
            self._add_issue(
                relative_path, 0, "file_error", "error", f"Could not read file: {e}"
            )

    def _check_metadata_presence(self, file_path: str, content: str):
        """Check if important documents have metadata blocks."""
        important_files = [
            "README.md",
            "architecture/system-overview.md",
            "api/services/nlp-api.md",
            "development/standards/",
        ]

        is_important = any(pattern in file_path for pattern in important_files)
        has_metadata = "**Document Metadata**" in content or "---" in content[:500]

        if is_important and not has_metadata:
            self._add_issue(
                file_path,
                1,
                "missing_metadata",
                "warning",
                "Important document missing metadata block",
                "Add metadata block with version, last updated, maintainer, etc.",
            )

    def _check_language_consistency(self, file_path: str, content: str):
        """Check language consistency based on file category."""
        # Detect current language
        spanish_indicators = len(
            re.findall(
                r"\b(el|la|los|las|un|una|de|del|que|para|con|por)\b", content.lower()
            )
        )
        english_indicators = len(
            re.findall(r"\b(the|a|an|of|to|for|with|by|in|on|at)\b", content.lower())
        )

        is_spanish = spanish_indicators > english_indicators

        # Check expected language based on path
        expected_english = any(
            pattern in file_path for pattern in self.language_rules["technical_docs"]
        )
        expected_spanish = any(
            pattern in file_path for pattern in self.language_rules["team_docs"]
        )

        if expected_english and is_spanish:
            self._add_issue(
                file_path,
                1,
                "language_inconsistency",
                "warning",
                "Technical document should be in English",
                "Translate to English per language usage standard",
            )
        elif expected_spanish and not is_spanish and "template" not in file_path:
            self._add_issue(
                file_path,
                1,
                "language_inconsistency",
                "info",
                "Team document could be in Spanish",
                "Consider Spanish for team communication docs",
            )

    def _check_required_sections(self, file_path: str, content: str):
        """Check if documents have required sections."""
        doc_type = self._get_document_type(file_path)
        if doc_type not in self.required_sections:
            return

        required = self.required_sections[doc_type]
        headers = re.findall(r"^#{1,6}\s+(.+)$", content, re.MULTILINE)

        missing_sections = []
        for section in required:
            if not any(section.lower() in header.lower() for header in headers):
                missing_sections.append(section)

        if missing_sections:
            self._add_issue(
                file_path,
                1,
                "missing_sections",
                "info",
                f"Missing recommended sections: {', '.join(missing_sections)}",
                f"Consider adding sections for {doc_type} documents",
            )

    def _check_link_format(self, file_path: str, lines: List[str]):
        """Check markdown link formatting."""
        for i, line in enumerate(lines, 1):
            # Check for malformed links
            malformed_links = re.findall(r"\[([^\]]*)\]\([^)]*\s[^)]*\)", line)
            if malformed_links:
                self._add_issue(
                    file_path,
                    i,
                    "malformed_link",
                    "warning",
                    "Link contains spaces in URL",
                    "Use %20 for spaces in URLs or check formatting",
                )

            # Check for relative path issues
            relative_paths = re.findall(r"\[([^\]]*)\]\((\.\./[^)]*)\)", line)
            if relative_paths:
                self._add_issue(
                    file_path,
                    i,
                    "relative_path",
                    "info",
                    "Using relative paths (../) in links",
                    "Consider using absolute paths from docs/ root",
                )

    def _check_code_block_format(self, file_path: str, lines: List[str]):
        """Check code block formatting."""
        in_code_block = False
        code_block_lang = None

        for i, line in enumerate(lines, 1):
            if line.strip().startswith("```"):
                if not in_code_block:
                    # Starting code block
                    in_code_block = True
                    lang = line.strip()[3:].strip()
                    if not lang and "example" in line.lower():
                        self._add_issue(
                            file_path,
                            i,
                            "missing_language",
                            "info",
                            "Code block missing language specification",
                            "Add language for syntax highlighting (bash, python, etc.)",
                        )
                    code_block_lang = lang
                else:
                    # Ending code block
                    in_code_block = False
                    code_block_lang = None

            elif in_code_block and code_block_lang == "bash":
                # Check for unsafe patterns in bash code
                if re.search(r"rm\s+-rf\s+/", line) or "sudo rm" in line:
                    self._add_issue(
                        file_path,
                        i,
                        "unsafe_command",
                        "warning",
                        "Potentially dangerous command in documentation",
                        "Review command safety or add warning",
                    )

    def _check_heading_structure(self, file_path: str, lines: List[str]):
        """Check heading hierarchy and structure."""
        headings = []
        for i, line in enumerate(lines, 1):
            match = re.match(r"^(#{1,6})\s+(.+)$", line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append((i, level, title))

        # Check for proper hierarchy (no skipping levels)
        prev_level = 0
        for line_num, level, title in headings:
            if level > prev_level + 1:
                self._add_issue(
                    file_path,
                    line_num,
                    "heading_hierarchy",
                    "info",
                    f"Heading level {level} skips levels (previous was {prev_level})",
                    "Use proper heading hierarchy (h1 -> h2 -> h3)",
                )
            prev_level = level

        # Check for duplicate headings
        titles = [title.lower() for _, _, title in headings]
        duplicates = [title for title in set(titles) if titles.count(title) > 1]
        if duplicates:
            self._add_issue(
                file_path,
                1,
                "duplicate_headings",
                "info",
                f"Duplicate headings found: {', '.join(duplicates)}",
                "Use unique heading titles for better navigation",
            )

    def _check_line_length(self, file_path: str, lines: List[str]):
        """Check for excessively long lines."""
        max_length = 120  # Reasonable limit for documentation
        long_lines = []

        for i, line in enumerate(lines, 1):
            # Skip code blocks and tables
            if line.strip().startswith("```") or "|" in line:
                continue
            if len(line) > max_length:
                long_lines.append(i)

        if len(long_lines) > 5:  # Only report if it's a pattern
            self._add_issue(
                file_path,
                long_lines[0],
                "long_lines",
                "info",
                f"Multiple long lines found ({len(long_lines)} lines > {max_length} chars)",
                "Consider breaking long lines for better readability",
            )

    def _check_security_patterns(self, file_path: str, content: str):
        """Check for potential security issues in documentation."""
        # Check for potential credential leaks
        suspicious_patterns = [
            (r'password\s*[=:]\s*[\'"][^\'"\s]+[\'"]', "potential_password"),
            (r'api[_-]?key\s*[=:]\s*[\'"][^\'"\s]+[\'"]', "potential_api_key"),
            (r'secret\s*[=:]\s*[\'"][^\'"\s]+[\'"]', "potential_secret"),
            (r'token\s*[=:]\s*[\'"][^\'"\s]+[\'"]', "potential_token"),
        ]

        for pattern, issue_type in suspicious_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[: match.start()].count("\n") + 1
                self._add_issue(
                    file_path,
                    line_num,
                    issue_type,
                    "warning",
                    f"Potential credential in documentation: {match.group()[:20]}...",
                    "Use placeholder values or environment variables",
                )

    def _get_document_type(self, file_path: str) -> str:
        """Determine document type based on path."""
        if "api/" in file_path:
            return "api"
        elif "architecture/" in file_path:
            return "architecture"
        elif "standards/" in file_path:
            return "standards"
        elif "setup/" in file_path:
            return "setup"
        elif file_path.startswith("decisions/ADR-"):
            return "adr"
        else:
            return "general"

    def _add_issue(
        self,
        file_path: str,
        line_number: int,
        issue_type: str,
        severity: str,
        message: str,
        suggestion: str = None,
    ):
        """Add a quality issue to the list."""
        self.issues.append(
            QualityIssue(
                file_path=file_path,
                line_number=line_number,
                issue_type=issue_type,
                severity=severity,
                message=message,
                suggestion=suggestion,
            )
        )

    def generate_report(self, issues: List[QualityIssue]) -> str:
        """Generate a formatted quality report."""
        if not issues:
            return (
                "✅ No quality issues found! Documentation is in excellent condition."
            )

        # Group issues by severity
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]
        info = [i for i in issues if i.severity == "info"]

        report = ["📊 Documentation Quality Report", "=" * 40, ""]

        # Summary
        report.extend(
            [
                f"Total issues found: {len(issues)}",
                f"❌ Errors: {len(errors)}",
                f"⚠️  Warnings: {len(warnings)}",
                f"ℹ️  Info: {len(info)}",
                "",
            ]
        )

        # Detailed issues
        for severity, issues_list, icon in [
            ("error", errors, "❌"),
            ("warning", warnings, "⚠️"),
            ("info", info, "ℹ️"),
        ]:
            if issues_list:
                report.append(f"{icon} {severity.upper()} Issues:")
                for issue in issues_list:
                    report.append(f"  📁 {issue.file_path}:{issue.line_number}")
                    report.append(f"     {issue.message}")
                    if issue.suggestion:
                        report.append(f"     💡 Suggestion: {issue.suggestion}")
                    report.append("")

        # Issue type summary
        issue_types = {}
        for issue in issues:
            issue_types[issue.issue_type] = issue_types.get(issue.issue_type, 0) + 1

        report.extend(
            [
                "📈 Issue Types Summary:",
                *[
                    f"  {itype}: {count}"
                    for itype, count in sorted(issue_types.items())
                ],
                "",
            ]
        )

        return "\n".join(report)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Check documentation quality")
    parser.add_argument("--repo-root", help="Path to repository root")
    parser.add_argument(
        "--severity",
        choices=["error", "warning", "info"],
        default="info",
        help="Minimum severity to report",
    )
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )

    args = parser.parse_args()

    try:
        checker = DocQualityChecker(args.repo_root)
        issues = checker.check_all_docs()

        # Filter by severity
        severity_order = {"error": 3, "warning": 2, "info": 1}
        min_severity = severity_order[args.severity]
        filtered_issues = [
            i for i in issues if severity_order[i.severity] >= min_severity
        ]

        # Generate report
        if args.format == "json":
            import json

            report_data = {
                "total_issues": len(filtered_issues),
                "issues": [
                    {
                        "file": issue.file_path,
                        "line": issue.line_number,
                        "type": issue.issue_type,
                        "severity": issue.severity,
                        "message": issue.message,
                        "suggestion": issue.suggestion,
                    }
                    for issue in filtered_issues
                ],
            }
            report = json.dumps(report_data, indent=2)
        else:
            report = checker.generate_report(filtered_issues)

        # Output report
        if args.output:
            with open(args.output, "w") as f:
                f.write(report)
            print(f"Report written to {args.output}")
        else:
            print(report)

        # Exit with appropriate code
        errors = [i for i in filtered_issues if i.severity == "error"]
        return 1 if errors else 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
