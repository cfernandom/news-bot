import hashlib
import json
import os
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlparse

from openai import OpenAI
from sqlalchemy import select

from services.copywriter.article_selector.src.main import choose_articles_for_structure
from services.copywriter.structure_builder.src.main import propose_structure
from services.copywriter.summary_generator.src.main import generate_summary_structured
from services.data.database.connection import db_manager
from services.data.database.models import Article as ArticleModel
from services.data.database.models import NewsSource
from services.decision_engine.src.main import decide_publications
from services.nlp.src.main import analyze_articles
from services.orchestrator.src.utils import markdown_to_html
from services.publisher.src.main import publish_newsletter_post
from services.scraper.fulltext.src.fulltext_scraper import scrape_full_text
from services.scraper.src.main import scrape_articles
from services.shared.models.article import Article
from services.shared.utils.dates import filter_articles_by_date_range


async def save_articles_to_database(articles: list[Article]) -> int:
    """
    Save scraped articles to the database
    Returns the number of articles successfully saved
    """
    if not articles:
        return 0

    saved_count = 0
    await db_manager.initialize()

    async with db_manager.get_session() as session:
        # Get all existing news sources for URL matching
        sources_result = await session.execute(select(NewsSource))
        sources = {source.base_url: source for source in sources_result.scalars().all()}

        for article in articles:
            try:
                # Extract domain from article URL to find matching source
                parsed_url = urlparse(article.url)
                domain = parsed_url.netloc.lower()

                # Find matching source by domain
                matching_source = None
                for base_url, source in sources.items():
                    if domain in base_url.lower() or base_url.lower() in domain:
                        matching_source = source
                        break

                if not matching_source:
                    # Create a new source for this domain
                    new_source = NewsSource(
                        name=domain.replace("www.", "")
                        .replace(".com", "")
                        .replace(".org", "")
                        .replace(".net", "")
                        .title(),
                        base_url=f"https://{domain}/",
                        language="en",
                        country="US",
                        is_active=True,
                        validation_status="pending",
                    )
                    session.add(new_source)
                    await session.flush()  # Get the ID
                    matching_source = new_source
                    sources[f"https://{domain}/"] = new_source
                    print(f"✅ Created new source for {domain}: {new_source.name}")

                # Check if article already exists
                existing_article = await session.execute(
                    select(ArticleModel).where(ArticleModel.url == article.url)
                )
                if existing_article.scalar_one_or_none():
                    print(f"📰 Article already exists: {article.title}")
                    continue

                # Generate content hash
                content_hash = hashlib.sha256(
                    (article.title + article.url + (article.content or "")).encode(
                        "utf-8"
                    )
                ).hexdigest()

                # Fix timezone issue - ensure timezone-naive datetime for database
                published_at = article.published_at
                if published_at and published_at.tzinfo:
                    published_at = published_at.replace(tzinfo=None)

                # Create new article
                db_article = ArticleModel(
                    source_id=matching_source.id,
                    title=article.title,
                    url=article.url,
                    content=article.content or "",
                    summary=article.summary or "",
                    published_at=published_at,
                    content_hash=content_hash,
                    word_count=len(article.content.split()) if article.content else 0,
                    processing_status="pending",
                )

                session.add(db_article)
                saved_count += 1
                print(f"💾 Saved article: {article.title[:50]}...")

            except Exception as e:
                print(f"❌ Error saving article {article.title}: {e}")
                continue

        # Commit all changes
        await session.commit()

    return saved_count


