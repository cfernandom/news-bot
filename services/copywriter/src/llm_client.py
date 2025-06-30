import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_system_prompt() -> str:
    prompt_path = "services/copywriter/src/prompts/newsletter_prompt.txt"
    if prompt_path and os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        DEFAULT_SYSTEM_PROMPT = """
        Eres un experto redactor de newsletters en temas médicos.
        """.strip()
        return DEFAULT_SYSTEM_PROMPT


def generate_newsletter_text(prompt: str) -> str:
    system_prompt = load_system_prompt()
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def generate_title(markdown_body: str) -> str:
    prompt = f"""
    Eres un experto redactor de newsletters en temas médicos.
    Genera un título atractivo y conciso para el siguiente contenido:
    """.strip()
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": markdown_body},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    # Example usage
    prompt = "Camrelizumab Seems Promising As New Triple-Negative Breast Cancer Treatment.\nAdding the immunotherapy medicine camrelizumab to chemotherapy offered better outcomes than chemotherapy alone for TNBC."
    newsletter_text = generate_newsletter_text(prompt)
    print(newsletter_text)
