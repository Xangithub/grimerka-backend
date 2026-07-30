from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class RiderRequest(BaseModel):
    text: str

@app.post("/parse-rider")
def parse_rider(req: RiderRequest):
    prompt = f"""
    Ты — парсер райдеров. Извлеки все предметы, оборудование, мебель и услуги.
    Верни строго JSON массив объектов:
    [
      {{"type": "...", "name": "...", "qty": ...}},
      ...
    ]
    Текст райдера:
    {req.text}
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://grimerka.up.railway.app",
            "X-Title": "Grimerka Rider Parser"
        },
        json={
            "model": "openai/gpt-4o-mini",   # дешевле и быстрее, чем gpt-4o
            "messages": [
                {"role": "system", "content": "Ты эксперт по райдерам."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
    )

    data = response.json()

    # Если OpenRouter вернул ошибку
    if "choices" not in data:
        return {
            "error": "OpenRouter did not return choices",
            "raw": data
        }

    content = data["choices"][0]["message"]["content"]

    # Парсим JSON
    try:
        parsed = json.loads(content)
    except Exception as e:
        return {
            "error": "JSON parsing failed",
            "exception": str(e),
            "raw": content
        }

    # Если модель вернула {"items": [...]}
    if isinstance(parsed, dict) and "items" in parsed:
        items = parsed["items"]
    else:
        items = parsed

    return {
        "status": "ok",
        "items": items
    }
