# PHASE 1 IMPLEMENTATION PLAN - Template Engine & Router Decomposition

## 🎯 **PHASE 1 OVERVIEW**

**Timeline:** Weeks 1-2
**Priority:** CRITICAL
**Goal:** Decompose monolithic files to improve maintainability
**Success Criteria:** Files <300 lines, 90%+ test coverage, zero functionality regression

---

## 🚨 **P1.1 TEMPLATE ENGINE DECOMPOSITION**

### **Current State Analysis**
- **File:** `services/scraper/automation/template_engine.py`
- **Size:** 1,789 lines
- **Functions:** 19 functions in single file
- **Issue:** Violates Single Responsibility Principle
- **Impact:** Maintenance nightmare, testing complexity

### **Target Architecture**
```
services/scraper/automation/template_engine/
├── __init__.py                    # Public API & backward compatibility
├── base_generator.py             # Abstract base class (TemplateGenerator)
├── cms_detectors.py              # CMS detection & site analysis
├── wordpress_generator.py        # WordPress-specific templates
├── drupal_generator.py          # Drupal-specific templates
├── medical_generator.py         # Medical site specialized patterns
├── generic_generator.py         # Fallback patterns & generic sites
└── templates/                   # External Jinja2 template files
    ├── wordpress.py.j2
    ├── drupal.py.j2
    ├── medical.py.j2
    └── generic.py.j2
```

### **Implementation Steps**

#### **Step 1: Preparation & Backup**
```bash
# Create feature branch for refactoring
git checkout -b refactor/template-engine-decomposition

# Run baseline tests
pytest services/scraper/tests/ -v
pytest --cov=services/scraper --cov-report=html

# Backup original file
cp services/scraper/automation/template_engine.py services/scraper/automation/template_engine_backup.py
```

#### **Step 2: Create Directory Structure**
```bash
# Create new directory structure
mkdir -p services/scraper/automation/template_engine/templates
touch services/scraper/automation/template_engine/__init__.py
touch services/scraper/automation/template_engine/base_generator.py
touch services/scraper/automation/template_engine/cms_detectors.py
touch services/scraper/automation/template_engine/wordpress_generator.py
touch services/scraper/automation/template_engine/drupal_generator.py
touch services/scraper/automation/template_engine/medical_generator.py
touch services/scraper/automation/template_engine/generic_generator.py
```

#### **Step 3: Extract Base Abstract Class**
**File:** `base_generator.py`
```python
"""
Abstract base class for template generators.
Defines common interface and shared functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from ..models import SiteStructure

class TemplateGenerator(ABC):
    """Abstract base class for template generators."""

    def __init__(self):
        self.cms_type: Optional[str] = None
        self.template_path: Optional[str] = None

    @abstractmethod
    async def detect_cms(self, site_structure: SiteStructure) -> bool:
        """Detect if this generator can handle the site."""
        pass

    @abstractmethod
    async def generate_scraper(self, site_structure: SiteStructure) -> str:
        """Generate scraper code for the site."""
        pass

    @abstractmethod
    def get_template_variables(self, site_structure: SiteStructure) -> Dict[str, Any]:
        """Get variables for template rendering."""
        pass

    def validate_structure(self, site_structure: SiteStructure) -> bool:
        """Validate site structure for this generator."""
        return True  # Default implementation
```

#### **Step 4: Extract CMS Detection Logic**
**File:** `cms_detectors.py`
```python
"""
CMS detection and site analysis utilities.
Centralized logic for identifying website content management systems.
"""

import re
from typing import Dict, List, Optional, Tuple
from ..models import SiteStructure

class CMSDetector:
    """Centralized CMS detection logic."""

    @staticmethod
    def detect_wordpress(site_structure: SiteStructure) -> bool:
        """Detect WordPress sites."""
        # Extract WordPress detection logic from original file
        # Look for wp-content, wp-includes, WordPress-specific patterns
        pass

    @staticmethod
    def detect_drupal(site_structure: SiteStructure) -> bool:
        """Detect Drupal sites."""
        # Extract Drupal detection logic
        pass

    @staticmethod
    def detect_medical_cms(site_structure: SiteStructure) -> bool:
        """Detect medical-specific CMS patterns."""
        # Extract medical site detection logic
        pass

    @staticmethod
    def analyze_site_patterns(site_structure: SiteStructure) -> Dict[str, Any]:
        """Analyze site for common patterns."""
        # Extract site analysis logic
        pass
```

