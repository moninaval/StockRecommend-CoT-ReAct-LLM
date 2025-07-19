import yfinance as yf
import pandas as pd
import pandas_ta as ta

def fetch_technical_indicators_enhanced(symbol):
    try:
        # Fetch 1 year of data to ensure enough for SMA_200
        df = yf.download(symbol, period="1y", interval="1d", progress=False)

        # 🔧 Fix for MultiIndex bug when yfinance returns columns like (symbol, data_type)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty or len(df) < 200:
            raise ValueError("Insufficient data for 200-day SMA")

        # Calculate indicators
        df.ta.rsi(length=14, append=True)
        df.ta.sma(length=50, append=True)
        df.ta.sma(length=200, append=True)
        df.ta.macd(append=True)
        df.ta.bbands(append=True)

        latest = df.iloc[-1]
        price = latest["Close"]

        # RSI Signal
        rsi_val = latest.get("RSI_14")
        if rsi_val is not None:
            if rsi_val > 70:
                rsi_state = "Overbought"
            elif rsi_val < 30:
                rsi_state = "Oversold"
            else:
                rsi_state = "Neutral"
        else:
            rsi_state = "N/A"

        # SMA Crossover
        sma_50 = latest.get("SMA_50")
        sma_200 = latest.get("SMA_200")
        cross_signal = (
            "Golden Cross (Bullish)" if sma_50 and sma_200 and sma_50 > sma_200
            else "Death Cross (Bearish)" if sma_50 and sma_200
            else "N/A"
        )

        # MACD Signal
        macd_line = latest.get("MACD_12_26_9")
        signal_line = latest.get("MACDs_12_26_9")
        if macd_line is not None and signal_line is not None:
            macd_signal = "Bullish Crossover" if macd_line > signal_line else "Bearish Crossover"
        else:
            macd_signal = "N/A"

        return {
            "Price": round(price, 2),
            "RSI_14": round(rsi_val, 2) if rsi_val else None,
            "SMA_50": round(sma_50, 2) if sma_50 else None,
            "SMA_200": round(sma_200, 2) if sma_200 else None,
            "MACD": round(macd_line, 2) if macd_line else None,
            "AI_Signal_RSI_State": rsi_state,
            "AI_Signal_Trend": "Above SMA_50" if sma_50 and price > sma_50 else "Below SMA_50",
            "AI_Signal_Long_Term_Trend": cross_signal,
            "AI_Signal_Momentum": macd_signal
        }

    except Exception as e:
        print(f"Error fetching enhanced technicals for {symbol}: {e}")
        return { "error": str(e) }
