import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseService:
    def __init__(self):
        self.db = None
        self.initialize_firebase()

    def initialize_firebase(self):
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate('service-account-key.json')
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        print("Connected to Firebase successfully!")

    def add_document(self, collection, data, doc_id=None):
        if doc_id:
            self.db.collection(collection).document(doc_id).set(data)
            return doc_id
        else:
            doc_ref = self.db.collection(collection).add(data)
            return doc_ref.id

    def get_document(self, collection, doc_id):
        doc = self.db.collection(collection).document(doc_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    def update_document(self, collection, doc_id, data):
        self.db.collection(collection).document(doc_id).update(data)

    def delete_document(self, collection, doc_id):
        self.db.collection(collection).document(doc_id).delete()

    def get_all_documents(self, collection):
        docs = self.db.collection(collection).stream()
        return [{**doc.to_dict(), 'id': doc.id} for doc in docs]

    def query_documents(self, collection, field, operator, value):
        docs = self.db.collection(collection).where(field, operator, value).stream()
        return [{**doc.to_dict(), 'id': doc.id} for doc in docs]