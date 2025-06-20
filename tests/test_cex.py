import pytest
from fastapi.testclient import TestClient
from cex.main import app

client = TestClient(app)

def test_get_ticker():
    resp = client.get("/ticker")
    assert resp.status_code == 200
    data = resp.json()
    assert "last" in data

def test_get_depth():
    resp = client.get("/depth")
    assert resp.status_code == 200
    data = resp.json()
    assert "bids" in data and "asks" in data

@pytest.mark.parametrize("side", ["buy", "sell"])
def test_create_order(side):
    payload = {"symbol": "ETH/USDT", "type": "market", "side": side, "amount": 1.0}
    resp = client.post("/order", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "closed"
    assert data["symbol"] == "ETH/USDT"
