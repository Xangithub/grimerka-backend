from fastapi import FastAPI, UploadFile, File
import requests
import os
import json

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_openrouter(prompt: str):
    """Отправляет запрос в OpenRouter через openrouter/free."""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://grimerka.up.railway.app",
            "X-OpenRouter-Title": "Grimerka Rider Parser"
        },
        json={
            "model": "openrouter/free",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Ты парсер райдеров. "
                        "Верни строго JSON. "
                        "Если данные не структурированы — структурируй."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
    )

    return response.json()


@app.post("/parse-text")
async def parse_text(text: str):
    """Парсинг текста райдера."""
    result = call_openrouter(text)
    return result


@app.post("/parse-file")
async def parse_file(file: UploadFile = File(...)):
    """Парсинг PDF/текста из файла."""
    content = await file.read()

    try:
        text = content.decode("utf-8")
    except:
        text = content.decode("latin-1")

    result = call_openrouter(text)
    return result


@app.get("/")
def root():
    return {"status": "ok", "message": "Grimerka backend running"}
