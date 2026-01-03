import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. CONFIGURATION
DATA_PATH = "/app/data"
DB_PATH = "/app/data/vector_db"  # We store the DB inside the data folder so it persists

def ingest_documents():
    """
    Reads all PDFs in the data folder, splits them, and stores them in ChromaDB.
    """
    # Initialize the Embedding Model (Runs locally, free)
    print("Loading embedding model (this may take a minute)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Check for PDFs
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data directory '{DATA_PATH}' not found.")
        return

    pdf_files = [f for f in os.listdir(DATA_PATH) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDFs found in /data. Please add a PDF file.")
        return

    documents = []
    for pdf_file in pdf_files:
        file_path = os.path.join(DATA_PATH, pdf_file)
        print(f"Processing file: {pdf_file}...")
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())

    # 2. CHUNKING 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} chunks.")

    # 3. STORING (Vector Database)
    print("Saving to Vector Database (ChromaDB)...")
    # This actually writes the folder structure to disk
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    print(f"Success! Vector DB created at {DB_PATH}")

if __name__ == "__main__":
    ingest_documents()