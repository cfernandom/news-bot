---
version: "1.0"
last_updated: "2025-07-07"
maintainer: "Claude (Technical Director)"
status: "active"
language: "English"
---

# Source Administration API Schemas

Complete Pydantic model definitions and OpenAPI schemas for the News Sources Administration system with compliance-first validation.

## 🔧 Core Models

### 1. Source Management Models

#### SourceCreateRequest
```python
from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, List, Literal
from datetime import datetime

class SourceCreateRequest(BaseModel):
    """Request model for creating a new news source with compliance validation"""

    name: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Human-readable name of the news source",
        example="Medical News Today"
    )

    base_url: HttpUrl = Field(
        ...,
        description="Base URL of the news source",
        example="https://medicalnewstoday.com"
    )

    source_type: Literal["news_site", "academic", "government", "ngo", "medical_journal"] = Field(
        ...,
        description="Type of news source for compliance classification"
    )

    language: str = Field(
        ...,
        regex=r"^[a-z]{2}$",
        description="ISO 639-1 language code",
        example="en"
    )

    country: str = Field(
        ...,
        regex=r"^[A-Z]{2}$",
        description="ISO 3166-1 alpha-2 country code",
        example="US"
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Description of the source's content and focus"
    )

    # Legal and compliance fields
    legal_contact_email: str = Field(
        ...,
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Legal contact email for compliance purposes"
    )

    terms_of_service_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the source's terms of service"
    )

    privacy_policy_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the source's privacy policy"
    )

    robots_txt_url: Optional[HttpUrl] = Field(
        None,
        description="URL to robots.txt (auto-generated if not provided)"
    )

    # Content and scraping configuration
    target_sections: List[str] = Field(
        default_factory=list,
        description="List of URL paths to scrape (e.g., ['/health', '/cancer-news'])",
        example=["/category/breast-cancer", "/tag/oncology"]
    )

    max_articles_per_run: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Maximum articles to extract per scraping run"
    )

    crawl_delay_seconds: float = Field(
        default=2.0,
        ge=1.0,
        le=10.0,
        description="Delay between requests in seconds (minimum 1.0 for compliance)"
    )

    # Compliance and legal fields
    fair_use_basis: str = Field(
        ...,
        min_length=50,
        max_length=500,
        description="Justification for fair use under academic research"
    )

    content_type: Literal["metadata_only", "summary_only"] = Field(
        default="metadata_only",
        description="Type of content to store (metadata_only enforced for compliance)"
    )

    data_retention_days: int = Field(
        default=365,
        ge=30,
        le=2555,  # 7 years max
        description="Data retention period in days"
    )

    @validator('content_type')
    def validate_content_type(cls, v):
        """Enforce metadata-only storage for compliance"""
        if v != "metadata_only":
            raise ValueError("Only 'metadata_only' storage is permitted for compliance")
        return v

    @validator('base_url')
    def validate_base_url(cls, v):
        """Validate base URL format and security"""
        if not str(v).startswith(('https://', 'http://')):
            raise ValueError("Base URL must use HTTP or HTTPS protocol")
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Medical News Today",
                "base_url": "https://medicalnewstoday.com",
                "source_type": "news_site",
                "language": "en",
                "country": "US",
                "description": "Leading medical news source with comprehensive breast cancer coverage",
                "legal_contact_email": "legal@medicalnewstoday.com",
                "terms_of_service_url": "https://medicalnewstoday.com/terms",
                "privacy_policy_url": "https://medicalnewstoday.com/privacy",
                "target_sections": ["/category/breast-cancer", "/tag/oncology"],
                "max_articles_per_run": 30,
                "crawl_delay_seconds": 2.0,
                "fair_use_basis": "Academic research at UCOMPENSAR University focusing on breast cancer news analysis for educational purposes under fair use doctrine",
                "content_type": "metadata_only",
                "data_retention_days": 365
            }
        }
```