async def run_pipeline():
    print("🔍 Scrapeando artículos...")
    articles = await scrape_articles()

    if not articles:
        print("⚠️ No se encontraron artículos para procesar.")
        return

    print(f"📰 {len(articles)} artículos encontrados")

    # Save articles to database
    print("💾 Guardando artículos en base de datos...")
    saved_count = await save_articles_to_database(articles)
    print(f"✅ {saved_count} artículos guardados en la base de datos")
    for article in articles:
        # Fix crash when published_at is None
        published_str = (
            article.published_at.strftime("%Y-%m-%d")
            if article.published_at
            else "Sin fecha"
        )
        print(
            f"- {article.title[:20]} ({published_str}) - Resumen: {article.summary[:30]} - URL: {article.url}"
        )

    # Filtro: últimos 7 días
    today_utc = datetime.now(timezone.utc)
    last_week = today_utc - timedelta(days=7)
    recent_articles = filter_articles_by_date_range(
        articles, start_date=last_week, end_date=today_utc
    )

    print(
        f"📚 {len(recent_articles)} artículos encontrados en los últimos 7 días. Procesando NLP..."
    )
    analyzed_articles = analyze_articles(recent_articles)

    print("🧠 Evaluando publicaciones...")
    decisions = decide_publications(analyzed_articles)
    to_publish = [d for d in decisions if d.should_publish]

    if not to_publish:
        print("⚠️ No se encontraron artículos relevantes para publicar.")
        return

    # Preparamos lista de diccionarios con campos básicos para proponer estructura
    print(
        f"📑 {len(to_publish)} artículos marcados para publicar. Generando estructura con LLM..."
    )
    candidates = []
    for d in to_publish:
        candidates.append(
            {
                "title": d.article.title,
                "summary": d.article.summary,
                "url": d.article.url,
                "date": d.article.published_at.strftime("%Y-%m-%d"),
            }
        )

    # 1) Proponer estructura
    structure_template = propose_structure(candidates)
    structure_dict = structure_template.model_dump()

    print("✏️ Estructura propuesta:")
    for sec in structure_dict["structure"]:
        print(f"- {sec['section_title']} ({sec['description']})")

    # 2) Seleccionar artículos definitivos según la estructura
    print("📋 Seleccionando artículos finales para cada sección...")
    selection_result = choose_articles_for_structure(structure_dict, candidates)
    final_articles = selection_result.final_articles

    # Verificación de coincidencia exacta de 'section'
    secciones_definidas = {sec["section_title"] for sec in structure_dict["structure"]}
    for art in final_articles:
        if art.section not in secciones_definidas:
            print(
                f'[NEWSLETTER][WARNING] El artículo "{art.title}" tiene section "{art.section}" '
                f"pero no coincide con ningún section_title: {secciones_definidas}"
            )

    # 3) Para cada artículo seleccionado: extraer fulltext y generar resumen estructurado
    print("🔄 Generando resúmenes detallados para cada artículo seleccionado...")
    articles_for_json = []
    from services.copywriter.summary_generator.src.models import (
        ArticleSummaryStructured,
    )

    for art in final_articles:
        url = art.url
        title = art.title
        section = art.section

        full_text = await scrape_full_text(url)
        if full_text:
            summary_struct = generate_summary_structured(full_text, section)
            if summary_struct is None:
                summary_struct = ArticleSummaryStructured(
                    key_points=[
                        f'No se pudo generar resumen detallado para "{title}".'
                    ],
                    pull_quote="",
                    narrative_summary=f"Resumen breve original: {title}",
                    implications="",
                    resources=[],
                )
        else:
            summary_struct = ArticleSummaryStructured(
                key_points=[f'No se pudo obtener el texto completo para "{title}".'],
                pull_quote="",
                narrative_summary=f"Resumen breve original: {title}",
                implications="",
                resources=[],
            )
            print(f"⚠️ No se pudo obtener el texto completo para: {title} (URL: {url})")

        raw = summary_struct.model_dump()
        if raw.get("resources"):
            for recurso in raw["resources"]:
                recurso["url"] = str(recurso["url"])

        articles_for_json.append(
            {"title": title, "url": url, "section": section, "summary_struct": raw}
        )

    # 4) Llamada final al LLM para generar el boletín completo en Markdown
    print("🤖 Construyendo prompt para generar newsletter completo...")
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "../../copywriter/src/prompts/generate_newsletter_prompt.txt",
    )

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    structure_json_str = json.dumps(structure_dict, ensure_ascii=False)
    articles_json_str = json.dumps(articles_for_json, ensure_ascii=False)

    print("[NEWSLETTER] → Generando prompt completo para el boletín")
    print(
        "STRUCTURE_JSON:",
        structure_json_str[:200] + ("..." if len(structure_json_str) > 200 else ""),
    )
    print(
        "ARTICLES_JSON:",
        articles_json_str[:200] + ("..." if len(articles_json_str) > 200 else ""),
    )

    prompt = prompt_template.replace("{structure_json}", structure_json_str).replace(
        "{articles_json}", articles_json_str
    )

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un redactor médico experto en oncología.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=6000,
        )
        newsletter_md = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Error] En llamada a OpenAI: {e}")
        return

    # 5) Convertir Markdown a HTML y publicar
    print("🔄 Convirtiendo Markdown a HTML...")
    print(newsletter_md)
    if newsletter_md.startswith("```markdown"):
        newsletter_md = (
            newsletter_md.replace("```markdown", "").replace("```", "").strip()
        )
    elif newsletter_md.startswith("```"):
        newsletter_md = newsletter_md.replace("```", "").strip()
    html_body = markdown_to_html(newsletter_md)

    post_title = (
        f"Boletín semanal de cáncer de seno — {date.today().strftime('%Y-%m-%d')}"
    )
    print(f"🚀 Publicando newsletter '{post_title}' en Plataforma...")
    result = publish_newsletter_post(title=post_title, content=html_body)

    status = (
        "✅ Publicado con éxito" if result.published else f"❌ Falló: {result.message}"
    )
    print(f"📢 Resultado: {status}")
