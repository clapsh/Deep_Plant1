from flask import Flask  # Flask Server import
import os  # Port Number assignment
from apscheduler.schedulers.background import (
    BackgroundScheduler,
)  # Background running function
import firebase_connect  # Firebase Connect
import s3_connect  # S3 Connect
import keyId  # Key data in this Backend file
from flask_sqlalchemy import SQLAlchemy  # For implement RDS database in server
import db_config  # For implement RDS database in server
from db_connect import rds_db, Meat, User1, User2, User3  # RDS Connect
import json  # For Using Json files
from flask_login import login_user, logout_user, current_user, LoginManager  # For Login
from flask import Blueprint, request, jsonify  # For web request
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)  # For password hashing
import hashlib  # For password hashing
from datetime import datetime  # 시간 출력용
from flask import abort  # For data non existence

"""
flask run --host=0.0.0.0 --port=8080
 ~/.pyenv/versions/deep_plant_backend/bin/python app.py
"""


class MyFlaskApp:
    def __init__(self, config):
        self.app = Flask(__name__)

        # 1. RDS Config
        self.config = config
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self._create_sqlalchemy_uri()
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Init RDS
        rds_db.init_app(self.app)
        with self.app.app_context():
            rds_db.create_all()  # This will create tables according to the models

        # 2. Firebase Config
        self.firestore_conn = firebase_connect.FireBase_()

        # 3. S3 Database Config
        self.s3_conn = s3_connect.S3Bucket(keyId.s3_folder_name)

        # 4. meat database 요청 Routing
        @self.app.route("/meat", methods=["GET"])  # 1. 전체 meat data 요청
        def get_meat_data():
            return self._get_meat_data()

        @self.app.route("/meat/<id>", methods=["GET"])  # 2. 특정 관리번호 meat data 요청
        def get_specific_meat_data(id):
            return self._get_specific_meat_data(id)
        
        # 5. user database 요청 Routiong
        @self.app.route("/user/<id>",methods=["GET"]) # 1. 특정 유저 id의 유저 정보 요청
        def get_specific_user_data(id):
            return self._get_specific_user_data(id)

    def transfer_data_to_rds(self):
        print("Trasfer DB Data [flask server -> RDS Database]", datetime.now(),"\n")
        """
        Flask server -> RDS
        Firebase에서 새로 저장된 데이터들은 각각 다음의 변수에 저장됩니다.
        self.firestore_conn.temp_user1_data <= user1 database
        self.firestore_conn.temp_user2_data <= user2 database
        self.firestore_conn.temp_user3_data <= user3 database
        self.firestore_conn.temp_meat_data <= meat database
        """
        # 1. Update Meat data to RDS
        meat_data = self.firestore_conn.temp_meat_data
        user1_data = self.firestore_conn.temp_user1_data
        user2_data = self.firestore_conn.temp_user2_data
        user3_data = self.firestore_conn.temp_user3_data

        with self.app.app_context():
            for key, value in meat_data.items():
                try:
                    meat = Meat(
                        id=key,
                        email=value.get("email"),
                        saveTime=value.get("saveTime"),
                        traceNumber=value.get("traceNumber"),
                        species=value.get("species"),
                        l_division=value.get("l_division"),
                        s_division=value.get("s_division"),
                        gradeNm=value.get("gradeNm"),
                        farmAddr=value.get("farmAddr"),
                        butcheryPlaceNm=value.get("butcheryPlaceNm"),
                        butcheryYmd=value.get("butcheryYmd"),
                        deepAging=json.dumps(value.get("deepAging")),
                        fresh=json.dumps(value.get("fresh")),
                        heated=json.dumps(value.get("heated")),
                        tongue=json.dumps(value.get("tongue")),
                        lab_data=json.dumps(value.get("lab_data")),
                    )
                    rds_db.session.add(meat)
                    print(f"Meat data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding meat data: {e}\n")
            

            # 2. Update User1 data to RDS

            for key, value in user1_data.items():
                try:
                    user = User1(
                        id=key,
                        meatList=value.get("meatList"),
                        lastLogin=value.get("lastLogin"),
                        name=value.get("name"),
                        company=value.get("company"),
                        position=value.get("position"),
                    )
                    rds_db.session.add(user)
                    
                    print(f"User1 data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding User1 data: {e}\n")

            # 3. Update User2 data to RDS

            for data in user2_data.items():
                try:
                    user = User2(
                        id=key,
                        meatList=data.get("meatList"),
                        lastLogin=data.get("lastLogin"),
                        name=data.get("name"),
                        company=data.get("company"),
                        position=data.get("position"),
                        revisionMeatList=data.get("revisionMeatList"),
                    )
                    rds_db.session.add(user)
                    
                    print(f"User2 data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding User2 data: {e}\n")

            # 4. Update User3 data to RDS

            for key, value in user3_data.items():
                try:
                    user = User3(
                        id=key,
                        lastLogin=value.get("lastLogin"),
                        name=value.get("name"),
                        company=value.get("company"),
                        position=value.get("position"),
                        pwd=value.get("password"),
                    )
                    rds_db.session.add(user)
                    
                    print(f"User3 data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding User3 data: {e}\n")

            # 5. Session commit 완료
            rds_db.session.commit()
        self.firestore_conn.temp_meat_data = {}
        self.firestore_conn.temp_user1_data = {}
        self.firestore_conn.temp_user2_data = {}
        self.firestore_conn.temp_user3_data = {}
        print(f"===============================================\n")

    def _get_meat_data(self):  # 전체 meat data 요청
        with self.app.app_context():
            meats = Meat.query.all()
            meat_list = []
            for meat in meats:
                meat_list.append(
                    {
                        "id": meat.id,
                        "email": meat.email,
                        "saveTime": meat.saveTime,
                        "traceNumber": meat.traceNumber,
                        "species": meat.species,
                        "l_division": meat.l_division,
                        "s_division": meat.s_division,
                        "gradeNm": meat.gradeNm,
                        "farmAddr": meat.farmAddr,
                        "butcheryPlaceNm": meat.butcheryPlaceNm,
                        "butcheryYmd": meat.butcheryYmd,
                        "deepAging": json.loads(
                            meat.deepAging
                        ),  # assuming the data was saved as JSON string
                        "fresh": json.loads(
                            meat.fresh
                        ),  # assuming the data was saved as JSON string
                        "heated": json.loads(
                            meat.heated
                        ),  # assuming the data was saved as JSON string
                        "tongue": json.loads(
                            meat.tongue
                        ),  # assuming the data was saved as JSON string
                        "lab_data": json.loads(
                            meat.lab_data
                        ),  # assuming the data was saved as JSON string
                    }
                )
            return jsonify(meat_list)

    def _get_specific_meat_data(self, id):  # 특정 관리번호 meat data 요청
        with self.app.app_context():
            meat = Meat.query.get(id)
            if meat is None:
                abort(404, description="No meat data found with the given ID")
            else:
                return jsonify(
                    {
                        "id": meat.id,
                        "email": meat.email,
                        "saveTime": meat.saveTime,
                        "traceNumber": meat.traceNumber,
                        "species": meat.species,
                        "l_division": meat.l_division,
                        "s_division": meat.s_division,
                        "gradeNm": meat.gradeNm,
                        "farmAddr": meat.farmAddr,
                        "butcheryPlaceNm": meat.butcheryPlaceNm,
                        "butcheryYmd": meat.butcheryYmd,
                        "deepAging": json.loads(
                            meat.deepAging
                        ),  # assuming the data was saved as JSON string
                        "fresh": json.loads(
                            meat.fresh
                        ),  # assuming the data was saved as JSON string
                        "heated": json.loads(
                            meat.heated
                        ),  # assuming the data was saved as JSON string
                        "tongue": json.loads(
                            meat.tongue
                        ),  # assuming the data was saved as JSON string
                        "lab_data": json.loads(
                            meat.lab_data
                        ),  # assuming the data was saved as JSON string
                    }
                )

    def _get_specific_user_data(self,id): # 특정 유저 id의 유저 정보 요청
        with self.app.app_context():
            #1. Fetch
            user1_data = User1.query.filter_by(id=id).first()
            user2_data = User2.query.filter_by(id=id).first()
            user3_data = User3.query.filter_by(id=id).first()

            #2. Init
            result = {}

            #3. add
            if user1_data:
                result["user1_data"] = self._to_dict(user1_data)

            if user2_data:
                result["user2_data"] = self._to_dict(user2_data)

            if user3_data:
                result["user3_data"] = self._to_dict(user3_data)

            return jsonify(result)

    def _to_dict(self, obj): # ditionary 생성 function
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    
    def _create_sqlalchemy_uri(self):  # uri 생성
        aws_db = self.config["aws_db"]
        return f"postgresql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}"

    def run(self, host="0.0.0.0", port=8080):  # server 구동
        self.app.run(host=host, port=port)


