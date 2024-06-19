from flask import Flask, request
from db import items, stores
import uuid
from flask_smorest import abort

app = Flask(__name__)


@app.get("/store")  # http://127.0.0.1:5000/store - get all stores data
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")  # http://127.0.0.1:5000/store - create new store
def create_stores():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"{store_data['name']} already exists")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")


@app.post("/item")  # http://127.0.0.1:5000/item - add new item to the store
def create_item():
    item_data = request.get_json()
    required_keys = ["price", "store_id", "name"]
    if not all(key in item_data for key in required_keys):
        abort(400, message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.")
    if item_data.get("store_id") not in stores:
        abort(404, message="Store not found")
    for item in items.values():
        if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
            abort(400, message=f"{item_data['name']} already exists")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/item")  # http://127.0.0.1:5000/item - get all items data
def get_items():
    return {"items": list(items.values())}


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    # There's  more validation to do here!
    # Like making sure price is a number, and also both items are optional
    # Difficult to do with an if statement...
    if "price" not in item_data or "name" not in item_data:
        abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )
    try:
        item = items[item_id]
        # https://blog.teclado.com/python-dictionary-merge-update-operators/
        item |= item_data

        return item
    except KeyError:
        abort(404, message="Item not found.")


@app.get("/store/<string:store_id>")  # http://127.0.0.1:5000/store/store_id- return the store info
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        abort(404, message="Store not found")


@app.get("/item/<string:item_id>")  # http://127.0.0.1:5000/item/item_id - return item
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        abort(404, message="Item not found")
