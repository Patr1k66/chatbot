from openai import OpenAI

from app.config import settings


def get_polza_client() -> OpenAI:
    return OpenAI(
        base_url="https://polza.ai/api/v1",
        api_key=settings.polza_api_key,
    )


def build_system_prompt(base_prompt: str, escalation_contact: str) -> str:
    rules = (
        "\n\nПравила:\n"
        "- Отвечай только на основе информации из инструкции выше.\n"
        "- Не выдумывай цены, сроки и условия, которых нет в инструкции.\n"
        "- Если не знаешь ответ — честно скажи об этом и предложи связаться с менеджером.\n"
        f"- Контакт для эскалации: {escalation_contact}.\n"
        "- Отвечай кратко, дружелюбно и по-русски."
    )
    return base_prompt.strip() + rules


def generate_reply(
    system_prompt: str,
    history: list[dict[str, str]],
    user_message: str,
) -> str:
    client = get_polza_client()
    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=settings.polza_model,
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Empty response from LLM")
    return content.strip()
