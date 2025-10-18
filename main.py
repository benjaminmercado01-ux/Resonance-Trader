# main.py
from fastapi import FastAPI, Query, HTTPException
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

# --- Load environment variables ---
COINS_API_KEY = os.getenv("COINS_API_KEY")
COINS_API_SECRET = os.getenv("COINS_API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # <-- new secure token
client = CoinsPHClient(COINS_API_KEY, COINS_API_SECRET)

# --- Helper function for authentication ---
def verify_token(token: str):
    if token != ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid access token")

# --- Basic health check route ---
@app.get("/")
def root():
    return {"message": "Coins.PH API running on Render ✅"}

# --- Get balance ---
@app.get("/balance")
def get_balance(access_token: str = Query(...)):
    verify_token(access_token)
    return client.get_balance()

# --- Get ticker (market prices) ---
@app.get("/ticker")
def get_ticker(symbol: str = Query(...)):
    # public endpoint (no token needed)
    return client.get_ticker(symbol)

# --- Get orderbook ---
@app.get("/orderbook")
def get_orderbook(symbol: str = Query(...)):
    # public endpoint (no token needed)
    return client.get_orderbook(symbol)

# --- Place trade ---
@app.get("/trade")
def trade(
    access_token: str = Query(...),
    symbol: str = Query(...),
    side: str = Query(..., regex="^(BUY|SELL)$"),
    otype: str = Query(..., regex="^(LIMIT|MARKET)$"),
    qty: float = Query(...),
    price: float = Query(None)
):
    verify_token(access_token)
    return client.place_order(symbol, side, otype, qty, price)
