import requests

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from pubmed_search import get_pubmed_context, search_pubmed


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory="./healthcare_db",
    embedding_function=embeddings
)

retriever = db.as_retriever(
    search_kwargs={"k": 50}
)


def get_local_research_context(query):
    docs = retriever.invoke(query)

    local_context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    local_papers = []

    for doc in docs:
        source = doc.metadata.get("source", "Unknown source")

        if source not in local_papers:
            local_papers.append(source)

    return local_context, local_papers[:5]


def research_chat(query):
    local_context, local_papers = get_local_research_context(query)

    pubmed_context = get_pubmed_context(query, max_results=5)
    pubmed_papers = search_pubmed(query, max_results=5)

    context = f"""
LOCAL RESEARCH PAPERS:

{local_context}


PUBMED PAPERS:

{pubmed_context}
"""

    prompt = f"""
You are an expert healthcare research assistant.

Use both local research papers and PubMed paper details.

Provide the answer in this format:

1. Main Findings
2. Important Insights
3. Recent Developments
4. Future Directions
5. Clinical Relevance

Do not invent references. Use only the provided context.

Context:
{context}

Research Query:
{query}

Answer:
"""

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "keep_alive": "30m"
        }
    )

    if response.status_code != 200:
        return {
            "summary": f"Ollama Error: {response.text}",
            "local_papers": local_papers,
            "pubmed_papers": pubmed_papers
        }

    data = response.json()

    if "response" not in data:
        return {
            "summary": f"Ollama Error: {data}",
            "local_papers": local_papers,
            "pubmed_papers": pubmed_papers
        }

    return {
        "summary": data["response"],
        "local_papers": local_papers,
        "pubmed_papers": pubmed_papers
    }


if __name__ == "__main__":
    query = input("Enter your query: ")

    result = research_chat(query)

    print("\nResearch Summary:\n")
    print(result["summary"])

    print("\nRecommended Local Papers:\n")
    for i, paper in enumerate(result["local_papers"], start=1):
        print(f"{i}. {paper}")

    print("\nPubMed Papers:\n")
    for i, paper in enumerate(result["pubmed_papers"], start=1):
        print(f"{i}. {paper['title']}")
        print(f"PMID: {paper['pmid']}")
        print(f"Journal: {paper['journal']}")
        print(f"Date: {paper['pub_date']}")
        print("-" * 50)