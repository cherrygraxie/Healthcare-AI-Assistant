from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llm_service import ask_llm

app = FastAPI()

# CORS FIX (THIS IS THE KEY PART)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Healthcare AI Assistant API"}

@app.get("/ask")
def ask(question: str):
    response = ask_llm(question)
    return {
        "question": question,
        "answer": response
    }