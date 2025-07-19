# File: tools/screener.py
from finvizfinance.screener import Screener

def get_stocks_by_market_cap(category: str) -> list[str]:
    """
    Finds stock symbols within a given market cap category.
    Valid categories include: 'Mega-Cap', 'Large-Cap', 'Mid-Cap', 'Small-Cap'.
    """
    category_map = {
        'mega-cap': 'over 200bln',
        'large-cap': 'over 10bln',
        'mid-cap': '2bln to 10bln',
        'small-cap': '300mln to 2bln',
    }
    
    finviz_category = category_map.get(category.lower().replace(" ", ""))
    if not finviz_category:
        return f"Error: Invalid category '{category}'. Please use Mega-Cap, Large-Cap, Mid-Cap, or Small-Cap."

    try:
        screener = Screener(filters=[f'marketcap_{finviz_category}'], table='Overview', order='marketcap')
        # The signal parameter can be used to limit results, e.g., 'Top Gainers'
        stock_list = screener.get_ticker_list()
        # Limit to a reasonable number for analysis
        return stock_list[:20] if len(stock_list) > 20 else stock_list
    except Exception as e:
        return f"Error fetching stocks from Finviz: {e}"