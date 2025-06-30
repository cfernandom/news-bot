import json
import os
from datetime import date, datetime, timedelta, timezone

from openai import OpenAI

from services.copywriter.article_selector.src.main import choose_articles_for_structure
from services.copywriter.structure_builder.src.main import propose_structure
from services.copywriter.summary_generator.src.main import generate_summary_structured
from services.decision_engine.src.main import decide_publications
from services.nlp.src.main import analyze_articles
from services.orchestrator.src.utils import markdown_to_html
from services.publisher.src.main import publish_newsletter_post
from services.scraper.fulltext.src.fulltext_scraper import scrape_full_text
from services.scraper.src.main import scrape_articles
from services.shared.utils.dates import filter_articles_by_date_range


async def run_pipeline():
    print("🔍 Scrapeando artículos...")
    articles = await scrape_articles()

    if not articles:
        print("⚠️ No se encontraron artículos para procesar.")
        return

    print(f"📰 {len(articles)} artículos encontrados")
    for article in articles:
        print(
            f"- {article.title[:20]} ({article.published_at.strftime('%Y-%m-%d')}) - Resumen: {article.summary[:30]} - URL: {article.url}"
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
