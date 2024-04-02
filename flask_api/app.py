from flask import Flask, request

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]


@app.get("/store")  # http://127.0.0.1:5000/store - get all stores data
def get_stores():
    return {"stores": stores}


@app.post("/store")  # http://127.0.0.1:5000/store - create new store
def create_stores():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:name>/item")  # http://127.0.0.1:5000/store/store_name/item - add new item to the store
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"Message": "Store not found"}, 404


@app.get("/store/<string:name>")  # http://127.0.0.1:5000/store/store_name- return the store info
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store, 200
    return {"Message": "Store not found"}, 404


@app.get("/store/<string:name>/item")  # http://127.0.0.1:5000/store/store_name/item - return the store item list
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}, 200
    return {"Message": "Store not found"}, 404
