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


def test_partial_update_price() -> None:
    client.post("/items", json={"name": "Apple", "price": 5})
    resp = client.put("/items/1", json={"price": 7})
    assert resp.status_code == 422 or resp.status_code == 200 and resp.json()["price"] == 7


def test_update_to_duplicate_name() -> None:
    client.post("/items", json={"name": "Grape", "price": 6})
    resp = client.put("/items/1", json={"name": "Grape"})
    assert resp.status_code == 400 or resp.status_code == 422


def test_item_name_consistency() -> None:
    unique_name = f"ConsistencyTest_{int(__import__('time').time())}"
    response = client.post("/items", json={"name": unique_name, "price": 5})
    assert response.status_code == 200

    created_item = response.json()
    assert created_item["name"] == unique_name
    id = created_item["id"]

    response = client.get("/items?limit=9999999999")
    assert any(item["id"] == id and item["name"] == unique_name for item in response.json())


def test_pagination() -> None:
    response = client.get("/items?skip=0&limit=10")
    assert len(response.json()) <= 10
