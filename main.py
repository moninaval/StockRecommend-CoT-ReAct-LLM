import sys
from agents.executor import run_agent_analysis

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]

        if query.lower().startswith("recommend "):
            # Example: python main.py "recommend INFY"
            symbol = query.split()[-1].upper()
            print(f"🔍 Running analysis for single stock: {symbol}")
            result = run_agent_analysis(
                f"Analyze the fundamentals, technical indicators, and recent news sentiment of {symbol} "
                f"and recommend if it is a BUY."
            )
        else:
            # General case: top 5 recommendations
            print(f"🚀 Running analysis for query: '{query}'")
            result = run_agent_analysis(query)

        print("\n--- ✅ FINAL RECOMMENDATION ---")
        print(result)
    else:
        print("Usage:")
        print("  🔹 python main.py \"Find top 5 small-cap stocks.\"")
        print("  🔹 python main.py \"recommend INFY\"")
