import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from src.tools.market_data import get_stock_price
from src.tools.calculator import calculator
from src.tools.rag import analyze_document

def initialize_agent():
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    tools = [get_stock_price, calculator, analyze_document]

    # CLEANER: No system prompt argument here at all.
    # We just give it the Brain (LLM) and the Hands (Tools).
    agent_graph = create_react_agent(model=llm, tools=tools)
    
    return agent_graph