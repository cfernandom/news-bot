from services.decision_engine.src.models import DecisionResult
from services.publisher.src.client import WordPressClient
from services.publisher.src.models import PublishResult

def build_content(decision: DecisionResult) -> str:
    """
    Genera el cuerpo del post a partir de la decisión.
    Incluye resumen, link original y palabras clave.
    """
    kws = ", ".join(decision.matched_keywords) or "Ninguna"
    content = (
        f"<p><strong>Resumen:</strong> {decision.article.summary}</p>"
        f"<p><strong>Razón:</strong> {decision.reason}</p>"
        f"<p><strong>Keywords:</strong> {kws}</p>"
        f"<p>Ver artículo original: <a href=\"{decision.article.url}\">{decision.article.url}</a></p>"
    )
    return content

def publish_decisions(decisions: list[DecisionResult]) -> list[PublishResult]:
    wp = WordPressClient()
    results: list[PublishResult] = []

    for d in decisions:
        if not d.should_publish:
            results.append(PublishResult(
                article_url=d.article.url,
                published=False,
                wp_post_id=None,
                message="No cumple umbral de publicación"
            ))
            continue
        try:
            content = build_content(d)
            post = wp.create_post(title=d.article.title, content=content)
            results.append(PublishResult(
                article_url=d.article.url,
                published=True,
                wp_post_id=post.get("id"),
                message="Publicado con éxito"
            ))
        except Exception as e:
            results.append(PublishResult(
                article_url=d.article.url,
                published=False,
                wp_post_id=None,
                message=f"Error: {str(e)}"
            ))
    return results

#! El siguiente es un ejemplo para ilustrar rápidamente el uso de la funcion publish decision
if __name__ == "__main__":
    # Ejemplo de consumo: cargar decisions desde un JSON o importarlas directamente
    # Aquí simulo dos decisiones:
    sample = [
        DecisionResult(article_url="https://ejemplo.com/a1", should_publish=True, reason="Score 3 ≥ 2", score=3, matched_keywords=["breast cancer","tumor"]),
        DecisionResult(article_url="https://ejemplo.com/a2", should_publish=False, reason="Score 1 < 2", score=1, matched_keywords=["hydratation"])
    ]

    res = publish_decisions(sample)
    for r in res:
        status = "✅" if r.published else "❌"
        print(f"{status} {r.article.url} → {r.message} (WP ID: {r.wp_post_id})")
