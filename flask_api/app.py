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


@app.get("/store/<string:store_id>")  # http://127.0.0.1:5000/store/store_id- return the store info
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError:
        return abort(404, message="Store not found")


@app.get("/item/<string:item_id>")  # http://127.0.0.1:5000/item/item_id - return item
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        return abort(404, message="Item not found")
