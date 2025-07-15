from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from services.scraper.src.utils import get_html_with_playwright
from services.shared.logging.structured_logger import get_logger
from services.shared.models.article import Article
from services.shared.utils.date_parser import parse_date_robust

logger = get_logger("scraper.sciencedaily")


async def scraper__sciencedaily() -> list[Article]:
    URL = "https://www.sciencedaily.com/news/health_medicine/breast_cancer/"
    BASE_URL = "https://www.sciencedaily.com"
    html = await get_html_with_playwright(URL)
    if not html:
        print(f"Failed to retrieve content from {URL}")
        return None
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    # Buscar todos los contenedores de artículos
    for article_div in soup.find_all("div", class_="col-md-6"):
        title_tag = article_div.find("div", class_="latest-head").find("a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        href = title_tag["href"]
        full_url = urljoin(BASE_URL, href)

        # Extraer resumen y fecha
        summary_div = article_div.find("div", class_="latest-summary")
        summary = ""
        date_str = ""

        if summary_div:
            # Extraer fecha
            date_span = summary_div.find("span", class_="story-date")
            if date_span:
                raw_date = date_span.get_text(strip=True)
                date_str = raw_date.replace("—", "").strip()
                date_span.extract()

            # Extraer resumen
            summary = summary_div.get_text(strip=True)

        # Parsear fecha con el parser robusto
        date = parse_date_robust(date_str) if date_str else None
        if date_str and not date:
            logger.date_parse_failed(date_str, full_url, "sciencedaily.com")
            # Continue processing instead of skipping article
            logger.info(
                "Processing article without date", title=title[:50], url=full_url
            )

        article_obj = Article(
            title=title, url=full_url, summary=summary, published_at=date, content=""
        )
        setattr(article_obj, "article_url", full_url)

        articles.append(article_obj)

    return articles
