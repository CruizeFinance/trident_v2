from services.firebase_cloud_client import FirebaseClient


def initialize_firebase_client():
    global firebase_client
    firebase_client = None
    firebase_client_obj = FirebaseClient()
    if not firebase_client:
        firebase_client = firebase_client_obj.get_firebase_client
    return firebase_client


firebase_client = initialize_firebase_client()
