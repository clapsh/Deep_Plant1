from flask import send_file
import firebase_admin  # Firestore init
from firebase_admin import firestore, storage
import keyId
import io
import os

KEY_PATH = "serviceAccountKey.json"


# FireBase Data(FireStore & FireStorage)
class FireBase_:
    def __init__(self):
        # 1. Making FireStore Connection
        cred = firebase_admin.credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)
        self.firebase_db = firestore.client()
        self.fix_data_state = dict()  # 바뀐게 있는 데이터 저장

        # 2. Making FireStorage Connection
        self.bucket = storage.bucket(keyId.firebase_bucket_address)

        # 3. Making Buffer Data (Firebase -> Flask Server )
        self.temp_data = dict()  # 버퍼
        self.temp_user1_data = dict() # 일반
        self.temp_user2_data = dict() # 직원
        self.temp_user3_data = dict() # 관리자
        self.temp_meat_data = dict()

    def print_flask_database(self):
        print(f"transfer user-1 data: {self.temp_user1_data}")
        print(f"transfer user-2 data: {self.temp_user2_data}")
        print(f"transfer user-3 data: {self.temp_user3_data}")
        print(f"transfer meat data: {self.temp_meat_data}")

    def transferDbData(self):
        # 1. 바뀐 데이터 확인
        self.firestoreCheck()

        # 2. 데이터 가져오기 (firestore -> Flask Server)
        if self.fix_data_state["fix_data"]["users_1"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("users_1")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_user1_data = self.temp_data
        if self.fix_data_state["fix_data"]["users_2"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("users_2")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_user2_data = self.temp_data
        if self.fix_data_state["fix_data"]["users_3"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("users_3")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_user3_data = self.temp_data
        if self.fix_data_state["fix_data"]["meat"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("meat")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_meat_data = self.temp_data
            # 3. fire storage -> server
            self.firestorage2server()

        # 3. 데이터 AWS RDS, S3에 저장하기(Flask Server -> S3 or RDS)
        self.print_flask_database()

    def firestoreCheck(self):  # Firestore Data 바뀐게 있는지 확인하는 method
        # 1. 0-0-0-0-0 document에서 바뀐 데이터 수합
        doc_ref = self.firebase_db.collection("meat").document("0-0-0-0-0")
        self.fix_data_state = doc_ref.get().to_dict()

        # 2. 바뀐 데이터 수합했으면 비워야 한다.
        doc_ref.update({"fix_data":{"users_1": [], "users_2": [], "users_3": [], "meat": []}})

    def firestore2server(
        self, collection
    ):  # Firestore에서 data 가져오기 (Firestore -> Flask Server)
        self.temp_data = dict()
        doc_ref = self.firebase_db.collection(collection)
        items = self.fix_data_state["fix_data"][
            collection
        ]  # users database -> uid 목록, meat database -> 관리번호 목록
        # 1. 바뀌었다고 한 id 대로 데이터 가져오기
        for i in items:
            doc = doc_ref.document(i).get().to_dict()
            self.temp_data[i] = doc

    def firestorage2server(self):
        # 'meat' 컬렉션의 문서 ID가 있는 리스트를 가져옵니다.
        items = self.fix_data_state["fix_data"]["meat"]

        # 저장할 이미지 디렉토리가 없다면 생성합니다.
        os.makedirs('images', exist_ok=True)

        for item_id in items:
            # Firebase Storage에서 해당 파일을 찾아 blob으로 가져옵니다.
            blob = self.bucket.blob(f"{item_id}.png")

            # blob이 존재하는지 확인하고 존재하면 파일로 저장합니다.
            if blob.exists():
                blob.download_to_filename(f"./images/{item_id}.png")
            else:
                print(f"No such file: {item_id}.png")
        
    def server2firestore(self):  # Firestore에 data 넣기 (Firestore <- Flask Server)
        pass

    def server2firestorage(self):
        pass
