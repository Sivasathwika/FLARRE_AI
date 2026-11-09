from fastapi import FastAPI
from pydantic import BaseModel
from rag import answer

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/echo")
def echo(text:str):
    return {"echo": text}

class Question(BaseModel):
    text: str

@app.post("/ask")
def ask(q: Question):
    return {"question": q.text, "answer": answer(q.text)}
