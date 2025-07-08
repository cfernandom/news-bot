"""
SQLAlchemy models for PreventIA News Analytics
Hybrid approach: ORM for basic operations, raw SQL for complex analytics
"""

from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# Enums for better type safety
class ValidationStatus(str, Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    FAILED = "failed"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ANALYZED = "analyzed"  # For backwards compatibility


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TopicCategory(str, Enum):
    PREVENTION = "prevention"
    TREATMENT = "treatment"
    DIAGNOSIS = "diagnosis"
    TESTIMONIALS = "testimonials"
    RESEARCH = "research"
    OTHER = "other"
    GENERAL = "general"  # For backwards compatibility
    SURGERY = "surgery"
    CHEMOTHERAPY = "chemotherapy"
    RADIATION = "radiation"
    IMMUNOTHERAPY = "immunotherapy"
    CLINICAL_TRIALS = "clinical_trials"


class KeywordType(str, Enum):
    MEDICAL_TERM = "medical_term"
    LOCATION = "location"
    PERSON = "person"
    ORGANIZATION = "organization"
    DRUG = "drug"
    PROCEDURE = "procedure"
    OTHER = "other"


# SQLAlchemy ORM Models (for CRUD operations)
class NewsSource(Base):
    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    base_url = Column(String(500), nullable=False, unique=True)
    language = Column(String(10), nullable=False, default="es")
    country = Column(String(50), nullable=False)
    extractor_class = Column(String(255))
    is_active = Column(Boolean, default=True)
    validation_status = Column(String(50), default=ValidationStatus.PENDING)
    validation_error = Column(Text)
    last_validation_at = Column(DateTime)

    # Legal compliance fields
    robots_txt_url = Column(String(500))
    robots_txt_last_checked = Column(DateTime)
    crawl_delay_seconds = Column(Integer, default=2)
    scraping_allowed = Column(Boolean)
    terms_of_service_url = Column(String(500))
    terms_reviewed_at = Column(DateTime)
    legal_contact_email = Column(String(255))
    fair_use_basis = Column(Text)  # Fair use documentation
    compliance_score = Column(Numeric(3, 2))  # 0.00 to 1.00
    last_compliance_check = Column(DateTime)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Relationships
    articles = relationship(
        "Article", back_populates="source", cascade="all, delete-orphan"
    )
    legal_notices = relationship(
        "LegalNotice", back_populates="source", cascade="all, delete-orphan"
    )


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    title = Column(Text, nullable=False)
    url = Column(String(1000), nullable=False, unique=True)
    content = Column(Text)  # Will be phased out for compliance
    summary = Column(Text)
    published_at = Column(DateTime, nullable=False)
    scraped_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Geographic and linguistic
    language = Column(String(10))
    country = Column(String(50))

    # Sentiment analysis
    sentiment_score = Column(Numeric(4, 3))  # -1.000 to 1.000
    sentiment_label = Column(String(20))
    sentiment_confidence = Column(Numeric(3, 2))

    # Topic classification
    topic_category = Column(String(50))
    topic_confidence = Column(Numeric(3, 2))

    # Processing metadata
    processing_status = Column(String(50), default=ProcessingStatus.PENDING)
    processing_error = Column(Text)
    content_hash = Column(String(64))
    word_count = Column(Integer)

    # Legal compliance fields
    robots_txt_compliant = Column(Boolean)
    copyright_status = Column(
        String(50), default="unknown"
    )  # unknown, cleared, fair_use, violation
    fair_use_basis = Column(Text)
    scraping_permission = Column(Boolean)
    content_type = Column(String(20), default="summary")  # full, summary, metadata
    legal_review_status = Column(
        String(50), default="pending"
    )  # pending, approved, rejected, needs_review
    data_retention_expires_at = Column(DateTime)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Relationships
    source = relationship("NewsSource", back_populates="articles")
    keywords = relationship(
        "ArticleKeyword", back_populates="article", cascade="all, delete-orphan"
    )


class ArticleKeyword(Base):
    __tablename__ = "article_keywords"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    keyword = Column(String(255), nullable=False)
    relevance_score = Column(Numeric(3, 2))
    keyword_type = Column(String(50))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Relationships
    article = relationship("Article", back_populates="keywords")

    __table_args__ = (
        UniqueConstraint("article_id", "keyword", name="_article_keyword_uc"),
    )


class WeeklyAnalytics(Base):
    __tablename__ = "weekly_analytics"

    id = Column(Integer, primary_key=True)
    week_start = Column(Date, nullable=False)
    week_end = Column(Date, nullable=False)

    # Article counts
    total_articles = Column(Integer, default=0)
    articles_by_language = Column(JSON)
    articles_by_country = Column(JSON)
    articles_by_source = Column(JSON)
    articles_by_topic = Column(JSON)

    # Sentiment analysis
    sentiment_distribution = Column(JSON)
    avg_sentiment_score = Column(Numeric(4, 3))

    # Popular content
    top_keywords = Column(JSON)


class ComplianceAuditLog(Base):
    __tablename__ = "compliance_audit_log"

    id = Column(Integer, primary_key=True)
    table_name = Column(String(100), nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(
        String(50), nullable=False
    )  # create, update, delete, validate, legal_review
    old_values = Column(JSON)
    new_values = Column(JSON)
    legal_basis = Column(String(255), default="academic_research_fair_use")
    performed_by = Column(String(255), nullable=False)
    performed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)

    # Compliance-specific fields
    compliance_score_before = Column(Numeric(3, 2))
    compliance_score_after = Column(Numeric(3, 2))
    risk_level = Column(String(20))
    violations_count = Column(Integer, default=0)
    
    # Don't set created_at explicitly - it's handled by the database with DEFAULT NOW()


# Pydantic schemas (for API serialization and validation)
class NewsSourceBase(BaseModel):
    name: str
    base_url: str
    language: str = "es"
    country: str
    extractor_class: Optional[str] = None
    is_active: bool = True


class NewsSourceCreate(NewsSourceBase):
    pass


class NewsSourceUpdate(BaseModel):
    name: Optional[str] = None
    base_url: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    extractor_class: Optional[str] = None
    is_active: Optional[bool] = None


class NewsSourceResponse(NewsSourceBase):
    id: int
    validation_status: str
    validation_error: Optional[str] = None
    last_validation_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ArticleBase(BaseModel):
    title: str
    url: str
    content: Optional[str] = None
    summary: Optional[str] = None
    published_at: datetime
    language: Optional[str] = None
    country: Optional[str] = None


class ArticleCreate(ArticleBase):
    source_id: int


class ArticleUpdate(BaseModel):
    content: Optional[str] = None
    summary: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    sentiment_confidence: Optional[float] = None
    topic_category: Optional[str] = None
    topic_confidence: Optional[float] = None
    processing_status: Optional[str] = None


class ArticleResponse(ArticleBase):
    id: int
    source_id: int
    source: Optional["NewsSourceResponse"] = None  # Forward reference
    scraped_at: datetime
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    sentiment_confidence: Optional[float] = None
    topic_category: Optional[str] = None
    topic_confidence: Optional[float] = None
    processing_status: str
    processing_error: Optional[str] = None
    word_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class KeywordCreate(BaseModel):
    keyword: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    keyword_type: KeywordType = KeywordType.OTHER


class KeywordResponse(BaseModel):
    id: int
    article_id: int
    keyword: str
    relevance_score: float
    keyword_type: KeywordType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WeeklyAnalyticsResponse(BaseModel):
    id: int
    week_start: date
    week_end: date
    total_articles: int
    articles_by_language: Dict[str, Any]
    articles_by_country: Dict[str, Any]
    articles_by_source: Dict[str, Any]
    articles_by_topic: Dict[str, Any]
    sentiment_distribution: Dict[str, Any]
    avg_sentiment_score: Optional[float]
    top_keywords: List[Dict[str, Any]]
    trending_topics: List[Dict[str, Any]]
    ai_summary: Optional[str]
    key_insights: List[Dict[str, Any]]
    generated_at: datetime
    articles_processed: int

    model_config = ConfigDict(from_attributes=True)


# Analytics schemas for complex queries (used with raw SQL)
class DashboardSummary(BaseModel):
    """Summary data for dashboard overview"""

    total_articles: int
    recent_articles: int
    sentiment_distribution: Dict[str, int]
    topic_distribution: Dict[str, int]
    active_sources: int
    avg_sentiment_score: float
    analysis_period_days: int


class TrendAnalysis(BaseModel):
    """Trend analysis data"""

    period: str  # "daily", "weekly", "monthly"
    data_points: List[Dict[str, Any]]
    trending_up: List[str]
    trending_down: List[str]


class GeographicDistribution(BaseModel):
    """Geographic distribution for map visualization"""

    countries: List[
        Dict[str, Any]
    ]  # [{"country": "Mexico", "count": 25, "sentiment": 0.3}]
    total_countries: int
    most_active_country: str


# Generic pagination response model
T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""

    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class LegalNotice(Base):
    __tablename__ = "legal_notices"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    notice_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    effective_date = Column(Date, nullable=False)
    expiration_date = Column(Date)
    status = Column(String(20), default="active")
    legal_contact = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    # Relationships
    source = relationship("NewsSource", back_populates="legal_notices")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(JSON, default=list)
    is_system_role = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime)
    password_changed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))


class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    assigned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
    assigned_by = Column(Integer, ForeignKey("users.id"))
    expires_at = Column(DateTime)

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="_user_role_uc"),)
