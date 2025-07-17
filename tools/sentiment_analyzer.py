from duckduckgo_search import DDGS
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def fetch_news_sentiment_enhanced(symbol: str) -> dict:
    query = f"{symbol} stock news"
    headlines = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.news(query, region='in-en', safesearch='Off', max_results=10):
                if r and r.get("title"):
                    headlines.append(r["title"])

        if not headlines:
            return {"error": "No headlines found."}

        sentiments = sentiment_pipeline(headlines)

        score = 0
        for s in sentiments:
            if s['label'] == 'positive':
                score += s['score']
            elif s['label'] == 'negative':
                score -= s['score']

        avg_sentiment_score = round(score / len(sentiments), 3)

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

        most_positive = max(sentiments, key=lambda s: s['score'] if s['label'] == 'positive' else -1)
        most_negative = max(sentiments, key=lambda s: s['score'] if s['label'] == 'negative' else -1)

        return {
            "Average Sentiment Score": avg_sentiment_score,
            "Overall Sentiment": sentiment_label,
            "Key Positive News": most_positive['label'] == 'positive' and headlines[sentiments.index(most_positive)],
            "Key Negative News": most_negative['label'] == 'negative' and headlines[sentiments.index(most_negative)],
        }

    except Exception as e:
        print(f"Error in sentiment analysis for {symbol}: {e}")
        return {"error": str(e)}
