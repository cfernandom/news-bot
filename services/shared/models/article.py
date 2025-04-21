from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    title: str
    date: datetime
    summary: str
    content: str
    url: str
