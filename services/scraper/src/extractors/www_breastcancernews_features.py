from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from typing import Optional

async def scraper__webmd_breast_cancer() -> list[Article]:
    URL = "https://www.webmd.com/breast-cancer/news-features"
    BASE_URL = "https://www.webmd.com"
    html = await get_html_with_playwright(URL)
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    ## Buscamos los elementos <li> que contienen los artículos
    for li in soup.find_all("li"):
        a_tag = li.find("a", href=True, attrs={"data-id": True})
        if not a_tag:
            continue
        
        href = a_tag["href"]
        full_url = urljoin(BASE_URL, href)
        
        title_span = a_tag.find("span", class_="title")
        title = title_span.get_text(strip=True) if title_span else ""
        # Resumen
        desc_p = a_tag.find("p", class_="desc")
        summary = ""
        date_str = ""
        
        if desc_p:
            date_span = desc_p.find("span", class_="tag")
        if date_span:
            # Extraemos el texto de la fecha
            raw_date = date_span.get_text(strip=True)
            # Removemos todo después del primer guión
            date_str = raw_date.split('—')[0].split('–')[0].strip()
            # Limpiamos espacios extras
            date_str = date_str.replace('  ', ' ').rstrip(' ,-–—')
            date_span.extract()
            
            summary = desc_p.get_text(strip=True)
        
        date = None
        if date_str:
            try:
            # formato exacto 
                date = datetime.strptime(date_str, "%B %d, %Y")
            except ValueError:
                try:
                # formato alternativo 
                    date = datetime.strptime(date_str, "%B %d, %Y").strftime("%Y-%m-%d")
                except:
                    print(f"   Formato no reconocido después de limpieza: '{date_str}'")
        
        # Si no se encuentra fecha en la noticia
        if not date:
            print(f"⚠️ Saltando noticia por falta de fecha: {title}")
            continue  # No guardar esta noticia
        
        articles.append(Article(
            title=title,
            url=full_url,
            summary=summary,
            date=date,
            content=""
        ))
    
    return articles