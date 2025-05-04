from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    title: str
    published_at: datetime
    summary: str
    content: str
    url: str
