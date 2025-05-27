import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

st.title("📈 Crypto Chart Signal Detector (AI)")

uploaded_file = st.file_uploader("📤 Upload chart screenshot (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart", use_column_width=True)

    st.write("🔍 **Analyzing chart...**")

    # Simulated price data (Random, for demonstration)
    close_prices = np.random.normal(loc=100, scale=5, size=100)
    df = pd.DataFrame({'close': close_prices})

    # Calculate RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Calculate MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    last_close = df['close'].iloc[-1]
    last_rsi = df['RSI'].iloc[-1]
    last_macd = df['MACD'].iloc[-1]
    last_signal = df['Signal'].iloc[-1]

    signal = None
    if last_rsi < 30 and last_macd > last_signal:
        signal = "📈 LONG"
    elif last_rsi > 70 and last_macd < last_signal:
        signal = "📉 SHORT"
    else:
        signal = "❓ Unclear Signal"

    entry = round(last_close, 4)
    if signal == "📈 LONG":
        take_profit = round(entry * 1.03, 4)
        stop_loss = round(entry * 0.98, 4)
    elif signal == "📉 SHORT":
        take_profit = round(entry * 0.97, 4)
        stop_loss = round(entry * 1.02, 4)
    else:
        take_profit = stop_loss = None

    st.subheader(f"🔍 **Signal Analysis**")
    st.write(f"**RSI:** {round(last_rsi,2)}")
    st.write(f"**MACD:** {round(last_macd,4)} vs Signal: {round(last_signal,4)}")
    st.write(f"### 🏁 **Final Decision:** {signal}")

    if signal != "❓ Unclear Signal":
        st.write(f"📍 **Entry Point:** {entry}")
        st.write(f"🎯 **Take Profit:** {take_profit}")
        st.write(f"⛔ **Stop Loss:** {stop_loss}")

    st.warning("⚠️ This is a prototype. Real trading decisions need advanced chart data extraction.")
else:
    st.info("⬆️ Please upload a chart screenshot to begin analysis.")
