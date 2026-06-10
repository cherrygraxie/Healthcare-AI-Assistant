# Imports
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Load all PDFs
def load_all_pdfs(folder_path):

    documents = []

    for filename in os.listdir(folder_path):

        if filename.endswith(".pdf"):

            pdf_path = os.path.join(folder_path, filename)

            loader = PyPDFLoader(pdf_path)

            docs = loader.load()

            documents.extend(docs)

    return documents


# Split into chunks
def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    return chunks


# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create vector database
def create_healthcare_db(chunks):

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./healthcare_db"
    )

    return db


# Main program
if __name__ == "__main__":

    docs = load_all_pdfs(
        "./knowledge_base/research_papers"
    )

    print("Documents loaded:", len(docs))

    chunks = split_documents(docs)

    print("Chunks created:", len(chunks))

    db = create_healthcare_db(chunks)

    print("Healthcare database created successfully!")