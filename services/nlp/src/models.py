from services.shared.models.article import Article
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class NLPResult:
    article: Article
    is_relevant: bool
    matched_keywords: list[str]
    score: int
    sentiment_data: Optional[Dict] = None

@dataclass
class SentimentResult:
    sentiment_label: str  # "positive", "negative", "neutral"
    confidence: float     # 0.0 to 1.0
    scores: Dict[str, float]  # VADER detailed scores
    text_length: int
    processed_text_length: int