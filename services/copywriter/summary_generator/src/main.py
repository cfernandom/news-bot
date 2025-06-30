import json
import os
from typing import Optional

from openai import OpenAI
from pydantic import ValidationError

from .models import ArticleSummaryStructured


def load_prompt_template() -> str:
    path = os.path.join(os.path.dirname(__file__), "prompts", "summarize_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_summary_structured(
    full_text: str, section: str, word_min: int = 100, word_max: int = 120
) -> Optional[ArticleSummaryStructured]:
    """
    Llama al LLM para generar un resumen estructurado en JSON de un artículo.
    Devuelve un objeto ArticleSummaryStructured, o None si falla.
    """
    prompt_base = load_prompt_template()
    safe_text = full_text[:12000]
    prompt = prompt_base.replace("{section_title}", section).replace(
        "{full_text}", safe_text
    )

    # Llamada a la API de OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print(f'[SUMMARY] → Generando resumen para artículo en sección "{section}"')
    print(
        "Texto a resumir (primeros 200 caracteres):",
        full_text[:200].replace("\n", " ") + "...",
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un redactor médico experto en oncología.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=4000,
        )

        text = response.choices[0].message.content.strip()
        print("[SUMMARY] ← Respuesta LLM (texto bruto):")
        print(text)
        # print(text[:1000] + ("..." if len(text) > 1000 else ""))

        # 🔥 Eliminar bloque de código Markdown (backticks) si existe
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        # Validación de que la respuesta es un JSON válido
        data = json.loads(text)
        summary_struct = ArticleSummaryStructured(**data)
        print(f'[SUMMARY] ✅ Resumen estructurado válido para "{section}" artículo.')
        return summary_struct

    except (json.JSONDecodeError, ValidationError) as e:
        print(
            f'[SUMMARY][ERROR] JSON inválido o esquema incorrecto para sección "{section}": {e}'
        )
        print("LLM devolvió:")
        print(text)
        return None
    except Exception as e:
        print(f"[Error] En llamada a OpenAI en generate_summary_structured: {e}")
        return None
