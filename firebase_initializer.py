import firebase_admin
from firebase_admin import credentials
FIREBASE_URI = "https://nasa-hackathon-team-2.firebaseio.com/"

def initialize_firebase():
    cred = credentials.Certificate('./credentials.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URI
    })