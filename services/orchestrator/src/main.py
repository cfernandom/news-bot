from services.scraper.src.main import scrape_articles
from services.nlp.src.main import analyze_articles
from services.decision_engine.src.main import decide_publications
from services.publisher.src.main import publish_newsletter_post
from services.copywriter.src.main import generate_copy
from services.orchestrator.src.utils import markdown_to_html
from services.copywriter.src.llm_client import generate_title 

async def run_pipeline():
    print("🔍 Scrapeando artículos...")
    articles = await scrape_articles()

    print(f"📚 {len(articles)} artículos extraídos. Procesando NLP...")
    analyzed_articles = analyze_articles(articles)

    print("🧠 Evaluando publicaciones...")
    decisions = decide_publications(analyzed_articles)

    filtered = [d for d in decisions if d.should_publish]
    if not filtered:
        print("⚠️ No se encontraron artículos relevantes para publicar.")
        return
    
    print("✍️ Generando newsletter con LLM...")
    markdown_body = generate_copy(filtered)
    title = generate_title(markdown_body)
    print(f"Publicación '{title}' generada.") 

    print("🔄 Convirtiendo Markdown a HTML...")
    html_body = markdown_to_html(markdown_body)

    print("🚀 Publicando newsletter en Plataforma...")
    result = publish_newsletter_post(
        title=title,
        content=html_body
    )

    status = "✅ Publicado con éxito" if result.published else f"❌ Falló: {result.message}"
    print(f"📢 Resultado: {status}")
