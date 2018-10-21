import time

import logging
import flask

from flask import Flask, request
from functools import lru_cache
from flask import request
from repositories.user_repository import UserRepository
from repositories.list_repository import ListRepository
from repositories.item_repository import ItemRepository
from repositories.disaster_repository import DisasterRepository

from firebase_initializer import initialize_firebase
import pandas as pd

logging.info("Initializing App")
app = Flask(__name__)
initialize_firebase()
user_repo = UserRepository()
list_repo = ListRepository()
item_repo = ItemRepository()
disaster_repo = DisasterRepository()

@app.route('/user/<user_id>', methods=["GET"])
def get_user(user_id):
    logging.debug("Getting User")
    user_json = flask.jsonify(user_repo.get(user_id))
    logging.debug(user_json)
    return user_json


@app.route('/user/<user_id>/update', methods=["PATCH"])
def update_user(user_id):
    logging.debug("Updating User")
    user = request.json
    user_json = user_repo.update(user_id, user)
    logging.debug(user_json)
    return user_json


@app.route('/user/insert/', methods=["POST", "PUT"])
def insert_user():
    logging.debug("Inserting User")
    user = request.json
    logging.debug(user)
    return flask.jsonify(user_repo.add(user))


@app.route('/disasters', methods=["GET"])
def get_disaster():
    logging.debug("Getting disaster collection")
    disasters = flask.jsonify(disaster_repo.get_collection())
    logging.debug(disasters)
    return disasters


@app.route('/disaster/<disaster_id>', methods=["GET"])
def get_disaster(disaster_id):
    logging.debug("Getting disaster")
    disaster_item = flask.jsonify(disaster_repo.get(disaster_id))
    logging.debug(disaster_item)
    return disaster_item


@app.route('/disaster/<disaster_id>/update', methods=["PATCH"])
def update_disaster(disaster_id):
    logging.debug("Updating List item")
    disaster_item = request.json
    disaster_item_json = disaster_repo.update(disaster_id, disaster_item)
    logging.debug(disaster_item_json)
    return disaster_item_json


@app.route('/disaster/insert/', methods=["POST", "PUT"])
def insert_disaster():
    logging.debug("Inserting List Item")
    disaster_item = request.json
    logging.debug(disaster_item)
    return flask.jsonify(disaster_repo.add(disaster_item))


@app.route('/disaster/<disaster_id>', methods=["DELETE"])
def delete_disaster(disaster_id):
    logging.debug("Delete List item")
    disaster_repo.delete(disaster_id)
    return "Success"


@app.route('/list_item/<list_item_id>', methods=["GET"])
def get_user(list_item_id):
    logging.debug("Getting List item")
    list_item = flask.jsonify(list_repo.get(list_item_id))
    logging.debug(list_item)
    return list_item


@app.route('/list_item/<list_item_id>/update', methods=["PATCH"])
def update_user(list_item_id):
    logging.debug("Updating List item")
    list_item = request.json
    list_item_json = list_repo.update(list_item_id, list_item)
    logging.debug(list_item_json)
    return list_item_json


@app.route('/list_item/insert/', methods=["POST", "PUT"])
def insert_user():
    logging.debug("Inserting List Item")
    list_item = request.json
    logging.debug(list_item)
    return flask.jsonify(list_repo.add(list_item))


@app.route('/list_item/<list_item_id>', methods=["DELETE"])
def delete_user(list_item_id):
    logging.debug("Delete List item")
    list_repo.delete(list_item_id)
    return "Success"


@app.route('get_list_for_disaster', methods=["GET"])
def get_list_for_disaster():
    logging.debug("Get item list for disaster")
    user_id = request.query_string["user_id"]
    disaster_id = request.query_string["disaster_id"]
    items = get_list_items(disaster_id, user_id)

    return flask.jsonify(items)


def get_list_items(disaster_id, user_id):
    user = user_repo.get(user_id)
    user_profile_df = pd.DataFrame(user, index=[user["id"]])
    list_items = list_repo.get_list_for_disaster(user_profile_df, disaster_id)
    item_ids = list(list_items["idItem"].values)
    items = item_repo.get_items(item_ids)
    return items


if __name__ == '__main__':
    app.run()
