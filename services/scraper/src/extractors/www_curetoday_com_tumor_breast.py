from services.shared.models.article import Article
from services.scraper.src.utils import get_html_with_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone
from typing import Optional
import re

async def scraper__www_curetoday_com_tumor_breast() -> list[Article]:
    URL = "https://www.curetoday.com/tumor/breast"
    BASE_URL = "https://www.curetoday.com"
    html = await get_html_with_playwright(URL)
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    
    # Set para guardar URLs ya procesadas y evitar los duplicados
    processed_urls = set()

    for i, article_div in enumerate(soup.find_all("div", class_="w-full h-full")):
        try:
            
            # Buscar el título en el párrafo con clase específica
            title_p = article_div.find("p", class_="font-bold text-[1rem] pl-4 text-undefined")
            title = ""
            href = ""
            
            if title_p:
                title_a = title_p.find("a", href=True)
                if title_a:
                    title = title_a.get_text(strip=True)
                    href = title_a["href"]
                else:
                    title = title_p.get_text(strip=True)
            
            # Si no encontramos título en el párrafo, buscar en enlaces directos
            if not title:
                all_links = article_div.find_all("a", href=True)
                for link in all_links:
                    link_text = link.get_text(strip=True)
                    if link_text and len(link_text) > 10 and not link_text.lower().startswith("ryan"):
                        title = link_text
                        href = link["href"]
                        break
            
            if not title:
                print(f"No se encontró título en artículo {i}, saltando")
                continue
                
            # Si no tenemos href, buscarlo
            if not href:
                main_link = article_div.find("a", href=lambda x: x and x.startswith("/view/"))
                if main_link:
                    href = main_link["href"]
                    
            if not href:
                print(f"No se encontró URL en artículo {i}, saltando")
                continue
                
            full_url = urljoin(BASE_URL, href)
            
            # VERIFICAR DUPLICADOS: Si ya procesamos esta URL, se saltara
            if full_url in processed_urls:
                continue
            
            # Agregar URL al set de procesadas
            processed_urls.add(full_url)

            # Extraer el resumen - buscar el párrafo con el texto del artículo
            summary = ""
            summary_p = article_div.find("p", class_="mt-4 text-gray-800 pl-4")
            if summary_p:
                summary = summary_p.get_text(strip=True)
            else:
                # Buscar otros posibles contenedores de resumen
                other_p = article_div.find_all("p")
                for p in other_p:
                    text = p.get_text(strip=True)
                    if (text and len(text) > 30 and 
                        not any(word in text.lower() for word in ["font-bold", "ryan scott", "may", "author"]) and
                        "pl-4" not in str(p.get("class", []))):
                        summary = text
                        break

            # Extrae la fecha de publicación con múltiples intentos
            date = None
            
            date_span = article_div.find("span", class_="text-sm text-gray-500 pl-4")
            if date_span:
                date_str = date_span.get_text(strip=True)
                date = parse_date(date_str)
            
            if not date:
                all_spans = article_div.find_all("span")
                for span in all_spans:
                    text = span.get_text(strip=True)
                    if any(month in text for month in ["January", "February", "March", "April", "May", "June",
                                                     "July", "August", "September", "October", "November", "December"]):
                        date = parse_date(text)
                        if date:
                            break
            
            if not date:
                all_text = article_div.get_text()
                date_patterns = [
                    r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4}',
                    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}(?:st|nd|rd|th)?\s+\d{4}'
                ]
                
                for pattern in date_patterns:
                    match = re.search(pattern, all_text)
                    if match:
                        date_str = match.group(0)
                        date = parse_date(date_str)
                        if date:
                            break

            # Crear el objeto Article
            article = Article(
                title=title,
                url=full_url,
                summary=summary,
                published_at=date,
                content=""
            )

            articles.append(article)
            
        except Exception as e:
            print(f"Error procesando artículo {i}: {e}")
            import traceback
            traceback.print_exc()
            continue

    return articles


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
        
    # Limpiar la cadena de fecha
    clean_date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str.strip())
    
    # Formatos de fecha a intentar
    date_formats = [
        "%B %d %Y",          # May 13 2025
        "%B %d, %Y",         # May 13, 2025
        "%b %d %Y",          # May 13 2025
        "%b %d, %Y",         # May 13, 2025
        "%m/%d/%Y",          # 05/13/2025
        "%d/%m/%Y",          # 13/05/2025
        "%Y-%m-%d",          # 2025-05-13
        "%d-%m-%Y",          # 13-05-2025
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(clean_date_str, fmt).replace(tzinfo=timezone.utc)
            return parsed_date
        except ValueError:
            continue
    
    # Intentamos extraer solo los números si los formatos anteriores fallan
    numbers = re.findall(r'\d+', clean_date_str)
    if len(numbers) >= 3:
        try:
            # Asumir formato MM/DD/YYYY o DD/MM/YYYY
            if int(numbers[0]) > 12:  # DD/MM/YYYY
                day, month, year = int(numbers[0]), int(numbers[1]), int(numbers[2])
            else:  # MM/DD/YYYY
                month, day, year = int(numbers[0]), int(numbers[1]), int(numbers[2])
            
            if year < 100: 
                year += 2000
                
            parsed_date = datetime(year, month, day, tzinfo=timezone.utc)
            return parsed_date
        except (ValueError, IndexError):
            pass
    
    return None