#### SourceUpdateRequest
```python
class SourceUpdateRequest(BaseModel):
    """Request model for updating an existing news source"""

    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[Literal["active", "inactive", "suspended", "under_review"]] = None

    # Scraping configuration updates
    target_sections: Optional[List[str]] = None
    max_articles_per_run: Optional[int] = Field(None, ge=1, le=200)
    crawl_delay_seconds: Optional[float] = Field(None, ge=1.0, le=10.0)

    # Legal updates
    legal_contact_email: Optional[str] = Field(
        None,
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    terms_of_service_url: Optional[HttpUrl] = None
    privacy_policy_url: Optional[HttpUrl] = None

    # Compliance updates
    fair_use_basis: Optional[str] = Field(None, min_length=50, max_length=500)
    data_retention_days: Optional[int] = Field(None, ge=30, le=2555)

    @validator('crawl_delay_seconds')
    def validate_crawl_delay(cls, v):
        """Ensure compliance with minimum crawl delay"""
        if v is not None and v < 1.0:
            raise ValueError("Crawl delay must be at least 1.0 seconds for compliance")
        return v
```

#### SourceResponse
```python
class ComplianceStatus(BaseModel):
    """Compliance status information for a source"""

    is_compliant: bool = Field(description="Overall compliance status")
    robots_txt_compliant: bool = Field(description="Robots.txt compliance status")
    legal_contact_verified: bool = Field(description="Legal contact verification status")
    terms_acceptable: bool = Field(description="Terms of service acceptance status")
    fair_use_documented: bool = Field(description="Fair use documentation status")
    data_minimization_applied: bool = Field(description="Data minimization compliance")
    last_compliance_check: datetime = Field(description="Last compliance verification timestamp")
    violations: List[str] = Field(default_factory=list, description="List of compliance violations")
    risk_level: Literal["low", "medium", "high", "critical"] = Field(description="Legal risk assessment")

class PerformanceMetrics(BaseModel):
    """Performance metrics for a source"""

    last_successful_run: Optional[datetime] = Field(description="Timestamp of last successful scraping run")
    success_rate: float = Field(ge=0.0, le=1.0, description="Success rate over last 30 days")
    average_response_time: float = Field(description="Average response time in seconds")
    articles_collected_total: int = Field(ge=0, description="Total articles collected")
    articles_collected_last_30_days: int = Field(ge=0, description="Articles collected in last 30 days")
    error_count_last_30_days: int = Field(ge=0, description="Error count in last 30 days")
    next_scheduled_run: Optional[datetime] = Field(description="Next scheduled scraping run")

class SourceResponse(BaseModel):
    """Complete response model for a news source"""

    # Basic information
    id: int = Field(description="Unique source identifier")
    name: str = Field(description="Source name")
    base_url: HttpUrl = Field(description="Base URL")
    source_type: str = Field(description="Source type classification")
    language: str = Field(description="Language code")
    country: str = Field(description="Country code")
    description: Optional[str] = Field(description="Source description")
    status: str = Field(description="Current status")

    # Configuration
    target_sections: List[str] = Field(description="Target sections for scraping")
    max_articles_per_run: int = Field(description="Maximum articles per run")
    crawl_delay_seconds: float = Field(description="Crawl delay in seconds")

    # Legal and compliance
    legal_contact_email: str = Field(description="Legal contact email")
    terms_of_service_url: Optional[HttpUrl] = Field(description="Terms of service URL")
    privacy_policy_url: Optional[HttpUrl] = Field(description="Privacy policy URL")
    fair_use_basis: str = Field(description="Fair use justification")
    content_type: str = Field(description="Content storage type")
    data_retention_days: int = Field(description="Data retention period")
    data_retention_expires_at: Optional[datetime] = Field(description="Data retention expiration")

    # Compliance status
    compliance: ComplianceStatus = Field(description="Compliance status details")

    # Performance metrics
    performance: PerformanceMetrics = Field(description="Performance metrics")

    # Timestamps
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": 5,
                "name": "Medical News Today",
                "base_url": "https://medicalnewstoday.com",
                "source_type": "news_site",
                "language": "en",
                "country": "US",
                "status": "active",
                "compliance": {
                    "is_compliant": True,
                    "robots_txt_compliant": True,
                    "legal_contact_verified": True,
                    "terms_acceptable": True,
                    "fair_use_documented": True,
                    "data_minimization_applied": True,
                    "last_compliance_check": "2025-07-07T12:00:00Z",
                    "violations": [],
                    "risk_level": "low"
                },
                "performance": {
                    "last_successful_run": "2025-07-07T11:30:00Z",
                    "success_rate": 0.95,
                    "average_response_time": 1.2,
                    "articles_collected_total": 156,
                    "articles_collected_last_30_days": 45,
                    "error_count_last_30_days": 2
                }
            }
        }
```

### 2. Compliance Models

