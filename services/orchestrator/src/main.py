from services.scraper.src.main import scrape_articles
from services.nlp.src.main import analyze_articles
from services.decision_engine.src.main import decide_publications
from services.publisher.src.main import publish_decisions

async def run_pipeline():
    print("🔍 Scrapeando artículos...")
    articles = await scrape_articles()

    print(f"📚 {len(articles)} artículos extraídos. Procesando NLP...")
    analyzed_articles = analyze_articles(articles)

    print("🧠 Evaluando publicaciones...")
    decisions = decide_publications(analyzed_articles)

    print("🚀 Publicando artículos seleccionados...")
    results = publish_decisions(decisions)

    print("📈 Resultados de publicación:")
    for r in results:
        status = "✅" if r.published else "❌"
        print(f"{status} {r.article_url} → {r.message}")
