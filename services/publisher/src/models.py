from dataclasses import dataclass

@dataclass
class PublishResult:
    article_url: str
    published: bool
    wp_post_id: int | None
    message: str
