import re
from services.shared.models.article import Article
from services.nlp.src.models import NLPResult
from services.nlp.src.keywords import KEYWORDS
from services.nlp.src.sentiment import get_sentiment_analyzer


def analyze_article(article: Article) -> NLPResult:
    """Enhanced article analysis with sentiment analysis"""
    text = f"{article.title} {article.summary}".lower()
    matched = [kw for kw in KEYWORDS if re.search(rf"\b{re.escape(kw)}\b", text)]
    score = len(matched)
    
    # Add sentiment analysis
    sentiment_analyzer = get_sentiment_analyzer()
    sentiment_data = sentiment_analyzer.analyze_sentiment(
        text=article.summary or "",
        title=article.title or ""
    )

    return NLPResult(
        article=article,
        is_relevant=score >= 2,  # regla simple: al menos 2 palabras clave
        matched_keywords=matched,
        score=score,
        sentiment_data=sentiment_data
    )