import time

import logging
import firebase_admin
import flask

from flask import Flask, request
from functools import lru_cache
from flask import request
from firebase_admin import credentials
from repositories .user_repository import UserRepository

_IDENTITY_ENDPOINT = ('https://identitytoolkit.googleapis.com/'
                      'google.identity.identitytoolkit.v1.IdentityToolkit')

_FIREBASE_SCOPES = [
    'https://www.googleapis.com/auth/firebase.database',
    'https://www.googleapis.com/auth/userinfo.email']

FIREBASE_URI = "https://nasa-hackathon-team-2.firebaseio.com/"

logging.info("Initializing App")
app = Flask(__name__)
cred = credentials.Certificate('./credentials.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_URI
})

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