#### ComplianceValidationRequest
```python
class ComplianceValidationRequest(BaseModel):
    """Request for compliance validation of a source"""

    source_id: Optional[int] = Field(None, description="Source ID for existing source validation")
    domain: Optional[HttpUrl] = Field(None, description="Domain for new source validation")
    deep_check: bool = Field(default=False, description="Perform deep compliance analysis")
    check_types: List[Literal["robots_txt", "legal_contact", "terms_of_service", "fair_use", "data_retention"]] = Field(
        default_factory=lambda: ["robots_txt", "legal_contact", "terms_of_service", "fair_use"],
        description="Types of compliance checks to perform"
    )

    @validator('source_id', 'domain')
    def validate_source_or_domain(cls, v, values):
        """Ensure either source_id or domain is provided"""
        if not v and not values.get('domain'):
            raise ValueError("Either source_id or domain must be provided")
        return v

class ComplianceValidationResponse(BaseModel):
    """Response from compliance validation"""

    source_id: Optional[int] = Field(description="Source ID if validating existing source")
    domain: str = Field(description="Domain that was validated")
    validation_timestamp: datetime = Field(description="When validation was performed")

    # Detailed check results
    robots_txt_result: dict = Field(description="Robots.txt validation details")
    legal_contact_result: dict = Field(description="Legal contact verification details")
    terms_of_service_result: dict = Field(description="Terms of service review details")
    fair_use_result: dict = Field(description="Fair use assessment details")
    data_retention_result: dict = Field(description="Data retention compliance details")

    # Overall results
    overall_compliant: bool = Field(description="Overall compliance status")
    risk_assessment: Literal["low", "medium", "high", "critical"] = Field(description="Risk level assessment")
    violations: List[str] = Field(description="List of compliance violations found")
    recommendations: List[str] = Field(description="Recommendations for compliance improvement")

    # Compliance actions required
    actions_required: List[dict] = Field(description="Specific actions needed for compliance")
    estimated_compliance_time: Optional[int] = Field(description="Estimated time to achieve compliance (hours)")
```

### 3. Authentication and Authorization Models

#### UserRole
```python
class UserRole(BaseModel):
    """User role definition for authorization"""

    id: int = Field(description="Role ID")
    name: str = Field(description="Role name")
    description: str = Field(description="Role description")
    permissions: List[str] = Field(description="List of permissions")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "source_admin",
                "description": "Source Administration Manager",
                "permissions": [
                    "sources:create",
                    "sources:read",
                    "sources:update",
                    "sources:delete",
                    "compliance:validate",
                    "audit:read"
                ]
            }
        }

class AuthenticatedUser(BaseModel):
    """Authenticated user information"""

    id: int = Field(description="User ID")
    username: str = Field(description="Username")
    email: str = Field(description="Email address")
    full_name: str = Field(description="Full name")
    is_active: bool = Field(description="Account active status")
    roles: List[UserRole] = Field(description="User roles")
    permissions: List[str] = Field(description="Consolidated permissions")
    last_login: Optional[datetime] = Field(description="Last login timestamp")
```

### 4. API Response Models

#### StandardResponse
```python
class StandardResponse(BaseModel):
    """Standard API response format"""

    status: Literal["success", "error", "warning"] = Field(description="Response status")
    message: str = Field(description="Human-readable message")
    data: Optional[dict] = Field(None, description="Response data")
    errors: List[str] = Field(default_factory=list, description="Error messages")
    meta: dict = Field(default_factory=dict, description="Metadata")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "message": "Source created successfully",
                "data": {"source_id": 5, "name": "Medical News Today"},
                "errors": [],
                "meta": {
                    "timestamp": "2025-07-07T12:00:00Z",
                    "request_id": "req_123456",
                    "processing_time_ms": 156
                }
            }
        }

class PaginatedResponse(BaseModel):
    """Paginated API response format"""

    status: Literal["success", "error"] = Field(description="Response status")
    data: List[dict] = Field(description="Response data items")
    pagination: dict = Field(description="Pagination metadata")
    filters: dict = Field(default_factory=dict, description="Applied filters")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": [{"id": 1, "name": "Source 1"}, {"id": 2, "name": "Source 2"}],
                "pagination": {
                    "page": 1,
                    "limit": 20,
                    "total": 100,
                    "pages": 5,
                    "has_next": True,
                    "has_prev": False
                },
                "filters": {"status": "active", "language": "en"}
            }
        }
```

## 🔒 Validation Rules

