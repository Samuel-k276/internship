from typing import List, Tuple

from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate


def get_items(min_price: float = 0.0) -> List[Item]:
    return [Item(**item) for item in items_db if item["price"] >= min_price]


def create_item(item: ItemCreate) -> Item:
    new_id = items_db[-1]["id"] + 1 if items_db else 1
    new_item = {"id": new_id, **item.dict()}
    items_db.append(new_item)
    return Item(**new_item)


def update_item_by_id(item_id: int, update: ItemUpdate) -> Tuple[Item, str]:
    # Check for duplicate name
    if any(i["name"] == update.name and i["id"] != item_id for i in items_db):
        return None, "Duplicated name"

    for item in items_db:
        if item["id"] == item_id:
            if update.name:
                item["name"] = update.name
            if update.price:
                item["price"] = update.price
            return Item(**item), ""
        
    return None,  "Not Found"
