from services.shared.models.article import Article
from dataclasses import dataclass

@dataclass
class NLPResult:
    article: Article
    is_relevant: bool
    matched_keywords: list[str]
    score: int