#### **Step 5: Create Specialized Generators**

**File:** `wordpress_generator.py`
```python
"""
WordPress-specific template generator.
Handles WordPress sites with specialized patterns and optimizations.
"""

from typing import Dict, Any
from .base_generator import TemplateGenerator
from .cms_detectors import CMSDetector
from ..models import SiteStructure

class WordPressGenerator(TemplateGenerator):
    """Generator for WordPress sites."""

    def __init__(self):
        super().__init__()
        self.cms_type = "wordpress"
        self.template_path = "templates/wordpress.py.j2"

    async def detect_cms(self, site_structure: SiteStructure) -> bool:
        """Detect WordPress sites."""
        return CMSDetector.detect_wordpress(site_structure)

    async def generate_scraper(self, site_structure: SiteStructure) -> str:
        """Generate WordPress-specific scraper."""
        # Extract WordPress scraper generation logic
        pass

    def get_template_variables(self, site_structure: SiteStructure) -> Dict[str, Any]:
        """Get WordPress-specific template variables."""
        # Extract WordPress template variable logic
        pass
```

**Repeat similar pattern for:**
- `drupal_generator.py`
- `medical_generator.py`
- `generic_generator.py`

#### **Step 6: Create Template Manager**
**File:** `__init__.py`
```python
"""
Template Engine - Public API and backward compatibility.
Main entry point for template generation system.
"""

from typing import List, Optional
from .base_generator import TemplateGenerator
from .wordpress_generator import WordPressGenerator
from .drupal_generator import DrupalGenerator
from .medical_generator import MedicalGenerator
from .generic_generator import GenericGenerator
from ..models import SiteStructure

class TemplateEngine:
    """Main template engine with generator registry."""

    def __init__(self):
        self.generators: List[TemplateGenerator] = [
            WordPressGenerator(),
            DrupalGenerator(),
            MedicalGenerator(),
            GenericGenerator()  # Fallback generator
        ]

    async def generate_scraper(self, site_structure: SiteStructure) -> str:
        """Generate scraper using appropriate generator."""
        for generator in self.generators:
            if await generator.detect_cms(site_structure):
                return await generator.generate_scraper(site_structure)

        # Fallback to generic generator
        return await self.generators[-1].generate_scraper(site_structure)

# Backward compatibility - maintain original function signatures
async def generate_scraper_code(site_structure: SiteStructure) -> str:
    """Backward compatibility function."""
    engine = TemplateEngine()
    return await engine.generate_scraper(site_structure)

# Export public API
__all__ = [
    'TemplateEngine',
    'generate_scraper_code',  # Backward compatibility
    'TemplateGenerator',
    'WordPressGenerator',
    'DrupalGenerator',
    'MedicalGenerator',
    'GenericGenerator'
]
```

#### **Step 7: Extract Jinja2 Templates**
**Files:** `templates/*.py.j2`

Move hardcoded template strings to external Jinja2 files:
- `wordpress.py.j2` - WordPress scraper template
- `drupal.py.j2` - Drupal scraper template
- `medical.py.j2` - Medical site template
- `generic.py.j2` - Generic fallback template

#### **Step 8: Update Imports**
Update all files that import from the original `template_engine.py`:
```python
# Old import:
from services.scraper.automation.template_engine import generate_scraper_code

# New import (backward compatible):
from services.scraper.automation.template_engine import generate_scraper_code
```

#### **Step 9: Testing Strategy**
```bash
# Unit tests for each generator
pytest services/scraper/tests/test_template_generators.py -v

# Integration tests
pytest services/scraper/tests/test_template_engine_integration.py -v

# Regression tests - ensure same output as original
pytest services/scraper/tests/test_template_engine_regression.py -v
```

### **Success Validation**
- [ ] All new modules <300 lines
- [ ] 90%+ test coverage maintained
- [ ] All existing tests pass
- [ ] Backward compatibility verified
- [ ] No performance regression

