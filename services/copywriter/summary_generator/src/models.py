from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ResourceLink(BaseModel):
    label: str
    url: HttpUrl

class ArticleSummaryStructured(BaseModel):
    key_points: List[str]
    pull_quote: str
    narrative_summary: str
    implications: str
    resources: Optional[List[ResourceLink]] = []