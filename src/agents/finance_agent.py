import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from src.tools.market_data import get_stock_price
from src.tools.calculator import calculator
from src.tools.rag import analyze_document

def initialize_agent():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    tools = [get_stock_price, calculator, analyze_document]

    # --- STRICTER PROMPT ---
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a decisive Financial Analyst Agent. "
                "You have access to market data, a calculator, and internal documents.\n\n"
                
                "### CRITICAL RULES (FOLLOW THESE OR FAIL) ###\n"
                "1. **NO MATH CHECKS**: If a tool returns a number (e.g., 'down $1.22'), **BELIEVE IT**. Do NOT use the calculator to verify it.\n"
                "2. **NO REPEATING**: Do not call 'analyze_document' twice for the same query. Search once, get the text, and use it.\n"
                "3. **CALCULATOR USAGE**: Only use the calculator if the user explicitly asks for a calculation (e.g., 'What is 50% of the price?') or if the data is missing.\n"
                "4. **FINISH FAST**: Once you have the Stock Price and the Document info, stop searching and answer the user immediately.\n\n"
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        max_iterations=5,           # Hard limit to stop infinite loops
        handle_parsing_errors=True  # recover if the LLM makes a typo
    )