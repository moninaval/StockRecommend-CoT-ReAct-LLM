#### **`main.py`**

import sys
from agent.executor import run_agent_analysis

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(f"🚀 Running analysis for query: '{query}'")
        result = run_agent_analysis(query)
        print("\n--- ✅ FINAL RECOMMENDATION ---")
        print(result)
    else:
        print("Please provide a query. Example: python main.py 'Find top 5 large-cap stocks.'")