import os

# URL base de tu WordPress, sin slash final, e.g. "https://tudominio.com"
WP_BASE_URL = os.getenv("WP_BASE_URL", "https://tudominio.com")

# Credenciales para autenticación Basic Auth
WP_USER = os.getenv("WP_USER", "usuario_wp")
WP_PASSWORD = os.getenv("WP_PASSWORD", "clave_wp")

# Ruta completa al endpoint de posts
WP_POSTS_ENDPOINT = f"{WP_BASE_URL}/wp-json/wp/v2/posts"
WP_FEATURE_IMAGE_ID = "277"