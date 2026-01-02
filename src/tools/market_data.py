from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from pydantic import BaseModel, Field

class StockPriceInput(BaseModel):
    ticker: str = Field(description="The stock ticker symbol (e.g., AAPL, TSLA)")

@tool("get_stock_price", args_schema=StockPriceInput)
def get_stock_price(ticker: str) -> str:
    """
    Fetches the current stock price.
    """
    try:
        print(f"DEBUG: querying Tavily for {ticker} (Targeted)...")
        
        # FIX 1: Max results 5 to increase chance of hitting a good site
        search = TavilySearchResults(max_results=5)
        
        # FIX 2: "Sniper Query"
        # We explicitly ask for 'MarketWatch' or 'Reuters' because they don't hide data behind 'Loading...' screens.
        query = f"{ticker} stock price quote MarketWatch Reuters"
        
        results = search.invoke(query)
        
        combined_data = []
        if results and isinstance(results, list):
            for res in results:
                content = res.get('content', '')
                url = res.get('url', '')
                
                # FIX 3: Filtering Garbage
                # If the result is just a "cookie consent" or "loading" message, skip it.
                if "Loading" in content or "cookies" in content.lower():
                    continue
                    
                combined_data.append(f"Source ({url}): {content}")
            
            if not combined_data:
                return "Error: Found search results, but they were all empty/loading screens."
                
            return "\n\n".join(combined_data)
        
        return "Error: No market data found."
        
    except Exception as e:
        return f"Error fetching market data: {str(e)}"