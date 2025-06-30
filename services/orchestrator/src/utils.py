import markdown as md


def markdown_to_html(markdown_text: str) -> str:
    """
    Convierte un string en Markdown a HTML válido.
    """
    return md.markdown(markdown_text, extensions=["extra", "sane_lists"])
