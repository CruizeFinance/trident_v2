import time

# TODO : refactor this file .
from settings_config import firebase_client


class FirebaseDataManager(object):
    def __init__(self):
        self.firebase_client = firebase_client

    def document_exists(self, document, collection_name):
        return (
            self.firebase_client.collection(collection_name)
            .document(document)
            .get()
            .exists
        )

    def update_data(self, document, collection_name, data):
        self.firebase_client.collection(collection_name).document(document).update(data)

    def store_data(self, data, document, collection_name):
        self.firebase_client.collection(collection_name).document(document).set(data)

    def bulk_store(self, data, collection_name, field):
        batch = self.firebase_client.batch()
        for key, value in data.items():
            write = self.firebase_client.collection(collection_name).document(key)
            batch.set(write, {field: str(value)})
        batch.commit()

    def store_sub_collections(
        self, data, collection, document_name, sub_collection, sub_document
    ):
        data["timestamp"] = time.time()
        self.firebase_client.collection(collection).document(document_name).collection(
            sub_collection
        ).document(sub_document).set(data)

    def fetch_sub_collections(self, collection, document_name, sub_collection):
        firebase_data = (
            self.firebase_client.collection(collection)
            .document(document_name)
            .collection(sub_collection)
            .get()
        )
        return firebase_data

    def fetch_data(self, collection_name, document_name):
        firebase_data = (
            self.firebase_client.collection(collection_name)
            .document(document_name)
            .get()
        )

        if firebase_data is not None:
            firebase_data = vars(firebase_data)
        return firebase_data.get("_data", None)

    def fetch_collections(self, collection_name):
        collection_obj = self.firebase_client.collection(collection_name)
        collection_data = collection_obj.stream()
        for d in collection_data:
            print(d.to_dict())
        return collection_data


if __name__ == "__main__":
    a = FirebaseDataManager()
