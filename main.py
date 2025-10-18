# main.py
from fastapi import FastAPI, Query
from coinsph_client import CoinsPHClient
import requests
import os

# --- Get and print Render server IP ---
try:
    ip = requests.get("https://ifconfig.me").text.strip()
    print(f"🛰️ Render outbound IP address: {ip}")
except Exception as e:
    print("⚠️ Could not fetch outbound IP:", e)

# --- Initialize app ---
app = FastAPI()

# --- Initialize CoinsPH client with environment variables ---
COINS_API_KEY = os.getenv("COINS_API_KEY")
COINS_API_SECRET = os.getenv("COINS_API_SECRET")
client = CoinsPHClient(COINS_API_KEY, COINS_API_SECRET)

# --- Basic health check route ---
@app.get("/")
def root():
    return {"message": "Coins.PH API running on Render ✅"}

# --- Get balance ---
@app.get("/balance")
def get_balance():
    return client.get_balance()

# --- Get ticker (market prices) ---
@app.get("/ticker")
def get_ticker(symbol: str = Query(...)):
    return client.get_ticker(symbol)

# --- Get orderbook ---
@app.get("/orderbook")
def get_orderbook(symbol: str = Query(...)):
    return client.get_orderbook(symbol)

# --- Place trade ---
@app.get("/trade")
def trade(
    symbol: str = Query(...),
    side: str = Query(..., regex="^(BUY|SELL)$"),
    otype: str = Query(..., regex="^(LIMIT|MARKET)$"),
    qty: float = Query(...),
    price: float = Query(None)
):
    return client.place_order(symbol, side, otype, qty, price)
