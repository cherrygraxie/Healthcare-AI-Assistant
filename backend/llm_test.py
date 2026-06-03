from fastapi import FastAPI
from llm_service import ask_llm

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Healthcare AI Assistant"}

@app.get("/ask")
def ask(question: str):
    response = ask_llm(question)

    return {
        "question": question,
        "answer": response
    }