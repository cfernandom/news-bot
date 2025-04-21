import re
from services.shared.models.article import Article
from services.nlp.src.models import NLPResult
from services.nlp.src.keywords import KEYWORDS


def analyze_article(article: Article) -> NLPResult:
    text = f"{article.title} {article.summary}".lower()
    matched = [kw for kw in KEYWORDS if re.search(rf"\b{re.escape(kw)}\b", text)]
    score = len(matched)

    return NLPResult(
        article=article,
        is_relevant=score >= 2,  # regla simple: al menos 2 palabras clave
        matched_keywords=matched,
        score=score
    )