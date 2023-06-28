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
from flask_login import login_user, logout_user, current_user, LoginManager # For Login 
from flask import Blueprint, request, jsonify # For web request
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing
import hashlib # For password hashing
from datetime import datetime # 시간 출력용

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

        # 2. Firebase Config
        self.firestore_conn = firebase_connect.FireBase_()

        # 3. S3 Database Config
        self.s3_conn = s3_connect.S3Bucket(keyId.s3_folder_name)

    def transfer_data_to_rds(self):
        print("Trasfer DB Data [flask server -> RDS Database]",datetime.now())
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
            for data in meat_data:
                meat = Meat(
                    id=data.get("id"),
                    email=data.get("email"),
                    saveTime=data.get("saveTime"),
                    traceNumber=data.get("traceNumber"),
                    species=data.get("species"),
                    l_division=data.get("l_division"),
                    s_division=data.get("s_division"),
                    gradeNm=data.get("gradeNm"),
                    farmAddr=data.get("farmAddr"),
                    butcheryPlaceNm=data.get("butcheryPlaceNm"),
                    butcheryYmd=data.get("butcheryYmd"),
                    deepAging=json.dumps(data.get("deepAging")),
                    fresh=json.dumps(data.get("fresh")),
                    heated=json.dumps(data.get("heated")),
                    tongue=json.dumps(data.get("tongue")),
                    lab_data=json.dumps(data.get("lab_data")),
                )
                rds_db.session.add(meat)

            # 2. Update User1 data to RDS
            
            for data in user1_data:
                user = User1(
                    id=data.get("id"),
                    meatList=data.get("meatList"),
                    lastLogin=data.get("lastLogin"),
                    name=data.get("name"),
                    company=data.get("company"),
                    position=data.get("position"),
                )
                rds_db.session.add(user)

            # 3. Update User2 data to RDS
            
            for data in user2_data:
                user = User2(
                    id=data.get("id"),
                    meatList=data.get("meatList"),
                    lastLogin=data.get("lastLogin"),
                    name=data.get("name"),
                    company=data.get("company"),
                    position=data.get("position"),
                    revisionMeatList=data.get("revisionMeatList"),
                )
                rds_db.session.add(user)

            # 4. Update User3 data to RDS
            
            for data in user3_data:
                user = User3(
                    id=data.get("id"),
                    lastLogin=data.get("lastLogin"),
                    name=data.get("name"),
                    company=data.get("company"),
                    position=data.get("company"),
                    pwd = data.get("password"),
                )
                rds_db.session.add(user)

            # 5. Session commit 완료
            rds_db.session.commit()

    def _create_sqlalchemy_uri(self):  # uri 생성
        aws_db = self.config["aws_db"]
        return f"mysql+pymysql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}?charset=utf8"

    def run(self, host="0.0.0.0", port=8080):  # server 구동
        self.app.run(host=host, port=port)


# Init RDS
myApp = MyFlaskApp(db_config.config)
rds_db.init_app(myApp.app)

# Routing

login_manager = LoginManager()
login_manager.init_app(myApp.app)

@login_manager.user_loader
def load_user(user_id):
    return User3.query.get(user_id)

@myApp.app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = hashlib.sha256(data["password"].encode()).hexdigest() #hash 화 후 저장
    user = User3(id=data["id"], name=data["name"], company=data["company"], position=data["position"], pwd=hashed_password)
    rds_db.session.add(user)
    rds_db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201

@myApp.app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    user = User3.query.filter_by(id=data["id"]).first()
    if user and user.pwd == hashlib.sha256(data["password"].encode()).hexdigest():
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@myApp.app.route("/logout", methods=['GET'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


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
        myApp.transfer_data_to_rds, "interval", minutes=0.5
    )  # 주기적 Json Data 전송 flask server -> RDS
    scheduler.start()

    # 3. Flask 서버 실행
    myApp.run()
