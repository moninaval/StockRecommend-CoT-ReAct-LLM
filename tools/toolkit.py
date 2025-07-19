from langchain.agents import Tool
from .screener import get_stocks_by_market_cap
from .fundamentals_api import fetch_fundamentals
from .technicals_analyzer import fetch_technical_indicators_enhanced
from .sentiment_analyzer import fetch_news_sentiment_enhanced

tools = [
    Tool(
        name="Stock_Screener",
        func=get_stocks_by_market_cap,
        description="Use this tool to get a list of stock symbols for a given market cap category (e.g., 'mid-cap' or 'large-cap')."
    ),
    Tool(
        name="Get_Fundamentals",
        func=fetch_fundamentals,
        description="Use this tool to get fundamental financial data for a single stock symbol. Provides P/E Ratio, ROE, etc."
    ),
    Tool(
        name="Get_Technicals",
        func=fetch_technical_indicators_enhanced,
        description="Use this tool to get technical indicators and signals (RSI, SMAs, Trend) for a single stock symbol."
    ),
    Tool(
        name="Get_News_Sentiment",
        func=fetch_news_sentiment_enhanced,
        description="Use this tool to get the latest news sentiment (Positive/Neutral/Negative) for a single stock symbol."
    )
]