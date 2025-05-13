from datetime import datetime
from typing import List
from services.shared.models.article import Article

def filter_articles_by_date_range(
    articles: List[Article],
    start_date: datetime,
    end_date: datetime
) -> List[Article]:
    filtered = []
    for article in articles:
        pub_date = article.published_at
        if pub_date is not None and pub_date.tzinfo is not None:
            if start_date <= pub_date <= end_date:
                filtered.append(article)
        else:
            print(f"⚠️ Ignorando artículo sin zona horaria o sin fecha: {article.url}")
    return filtered