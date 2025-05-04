from services.copywriter.src.prompt_builder import build_news_prompt
from services.copywriter.src.llm_client import generate_newsletter_text
from services.decision_engine.src.models import DecisionResult

def generate_copy(decisions: list[DecisionResult]) -> str:
    filtered = [d for d in decisions if d.should_publish]
    if not filtered:
        return "No hay contenido aprobado para generar copy."
    
    prompt = build_news_prompt(filtered)
    return generate_newsletter_text(prompt)
