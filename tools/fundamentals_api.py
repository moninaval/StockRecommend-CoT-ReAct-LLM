import yfinance as yf

def fetch_fundamentals(symbol):
    try:
        data = yf.Ticker(symbol).info
        return {
            "P/E Ratio": round(data["trailingPE"], 2) if "trailingPE" in data else None,
            "P/S Ratio": round(data["priceToSalesTrailing12Months"], 2) if "priceToSalesTrailing12Months" in data else None,
            "P/B Ratio": round(data["priceToBook"], 2) if "priceToBook" in data else None,
            "PEG Ratio": round(data["pegRatio"], 2) if "pegRatio" in data else None,
            "P/CF Ratio": round(data["priceToCashflow"], 2) if "priceToCashflow" in data else None,
            "Free Cash Flow": data["freeCashflow"] if "freeCashflow" in data else None,

            "ROE": round(data["returnOnEquity"] * 100, 2) if "returnOnEquity" in data and data["returnOnEquity"] is not None else None,
            "Net Profit Margin": round(data["netMargins"] * 100, 2) if "netMargins" in data and data["netMargins"] is not None else None,
            "Operating Margin": round(data["operatingMargins"] * 100, 2) if "operatingMargins" in data and data["operatingMargins"] is not None else None,
            "Revenue Growth (YoY)": round(data["revenueGrowth"] * 100, 2) if "revenueGrowth" in data and data["revenueGrowth"] is not None else None,
            "EPS Growth (YoY)": round(data["earningsQuarterlyGrowth"] * 100, 2) if "earningsQuarterlyGrowth" in data and data["earningsQuarterlyGrowth"] is not None else None,

            "Debt/Equity Ratio": round(data["debtToEquity"], 2) if "debtToEquity" in data and data["debtToEquity"] is not None else None,
            "Current Ratio": round(data["currentRatio"], 2) if "currentRatio" in data and data["currentRatio"] is not None else None,
            "Interest Coverage Ratio": round(data["interestCoverage"], 2) if "interestCoverage" in data and data["interestCoverage"] is not None else None,

            "Dividend Yield": round(data["dividendYield"] * 100, 2) if "dividendYield" in data and data["dividendYield"] is not None else None,
            "Payout Ratio": round(data["payoutRatio"] * 100, 2) if "payoutRatio" in data and data["payoutRatio"] is not None else None
        }
    except Exception as e:
        print(f"Error fetching fundamentals for {symbol}: {e}")
        return {}