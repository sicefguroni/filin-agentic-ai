import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.finance_agent import initialize_agent
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Financial Analyst Agent Initialized...")
    print("Ask anything about stocks and financial data. Type 'exit' to quit.")

    # Initialize the agent
    agent_executor = initialize_agent()

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
        
            # Run the agent
            response = agent_executor.invoke({"input": user_input})

            print("\nAgent: ", response["output"])

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()