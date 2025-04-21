from dataclasses import dataclass
from services.nlp.src.models import NLPResult

@dataclass
class DecisionResult:
    article_url: str
    should_publish: bool
    reason: str
    score: int
    matched_keywords: list[str]

    @classmethod
    def from_nlp(cls, nlp: NLPResult, threshold: int):
        """Construye un DecisionResult a partir del resultado NLP."""
        publish = nlp.score >= threshold
        reason = (
            f"Score {nlp.score} ≥ {threshold}"
            if publish
            else f"Score {nlp.score} < {threshold}"
        )
        return cls(
            article_url=nlp.article.url,
            should_publish=publish,
            reason=reason,
            score=nlp.score,
            matched_keywords=nlp.matched_keywords
        )