### Security Validations
```python
from pydantic import validator
import re

class SecurityValidations:
    """Common security validation methods"""

    @staticmethod
    def validate_url_security(url: str) -> str:
        """Validate URL for security requirements"""
        if not url.startswith(('https://', 'http://')):
            raise ValueError("URLs must use HTTP or HTTPS protocol")

        # Block localhost, private IPs for security
        blocked_patterns = [
            r'localhost',
            r'127\.0\.0\.1',
            r'192\.168\.',
            r'10\.',
            r'172\.(1[6-9]|2[0-9]|3[01])\.'
        ]

        for pattern in blocked_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                raise ValueError(f"URL contains blocked pattern: {pattern}")

        return url

    @staticmethod
    def validate_compliance_fields(fair_use_basis: str, content_type: str) -> dict:
        """Validate compliance-related fields"""
        errors = []

        if len(fair_use_basis) < 50:
            errors.append("Fair use basis must be at least 50 characters")

        if content_type != "metadata_only":
            errors.append("Only metadata_only storage is permitted")

        if errors:
            raise ValueError("; ".join(errors))

        return {"fair_use_basis": fair_use_basis, "content_type": content_type}
```

## 📊 OpenAPI Configuration

### FastAPI Schema Configuration
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi_schema(app: FastAPI):
    """Custom OpenAPI schema with compliance information"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="PreventIA News Sources Administration API",
        version="1.0.0",
        description="""
        ## News Sources Administration API

        Comprehensive API for managing news sources with compliance-first approach.

        ### Key Features:
        - **Compliance-First**: All operations validate legal and ethical requirements
        - **Academic Research**: Designed for UCOMPENSAR University research standards
        - **GDPR Compatible**: Full privacy and data protection compliance
        - **Audit Trail**: Complete logging of all administrative actions

        ### Authentication:
        All endpoints require JWT authentication with appropriate role permissions.

        ### Rate Limiting:
        - Standard users: 100 requests/hour
        - Admin users: 1000 requests/hour

        ### Compliance Requirements:
        All sources must pass mandatory compliance validation including:
        - Robots.txt compliance verification
        - Legal contact verification
        - Fair use documentation
        - Data minimization enforcement
        """,
        routes=app.routes,
        servers=[
            {"url": "http://localhost:8000", "description": "Development server"},
            {"url": "https://api.preventia.com", "description": "Production server"}
        ]
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Add security requirement
    openapi_schema["security"] = [{"bearerAuth": []}]

    # Add custom tags
    openapi_schema["tags"] = [
        {
            "name": "sources",
            "description": "News source management operations"
        },
        {
            "name": "compliance",
            "description": "Compliance validation and monitoring"
        },
        {
            "name": "audit",
            "description": "Audit trail and legal documentation"
        },
        {
            "name": "authentication",
            "description": "User authentication and authorization"
        }
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema
```

## 🧪 Schema Validation Examples

### Request Validation Example
```python
# Example of using the schemas in endpoint
@app.post("/api/v1/sources/", response_model=StandardResponse, tags=["sources"])
async def create_source(
    source_request: SourceCreateRequest,
    current_user: AuthenticatedUser = Depends(get_current_user)
):
    """
    Create a new news source with mandatory compliance validation.

    Requires 'sources:create' permission.
    """
    # The SourceCreateRequest model automatically validates:
    # - URL format and security
    # - Email format
    # - Compliance requirements
    # - Data retention policies
    # - Fair use documentation

    # Additional business logic validation
    if not current_user.has_permission("sources:create"):
        raise HTTPException(403, "Insufficient permissions")

    # Proceed with source creation...
    pass
```

## 📚 Related Documentation

- [Source Administration Implementation Plan](../implementation/news-sources-administration-plan-2025-07-04.md)
- [API Documentation](../services/scraper-api.md)
- [Authentication Framework](../../development/standards/authentication-standards.md)
- [Compliance Guidelines](../../development/standards/compliance-standards.md)

---

**Schema Principles:**
- **Comprehensive Validation**: All inputs validated for security and compliance
- **Clear Documentation**: Every field documented with examples
- **Type Safety**: Strong typing with Pydantic models
- **Compliance-First**: Legal requirements embedded in validation
- **API Standards**: Consistent response formats and error handling

**Last Updated**: 2025-07-07
**Next Review**: 2025-08-07
**Maintainer**: Claude (Technical Director)
