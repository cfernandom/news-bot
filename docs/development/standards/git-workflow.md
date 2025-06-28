# Git Workflow Standard - PreventIA News Analytics

## Overview

This document defines the Git workflow, commit conventions, and branching strategy for PreventIA News Analytics to ensure consistent, traceable, and professional version control.

## Branch Strategy

### Branch Structure
```
main (production)
├── dev (development integration)
    ├── feature/phase-3-fastapi
    ├── feature/dashboard-frontend
    ├── hotfix/sentiment-analysis-bug
    └── docs/api-documentation
```

### Branch Types

#### 1. Main Branch (`main`)
- **Purpose**: Production-ready code
- **Protection**: Protected, requires PR approval
- **Deployment**: Auto-deploys to production
- **Merge Strategy**: Squash and merge from `dev`

#### 2. Development Branch (`dev`)
- **Purpose**: Integration of completed features
- **Protection**: Requires PR approval
- **Testing**: All tests must pass
- **Merge Strategy**: Merge commits to preserve history

#### 3. Feature Branches
```bash
# Format: feature/description-with-hyphens
feature/nlp-sentiment-analysis
feature/testing-framework
feature/api-endpoints
```

#### 4. Documentation Branches
```bash
# Format: docs/description-with-hyphens
docs/api-documentation
docs/adr-updates
docs/testing-strategy
```

#### 5. Hotfix Branches
```bash
# Format: hotfix/description-with-hyphens
hotfix/database-connection-leak
hotfix/sentiment-analysis-crash
```

### Branch Naming Conventions
- **Lowercase with hyphens**: `feature/nlp-sentiment-analysis`
- **Descriptive**: Clear purpose from name
- **Type prefix**: `feature/`, `docs/`, `hotfix/`, `chore/`
- **Max length**: 50 characters

## Commit Conventions

### Conventional Commits Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

#### Primary Types
- **feat**: New feature for users
- **fix**: Bug fix for users
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring (no feature change or bug fix)
- **test**: Adding or updating tests
- **chore**: Maintenance tasks (dependencies, build process)

#### Project-Specific Types
- **migration**: Database migrations or data migrations
- **scraper**: Changes to web scraping functionality
- **nlp**: Natural Language Processing improvements
- **analytics**: Analytics and reporting features

### Commit Scopes (Optional)
```bash
feat(nlp): add sentiment analysis with VADER
fix(database): resolve connection pool leak
docs(api): add NLP service documentation
test(integration): add database integration tests
chore(deps): update dependencies to latest versions
```

### Commit Message Guidelines

#### Subject Line (Required)
- **Length**: 50 characters or less
- **Case**: Lowercase
- **No period**: Don't end with a period
- **Imperative mood**: "add feature" not "added feature"

#### Body (Optional)
- **Length**: 72 characters per line
- **What and why**: Explain what changed and why
- **Separate**: Blank line between subject and body

#### Footer (Optional)
- **Breaking changes**: `BREAKING CHANGE: description`
- **Issue references**: `Closes #123`, `Fixes #456`
- **Co-authors**: `Co-authored-by: Name <email>`

### Examples

#### Good Commits
```bash
feat(nlp): add VADER sentiment analysis for medical content

Implement sentiment analysis specialized for medical news articles
with conservative thresholds. Processes 56 articles with 95% accuracy.

- Conservative thresholds (±0.3 vs ±0.05 standard)
- Medical content bias adjustment
- Batch processing optimization (~2 articles/second)

Closes #42

docs(standards): add comprehensive testing strategy

Add testing pyramid strategy with unit/integration/e2e structure,
performance benchmarks, and CI/CD integration guidelines.

chore(gitignore): fix test file exclusion pattern

Change overly broad `test_*.py` pattern to `test_temp_*.py` 
to allow legitimate test files while excluding temporary ones.
```

#### Bad Commits
```bash
# ❌ Too vague
fix stuff

# ❌ Too long subject
feat(nlp): implement comprehensive sentiment analysis system with VADER and spaCy integration for medical content

# ❌ Wrong case/format
Fix: Database connection issues
Update documentation

# ❌ No context
refactor: code improvements
```

## Atomic Commits Strategy

### What Makes a Good Atomic Commit
1. **Single responsibility**: One logical change per commit
2. **Complete**: Commit should not break the build
3. **Focused**: Related changes grouped together
4. **Testable**: Each commit can be tested independently

### Examples

#### ✅ Good Atomic Commits
```bash
# Separate commits for different aspects
feat(nlp): add VADER sentiment analyzer core implementation
test(nlp): add 14 comprehensive unit tests for sentiment analysis
docs(nlp): add NLP API documentation with usage examples
feat(nlp): integrate sentiment analysis into NLP pipeline
```

