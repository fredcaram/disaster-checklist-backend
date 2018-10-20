from flask import Flask
from functools import lru_cache

import json
import os
import re
import time
import urllib


import flask
from flask import request
import httplib2
from oauth2client.client import GoogleCredentials


_FIREBASE_CONFIG = '_firebase_config.html'

_IDENTITY_ENDPOINT = ('https://identitytoolkit.googleapis.com/'
                      'google.identity.identitytoolkit.v1.IdentityToolkit')
_FIREBASE_SCOPES = [
    'https://www.googleapis.com/auth/firebase.database',
    'https://www.googleapis.com/auth/userinfo.email']

_FIREBASE_SCOPES = [
    'https://www.googleapis.com/auth/firebase.database',
    'https://www.googleapis.com/auth/userinfo.email']

app = Flask(__name__)


@app.route('/user/<user_id>')
def get_user(user_id):
    return


if __name__ == '__main__':
    app.run()
