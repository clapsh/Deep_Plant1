import firebase_admin # Firestore init
from google.cloud import storage
import io
KEY_PATH =  "serviceAccountKey.json" 
# 1. Firestore 연동
class FireStore:
    def __init__(self):
        cred = firebase_admin.credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)
        self.firebase_db = firebase_admin.firestore.client()



# 2. firebase storage 연동
class FirebaseStorage:
    def __init__(self,bucket_name):
        self.storage_client = storage.Client.from_service_account_json(KEY_PATH)
        self.bucket = self.storage_client.get_bucket(bucket_name)

# 3. Firestore에서 data 가져오기 (Firestore -> Flask Server)

# 4. Firestore에 data 넣기 (Firestore <- Flask Server)

# 5. Firestorage에서 data(image) 가져오기 (Storage -> Flask Server)

# 6. Firestorage로 data(image) 넣기 (Storage <- Flask Server)
