from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from typing import Optional

async def scraper__www_breast_cancer_org() -> list[Article]:
    URL = "https://www.breastcancer.org/research-news"
    BASE_URL = "https://www.breastcancer.org"
    html = await get_html_with_playwright(URL)
    if not html:
        print(f"Failed to retrieve content from {URL}")
        return None
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if (
            href.startswith("/research-news/")
            and "topic/" not in href.lower()
        ):
            title = a_tag.get_text(strip=True)
            full_url = urljoin(BASE_URL, href)

            # resumen
            parent = a_tag.find_parent("div")
            p = parent.find_next("p") if parent else None
            summary = p.get_text(strip=True) if p else ""

            # fecha
            date: Optional[datetime] = None
            info_div = parent.find_next(
                "div",
                class_="Info_dateAndAuthorWrapper__M8I4F"
            ) if parent else None

            if info_div:
                raw = info_div.get_text(" ", strip=True)
                date_str = raw.split("|", 1)[0].strip()
                try:
                    date = datetime.strptime(date_str, "%b %d, %Y")
                except ValueError:
                    # imprime raw para ver qué formato real está llegando
                    print(f"Fecha no parseable en {full_url}:", raw)
                    date = None
                    continue

            articles.append(Article(
                title=title,
                url=full_url,
                summary=summary,
                published_at=date.replace(tzinfo=timezone.utc),
                content=""
            ))

    return articles
