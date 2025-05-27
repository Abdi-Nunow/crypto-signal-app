# app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import ta
import matplotlib.pyplot as plt

# Title
st.title("📈 Crypto Chart Signal Detector (AI)")

# Upload chart image
uploaded_file = st.file_uploader("📤 Upload chart screenshot (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_column_width=True)

    # Convert to OpenCV format
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    st.write("🔍 **Analyzing chart...**")

    # For now, we will simulate data (in real-world, use OCR/AI)
    # Simulate extracted price data
    close_prices = np.random.normal(loc=100, scale=5, size=100)  # Random price data for indicators
    df = ta.utils.dropna(ta.add_all_ta_features(
        pd.DataFrame({'close': close_prices, 'open': close_prices, 'high': close_prices+2, 'low': close_prices-2, 'volume': np.random.randint(100, 1000, size=100)})
    ))

    # Calculate last values
    last_close = df['close'].iloc[-1]
    last_rsi = df['momentum_rsi'].iloc[-1]
    last_macd = df['trend_macd'].iloc[-1]
    last_macd_signal = df['trend_macd_signal'].iloc[-1]

    # Decision logic
    signal = None
    if last_rsi < 30 and last_macd > last_macd_signal:
        signal = "📈 LONG"
    elif last_rsi > 70 and last_macd < last_macd_signal:
        signal = "📉 SHORT"
    else:
        signal = "❓ Unclear Signal"

    # Entry/TP/SL suggestion
    entry = round(last_close, 4)
    if signal == "📈 LONG":
        take_profit = round(entry * 1.03, 4)
        stop_loss = round(entry * 0.98, 4)
    elif signal == "📉 SHORT":
        take_profit = round(entry * 0.97, 4)
        stop_loss = round(entry * 1.02, 4)
    else:
        take_profit = stop_loss = None

    # Display results
    st.subheader(f"🔍 **Signal Analysis**")
    st.write(f"**RSI:** {round(last_rsi,2)}")
    st.write(f"**MACD:** {round(last_macd,4)} vs Signal: {round(last_macd_signal,4)}")
    st.write(f"### 🏁 **Final Decision:** {signal}")

    if signal != "❓ Unclear Signal":
        st.write(f"📍 **Entry Point:** {entry}")
        st.write(f"🎯 **Take Profit:** {take_profit}")
        st.write(f"⛔ **Stop Loss:** {stop_loss}")

    st.warning("⚠️ This is a prototype. Real trading decisions need advanced chart data extraction.")
else:
    st.info("⬆️ Please upload a chart screenshot to begin analysis.")
