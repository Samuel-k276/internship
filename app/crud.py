from typing import List, Tuple

from app.database import items_db
from app.models import Item, ItemCreate, ItemUpdate

"""
I would apply Pagination to the get_items function, introducing skip and limit parameters.
This would allow the client to specify how many items to skip and how many to return.

Explaination:
- Because most of the time consumed is in constructing the response, 
we can optimize the get_items function by adding pagination.
- This will allow the client to request only a subset of items, 
reducing the amount of data processed and sent over the network
- If there is still a need to fetch all items,
the client can set skip to 0 and limit to a crazy large number.

Now that the number of items is independent of the number of items in the database (in most cases),
the time it takes to process the request will be heavily reduced.

Time comparison:
- Before: O(n) for filtering and O(n) for constructing the response,
- After: O(n) for filtering and O(1) for constructing the response.

We could also use a pagination approach with page and size as parameters
or a token-based pagination approach (using a cursor to track the last item seen)
"""
def get_items(min_price: float = 0.0, skip: int = 0, limit: int = 100) -> List[Item]:
   return [Item(**item) for item in items_db[skip : skip + limit] if item["price"] >= min_price]


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
