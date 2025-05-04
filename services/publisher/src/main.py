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

def publish_newsletter_post(title: str, content: str) -> PublishResult:
    """
    Publica una entrada de tipo newsletter en WordPress.
    """
    client = WordPressClient()

    try:
        post_data = client.create_post(title=title, content=content)
        post_id = post_data.get("id")
        link = post_data.get("link", "Desconocido")

        return PublishResult(
            article_url=link,
            published=True,
            wp_post_id=post_id,
            message="Publicado correctamente"
        )
    except Exception as e:
        return PublishResult(
            article_url="newsletter",
            published=False,
            wp_post_id=None,
            message=str(e)
        )