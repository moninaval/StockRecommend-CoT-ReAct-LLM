from screener import get_stocks_by_market_cap

if __name__ == "__main__":
    print("Available categories: Mega-Cap, Large-Cap, Mid-Cap, Small-Cap, Micro-Cap")
    category = input("Enter category: ").strip()
    stocks = get_stocks_by_market_cap(category)

    if stocks and stocks[0].startswith("❌"):
        print(stocks[0])
    else:
        print(f"\n✅ Found {len(stocks)} stocks in '{category}':\n")
        print(", ".join(stocks))
