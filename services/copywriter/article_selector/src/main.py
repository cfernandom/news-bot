import json
import os
from typing import Dict, List

from openai import OpenAI
from pydantic import BaseModel, ValidationError


class FinalArticle(BaseModel):
    url: str
    title: str
    section: str
    justification: str


class ArticleSelectionResult(BaseModel):
    final_articles: List[FinalArticle]


def load_prompt_template() -> str:
    path = os.path.join(
        os.path.dirname(__file__), "prompts", "choose_articles_prompt.txt"
    )
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def choose_articles_for_structure(
    structure: Dict, articles: List[Dict]
) -> ArticleSelectionResult:
    """
    structure: dict con la clave "structure" (lista de secciones)
    articles: lista de dicts con keys: url, title, summary, date
    """
    prompt_base = load_prompt_template()
    structure_json = json.dumps(structure, ensure_ascii=False)
    articles_json = json.dumps(articles, ensure_ascii=False)
    prompt = prompt_base.replace("{structure_json}", structure_json).replace(
        "{articles_json}", articles_json
    )

    print("[SELECTOR] → Escogiendo artículos para estructura:")
    print(
        "STRUCTURE_JSON:",
        structure_json[:200] + ("..." if len(structure_json) > 200 else ""),
    )
    print(
        "CANDIDATES_JSON:",
        articles_json[:200] + ("..." if len(articles_json) > 200 else ""),
    )

    # Llamada a la API de OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente para asignar artículos a secciones de una newsletter médica.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.25,
        max_tokens=800,
    )
    text = response.choices[0].message.content.strip()
    print("[SELECTOR] ← Respuesta LLM (texto bruto):")
    print(text[:500] + ("..." if len(text) > 500 else ""))

    # Validación de que la respuesta es un JSON válido
    try:
        selection = ArticleSelectionResult.model_validate_json(text)
        print("[SELECTOR] ✅ Selección validada")
        return selection
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"[SELECTOR][ERROR] JSON inválido o esquema incorrecto: {e}")
        print("LLM devolvió el siguiente texto:")
        print(text)
        raise RuntimeError(
            f"Error validando respuesta de choose_articles_for_structure: {e}\nRespuesta LLM: {text}"
        )
