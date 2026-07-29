from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI()

class RiderRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def root():
    with open("index.html", "r") as f:
        return f.read()
    

@app.post("/parse-rider")
def parse_rider(req: RiderRequest):
    prompt = f"""
    Ты — парсер райдеров. Твоя задача: извлечь из текста райдера все товары, оборудование, мебель, услуги.

    Верни строго JSON массив объектов:
    [
      {{"type": "...", "name": "...", "qty": ...}},
      ...
    ]

    Где:
    - "type" — один из: "товар", "оборудование", "мебель", "услуга"
    - "name" — название предмета (как в тексте)
    - "qty" — количество (целое число)

    Текст райдера:
    {req.text}

    Верни только JSON, без пояснений.
    """

    response = requests.post(
        "https://api.deepinfra.com/v1/openai/chat/completions",
        json={
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": "Ты эксперт по райдерам и структурированию данных."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
    )

    data = response.json()

    return {
        "status": "ok",
        "items": data["choices"][0]["message"]["content"]
    }
