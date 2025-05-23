from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from typing import Optional

async def scraper__www_nature_com_breast_cancer() -> list[Article]:
    URL = "https://www.nature.com/subjects/breast-cancer"
    BASE_URL = "https://www.nature.com"
    html = await get_html_with_playwright(URL)
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    article_items = soup.find_all("li", class_="app-article-list-row__item")

    for item in article_items:
        try:
            article_tag = item.find("article")
            if not article_tag:
                continue

            # Título y URL
            title_tag = article_tag.find("h3", class_="c-card__title").find("a")
            title = title_tag.get_text(strip=True)
            href = title_tag["href"]
            full_url = urljoin(BASE_URL, href)

            # Resumen 
            summary_tag = article_tag.find("div", {"data-test": "article-description"})
            summary = summary_tag.get_text(strip=True) if summary_tag else ""

            # Fecha
            date_tag = article_tag.find("time", itemprop="datePublished")
            date: Optional[datetime] = None
            if date_tag and date_tag.has_attr("datetime"):
                try:
                    date = datetime.strptime(date_tag["datetime"], "%Y-%m-%d")
                    date = date.replace(tzinfo=timezone.utc)
                except ValueError:
                    print("Fecha no parseable:", date_tag["datetime"])

            article = Article(
                title=title,
                url=full_url,
                summary=summary,
                published_at=date,
                content=""
            )

            articles.append(article)

        except Exception as e:
            print("Error procesando un artículo:", e)

    return articles
