import os
from ddgs import DDGS
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import time # Added for potential rate limiting

# Load FinBERT model (ensure this is done once, outside the function if called repeatedly)
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def fetch_news_sentiment_enhanced(symbol: str) -> dict:
    # Append .NS for consistency with fundamental data, but DDGS might work better without it for general news search
    search_symbol = symbol.strip().upper() 
    query = f"{search_symbol} stock actual news article" # More specific query
    
    # List of known good Indian financial news sources to prioritize
    # You might want to expand this list
    good_sources = [
        "moneycontrol.com", "economictimes.indiatimes.com", "livemint.com", 
        "business-standard.com", "ndtv.com/business", "zeebiz.com",
        "cnbctv18.com", "businessinsider.in", "thehindubusinessline.com",
        "reuters.com", "bloomberg.com", # General but often cover Indian news
    ]

    headlines_and_snippets = []

    try:
        # Get headlines
        with DDGS() as ddgs:
            # Iterating more results to find relevant ones
            raw_results = []
            for r in ddgs.news(query, region='in-en', safesearch='Off', max_results=20): # Increased max_results
                raw_results.append(r)
                time.sleep(0.5) # Add a small delay between DDGS calls if fetching multiple pages or many symbols

            for r in raw_results:
                title = r.get("title")
                snippet = r.get("body") # DDGS often returns 'body' for snippet/description
                url = r.get("url")
                source = r.get("source") # Get the source
                
                # --- Advanced Filtering ---
                # 1. Check if symbol is in title or snippet
                is_relevant_content = False
                if title and search_symbol in title.upper():
                    is_relevant_content = True
                if snippet and search_symbol in snippet.upper():
                    is_relevant_content = True

                if not is_relevant_content:
                    continue # Skip if symbol not found in title/snippet

                # 2. Prioritize known good news sources or exclude known bad ones
                is_from_good_source = False
                if source:
                    for gs in good_sources:
                        if gs in source.lower() or (url and gs in url.lower()):
                            is_from_good_source = True
                            break
                
                # Exclude common aggregator/profile sites if they don't seem like actual news
                # You can add more patterns here
                if url and any(agg in url.lower() for agg in ["screener.in", "moneycontrol.com/india/stockpricequote", "yahoo.com/quote", "morningstar.in", "nseindia.com"]):
                     # Only keep if it's explicitly from a 'news' or 'article' subpath on those sites
                     if not any(keyword in url.lower() for keyword in ["/news/", "/articles/", "/latest-updates/"]):
                         continue # Skip if it looks like a profile page and not an actual news article link

                # If it passed filters, add it
                if is_relevant_content and (is_from_good_source or not url or not any(agg in url.lower() for agg in ["stockprice", "quote", "company-profile"])): # Heuristic to try and filter profile pages
                    text_to_analyze = f"{title}. {snippet}" if snippet else title
                    headlines_and_snippets.append(text_to_analyze.strip())

        # Print/log what's actually going into FinBERT
        if not headlines_and_snippets:
            print(f"⚠️ No relevant news content found for {symbol} after filtering.")
            return {"error": "No valid news headlines/snippets found after filtering."}
        
        print(f"\n📰 Content going into FinBERT for {symbol.upper()}:")
        for i, text in enumerate(headlines_and_snippets, 1):
            print(f"{i}. {text}")

        # Analyze sentiment
        sentiments = sentiment_pipeline(headlines_and_snippets)
        if not sentiments:
            return {"error": "Sentiment pipeline returned no results."}

        # Calculate score (your existing logic is good here)
        score = 0
        for s in sentiments:
            label = s['label'].lower()
            if label == 'positive':
                score += s['score']
            elif label == 'negative':
                score -= s['score']
            # Neutral scores are ignored

        avg_sentiment_score = round(score / len(sentiments), 3)

        # Label sentiment
        if avg_sentiment_score > 0.3:
            sentiment_label = "Strongly Positive"
        elif avg_sentiment_score > 0.1:
            sentiment_label = "Positive"
        elif avg_sentiment_score > -0.1:
            sentiment_label = "Neutral"
        elif avg_sentiment_score > -0.3:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Strongly Negative"

        # Most relevant headlines (using the original text that went into analysis)
        most_positive_index = -1
        max_positive_score = -1
        most_negative_index = -1
        max_negative_score = -1

        for i, s in enumerate(sentiments):
            if s['label'].lower() == 'positive' and s['score'] > max_positive_score:
                max_positive_score = s['score']
                most_positive_index = i
            elif s['label'].lower() == 'negative' and s['score'] > max_negative_score:
                max_negative_score = s['score']
                most_negative_index = i

        key_positive_news = headlines_and_snippets[most_positive_index] if most_positive_index != -1 else None
        key_negative_news = headlines_and_snippets[most_negative_index] if most_negative_index != -1 else None

        return {
            "Average Sentiment Score": avg_sentiment_score,
            "Overall Sentiment": sentiment_label,
            "Key Positive News": key_positive_news,
            "Key Negative News": key_negative_news,
            "All Headlines Analyzed": headlines_and_snippets, # Renamed for clarity
        }

    except Exception as e:
        print(f"❌ Error in sentiment analysis for {symbol}: {e}")
        return {"error": str(e)}