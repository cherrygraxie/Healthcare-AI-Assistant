from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from research_search import research_chat
import shutil
import os

from rag import process_pdf, ask_document
from agents.agent_graph import build_agent_graph

app = FastAPI()

chat_history = []
agent_graph = build_agent_graph()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Healthcare AI Assistant API Running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks_count = process_pdf(file_path)

    return {
        "message": "PDF processed successfully",
        "chunks": chunks_count
    }


@app.get("/document-chat")
def document_chat(question: str):

    global chat_history

    history_text = "\n".join(chat_history)

    print("Current History:")
    print(chat_history)

    answer = ask_document(question, history_text)

    chat_history.append(
        f"User: {question}"
    )

    chat_history.append(
        f"Assistant: {answer}"
    )

    return {
        "question": question,
        "answer": answer
    }

@app.get("/clear-chat")
def clear_chat():

    global chat_history

    chat_history.clear()

    return {
        "message": "Chat history cleared"
    }

@app.get("/research-chat")
def research_endpoint(query: str):

    result = research_chat(query)

    return {
        "query": query,
        "summary": result["summary"],
        "local_papers": result["local_papers"],
        "pubmed_papers": result["pubmed_papers"]
    }

@app.get("/agent-chat")
def agent_chat(question: str):

    result = agent_graph.invoke({
        "question": question,
        "route": "",
        "research_result": "",
        "drug_result": "",
        "report_result": "",
        "health_result": "",
        "health_data": {},
        "summary": "",
        "verification": "",
        "final_answer": ""
    })

    return {
        "question": question,
        "answer": result["final_answer"],
        "health_data": result.get("health_data", {})
    }