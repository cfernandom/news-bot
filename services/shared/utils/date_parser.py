"""
Robust date parser for handling multiple date formats across news sources.
Handles common date formats found in news articles with fallback strategies.
"""

import logging
import re
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


class RobustDateParser:
    """
    Robust date parser that handles multiple date formats with fallback strategies.
    """

    # Common date formats found in news sources
    DATE_FORMATS = [
        # Full month names
        "%B %d, %Y",  # May 22, 2025
        "%B %d %Y",  # May 22 2025
        "%d %B %Y",  # 22 May 2025
        "%d %B, %Y",  # 22 May, 2025
        # Abbreviated month names
        "%b %d, %Y",  # May 22, 2025
        "%b %d %Y",  # May 22 2025
        "%b. %d, %Y",  # Apr. 30, 2025 (with period)
        "%b. %d %Y",  # Apr. 30 2025
        "%d %b %Y",  # 22 May 2025
        "%d %b, %Y",  # 22 May, 2025
        # Numeric formats
        "%Y-%m-%d",  # 2025-05-22
        "%m/%d/%Y",  # 05/22/2025
        "%d/%m/%Y",  # 22/05/2025
        "%m-%d-%Y",  # 05-22-2025
        "%d-%m-%Y",  # 22-05-2025
        # ISO formats
        "%Y-%m-%dT%H:%M:%S",  # 2025-05-22T10:30:00
        "%Y-%m-%dT%H:%M:%SZ",  # 2025-05-22T10:30:00Z
        "%Y-%m-%d %H:%M:%S",  # 2025-05-22 10:30:00
    ]

    @staticmethod
    def parse_date(date_str: str) -> Optional[datetime]:
        """
        Parse date string with robust fallback strategies.

        Args:
            date_str: String containing date information

        Returns:
            datetime object with UTC timezone or None if parsing fails
        """
        if not date_str or not isinstance(date_str, str):
            return None

        # Clean the date string
        clean_date_str = RobustDateParser._clean_date_string(date_str)

        # Try direct parsing with known formats
        parsed_date = RobustDateParser._try_direct_parsing(clean_date_str)
        if parsed_date:
            return parsed_date

        # Try regex extraction and parsing
        parsed_date = RobustDateParser._try_regex_extraction(clean_date_str)
        if parsed_date:
            return parsed_date

        # Try numeric extraction as last resort
        parsed_date = RobustDateParser._try_numeric_extraction(clean_date_str)
        if parsed_date:
            return parsed_date

        logger.warning(f"Could not parse date: '{date_str}'")
        return None

    @staticmethod
    def _clean_date_string(date_str: str) -> str:
        """Clean date string removing common noise."""
        # Remove ordinal suffixes (1st, 2nd, 3rd, 4th, etc.)
        clean_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str.strip())

        # Remove extra whitespace
        clean_str = " ".join(clean_str.split())

        # Handle common timezone abbreviations
        clean_str = re.sub(r"\s+(UTC|GMT|PST|EST|CST|MST)\s*$", "", clean_str)

        return clean_str

    @staticmethod
    def _try_direct_parsing(date_str: str) -> Optional[datetime]:
        """Try parsing with predefined formats."""
        for fmt in RobustDateParser.DATE_FORMATS:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                # Ensure timezone is UTC
                if parsed_date.tzinfo is None:
                    parsed_date = parsed_date.replace(tzinfo=timezone.utc)
                logger.debug(f"Successfully parsed '{date_str}' with format '{fmt}'")
                return parsed_date
            except ValueError:
                continue
        return None

    @staticmethod
    def _try_regex_extraction(date_str: str) -> Optional[datetime]:
        """Try extracting date using regex patterns."""
        # Pattern for "Month DD, YYYY" format
        month_day_year_pattern = r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})"
        match = re.search(month_day_year_pattern, date_str, re.IGNORECASE)
        if match:
            try:
                month_name, day, year = match.groups()
                date_string = f"{month_name} {day}, {year}"
                return datetime.strptime(date_string, "%B %d, %Y").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                pass

        # Pattern for abbreviated months "MMM DD, YYYY"
        abbrev_month_pattern = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+(\d{1,2}),?\s+(\d{4})"
        match = re.search(abbrev_month_pattern, date_str, re.IGNORECASE)
        if match:
            try:
                month_abbrev, day, year = match.groups()
                date_string = f"{month_abbrev} {day}, {year}"
                return datetime.strptime(date_string, "%b %d, %Y").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                pass

        # Pattern for numeric dates "MM/DD/YYYY" or "DD/MM/YYYY"
        numeric_pattern = r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})"
        match = re.search(numeric_pattern, date_str)
        if match:
            num1, num2, year = match.groups()
            # Try MM/DD/YYYY first
            try:
                return datetime.strptime(f"{num1}/{num2}/{year}", "%m/%d/%Y").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                # Try DD/MM/YYYY as fallback
                try:
                    return datetime.strptime(
                        f"{num2}/{num1}/{year}", "%m/%d/%Y"
                    ).replace(tzinfo=timezone.utc)
                except ValueError:
                    pass

        return None

    @staticmethod
    def _try_numeric_extraction(date_str: str) -> Optional[datetime]:
        """Extract numbers and try to construct date."""
        numbers = re.findall(r"\d+", date_str)
        if len(numbers) >= 3:
            try:
                # Find the year (4 digits)
                year = None
                for num in numbers:
                    if len(num) == 4 and num.startswith("20"):
                        year = int(num)
                        break

                if not year:
                    return None

                # Get remaining numbers for month and day
                remaining = [int(n) for n in numbers if n != str(year)]

                if len(remaining) >= 2:
                    # Try different combinations
                    for month, day in [
                        (remaining[0], remaining[1]),
                        (remaining[1], remaining[0]),
                    ]:
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            try:
                                return datetime(year, month, day, tzinfo=timezone.utc)
                            except ValueError:
                                continue

            except (ValueError, IndexError):
                pass

        return None


# Convenience function for backward compatibility
def parse_date_robust(date_str: str) -> Optional[datetime]:
    """
    Parse date string with robust fallback strategies.

    Args:
        date_str: String containing date information

    Returns:
        datetime object with UTC timezone or None if parsing fails
    """
    return RobustDateParser.parse_date(date_str)


# Common date formats for testing
SUPPORTED_FORMATS = [
    "May 22, 2025",
    "Apr. 30, 2025",
    "Apr 30, 2025",
    "22 May 2025",
    "2025-05-22",
    "05/22/2025",
    "22/05/2025",
    "2025-05-22T10:30:00Z",
    "May 22 2025",
    "22 May, 2025",
]
