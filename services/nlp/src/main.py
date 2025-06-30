from services.nlp.src.analyzer import analyze_article
from services.nlp.src.models import NLPResult
from services.shared.models.article import Article


def analyze_articles(articles: list[Article]) -> list[NLPResult]:
    nlp_results = [analyze_article(a) for a in articles]
    return nlp_results
