# backend/llm_service.py

import requests

def ask_llm(question: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": question,
            "stream": False
        }
    )

    data = response.json()
    return data["response"]
