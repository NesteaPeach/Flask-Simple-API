import uuid

from flask import Flask, request
from db import items, stores
import uuid

app = Flask(__name__)


@app.get("/store")  # http://127.0.0.1:5000/store - get all stores data
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")  # http://127.0.0.1:5000/store - create new store
def create_stores():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")  # http://127.0.0.1:5000/item - add new item to the store
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"Message": "Store not found"}, 404
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
        return {"Message": "Store not found"}, 404


@app.get("/item/<string:item_id>")  # http://127.0.0.1:5000/item/item_id - return item
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError:
        return {"Message": "item not found"}, 404
