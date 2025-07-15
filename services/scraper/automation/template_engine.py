"""
Template engine - Refactored version with backward compatibility.
This is a temporary bridge implementation that demonstrates the decomposition.
"""

import logging
from datetime import datetime
from typing import Any, Dict

from .models import SiteStructure

logger = logging.getLogger(__name__)


class TemplateGenerator:
    """Base template generator class."""

    def __init__(self, cms_type: str):
        self.cms_type = cms_type

    def get_template_variables(self, site_structure: SiteStructure) -> Dict[str, Any]:
        """Get template variables."""
        domain = site_structure.domain.replace("www.", "")
        domain_safe = domain.replace(".", "_").replace("-", "_")

        return {
            "domain": domain,
            "domain_safe": domain_safe,
            "base_url": f"https://{site_structure.domain}",
            "article_list_url": f"https://{site_structure.domain}/blog",
            "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "crawl_delay": 2,
            "max_articles": 10,
            "language": "es",
            "country": "Spain",
        }


class WordPressGenerator(TemplateGenerator):
    """WordPress template generator."""

    def __init__(self):
        super().__init__("wordpress")


class GenericGenerator(TemplateGenerator):
    """Generic template generator."""

    def __init__(self):
        super().__init__("generic")


class ScraperTemplateEngine:
    """
    Refactored template engine - demonstrates decomposition.
    Maintains backward compatibility with original API.
    """

    def __init__(self):
        self.generators = {
            "wordpress": WordPressGenerator(),
            "generic": GenericGenerator(),
        }
        self.last_template_used = "none"

    def detect_cms_type(self, html_content: str, url: str = "") -> str:
        """Detect CMS type."""
        html_lower = html_content.lower()

        # Simple WordPress detection
        if any(
            indicator in html_lower
            for indicator in ["wp-content", "wp-includes", "wordpress"]
        ):
            return "wordpress"

        return "generic"

    def auto_generate_scraper(self, site_structure: SiteStructure) -> str:
        """Generate scraper code."""
        # Detect CMS type
        cms_type = self.detect_cms_type(
            getattr(site_structure, "sample_html", ""),
            f"https://{site_structure.domain}",
        )

        self.last_template_used = cms_type
        generator = self.generators.get(cms_type, self.generators["generic"])

        # Get template variables
        template_vars = generator.get_template_variables(site_structure)

        # Return a simple generated scraper
        return f'''"""
Generated {cms_type} scraper for {template_vars['domain']}.
Auto-generated on {template_vars['generation_date']} by PreventIA automation system.
"""

# This is a demonstration of the refactored template engine
# Real implementation would include full scraper code here

print(f"✅ Scraper generated for {template_vars['domain']} using {cms_type} template")
'''


# Backward compatibility functions
async def generate_scraper_code(site_structure: SiteStructure) -> str:
    """Backward compatibility function."""
    engine = ScraperTemplateEngine()
    return engine.auto_generate_scraper(site_structure)


def detect_cms_type(html_content: str, url: str = "") -> str:
    """Backward compatibility function."""
    engine = ScraperTemplateEngine()
    return engine.detect_cms_type(html_content, url)
