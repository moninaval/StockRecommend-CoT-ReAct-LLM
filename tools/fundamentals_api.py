import yfinance as yf
import time

def fetch_fundamentals(symbol):
    ns_symbol = symbol.strip().upper() + ".NS"

    def is_valid(symbol):
        try:
            hist = yf.Ticker(symbol).history(period="1d")
            return not hist.empty
        except:
            return False

    if not is_valid(ns_symbol):
        print(f"❌ Invalid or delisted symbol: {ns_symbol}")
        return {}

    try:
        data = yf.Ticker(ns_symbol).info
    except Exception as e:
        print(f"⚠️ Error fetching fundamentals for {ns_symbol}, retrying: {e}")
        time.sleep(2)
        try:
            data = yf.Ticker(ns_symbol).info
        except Exception as e2:
            print(f"❌ Failed again for {ns_symbol}: {e2}")
            return {}

    return {
        "Symbol": ns_symbol,
        "P/E Ratio": round(data["trailingPE"], 2) if "trailingPE" in data else None,
        "P/S Ratio": round(data["priceToSalesTrailing12Months"], 2) if "priceToSalesTrailing12Months" in data else None,
        "P/B Ratio": round(data["priceToBook"], 2) if "priceToBook" in data else None,
        "PEG Ratio": round(data["pegRatio"], 2) if "pegRatio" in data else None,
        "P/CF Ratio": round(data["priceToCashflow"], 2) if "priceToCashflow" in data else None,
        "Free Cash Flow": data["freeCashflow"] if "freeCashflow" in data else None,

        "ROE": round(data["returnOnEquity"] * 100, 2) if data.get("returnOnEquity") is not None else None,
        "Net Profit Margin": round(data["netMargins"] * 100, 2) if data.get("netMargins") is not None else None,
        "Operating Margin": round(data["operatingMargins"] * 100, 2) if data.get("operatingMargins") is not None else None,
        "Revenue Growth (YoY)": round(data["revenueGrowth"] * 100, 2) if data.get("revenueGrowth") is not None else None,
        "EPS Growth (YoY)": round(data["earningsQuarterlyGrowth"] * 100, 2) if data.get("earningsQuarterlyGrowth") is not None else None,

        "Debt/Equity Ratio": round(data["debtToEquity"], 2) if data.get("debtToEquity") is not None else None,
        "Current Ratio": round(data["currentRatio"], 2) if data.get("currentRatio") is not None else None,
        "Interest Coverage Ratio": round(data["interestCoverage"], 2) if data.get("interestCoverage") is not None else None,

        "Dividend Yield": round(data["dividendYield"] * 100, 2) if data.get("dividendYield") is not None else None,
        "Payout Ratio": round(data["payoutRatio"] * 100, 2) if data.get("payoutRatio") is not None else None
    }
