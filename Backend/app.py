from flask import Flask, make_response  # Flask Server import
import os  # Port Number assignment
from apscheduler.schedulers.background import (
    BackgroundScheduler,
)  # Background running function
import firebase_connect  # Firebase Connect
import s3_connect  # S3 Connect
import keyId  # Key data in this Backend file
from flask_sqlalchemy import SQLAlchemy  # For implement RDS database in server
import db_config  # For implement RDS database in server
from db_connect import *  # RDS Connect
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
from flask import make_response  # For making response in flask
from werkzeug.exceptions import BadRequest  # For making Error response
from werkzeug.utils import secure_filename  # For checking file name from react page
from datetime import datetime

"""
flask run --host=0.0.0.0 --port=8080
 ~/.pyenv/versions/deep_plant_backend/bin/python app.py
"""
UPDATE_IMAGE_FOLDER_PATH = "./update_images/"


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
            load_initial_data(rds_db) # Set initial tables

        # 2. Firebase Config
        self.firestore_conn = firebase_connect.FireBase_()

        # 3. S3 Database Config
        self.s3_conn = s3_connect.S3Bucket()

        # 4. meat database 요청 Routing
        @self.app.route("/meat", methods=["GET"])  # 1. 전체 meat data 요청
        def get_meat_data():
            id = request.args.get("id")
            offset = request.args.get("offset")
            count = request.args.get("count")
            part_id = request.args.get("part_id")
            if id:
                return _make_response(
                    self._get_specific_meat_data(id), "http://localhost:3000"
                )
            elif part_id:
                return _make_response(
                    self._get_specific_meat_data_part(part_id), "http://localhost:3000"
                )
            elif offset and count:
                return _make_response(
                    self._get_range_meat_data(offset, count), "http://localhost:3000"
                )
            else:
                return _make_response(self._get_meat_data(), "http://localhost:3000")

        @self.app.route("/meat/update", methods=["POST"])  # 3. 특정 육류 데이터 수정(db data만)
        def update_specific_meat_data():
            id = request.args.get("id")
            if id:
                return _make_response(
                    self._update_specific_meat_data(id), "http://localhost:3000"
                )
            else:
                abort(400, description="No id Provided for update data")

        @self.app.route("/meat/upload_image", methods=["POST"])  # 4. 특정 육류 이미지 데이터 수정
        def update_specific_meat_image():
            id = request.args.get("id")
            folder = request.args.get("folder")  # meats 이거나 qr_codes
            if id:
                return _make_response(
                    self._update_specific_meat_image(id, folder),
                    "http://localhost:3000",
                )
            else:
                abort(400, description="No id Provided for upload image")

        @self.app.route("/meat/delete", methods=["POST"])  # 5. meat data 삭제
        def delete_meat_data():
            id = request.args.get("id")
            offset = request.args.get("offset")
            count = request.args.get("count")
            if id:  # 특정 id 삭제
                return _make_response(
                    self._delete_specific_meat_data(id), "http://localhost:3000"
                )
            elif offset and count:  # savetime 기준으로 offset * count 부터 count개 삭제
                return _make_response(
                    self._delete_range_meat_data(offset, count), "http://localhost:3000"
                )
            else:  # 전체 육류 데이터 삭제
                return _make_response(self._delete_meat_data(), "http://localhost:3000")

        # 5. user database 요청 Routiong
        @self.app.route("/user", methods=["GET"])  # 1. 특정 유저 id의 유저 정보 요청
        def get_specific_user_data():
            id = request.args.get("id")
            if id:
                return _make_response(
                    self._get_specific_user_data(id), "http://localhost:3000"
                )
            else:
                return _make_response(self._get_user_data(), "http://localhost:3000")

        @self.app.route("/user/update", methods=["POST"])  # 2. 특정 유저 정보 업데이트
        def update_specific_user_data():
            id = request.args.get("id")
            if id:
                return _make_response(
                    self._update_specific_user_data(id), "http://localhost:3000"
                )
            else:
                abort(400, description="No id Provided for Update User information")
    
    # 1. Meat DB API

    # 2. User DB API
    # 3. Utils
    def _to_dict(self, model):  # database 생성 메서드
        if model is None:
            return None
        # Also includes related objects
        result = {c.name: getattr(model, c.name) for c in model.__table__.columns}

        return result

    def _create_sqlalchemy_uri(self):  # uri 생성
        aws_db = self.config["aws_db"]
        return f"postgresql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}"

    def run(self, host="0.0.0.0", port=8080):  # server 구동
        self.app.run(host=host, port=port)


def _make_response(data, url):  # For making response
    response = make_response(data)
    response.headers["Access-Control-Allow-Origin"] = url
    return response


def convert2datetime(date_string, format):  # For converting date string to datetime
    if format == 1:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    elif format == 2:
        return datetime.strptime(date_string, "%Y%m%d")
    else:
        return date_string


# Init RDS
myApp = MyFlaskApp(db_config.config)

# 1. Login/Register Routing
login_manager = LoginManager()
login_manager.init_app(myApp.app)


def validate_type(type_id):
    """Check if the provided type_id exists in the UserType table."""
    user_type = UserType.query.get(type_id)
    if user_type is None:
        abort(400, description="Invalid user type.")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@myApp.app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = hashlib.sha256(
        data["password"].encode()
    ).hexdigest()  # hash 화 후 저장
    # 1. Validate user type
    validate_type(data["type"])

    # 2. Input data
    user = User(
        userId=data["userId"],
        createdAt=data["createdAt"],
        updatedAt=data["updatedAt"],
        loginAt=data["loginAt"],
        name=data["name"],
        company=data["company"],
        jobTitle=data["jobTitle"],
        password=hashed_password,
        type=data["type"],  # 0: Normal, 1: Researcher, 2: Manager, 그 이외는 오류
    )

    # 3. Session end
    rds_db.session.add(user)
    rds_db.session.commit()
    return jsonify({"message": "Registered successfully"}), 201


@myApp.app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(id=data["userId"]).first()
    if user and user.pwd == hashlib.sha256(data["password"].encode()).hexdigest():
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@myApp.app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


def scheduler_function():  # 일정 주기마다 실행하는 함수
    myApp.firestore_conn.transferDbData()  # (FireStore -> Flask Server)
    myApp.s3_conn.transferImageData("meats")  # (Flask server(images folder) -> S3)
    myApp.s3_conn.transferImageData("qr_codes")  # (Flask server(images folder) -> S3)
    myApp.transfer_data_to_rds()  #  (FireStore -> RDS)


# Server 구동
if __name__ == "__main__":
    # 2. Flask 서버 실행
    myApp.run()
