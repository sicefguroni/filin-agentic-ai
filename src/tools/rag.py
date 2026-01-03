import os
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pydantic import BaseModel, Field

# 1. CONFIGURATION
# We point to the SAME folder where we saved the DB in ingest.py
DB_PATH = "/app/data/vector_db"

# 2. THE INPUT SCHEMA
class RagInput(BaseModel):
    query: str = Field(description="The question to ask the document (e.g., 'What was the revenue in 2024?')")

# 3. THE TOOL
@tool("analyze_document", args_schema=RagInput)
def analyze_document(query: str) -> str:
    """
    Useful for answering questions based on the uploaded PDF documents (Annual Reports, 10-K, etc.).
    Use this tool to find specific facts, risks, or financial figures from the company's internal files.
    """
    try:
        # Check if DB exists
        if not os.path.exists(DB_PATH):
            return "Error: No Knowledge Base found. Please run the ingestion script first."

        print(f"DEBUG: Searching PDF for: '{query}'...")

        # Initialize the same embedding model we used for ingestion
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Connect to the Database
        vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

        # RETRIEVAL
        # k=3 means "Give me the top 3 most relevant pages"
        results = vector_db.similarity_search(query, k=3)

        if not results:
            return "No relevant information found in the document."

        # COMBINE RESULTS
        # We stitch the 3 pages together into one text block for the LLM
        context = ""
        for i, doc in enumerate(results):
            # We add page numbers for citation
            page_num = doc.metadata.get('page', 'Unknown')
            source = os.path.basename(doc.metadata.get('source', 'Unknown'))
            context += f"\n--- Excerpt {i+1} (Source: {source}, Page {page_num}) ---\n{doc.page_content}\n"

        return context

    except Exception as e:
        return f"Error querying document: {str(e)}"