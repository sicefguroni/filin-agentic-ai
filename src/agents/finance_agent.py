import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from src.tools.market_data import get_stock_price
from src.tools.calculator import calculator

def initialize_agent():
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    tools = [get_stock_price, calculator]

    # --- THE FIX: IMPROVED SYSTEM PROMPT ---
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert Financial Analyst Agent. "
                "Your goal is to provide accurate stock market data and perform precise calculations.\n\n"
                
                "CRITICAL INSTRUCTIONS:\n"
                "1. **Fetch First**: Always use 'get_stock_price' to get the real data before doing ANY math.\n"
                "2. **Extract Numbers**: Never pass text labels like 'previous price' to the calculator. You must pass EXACT NUMBERS (e.g., '150.00 / 145.20').\n"
                "3. **Read Carefully**: If the stock tool output already tells you the percentage change (e.g., 'up 2%'), just report that. Do not recalculate it unless asked.\n"
                "4. **Formatting**: Format all monetary values with $ and 2 decimal places.\n\n"
                
                "Example of Correct Logic:\n"
                "User: 'Is AAPL up?'\n"
                "Step 1: Call get_stock_price('AAPL') -> Returns 'Price is 150, Open was 145'\n"
                "Step 2: Calculate '150 - 145' using the calculator.\n"
                "Step 3: Answer 'It is up by $5.'"
            ),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)