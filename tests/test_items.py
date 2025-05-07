from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_min_price_filter() -> None:
    response = client.get("/items?min_price=4")
    assert all(item["price"] >= 4 for item in response.json())


def test_short_name() -> None:
    response = client.post("/items", json={"name": "ab", "price": 5})
    assert response.status_code == 422


def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422


def test_item_name_consistency() -> None:
    response = client.get("/items")
    names = [item["name"] for item in response.json()]
    assert "Item500000" in names

def test_pagination() -> None:
    response = client.get("/items?skip=0&limit=10")
    assert len(response.json()) == 10
    assert all(item["id"] <= 10 for item in response.json())

def test_pagination_with_limit_above_1000() -> None:
    response = client.get("/items?skip=0&limit=2000")
    assert response.status_code == 422