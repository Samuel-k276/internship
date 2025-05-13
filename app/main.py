from fastapi import FastAPI, HTTPException, Query

from app.crud import create_item, get_items, update_item_by_id
from app.models import Item, ItemCreate, ItemUpdate

app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items")
def list_items(min_price: float = Query(0.0), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1)) -> list[Item]:
    return get_items(min_price=min_price, skip=skip, limit=limit)


@app.post("/items")
def add_item(item: ItemCreate) -> Item:
    item = create_item(item)
    if item is None:
        raise HTTPException(status_code=422, detail="Item name already exists")
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate) -> Item:
    updated, error = update_item_by_id(item_id, item)
    if error == "Duplicated name":
        raise HTTPException(status_code=422, detail="Item name already exists")
    if error == "Not Found":
        raise HTTPException(status_code=404, detail="Item not found")
    return updated
