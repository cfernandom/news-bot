"""
Shared utilities for sources functionality.
Common functions, models, and utilities used across source modules.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import Depends
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from services.data.database.connection import DatabaseManager
from services.data.database.models import (
    ComplianceAuditLog,
    NewsSource,
    ValidationStatus,
)


# Pydantic models for request/response
class SourceCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    base_url: HttpUrl = Field(..., description="Base URL of the news source")
    language: str = Field(default="es", pattern="^[a-z]{2}$")
    country: str = Field(..., min_length=2, max_length=50)
    extractor_class: Optional[str] = Field(None, max_length=255)

    # Legal compliance fields (mandatory)
    robots_txt_url: Optional[HttpUrl] = Field(
        None, description="URL to robots.txt file"
    )
    terms_of_service_url: Optional[HttpUrl] = Field(
        None, description="URL to terms of service"
    )
    legal_contact_email: Optional[str] = Field(None, pattern=r"^[^@]+@[^@]+\.[^@]+$")
    crawl_delay_seconds: int = Field(default=2, ge=1, le=30)

    # Fair use documentation
    fair_use_basis: Optional[str] = Field(None, description="Legal basis for fair use")


class SourceUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    base_url: Optional[HttpUrl] = Field(None)
    language: Optional[str] = Field(None, pattern="^[a-z]{2}$")
    country: Optional[str] = Field(None, min_length=2, max_length=50)
    extractor_class: Optional[str] = Field(None, max_length=255)
    robots_txt_url: Optional[HttpUrl] = Field(None)
    terms_of_service_url: Optional[HttpUrl] = Field(None)
    legal_contact_email: Optional[str] = Field(None, pattern=r"^[^@]+@[^@]+\.[^@]+$")
    crawl_delay_seconds: Optional[int] = Field(None, ge=1, le=30)
    fair_use_basis: Optional[str] = Field(None)


class SourceResponse(BaseModel):
    id: int
    name: str
    base_url: str
    language: str
    country: str
    extractor_class: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    validation_status: ValidationStatus
    robots_txt_url: Optional[str]
    terms_of_service_url: Optional[str]
    legal_contact_email: Optional[str]
    crawl_delay_seconds: int
    fair_use_basis: Optional[str]

    class Config:
        from_attributes = True


class ComplianceValidationResult(BaseModel):
    is_compliant: bool
    robots_txt_compliant: bool
    legal_contact_verified: bool
    terms_acceptable: bool
    fair_use_documented: bool
    data_minimization_applied: bool
    violations: List[str] = []
    crawl_delay: Optional[float] = None


class LegalReviewRequest(BaseModel):
    reviewer_id: str = Field(..., min_length=1, max_length=100)
    review_notes: str = Field(..., min_length=1, max_length=2000)
    legal_approval: bool = Field(...)
    compliance_recommendations: Optional[str] = Field(None, max_length=1000)


# Database dependency
async def get_db_session():
    """Get database session."""
    db_manager = DatabaseManager()
    await db_manager.initialize()
    async with db_manager.get_session() as session:
        yield session


async def validate_source_compliance(
    source_data: SourceCreateRequest,
) -> ComplianceValidationResult:
    """
    Validate source compliance with legal and ethical requirements.

    Args:
        source_data: Source data to validate

    Returns:
        Compliance validation result
    """
    violations = []

    # Check robots.txt compliance
    robots_txt_compliant = True
    if not source_data.robots_txt_url:
        violations.append("robots_txt_url is required for compliance")
        robots_txt_compliant = False
    else:
        try:
            from services.scraper.src.compliance.robots_checker import (
                check_robots_compliance,
            )

            compliance_result = await check_robots_compliance(str(source_data.base_url))
            if not compliance_result["allowed"]:
                violations.append(
                    f"Robots.txt disallows crawling: {compliance_result.get('reason', 'Unknown')}"
                )
                robots_txt_compliant = False
        except Exception as e:
            violations.append(f"Unable to verify robots.txt: {str(e)}")
            robots_txt_compliant = False

    # Check legal contact
    legal_contact_verified = bool(source_data.legal_contact_email)
    if not legal_contact_verified:
        violations.append("Legal contact email is required")

    # Check terms of service
    terms_acceptable = bool(source_data.terms_of_service_url)
    if not terms_acceptable:
        violations.append("Terms of service URL is required")

    # Check fair use documentation
    fair_use_documented = bool(source_data.fair_use_basis)
    if not fair_use_documented:
        violations.append("Fair use basis documentation is required")

    # Data minimization check
    data_minimization_applied = source_data.crawl_delay_seconds >= 2
    if not data_minimization_applied:
        violations.append(
            "Crawl delay must be at least 2 seconds for data minimization"
        )

    # Overall compliance
    is_compliant = (
        robots_txt_compliant
        and legal_contact_verified
        and terms_acceptable
        and fair_use_documented
        and data_minimization_applied
    )

    return ComplianceValidationResult(
        is_compliant=is_compliant,
        robots_txt_compliant=robots_txt_compliant,
        legal_contact_verified=legal_contact_verified,
        terms_acceptable=terms_acceptable,
        fair_use_documented=fair_use_documented,
        data_minimization_applied=data_minimization_applied,
        violations=violations,
        crawl_delay=float(source_data.crawl_delay_seconds),
    )


async def log_compliance_action(
    session: AsyncSession,
    source_id: int,
    action: str,
    details: Dict[str, Any],
    reviewer_id: Optional[str] = None,
) -> None:
    """
    Log compliance-related actions for audit trail.

    Args:
        session: Database session
        source_id: Source ID
        action: Action performed
        details: Action details
        reviewer_id: Optional reviewer ID
    """
    audit_log = ComplianceAuditLog(
        source_id=source_id,
        action=action,
        details=details,
        reviewer_id=reviewer_id,
        timestamp=datetime.now(timezone.utc),
    )

    session.add(audit_log)
    await session.commit()
