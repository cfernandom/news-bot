from requests.auth import HTTPBasicAuth
from services.publisher.src.config import WP_POSTS_ENDPOINT, WP_USER, WP_PASSWORD
from typing import Any
import base64
import requests

class WordPressClient:
    def __init__(self, timeout: int = 10):
        self.endpoint = WP_POSTS_ENDPOINT
        self.auth_token = self.encode_basic_auth(WP_USER, WP_PASSWORD)
        self.headers = {
            "Authorization": f"Basic {self.auth_token}",
            "Content-Type": "application/json"
        }
        self.timeout = timeout

    def create_post(self, title: str, content: str, status: str = "publish") -> dict[str, Any]:
        """
        Crea un post en WordPress vía REST API.
        - title: título del post
        - content: contenido HTML/texto del post
        - status: 'publish' publica inmediatamente
        """
        payload = {
            "title": title,
            "content": content,
            "status": status
        }
        resp = requests.post(
            self.endpoint,
            json=payload,
            headers=self.headers,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def encode_basic_auth(self, user: str, password: str) -> str:
        """
        Codifica el par usuario:contraseña en Base64 para el header Authorization.
        """
        auth_string = f"{user}:{password}"
        auth_token = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        return auth_token
