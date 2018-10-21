import firebase_admin
from firebase_admin import credentials
from os import path
from pathlib import Path

FIREBASE_URI = "https://nasa-hackathon-team-2.firebaseio.com/"

def initialize_firebase():
    rootpath = Path(path.dirname(__file__))
    cred = credentials.Certificate(str((rootpath / 'credentials.json')))
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URI
    })