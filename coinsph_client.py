# coinsph_client.py
import time, hmac, hashlib, json, requests, os

BASE_URL = "https://api.pro.coins.ph"

class CoinsPHClient:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv("COINS_API_KEY")
        self.api_secret = api_secret or os.getenv("COINS_API_SECRET")
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API credentials")
    
    def _timestamp(self):
        return str(int(time.time() * 1000))
    
    def _sign(self, method, path, body=None):
        body_str = json.dumps(body, separators=(",", ":"), sort_keys=True) if body else ""
        prehash = self._timestamp() + method.upper() + path + body_str
        sig = hmac.new(self.api_secret.encode(), prehash.encode(), hashlib.sha256).hexdigest()
        return sig

    def _headers(self, method, path, body=None):
        ts = self._timestamp()
        sig = self._sign(method, path, body)
        return {
            "X-COINS-APIKEY": self.api_key,
            "X-COINS-TIMESTAMP": ts,
            "X-COINS-SIGNATURE": sig,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _req(self, method, path, params=None, body=None, public=False):
        url = BASE_URL + path
        headers = self._headers(method, path, body) if not public else {"Accept": "application/json"}
        r = requests.request(method, url, headers=headers, params=params, json=body, timeout=10)
        return r.json()

    # --- Public ---
    def ticker(self, symbol): return self._req("GET", "/api/v3/ticker/price", {"symbol": symbol}, public=True)
    def orderbook(self, symbol): return self._req("GET", "/api/v3/depth", {"symbol": symbol, "limit": 20}, public=True)

    # --- Private ---
    def account(self): return self._req("GET", "/api/v3/account")
    def orders(self): return self._req("GET", "/api/v3/openOrders")
    def place_order(self, symbol, side, otype, qty, price=None):
        body = {"symbol": symbol, "side": side, "type": otype}
        if price: body["price"] = str(price)
        if qty: body["quantity"] = str(qty)
        return self._req("POST", "/api/v3/order", body=body)
