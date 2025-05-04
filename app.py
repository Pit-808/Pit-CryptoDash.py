# app.py – Haupt-Streamlit-Datei
pip install pytrends


import streamlit as st
from pytrends.request import TrendReq
import requests
import pandas as pd
from utils.gli import load_gli_data, calculate_gli_index
from utils.economic_data import load_interest_rates

st.set_page_config(page_title="Krypto Analyse Hub", layout="wide")

st.title("📊 Krypto Analyse & Vergleichsdaten")

coin = st.sidebar.selectbox("Kryptowährung auswählen", ["bitcoin", "ethereum", "solana", "cardano"])
vs_currency = st.sidebar.selectbox("Währung", ["usd", "eur"])
days = st.sidebar.slider("Zeitraum (in Tagen)", 7, 365, 90)

@st.cache_data
def load_crypto_data(coin, vs_currency, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    response = requests.get(url, params=params)
    data = response.json()
    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    prices["date"] = pd.to_datetime(prices["timestamp"], unit="ms")
    return prices[["date", "price"]]

prices_df = load_crypto_data(coin, vs_currency, days)
st.subheader(f"{coin.capitalize()} Preisverlauf")
st.line_chart(prices_df.set_index("date")["price"])

st.subheader("🌍 Global Liquidity Index (Howell Proxy)")
gli_df = calculate_gli_index(load_gli_data())
st.line_chart(gli_df.set_index("date")["GLI"])

st.subheader("🏦 Zentralbank-Zinssätze")
rates_df = load_interest_rates()
st.line_chart(rates_df.set_index("date"))