# Init RDS
myApp = MyFlaskApp(db_config.config)

# 1. Login/Register Routing
login_manager = LoginManager()
login_manager.init_app(myApp.app)


@login_manager.user_loader
def load_user(user_id):
    return User3.query.get(user_id)


@myApp.app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = hashlib.sha256(
        data["password"].encode()
    ).hexdigest()  # hash 화 후 저장
    user = User3(
        id=data["id"],
        name=data["name"],
        company=data["company"],
        position=data["position"],
        pwd=hashed_password,
    )
    rds_db.session.add(user)
    rds_db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201


@myApp.app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User3.query.filter_by(id=data["id"]).first()
    if user and user.pwd == hashlib.sha256(data["password"].encode()).hexdigest():
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@myApp.app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


# 3. user(1,2,3) database 요청 Routing


# Server 구동
if __name__ == "__main__":
    # 1. Background Fetch Data (FireStore -> Flask Server) , 30sec 주기
    scheduler = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
    scheduler.add_job(
        myApp.firestore_conn.transferDbData, "interval", minutes=0.5
    )  # 주기적 데이터 전송 firebase -> flask server

    # 2. Send data to S3 storage (Flask server(images folder) -> S3), 30sec
    scheduler.add_job(
        myApp.s3_conn.transferImageData, "interval", minutes=0.5
    )  # 주기적 이미지 데이터 전송 flask server -> S3

    # 3. Send data to RDS (FireStore -> RDS), 30sec
    scheduler.add_job(
        myApp.transfer_data_to_rds, "interval", minutes=0.6
    )  # 주기적 Json Data 전송 flask server -> RDS
    scheduler.start()

    # 3. Flask 서버 실행
    myApp.run()
