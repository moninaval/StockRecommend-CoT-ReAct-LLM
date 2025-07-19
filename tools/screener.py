import os
import csv
import re

CATEGORY_TO_FILE = {
    'mega-cap': 'ind_nifty50list.csv',
    'large-cap': 'ind_niftynext50list.csv',
    'mid-cap': 'ind_niftymidcap150list.csv',
    'small-cap': 'ind_niftysmallcap250list.csv',
    'micro-cap': 'ind_niftymicrocap250list.csv',
}

def get_stocks_by_market_cap(category: str) -> list[str]:
    """
    Reads a CSV file from ../data/nse_indices/ for the given market cap category.
    This script is intended to be run from inside the 'tools/' directory.
    """
    # Normalize input using regex to remove non-alpha characters (e.g. quotes, dashes, spaces)
    normalized = re.sub(r'[^a-z]', '', category.lower())
    matched = next(
        (k for k in CATEGORY_TO_FILE if re.sub(r'[^a-z]', '', k.lower()) == normalized), 
        None
    )

    if not matched:
        return [f"❌ Invalid category '{category}'. Valid options: {', '.join(CATEGORY_TO_FILE.keys())}"]

    # Resolve correct path from tools/ to root-level data/nse_indices/
    script_dir = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(script_dir, "..", "data", "nse_indices", CATEGORY_TO_FILE[matched]))

    if not os.path.exists(filepath):
        return [f"❌ File not found: {filepath}. Please place the CSV manually in 'data/nse_indices/'"]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            print(f"🧪 Reading: {filepath}")
            print(f"🧪 Detected columns: {reader.fieldnames}")
            columns = {col.lower(): col for col in reader.fieldnames}
            symbol_col = columns.get("symbol")
            if not symbol_col:
                return [f"❌ 'Symbol' column not found in file: {CATEGORY_TO_FILE[matched]}"]
            return [row[symbol_col].strip() for row in reader if row[symbol_col].strip()]
    except Exception as e:
        return [f"❌ Error reading CSV: {e}"]
