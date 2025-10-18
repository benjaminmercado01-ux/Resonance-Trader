# main.py
from fastapi import FastAPI, Query
from coinsph_client import CoinsPHClient

app = FastAPI(title="Coins.PH Trading API")

@app.get("/")
def root():
    return {"message": "Coins.PH API running on Render ✅"}

@app.get("/balance")
def get_balance():
    client = CoinsPHClient()
    return client.account()

@app.get("/ticker")
def ticker(symbol: str = Query(..., description="e.g. WLD-PHP")):
    client = CoinsPHClient()
    return client.ticker(symbol)

@app.get("/orderbook")
def orderbook(symbol: str = Query(...)):
    client = CoinsPHClient()
    return client.orderbook(symbol)

@app.post("/trade")
def trade(symbol: str, side: str, otype: str, qty: float, price: float = None):
    client = CoinsPHClient()
    return client.place_order(symbol, side.upper(), otype.upper(), qty, price)
