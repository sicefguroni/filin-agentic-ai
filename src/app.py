import streamlit as st
import sys
import os
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.agents.finance_agent import initialize_agent

SYSTEM_PROMPT = (
    "You are a decisive Financial Analyst Agent. "
    "### CRITICAL RULES ###\n"
    "1. If a tool returns a number, BELIEVE IT. No math checks.\n"
    "2. Do not call 'analyze_document' twice for the same query.\n"
    "3. Only use the calculator if explicitly asked.\n"
    "4. FINISH FAST: Answer immediately once you have data."
)

st.title("💰 Autonomous Finance Agent")

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    
    agent = initialize_agent()
    messages = [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=prompt)]

    # --- INDUSTRY STANDARD: REAL-TIME STREAMING ---
    with st.chat_message("ai"):
        # Create a placeholder to stream the answer chunks
        response_placeholder = st.empty()
        thought_process = st.expander("Show Thought Process", expanded=True)
        
        final_answer = ""
        
        # We use stream() to get events as they happen
        # recursion_limit=5 prevents infinite loops!
        stream = agent.stream(
            {"messages": messages}, 
            config={"recursion_limit": 5}
        )
        
        for event in stream:
            # Check if this event comes from the Model (Agent)
            if "agent" in event:
                message = event["agent"]["messages"][0]
                
                # If it's a tool call (Thinking)
                if message.tool_calls:
                    tool_name = message.tool_calls[0]['name']
                    thought_process.write(f"🛠️ **Calling Tool:** `{tool_name}`...")
                
                # If it's a final answer (Speaking)
                elif message.content:
                    final_answer = message.content
                    response_placeholder.write(final_answer)

            # Check if this event comes from a Tool (Action)
            elif "tools" in event:
                tool_message = event["tools"]["messages"][0]
                thought_process.write(f"✅ **Tool Result:** `{tool_message.content[:100]}...`")