---

## 🚨 **P1.2 API ROUTER DECOMPOSITION**

### **Current State Analysis**
- **Files:**
  - `services/api/routers/exports.py` (946 lines)
  - `services/api/routers/sources.py` (938 lines)
- **Issue:** Large router files with multiple responsibilities
- **Impact:** Difficult to maintain, test, and extend

### **Implementation Plan**

#### **Exports Router Decomposition**
```
services/api/routers/exports/
├── __init__.py                   # Main router assembly
├── csv_exports.py               # CSV generation endpoints
├── excel_exports.py             # Excel generation endpoints
├── pdf_exports.py               # PDF generation endpoints
├── chart_exports.py             # Chart generation endpoints
└── validation.py                # Export validation logic
```

#### **Sources Router Decomposition**
```
services/api/routers/sources/
├── __init__.py                  # Main router assembly
├── crud_operations.py           # Basic CRUD endpoints
├── compliance_checks.py         # Compliance validation
├── automation_endpoints.py      # Scraper automation
└── validation_handlers.py       # Input validation
```

### **Implementation Steps**
1. **Analyze Current Endpoints** - Group related functionality
2. **Extract Shared Logic** - Identify common validation/utilities
3. **Create Feature Modules** - Split by functionality
4. **Maintain Router Assembly** - Single entry point for FastAPI
5. **Update Dependencies** - Fix imports across codebase
6. **Comprehensive Testing** - Ensure all endpoints work

---

## 📋 **TESTING STRATEGY FOR PHASE 1**

### **Pre-Refactoring Tests**
```bash
# Establish baseline
pytest --cov=services --cov-report=html
pytest services/scraper/tests/ -v
pytest services/api/tests/ -v

# Performance baseline
python -m pytest services/scraper/tests/test_template_engine.py::test_generation_performance
```

### **During Refactoring Tests**
```bash
# After each major change
pytest services/scraper/tests/test_template_engine.py -v
pytest services/api/tests/test_routers.py -v

# Regression tests
python scripts/test_template_engine_regression.py
```

### **Post-Refactoring Validation**
```bash
# Full test suite
pytest --cov=services --cov-report=term-missing

# Integration tests
pytest -m integration

# System health check
./preventia-cli status
```

---

## 🎯 **SUCCESS CRITERIA & ROLLBACK PLAN**

### **Phase 1 Success Criteria**
- [ ] Template engine: 6 modules, each <300 lines
- [ ] API routers: Feature-organized, backward compatible
- [ ] Test coverage: Maintained at 85%+
- [ ] Performance: No degradation in scraper generation
- [ ] Functionality: Zero regression in existing features

### **Rollback Plan**
If any success criteria fails:
1. **Revert to backup branch**
2. **Restore original files from backup**
3. **Document lessons learned**
4. **Adjust strategy before retry**

### **Emergency Commands**
```bash
# Quick rollback
git checkout deployment
git branch -D refactor/template-engine-decomposition

# Restore from backup
cp services/scraper/automation/template_engine_backup.py services/scraper/automation/template_engine.py

# Verify system health
./preventia-cli status
pytest --tb=short
```

---

## 📊 **PROGRESS TRACKING**

### **Template Engine Decomposition**
- [ ] Step 1: Preparation & Backup
- [ ] Step 2: Create Directory Structure
- [ ] Step 3: Extract Base Abstract Class
- [ ] Step 4: Extract CMS Detection Logic
- [ ] Step 5: Create Specialized Generators
- [ ] Step 6: Create Template Manager
- [ ] Step 7: Extract Jinja2 Templates
- [ ] Step 8: Update Imports
- [ ] Step 9: Testing Strategy

### **Router Decomposition**
- [ ] Analyze Current Endpoints
- [ ] Extract Shared Logic
- [ ] Create Feature Modules
- [ ] Maintain Router Assembly
- [ ] Update Dependencies
- [ ] Comprehensive Testing

**Next Claude Code Session Should:**
1. Read this plan thoroughly
2. Execute Step 1-3 of Template Engine Decomposition
3. Update progress in CLAUDE.md
4. Document any architectural decisions made
