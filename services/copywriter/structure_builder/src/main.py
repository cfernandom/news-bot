import json
import os
from typing import Dict, List

from openai import OpenAI
from pydantic import BaseModel, ValidationError


class Section(BaseModel):
    section_title: str
    description: str


class StructureTemplate(BaseModel):
    structure: List[Section]


def load_prompt_template() -> str:
    path = os.path.join(
        os.path.dirname(__file__), "prompts", "propose_structure_prompt.txt"
    )
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def propose_structure(articles: List[Dict]) -> StructureTemplate:
    prompt_base = load_prompt_template()

    # Insertar JSON de artículos en el prompt
    articles_json = json.dumps(articles, ensure_ascii=False)
    prompt = prompt_base.replace("{articles_json}", articles_json)

    # Llamada a la API de OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print(f"[STRUCTURE] → Proponiendo estructura con {len(articles)} candidatos:")
    print(articles_json[:200] + ("..." if len(articles_json) > 200 else ""))

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente para diseñar estructuras de newsletter.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=800,
    )

    text = response.choices[0].message.content.strip()
    print("[STRUCTURE] ← Respuesta LLM (texto bruto):")
    print(text[:500] + ("..." if len(text) > 500 else ""))

    try:
        structure = StructureTemplate.model_validate_json(text)
        print("[STRUCTURE] ✅ Estructura validada")
        return structure
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"[STRUCTURE][ERROR] JSON inválido o esquema incorrecto: {e}")
        print("LLM devolvió el siguiente texto:")
        print(text)
        raise RuntimeError(
            f"Error validando respuesta de propose_structure: {e}\nRespuesta LLM: {text}"
        )
