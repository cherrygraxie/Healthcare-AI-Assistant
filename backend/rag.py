from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import requests
import os
import shutil


CHROMA_PATH = "./chroma_db"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def load_pdf(file_path):
    loader = PyMuPDFLoader(file_path)
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150
    )
    return splitter.split_documents(documents)


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vectorstore(chunks):
    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="healthcare_docs"
    )

    return vectorstore


def process_pdf(pdf_path):
    docs = load_pdf(pdf_path)

    chunks = split_documents(docs)

    create_vectorstore(chunks)

    return len(chunks)


def get_retriever():
    embeddings = get_embeddings()

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 6}
    )


def call_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        data = response.json()

        if "response" not in data:
            return f"Ollama Error: {data}"

        return data["response"]

    except Exception as e:
        return f"Ollama Connection Error: {str(e)}"


def ask_document(question, history=""):

    if not os.path.exists(CHROMA_PATH) or len(os.listdir(CHROMA_PATH)) == 0:
        return call_ollama(question)

    retriever = get_retriever()

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    print("\n========== RETRIEVED CONTEXT ==========")
    print(context)
    print("=======================================\n")

    prompt = f"""
You are HELIO, a friendly healthcare AI assistant.

Rules:
1. Answer naturally and directly.
2. Do not say phrases like "based on the previous context", "based on the provided context", or "according to the context".
3. Use conversation history only when it helps understand follow-up questions.
4. If document context is relevant, use it silently.
5. For medical report questions, answer ONLY using values found in the document context.
6. Do not invent test names, values, diagnosis, treatment, or normal/abnormal status.
7. If a test value or detail is missing from the document context, say "Not found in the report."
8. When summarizing medical reports, list actual test names and values found in the report.
9. Do not give diagnosis. Say that a qualified doctor should confirm medical interpretation.
Rules:
10. When asked to summarize a lab report, create sections:
    - Normal Results
    - Above Range
    - Below Range
    - Important Findings
11. Compare values against the provided reference range when available.
12. Do not diagnose diseases.
13. Present findings in a clear medical report format.
14. Do not classify a result as normal unless the value falls inside the reference range.
15. Carefully compare each value with its reference range before describing it.
16. If unsure, report the value and reference range without interpretation.

Conversation History:
{history}

Document Context:
{context}

User Question:
{question}

Answer:
"""

    return call_ollama(prompt)