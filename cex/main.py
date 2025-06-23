import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Response
from pydantic import BaseModel
from typing import List
import uvicorn
import asyncio
import time
import random
from threading import Thread

app = FastAPI(title="Mock CEX API")

CEX_PORT = int(os.getenv("CEX_PORT", 8000))

# Simulate multiple tokens
tokens = [
    {"symbol": "TestTokenA/USDT", "last": 1.23},
    {"symbol": "TestTokenB/USDT", "last": 2.34},
    {"symbol": "TestTokenC/USDT", "last": 3.45},
    {"symbol": "TestTokenD/USDT", "last": 4.56},
]

ticker_states = {t["symbol"]: {
    "symbol": t["symbol"], "timestamp": None, "datetime": None, "high": 0, "low": 0, "bid": 0, "ask": 0, "vwap": 0, "open": 0, "close": 0, "last": t["last"], "baseVolume": 0, "quoteVolume": 0
} for t in tokens}

class OrderRequest(BaseModel):
    symbol: str
    type: str  # 'limit' or 'market'
    side: str  # 'buy' or 'sell'
    amount: float
    price: float = None

class OrderResponse(BaseModel):
    id: str
    timestamp: int
    datetime: str
    symbol: str
    type: str
    side: str
    price: float
    amount: float
    status: str  # 'open', 'closed', etc.

@app.get("/ticker")
def get_ticker(symbol: str = "TestTokenA/USDT"):
    try:
        print(f"/ticker called with symbol: {symbol}")
        print(f"Available ticker_states keys: {list(ticker_states.keys())}")
        result = ticker_states.get(symbol, ticker_states.get("TestTokenA/USDT"))
        print(f"Result: {result}")
        return result
    except Exception as e:
        print(f"Error in /ticker: {e}")
        return {"error": str(e)}, 500

@app.get("/tickers")
def get_all_tickers():
    """Return all tickers."""
    return list(ticker_states.values())

@app.get("/depth")
def get_order_book(symbol: str = "ETH/USDT"):
    """Return mock order book depth for a symbol."""
    last = ticker_states.get(symbol, ticker_states["ETH/USDT"])['last']
    return {
        "bids": [[last - 1, 5], [last - 1.5, 3]],
        "asks": [[last + 1, 4], [last + 2, 2]]
    }

order_count = 0
request_latencies = []
order_counts = {t["symbol"]: 0 for t in tokens}

@app.middleware("http")
async def add_latency_metrics(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    request_latencies.append(latency)
    # Keep only the last 100 latencies for simplicity
    if len(request_latencies) > 100:
        request_latencies.pop(0)
    return response

@app.post("/order")
def create_order(order: OrderRequest):
    global order_count
    order_count += 1
    order_counts[order.symbol] = order_counts.get(order.symbol, 0) + 1
    resp = OrderResponse(
        id="123456",
        timestamp=app.router.__hash__(),
        datetime="2025-06-19T00:00:00Z",
        symbol=order.symbol,
        type=order.type,
        side=order.side,
        price=order.price or ticker_states[order.symbol]['last'],
        amount=order.amount,
        status="closed"
    )
    return resp

@app.get("/metrics")
def metrics():
    avg_latency = sum(request_latencies) / len(request_latencies) if request_latencies else 0
    metrics_str = f"""
# HELP order_count Total number of orders placed\n# TYPE order_count counter
order_count {order_count}
# HELP request_latency_seconds Average request latency in seconds\n# TYPE request_latency_seconds gauge
request_latency_seconds {avg_latency}
"""
    for symbol, state in ticker_states.items():
        metrics_str += f"# HELP price_{symbol.replace('/', '_')} Last price for {symbol}\n# TYPE price_{symbol.replace('/', '_')} gauge\nprice_{symbol.replace('/', '_')} {state['last']}\n"
        metrics_str += f"# HELP order_count_{symbol.replace('/', '_')} Orders for {symbol}\n# TYPE order_count_{symbol.replace('/', '_')} counter\norder_count_{symbol.replace('/', '_')} {order_counts[symbol]}\n"
    return Response(content=metrics_str, media_type="text/plain")

# WebSocket manager for pushing ticker updates
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for conn in list(self.active_connections):
            try:
                await conn.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws/ticker")
async def ws_ticker(websocket: WebSocket):
    """WebSocket endpoint streaming all tickers every second."""
    await manager.connect(websocket)
    try:
        while True:
            # simulate price update for each token
            for state in ticker_states.values():
                # Random walk for price
                state['last'] += random.uniform(-1, 1)
            await manager.broadcast({"type": "tickers", "data": list(ticker_states.values())})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Background task to update prices every second
def price_update_loop():
    while True:
        for state in ticker_states.values():
            state['last'] += random.uniform(-1, 1)
        time.sleep(0.1)  # 100ms update interval

# Start the background price update thread
Thread(target=price_update_loop, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CEX_PORT, reload=True)
