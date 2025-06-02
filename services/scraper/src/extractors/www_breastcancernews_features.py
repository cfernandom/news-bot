from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from typing import Optional
import re
from datetime import datetime
from zoneinfo import ZoneInfo

async def scraper__webmd_breast_cancer() -> list[Article]:
    URL = "https://www.webmd.com/breast-cancer/news-features"
    BASE_URL = "https://www.webmd.com"
    html = await get_html_with_playwright(URL)
    if not html:
        print(f"Failed to retrieve content from {URL}")
        return None
    soup = BeautifulSoup(html, "html.parser")
    articles = []

    # Recorremos los <li> dentro de la lista de artículos
    for li in soup.select("ul.list > li"):
        a_tag = li.find("a", href=True, attrs={"data-id": True})
        if not a_tag:
            continue

        href = a_tag["href"]
        full_url = urljoin(BASE_URL, href)

        title_span = a_tag.find("span", class_="title")
        title = title_span.get_text(strip=True) if title_span else ""

        desc_p = a_tag.find("p", class_="desc")
        summary = ""
        date_str = ""

        if desc_p:
            date_span = desc_p.find("span", class_="tag")
            if date_span:
                raw_date = date_span.get_text(strip=True)
                
                date_match = re.search(r'([A-Za-z]+\s+\d+,\s+\d{4})', raw_date)
                if date_match:
                    date_str = date_match.group(1).strip()
                else:
                    date_match = re.search(r'([A-Za-z]+\s+\d+\s+\d{4})', raw_date)
                    if date_match:
                        date_str = date_match.group(1).strip()
                
                
                date_span.extract()
                summary = desc_p.get_text(strip=True)

        date = None
        if date_str:
            try:
                date = datetime.strptime(date_str, "%B %d, %Y")
            except ValueError:
                try:
                    date = datetime.strptime(date_str, "%b %d, %Y")
                except ValueError:
                    try:
                        date = datetime.strptime(date_str, "%B %d %Y")
                    except ValueError:
                        try:
                            date = datetime.strptime(date_str, "%b %d %Y")
                        except Exception as e:
                            print(f"❌ Error al parsear fecha '{date_str}': {e}")
                            try:
                                date_parts = re.match(r'([A-Za-z]+)\s+(\d+),?\s+(\d{4})', date_str)
                                if date_parts:
                                    month, day, year = date_parts.groups()
                                    # Convertir el mes a número
                                    months = {
                                        'January': 1, 'February': 2, 'March': 3, 'April': 4, 
                                        'May': 5, 'June': 6, 'July': 7, 'August': 8, 
                                        'September': 9, 'October': 10, 'November': 11, 'December': 12,
                                        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                                        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                                    }
                                    month_num = months.get(month, 1)
                                    date = datetime(int(year), month_num, int(day))
                            except Exception as e2:
                                print(f"❌ Error en segundo intento de parseo: {e2}")

        if not date:
            print(f"⚠️ {BASE_URL} Saltando noticia por falta de fecha: {title}")
            continue
            
        # Asegurarse de que la fecha tenga zona horaria (UTC por defecto)
        if date and date.tzinfo is None:
            date = date.replace(tzinfo=ZoneInfo("UTC"))
            
        article = Article(
            title=title,
            url=full_url,
            summary=summary,
            published_at=date,
            content=""
        )

        setattr(article, "article_url", full_url)
        articles.append(article)

    return articles