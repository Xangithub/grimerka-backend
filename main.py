from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RiderRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/parse-rider")
def parse_rider(req: RiderRequest):
    return {
        "status": "parsed",
        "items": [
            {"name": "Evian", "qty": 20},
            {"name": "Borjomi", "qty": 8}
        ]
    }
