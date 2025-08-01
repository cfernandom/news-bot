from datetime import datetime, timezone
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from services.scraper.src.utils import get_html_with_playwright
from services.shared.models.article import Article


async def scraper__news_medical() -> list[Article]:
    URL = "https://www.news-medical.net/condition/Breast-Cancer"
    BASE_URL = "https://www.news-medical.net"
    html = await get_html_with_playwright(URL)
    if not html:
        print(f"Failed to retrieve content from {URL}")
        return None
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    for article in soup.find_all("div", class_="row"):
        if not article.find("h3") or "paging" in article.get("class", []):
            continue

        # Extraer título
        title_tag = article.find("h3").find("a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        href = title_tag["href"]
        full_url = urljoin(BASE_URL, href)

        # Extraer resumen
        summary_tag = article.find("p", class_="hidden-xs item-desc")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""

        # Extraer fecha
        date_row = article.find_next_sibling("div", class_="row")
        date = None
        if date_row:
            date_span = date_row.find("span", class_="article-meta-date")
            if date_span:
                date_str = date_span.get_text(strip=True)
                try:
                    date = datetime.strptime(date_str, "%d %b %Y")
                except ValueError:
                    try:
                        # Intentar otro formato por si acaso
                        date = datetime.strptime(date_str, "%d %B %Y")
                    except ValueError:
                        print(
                            f"⚠️ Formato de fecha no reconocido: {date_str} en artículo: {title}"
                        )
                        continue

        articles.append(
            Article(
                title=title,
                url=full_url,
                summary=summary,
                published_at=date.replace(tzinfo=timezone.utc),
                content="",
            )
        )
    return articles
