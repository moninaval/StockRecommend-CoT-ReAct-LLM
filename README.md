# StockRecommend-CoT-ReAct-LLM

# Stock Recommendation ReAct Agent

This project uses a LangChain ReAct agent to recommend the top 5 stocks from a given market cap category.

## Setup

1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4.  Install dependencies: `pip install -r requirements.txt`
5.  Copy the contents of `.env.example` to a new `.env` file and add your API keys.

## Usage

Run the agent from the command line:

```sh
python main.py "Find the top 5 mid-cap stocks with strong growth potential."
python main.py "recommend INFY"