#### ❌ Bad Monolithic Commit
```bash
# Everything in one commit
feat: implement complete NLP system with sentiment analysis, testing, documentation, and pipeline integration
```

## Pull Request Process

### PR Requirements
1. **Descriptive title**: Clear, concise description
2. **Body template**: Use PR template (below)
3. **Tests passing**: All CI checks green
4. **Code review**: At least one approval required
5. **Up to date**: Branch must be current with target

### PR Template
```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to not work)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Changes Made
- List specific changes
- Include technical details
- Reference any ADRs if architectural

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Documentation
- [ ] Code comments added/updated
- [ ] API documentation updated
- [ ] ADR created if needed
- [ ] README updated if needed

## Checklist
- [ ] Self-review completed
- [ ] Code follows style guidelines
- [ ] No sensitive data included
- [ ] Database migrations tested (if applicable)
```

### Merge Strategies

#### Feature → Dev
- **Strategy**: Merge commit
- **Reason**: Preserve feature development history
- **Command**: `git merge --no-ff feature/branch-name`

#### Dev → Main
- **Strategy**: Squash and merge
- **Reason**: Clean main branch history
- **Command**: `git merge --squash dev`

## Pre-commit Hooks (Recommended)

### Setup Pre-commit
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88]

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
EOF

# Install hooks
pre-commit install
```

### Hook Categories
1. **Code Quality**: Black formatting, flake8 linting
2. **Security**: Gitleaks secret detection
3. **General**: Trailing whitespace, large files
4. **Project-Specific**: Test validation, documentation checks

## Release Process

### Versioning Strategy
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Current**: v2.0.0 (Phase 2 completed)
- **Next**: v3.0.0 (Phase 3 - Dashboard)

### Release Steps
1. **Create release branch**: `release/v3.0.0`
2. **Update version numbers**: package.json, __init__.py, etc.
3. **Update CHANGELOG.md**: Document all changes
4. **Create release PR**: `release/v3.0.0` → `main`
5. **Tag release**: `git tag v3.0.0`
6. **Deploy**: Automated deployment on tag push

## Git Aliases (Recommended)

```bash
# Add to ~/.gitconfig
[alias]
    # Commit shortcuts
    c = commit
    ca = commit -a
    cm = commit -m
    cam = commit -am
    
    # Branch operations
    co = checkout
    br = branch
    sw = switch
    
    # Status and log
    st = status
    lg = log --oneline --graph --decorate --all
    last = log -1 HEAD
    
    # Useful shortcuts
    unstage = reset HEAD --
    uncommit = reset --soft HEAD~1
    recommit = commit --amend --no-edit
    
    # Project-specific
    phase = !git log --oneline --grep="feat\\|docs\\|fix" -10
    docs-only = !git log --oneline --grep="docs" -10
```

## Emergency Procedures

### Hotfix Process
```bash
# Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-issue

# Make fix and test
# ... fix code ...

# Create emergency PR
git push origin hotfix/critical-security-issue
# Open PR: hotfix/critical-security-issue → main
# Fast-track review and merge

# Backport to dev
git checkout dev
git merge main
```

### Rollback Process
```bash
# If deployment fails, rollback
git checkout main
git revert HEAD
git push origin main

# Or reset to previous version
git reset --hard v2.1.0
git push --force-with-lease origin main
```

## Quality Gates

### Commit Quality Checks
- [ ] Follows conventional commit format
- [ ] Subject line ≤ 50 characters
- [ ] No sensitive data (API keys, passwords)
- [ ] Atomic (single logical change)
- [ ] Tests pass locally

### PR Quality Checks
- [ ] All CI checks pass
- [ ] Code review approved
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Performance impact assessed

### Release Quality Checks
- [ ] All tests pass in staging
- [ ] Documentation complete
- [ ] Breaking changes documented
- [ ] Migration scripts tested
- [ ] Rollback plan prepared

## Troubleshooting

### Common Issues

#### Merge Conflicts
```bash
# Resolve conflicts manually, then:
git add .
git commit  # Complete the merge
```

#### Wrong Branch
```bash
# Move commits to correct branch
git cherry-pick <commit-hash>
git checkout wrong-branch
git reset --hard HEAD~1
```

#### Sensitive Data Committed
```bash
# Remove from history (dangerous!)
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch path/to/sensitive/file' \
--prune-empty --tag-name-filter cat -- --all
```

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://sethrobertson.github.io/GitBestPractices/)
- [Atlassian Git Workflows](https://www.atlassian.com/git/tutorials/comparing-workflows)
- [Pre-commit Hooks](https://pre-commit.com/)

---
**Version**: 1.0  
**Effective Date**: 2025-06-28  
**Next Review**: 2025-09-28  
**Approved By**: Technical Team