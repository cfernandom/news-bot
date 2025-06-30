from services.scraper.src.extractors.www_breastcancer_org import (
    scraper__www_breast_cancer_org,
)
from services.scraper.src.extractors.www_breastcancernews_features import (
    scraper__webmd_breast_cancer,
)
from services.scraper.src.extractors.www_breastcancernow_org import (
    scraper__breast_cancer_now_org,
)
from services.scraper.src.extractors.www_curetoday_com_tumor_breast import (
    scraper__www_curetoday_com_tumor_breast,
)
from services.scraper.src.extractors.www_medicalxpress_breast_cancer import (
    scraper__medicalxpress_com_breast_cancer,
)
from services.scraper.src.extractors.www_nature_com_breast_cancer import (
    scraper__www_nature_com_breast_cancer,
)
from services.scraper.src.extractors.www_scraper__news_medical import (
    scraper__news_medical,
)
from services.scraper.src.extractors.www_scraper_sciencedaily import (
    scraper__sciencedaily,
)
from services.shared.models.article import Article


async def scrape_articles() -> list[Article]:
    articles = []

    # Lista de llamadas a funciones scraper
    scrapers = [
        scraper__www_breast_cancer_org,
        scraper__breast_cancer_now_org,
        scraper__webmd_breast_cancer,
        scraper__news_medical,
        scraper__sciencedaily,
        scraper__www_nature_com_breast_cancer,
        scraper__medicalxpress_com_breast_cancer,
        scraper__www_curetoday_com_tumor_breast,
    ]

    # Ejecutar cada scraper y asegurarse de que no es None
    for scraper_func in scrapers:
        result = await scraper_func()
        if result:
            articles.extend(result)

    return articles
