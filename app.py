import time

import logging
import flask

from flask import Flask, request
from functools import lru_cache
from flask import request
from repositories .user_repository import UserRepository
from firebase_initializer import initialize_firebase

logging.info("Initializing App")
app = Flask(__name__)
initialize_firebase()
user_repo = UserRepository()

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


if __name__ == '__main__':
    app.run()
