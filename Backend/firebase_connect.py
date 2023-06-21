import firebase_admin # Firestore init

# 1. Firestore 연동
def firestore_connection(key_path): # key_path는 "serviceAccountKey.json" 이어야함
    cred = firebase_admin.credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)
    firebase_db = firebase_admin.client()

# 2. Firestore에서 data 가져오기 (Firestore -> Flask Server)

# 3. Firestore에 data 넣기 (Firestore <- Flask Server)

# 4. Firestorage에서 data(image) 가져오기 (Storage -> Flask Server)

# 5. Firestorage로 data(image) 넣기 (Storage <- Flask Server)
