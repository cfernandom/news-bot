from services.scraper.src.extractors.www_breastcancer_org import scraper__www_breast_cancer_org
from services.nlp.src.models import Article, NLPResult
from services.nlp.src.analyzer import analyze_article
from services.decision_engine.src.engine import decide

async def main():
    # flujo: scraper → nlp → decisión
    articles = await scraper__www_breast_cancer_org()
    # Paso NLP
    nlp_results = [analyze_article(a) for a in articles]

    # Paso Decision Engine
    decisions = decide(nlp_results)

    # Salida de decisiones
    for d in decisions:
        action = "🟢 Publish" if d.should_publish else "🔴 Discard"
        print(f"{action}: {d.article_url}")
        print(f"  Reason: {d.reason}")
        print(f"  Matched keywords: {d.matched_keywords}\n")
