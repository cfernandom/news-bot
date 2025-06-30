from services.decision_engine.src.models import DecisionResult


def build_news_prompt(decisions: list[DecisionResult]) -> str:
    prompt = ""
    for i, d in enumerate(decisions, 1):
        if not d.should_publish:
            continue
        prompt += (
            f"{i}. Título: {d.article.title}\n"
            f"   Resumen: {d.article.summary}\n"
            f"   Fecha de publicación: {d.article.published_at.strftime('%Y-%m-%d')}\n"
            f"   Fuente: {d.article.url}\n\n"
        )
    return prompt.strip()
