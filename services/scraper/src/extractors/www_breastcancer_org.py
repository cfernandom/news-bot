from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from typing import Optional

async def scraper__www_breast_cancer_org() -> list[Article]:
    URL = "https://www.breastcancer.org/research-news"
    BASE_URL = "https://www.breastcancer.org"
    html = await get_html_with_playwright(URL)
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    # Buscamos todos los enlaces relevantes dentro del cuerpo
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        text = a_tag.get_text(strip=True)
        # Heurística: buscamos enlaces internos relacionados con noticias
        if (
            href.startswith("/research-news/")
            and "topic/" not in href.lower()
        ):
            title = text
            full_url = urljoin(BASE_URL, href)
            # extraer párrafo y resumen después del link
            parent = a_tag.find_parent("div")
            p = parent.find_next("p") if parent else None
            summary = p.get_text(strip=True) if p else ""
            # extraer la fecha desde el div con data-sentry-component="Info"
            date: Optional[datetime] = None
            info_div = parent.find_next("div", attrs={"data-sentry-component": "Info"}) if parent else None
            if info_div:
                # El contenido de info_div suele ser: "Dec 19, 2024 | <autor>"
                raw = info_div.get_text(" ", strip=True)
                date_str = raw.split("|", 1)[0].strip()
                try:
                    date = datetime.strptime(date_str, "%b %d, %Y")
                except ValueError:
                    date = None
            articles.append(Article(
                title=title,
                url=full_url,
                summary=summary,
                date=date,
                content=""
            ))
    return articles