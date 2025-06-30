# Documentation Standards - PreventIA News Analytics

## Overview

This document establishes standardized practices for documentation maintenance, verification, and consistency across the PreventIA News Analytics project.

## Automated Documentation Verification

### Documentation Verification Script

**Location**: `scripts/verify_docs.py`

**Purpose**: Automatically verify all documentation links in `docs/README.md` and maintain accurate status indicators.

#### Usage

```bash
# Verify documentation and update README automatically
python scripts/verify_docs.py

# Dry run to see what would be changed without modifying files
python scripts/verify_docs.py --dry-run

# Specify custom repository root
python scripts/verify_docs.py --repo-root /path/to/repo
```

#### Features

1. **Link Verification**: Scans all markdown links in `docs/README.md`
2. **Status Updates**: Automatically adds ✅ (exists) or (Pendiente) (missing) indicators
3. **Metrics Generation**: Calculates completion percentage and generates reports
4. **Automated Reporting**: Updates documentation status section with current metrics

### Status Indicators

#### Format Standard
```markdown
[Document Title](path/to/file.md) - ✅ Description for existing file
[Document Title](path/to/file.md) - (Pendiente) Description for missing file
```

#### Status Types
- **✅**: File exists and is accessible
- **(Pendiente)**: File referenced but not yet created
- **No indicator**: External links or anchors (not verified)

## Documentation Structure Standards

### File Naming Conventions

#### Files
- **Lowercase with hyphens**: `system-overview.md`, `testing-strategy.md`
- **Descriptive names**: Clear purpose from filename
- **Consistent suffixes**: `-guide.md`, `-strategy.md`, `-standards.md`

#### Directories
- **Lowercase**: `development/`, `architecture/`, `decisions/`
- **Descriptive**: Clear organizational purpose
- **Hierarchical**: Logical grouping of related documents

### Link Standards

#### Internal Links
```markdown
# ✅ Correct
[System Overview](architecture/system-overview.md)
[ADR-001](decisions/ADR-001-project-scope-change.md)

# ❌ Incorrect
[System Overview](../architecture/system-overview.md)  # No relative paths
[ADR 001](decisions/ADR 001.md)  # No spaces in filenames
```

#### External Links
```markdown
# ✅ Correct
[pytest Documentation](https://docs.pytest.org/)
[Conventional Commits](https://www.conventionalcommits.org/)

# Note: External links are not verified by automation
```

### Content Standards

#### Language Usage
- **Technical Documentation**: English (APIs, code standards)
- **Team Decisions**: Spanish (ADRs, implementation results)
- **Mixed Content**: Follow primary document language
- **Reference**: See [Language Usage Standard](language-usage-standard.md)

#### Format Consistency
```markdown
# Document Header
# Document Title - Purpose

## Overview
Brief description of document purpose

## Sections
Organize content logically

## References
- [Related Document](path.md)
- [External Resource](https://example.com)

---
**Last Updated**: YYYY-MM-DD
**Maintainer**: Role/Name
```

## Automation Workflow

### Manual Verification Process (Legacy)
1. Find all markdown links in docs/README.md
2. Check each file exists
3. Manually update status indicators
4. Update completion metrics
5. Commit changes

**Time**: 30-45 minutes
**Error prone**: Yes
**Token consumption**: High

### Automated Verification Process (Current)
1. Run `python scripts/verify_docs.py`
2. Review output report
3. Commit if changes made

**Time**: 2-3 minutes
**Error prone**: No
**Token consumption**: Minimal

### Integration Options

#### Pre-commit Hook (Recommended for FASE 3)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: docs-verification
        name: Verify documentation links
        entry: python scripts/verify_docs.py
        language: python
        pass_filenames: false
        always_run: true
```

#### GitHub Actions (Future)
```yaml
# .github/workflows/docs-check.yml
name: Documentation Check
on: [pull_request]
jobs:
  verify-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify Documentation
        run: python scripts/verify_docs.py --dry-run
```

## Quality Gates

### Documentation Completion Targets

#### Phase-based Targets
- **FASE 1**: 40% completion (basic setup and architecture)
- **FASE 2**: 60% completion (standards and implementation docs)
- **FASE 3**: 80% completion (API docs and operations)
- **Production**: 90%+ completion (comprehensive coverage)

#### Priority Categories
1. **Critical**: Setup guides, API docs, architecture
2. **Important**: Standards, testing, operations
3. **Nice-to-have**: Advanced guides, troubleshooting

### Review Process

#### Weekly Reviews
- Run verification script
- Review completion metrics
- Identify priority documentation gaps
- Plan documentation tasks for upcoming work

#### Release Reviews
- Ensure all new features documented
- Update API documentation
- Review and update completion targets
- Validate all links work correctly

## Error Handling

### Common Issues

#### Duplicate Links
**Problem**: Same file referenced multiple times with different descriptions
**Solution**: Consolidate references or use one primary reference

#### Broken Paths
**Problem**: Files moved but links not updated
**Solution**: Automation detects and reports broken links

#### Inconsistent Status
**Problem**: Manual status indicators get out of sync
**Solution**: Regular automated verification updates

### Troubleshooting

#### Script Errors
```bash
# Check Python path and dependencies
python --version
python -c "import re, sys, pathlib"

# Verify script permissions
ls -la scripts/verify_docs.py

# Run with explicit path
python scripts/verify_docs.py --repo-root .
```

#### False Positives
- **External links**: Not verified (expected)
- **Anchor links**: Skip verification (expected)
- **Conditional content**: May need manual review

## Metrics and Reporting

### Standard Metrics
- **Total files referenced**: Count of all documentation links
- **Existing files**: Count of files that exist
- **Missing files**: Count of files that need creation
- **Completion rate**: Percentage of existing vs total files

### Reporting Format
```
📊 Documentation Verification Report
========================================
Total files referenced: 41
Existing files: 25
Missing files: 16
Completion rate: 61.0%
```

### Historical Tracking
- Track completion rate over time
- Identify documentation debt trends
- Plan documentation sprints based on gaps

## Future Enhancements

### Planned Features
1. **Content validation**: Check for required sections in documents
2. **Link validation**: Verify external links are accessible
3. **Template compliance**: Ensure documents follow templates
4. **Automatic TOC**: Generate table of contents automatically

### Integration Opportunities
1. **IDE integration**: VS Code extension for real-time verification
2. **Dashboard**: Web dashboard showing documentation health
3. **Notifications**: Slack/email alerts for broken documentation

## References

- [Language Usage Standard](language-usage-standard.md)
- [Git Workflow Standard](git-workflow.md)
- [Testing Strategy](testing-strategy.md)
- [Documentation Verification Script](../../scripts/verify_docs.py)

---
**Version**: 1.0
**Effective Date**: 2025-06-28
**Next Review**: 2025-08-28
**Maintainer**: Technical Team
