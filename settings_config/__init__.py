import os

import firebase_admin
from firebase_admin import credentials, firestore


def initialize_firebase_client():
    global firebase_client
    firebase_client = None

    if not firebase_admin._apps:
        print('Initializing Firebase Client')
        cred = credentials.Certificate(
            os.path.abspath(os.path.dirname(__file__)) + "/firebase_config.json"
        )

        firebase_admin.initialize_app(cred)
        return firestore.client()

    # global firebase_client
    # firebase_client = None
    # firebase_client_obj = FirebaseClient()
    # if not firebase_client:
    #     firebase_client = firebase_client_obj.get_firebase_client
    # return firebase_client


firebase_client = initialize_firebase_client()
