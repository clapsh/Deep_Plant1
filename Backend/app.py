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
from db_connect import (
    rds_db,
    Meat,
    User,
    DeepAging,
    Fresh,
    Heated,
    LabData,
    Tongue,
    Normal,
    Researcher,
    Manager,
)  # RDS Connect
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
            if id:
                return _make_response(
                    self._get_specific_meat_data(id), "http://localhost:3000"
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

        @self.app.route("/user/update", methods=["POST"])
        def update_specific_user_data():
            id = request.args.get("id")
            if id:
                return _make_response(
                    self._update_specific_user_data(id), "http://localhost:3000"
                )
            else:
                abort(400, description="No id Provided for Update User information")

    def transfer_data_to_rds(self):
        print("3. Trasfer DB Data [flask server -> RDS Database]", datetime.now(), "\n")
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
        normal_data = self.firestore_conn.temp_normal_data
        researcher_data = self.firestore_conn.temp_researcher_data
        manager_data = self.firestore_conn.temp_manager_data

        with self.app.app_context():
            for key, value in meat_data.items():
                try:
                    saveTime = convert2datetime(value.get("saveTime"), 1)
                    butcheryYmd = convert2datetime(value.get("butcheryYmd"), 2)

                    deepAging_data = value.get("deepAging")
                    deepAging = DeepAging(id=key, period=deepAging_data)

                    fresh_data = value.get("fresh")
                    fresh = Fresh(id=key, **fresh_data) if fresh_data else None

                    heated_data = value.get("heated")
                    heated = Heated(id=key, **heated_data) if heated_data else None

                    tongue_data = value.get("tongue")
                    tongue = Tongue(id=key, **tongue_data) if tongue_data else None

                    lab_data_data = value.get("lab_data")
                    lab_data = (
                        LabData(id=key, **lab_data_data) if lab_data_data else None
                    )

                    meat = Meat(
                        id=key,
                        email=value.get("email"),
                        saveTime=saveTime,
                        traceNumber=value.get("traceNumber"),
                        species=value.get("species"),
                        l_division=value.get("l_division"),
                        s_division=value.get("s_division"),
                        gradeNm=value.get("gradeNm"),
                        farmAddr=value.get("farmAddr"),
                        butcheryPlaceNm=value.get("butcheryPlaceNm"),
                        butcheryYmd=butcheryYmd,
                        deepAging=deepAging,
                        fresh=fresh,
                        heated=heated,
                        tongue=tongue,
                        lab_data=lab_data,
                    )

                    rds_db.session.merge(meat)
                    if deepAging is not None:
                        rds_db.session.merge(deepAging)
                    if fresh is not None:
                        rds_db.session.merge(fresh)
                    if heated is not None:
                        rds_db.session.merge(heated)
                    if tongue is not None:
                        rds_db.session.merge(tongue)
                    if lab_data is not None:
                        rds_db.session.merge(lab_data)
                    print(f"Meat data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding meat data: {e}\n")

            # 2. Update Normal data to RDS
            for key, value in normal_data.items():
                try:
                    lastLogin = convert2datetime(value.get("lastLogin"), 1)
                    meat_list = []
                    for m_id in value.get("meatList"):
                        try:

                            meat_list.append(Meat.query.get(m_id))
                        except:
                            print(f"Error adding Meat data - No meat id in DB{m_id}")
                    normal = Normal(
                        id=key,
                        meatList=meat_list,
                        lastLogin=lastLogin,
                        name=value.get("name"),
                        company=value.get("company"),
                        position=value.get("position"),
                    )
                    rds_db.session.merge(normal)

                    print(f"Normal data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding Normal data: {e}\n")

            # 3. Update Researcher data to RDS
            for key, value in researcher_data.items():
                try:
                    meat_list = []
                    revision_meat_list = []
                    lastLogin = convert2datetime(value.get("lastLogin"), 1)
                    for m_id in value.get("meatList"):
                        try:
                            meat_list.append(Meat.query.get(m_id))
                        except:
                            meat_list.append(None)

                    for m_id in value.get("revisionMeatList"):
                        try:
                            revision_meat_list.append(Meat.query.get(m_id))
                        except:
                            revision_meat_list.append(None)
                    researcher = Researcher(
                        id=key,
                        meatList=meat_list,
                        revisionMeatList=revision_meat_list,
                        lastLogin=lastLogin,
                        name=value.get("name"),
                        company=value.get("company"),
                        position=value.get("position"),
                    )
                    rds_db.session.merge(researcher)

                    print(f"Researcher data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding Researcher data: {e}\n")

            # 4. Update Manager data to RDS
            for key, value in manager_data.items():
                try:
                    lastLogin = convert2datetime(value.get("lastLogin"), 1)
                    manager = Manager(
                        id=key,
                        lastLogin=lastLogin,
                        name=value.get("name"),
                        company=value.get("company"),
                        position=value.get("position"),
                        pwd=value.get("password"),
                    )
                    rds_db.session.merge(manager)

                    print(f"Manager data added: {key} : {value}\n")
                except Exception as e:
                    print(f"Error adding Manager data: {e}\n")

            # 5. Session commit 완료
            rds_db.session.commit()
        self.firestore_conn.temp_meat_data = {}
        self.firestore_conn.temp_normal_data = {}
        self.firestore_conn.temp_researcher_data = {}
        self.firestore_conn.temp_manager_data = {}
        print(f"===============================================\n")

    def _get_meat_data(self):  # 전체 meat data 요청
        with self.app.app_context():
            meats = Meat.query.all()
            meat_list = []
            for meat in meats:
                meat_dict = self._to_dict(meat)

                # Update this part to convert each model instance to dictionary
                meat_dict["deepAging"] = self._to_dict(meat.deepAging)
                meat_dict["fresh"] = self._to_dict(meat.fresh)
                meat_dict["heated"] = self._to_dict(meat.heated)
                meat_dict["tongue"] = self._to_dict(meat.tongue)
                meat_dict["lab_data"] = self._to_dict(meat.lab_data)

                # imagePath field
                meat_dict[
                    "meat_imagePath"
                ] = f"https://deep-plant-flask-server.s3.ap-northeast-2.amazonaws.com/meats/{meat_dict['id']}"
                meat_dict[
                    "qr_imagePath"
                ] = f"https://deep-plant-flask-server.s3.ap-northeast-2.amazonaws.com/qr_codes/{meat_dict['id']}"
                meat_list.append(meat_dict)
            return jsonify(meat_list)

    def _get_specific_meat_data(self, id):  # 특정 관리번호 meat data 요청
        with self.app.app_context():
            meat = Meat.query.get(id)
            if meat is None:
                abort(404, description="No meat data found with the given ID")
            else:
                meat_dict = self._to_dict(meat)

                # Update this part to convert each model instance to dictionary
                meat_dict["deepAging"] = self._to_dict(meat.deepAging)
                meat_dict["fresh"] = self._to_dict(meat.fresh)
                meat_dict["heated"] = self._to_dict(meat.heated)
                meat_dict["tongue"] = self._to_dict(meat.tongue)
                meat_dict["lab_data"] = self._to_dict(meat.lab_data)

                # imagePath field
                meat_dict[
                    "imagePath"
                ] = f"https://deep-plant-flask-server.s3.ap-northeast-2.amazonaws.com/{self.s3_conn.folder}/{meat_dict['id']}.png"
                return jsonify(meat_dict)

    def _get_range_meat_data(self, offset, count):  # 날짜를 기준으로 특정 범위의 meat data 요청
        offset = int(offset)
        count = int(count)
        meat_data = (
            Meat.query.order_by(Meat.saveTime.desc())
            .offset(offset * count)
            .limit(count)
            .all()
        )
        return [self._to_dict(data) for data in meat_data]

    def _get_specific_user_data(self, id):  # 특정 ID의 유저정보 요청
        with self.app.app_context():
            # 1. Fetch
            user_data = User.query.get(id)

            # 2. If no user data is found with the given ID
            if user_data is None:
                abort(404, description="No user data was found with the given ID")

            # 3. Convert the SQLAlchemy User instance to a dictionary
            user_dict = self._to_dict(user_data)

            # 4. If the user type is 'normal' or 'researcher', convert meat list from SQLAlchemy objects to dictionaries
            if user_data.type in ["normal", "researcher"]:
                user_dict["meatList"] = [
                    self._to_dict(meat) for meat in user_data.meatList
                ]
                if user_data.type == "researcher":
                    user_dict["revisionMeatList"] = [
                        self._to_dict(meat) for meat in user_data.revisionMeatList
                    ]

            return jsonify(user_dict)

    def _get_user_data(self):  # 모든 유저 정보 반환
        with self.app.app_context():
            # 1. 모든 유저 정보 가져오기
            all_users = User.query.all()

            # 2. 구분해 반환 예정
            user_data_by_type = {"normal": [], "researcher": [], "manager": []}

            # 3. Convert
            for user in all_users:
                user_dict = self._to_dict(user)

                if user.type in ["normal", "researcher"]:
                    user_dict["meatList"] = [
                        self._to_dict(meat) for meat in user.meatList
                    ]
                    if user.type == "researcher":
                        user_dict["revisionMeatList"] = [
                            self._to_dict(meat) for meat in user.revisionMeatList
                        ]

                user_data_by_type[user.type].append(user_dict)

            return jsonify(user_data_by_type)

    def _update_specific_meat_data(self, id):  # 특정 육류 데이터 수정(db data만)
        # 전제: 관리번호는 죽어도 수정되지 않는다!!!
        # 1. 데이터 Valid Check
        if not request.json:
            abort(400, description="No data sent for update")

        # 2. Data 받기
        update_data = request.json

        with self.app.app_context():
            # 3. 육류 DB 체크
            meat = Meat.query.get(id)

            if meat is None:
                abort(404, description="No meat data found with the given ID")

            # Update RDS
            for field, new_value in update_data.items():
                if hasattr(meat, field):
                    if field == "saveTime":
                        new_value = convert2datetime(new_value, 1)
                    elif field == "butcheryYmd":
                        new_value = convert2datetime(new_value, 2)
                    # Update this part to handle the case of associated tables
                    if field in ["deepAging", "fresh", "heated", "tongue", "lab_data"]:
                        related_obj = getattr(meat, field)
                        if related_obj is None:
                            abort(
                                400,
                                description=f"No related data found for field '{field}'",
                            )
                        for subfield, new_subvalue in new_value.items():
                            if hasattr(related_obj, subfield):
                                setattr(related_obj, subfield, new_subvalue)
                            else:
                                raise BadRequest(
                                    f"Subfield '{subfield}' not in {field.capitalize()}"
                                )
                    else:
                        setattr(meat, field, new_value)
                else:
                    raise BadRequest(f"Field '{field}' not in Meat")

            rds_db.session.commit()

            return jsonify(self._to_dict(meat))

    def _update_specific_meat_image(self, id, folder):  # 특정 육류 이미지 데이터 수정
        # Axios 라이브러리 post을 이용해 저장한 파일을 첨부했을 경우에 이용되는 API
        # 1. 파일이 없을 경우
        if "file" not in request.files:
            abort(400, description="No file part")

        file = request.files["file"]

        # 2. 파일 확인
        if file.filename == "":
            abort(400, description="No file selected for uploading")

        if file:
            # 1. Flask local server에 저장
            filename = secure_filename(f"{id}.png")
            file.save(os.path.join(UPDATE_IMAGE_FOLDER_PATH, filename))

            # 2. S3에 저장
            new_filepath = os.path.join(UPDATE_IMAGE_FOLDER_PATH, filename)
            success = self.s3_conn.update_image(new_filepath, id, folder)

            if not success:
                print(f"Failed to upload new image for ID: {id}")
        else:
            abort(400, description="Invalid file type, Only PNG files are allowed.")

    def _update_specific_user_data(self, id):  # 특정 유저 정보 업데이트
        # 1. 유효성 확인
        if not request.json:
            abort(400, description="No data sent for update")
        update_data = request.json

        with self.app.app_context():
            # 2. User 확인
            user = User.query.get(id)
            if user is None:
                abort(404, description="No user data was found with the given ID")

            # 3. type 확인
            change_to_type = update_data.get("type")  # Change_to_type

            if change_to_type:
                # 기존 유저 정보 탐색
                old_user_data = self._to_dict(user)

                # 유저 DB 이동
                if change_to_type == "normal":
                    fields_to_ignore = ["revisionMeatList"]
                    old_user_data = {
                        k: v
                        for k, v in old_user_data.items()
                        if k not in fields_to_ignore
                    }
                    new_user = Normal(**old_user_data)
                elif change_to_type == "researcher":
                    new_user = Researcher(**old_user_data)
                elif change_to_type == "manager":
                    new_user = Manager(**old_user_data)
                else:
                    abort(400, description="Invalid type")

                # 혹시 추가 데이터로 Update를 원한다면 추가
                for field, new_value in update_data.items():
                    if field == "lastLogin":
                        new_value = convert2datetime(new_value, 1)
                    if hasattr(new_user, field):
                        setattr(new_user, field, new_value)
                    else:
                        abort(400, description=f"Field '{field}' not in User")

                rds_db.session.delete(user)  # delete old user
                rds_db.session.add(new_user)  # add new user

            else:
                # Changing에 없다면 데이터 추가
                for field, new_value in update_data.items():
                    if hasattr(user, field):
                        setattr(user, field, new_value)
                    else:
                        abort(400, description=f"Field '{field}' not in User")

            rds_db.session.commit()
            response_data = new_user if change_to_type else old_user_data
            return jsonify(self._to_dict(response_data))

    def _to_dict(self, model):  # database 생성 메서드
        if model is None:
            return None
        return {c.name: getattr(model, c.name) for c in model.__table__.columns}

    def _create_sqlalchemy_uri(self):  # uri 생성
        aws_db = self.config["aws_db"]
        return f"postgresql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}"

    def run(self, host="0.0.0.0", port=8080):  # server 구동
        self.app.run(host=host, port=port)


def _make_response(data, url):  # For making response
    response = make_response(data)
    response.headers["Access-Control-Allow-Origin"] = url
    return response


def convert2datetime(date_string, format):
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


@login_manager.user_loader
def load_user(user_id):
    return Manager.query.get(user_id)


@myApp.app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = hashlib.sha256(
        data["password"].encode()
    ).hexdigest()  # hash 화 후 저장
    user = Manager(
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
    user = Manager.query.filter_by(id=data["id"]).first()
    if user and user.pwd == hashlib.sha256(data["password"].encode()).hexdigest():
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@myApp.app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


def scheduler_function():
    myApp.firestore_conn.transferDbData()  # (FireStore -> Flask Server)
    myApp.s3_conn.transferImageData("meats")  # (Flask server(images folder) -> S3)
    myApp.s3_conn.transferImageData("qr_codes")  # (Flask server(images folder) -> S3)
    myApp.transfer_data_to_rds()  #  (FireStore -> RDS)


# Server 구동
if __name__ == "__main__":
    # 1. Background Fetch Data (FireStore -> Flask Server) , 30sec 주기
    scheduler = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
    scheduler.add_job(
        scheduler_function, "interval", minutes=0.5
    )  # 주기적 데이터 전송 firebase -> flask server
    scheduler.start()

    # 2. Flask 서버 실행

    myApp.run()
