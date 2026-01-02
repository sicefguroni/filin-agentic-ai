import numexpr
from langchain.tools import tool
from pydantic import BaseModel, Field

# 1. THE SCHEMA
class CalculatorInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate (e.g., '200 * 1.05').")

# 2. THE TOOL
@tool("calculator", args_schema=CalculatorInput)
def calculator(expression: str) -> str:
    """
    Useful for performing mathematical calculations.
    Use this tool when you need to answer questions about financial calculations.
    """
    try:
        # Character Sanitization
        clean_expression = expression.replace("=", "").replace("import", "").strip()

        # Safe Evaluation
        result = numexpr.evaluate(clean_expression)

        return f"The result of the expression '{expression}' is {result}"

    except Exception as e:
        return f"Error calculating: {str(e)}"

# 3. TEST THE TOOL
if __name__ == "__main__":
    print(calculator.invoke({"expression": "200 * 1.05"}))