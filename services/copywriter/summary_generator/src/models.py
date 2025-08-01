from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class ResourceLink(BaseModel):
    label: str
    url: HttpUrl


class ArticleSummaryStructured(BaseModel):
    key_points: List[str]
    pull_quote: str
    narrative_summary: str
    implications: str
    resources: Optional[List[ResourceLink]] = []
