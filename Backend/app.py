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
from utils import *

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
            load_initial_data(rds_db)  # Set initial tables

        # 2. Firebase Config
        self.firestore_conn = firebase_connect.FireBase_()

        # 3. S3 Database Config
        self.s3_conn = s3_connect.S3Bucket()

        # 4. meat database 요청 Routing
        @self.app.route("/meat/get", methods=["GET"])  # 1. 전체 meat data 요청
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

        @self.app.route("/meat/add", methods=["POST"])  # 3. meat db 추가(OpenAPI 정보)
        def add_specific_meat_data():
            return _make_response(
                self._add_specific_meat_data(), "http://localhost:3000"
            )

        @self.app.route(
            "/meat/add/sensory_eval", methods=["POST"]
        )  # 3. meat db 추가(OpenAPI 정보)
        def add_specific_sensory_data():
            return _make_response(
                self._add_specific_sensory_data(), "http://localhost:3000"
            )

        @self.app.route(
            "/meat/add/heatedmeat_eval", methods=["POST"]
        )  # 3. meat db 추가(OpenAPI 정보)
        def add_specific_heatedmeat_sensory_data():
            return _make_response(
                self._add_specific_heatedmeat_sensory_data(), "http://localhost:3000"
            )

        @self.app.route(
            "/meat/add/probexpt_data", methods=["POST"]
        )  # 3. meat db 추가(OpenAPI 정보)
        def add_specific_probexpt_data():
            return _make_response(
                self._add_specific_probexpt_data(), "http://localhost:3000"
            )

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

    # 1. Meat DB API
    def _get_specific_meat_data(self, id):
        result = get_meat(rds_db, id)
        if result:
            return jsonify(get_meat(rds_db, id))
        else:
            return abort(404, description=f"No Meat data found for {id}")

    def _get_specific_meat_data_part(self, part_id):  # part_id가 id에 해당하는 육류 id 목록 반환
        len = Meat.query.count()
        meat_list = self._get_range_meat_data(0, len)["meat_list"]

        # Using list comprehension to filter meat_list
        part_id_meat_list = [meat for meat in meat_list if part_id in meat]
        result = []
        for i in part_id_meat_list:
            result.append(self._get_specific_meat_data(i).get_json())
        return jsonify({part_id: result})

    def _get_range_meat_data(self, offset, count):  #
        offset = int(offset)
        count = int(count)
        meat_data = (
            Meat.query.options()
            .order_by(Meat.createdAt.desc())
            .offset(offset * count)
            .limit(count)
            .all()
        )
        meat_result = [data.id for data in meat_data]
        result = {"len": Meat.query.count(), "meat_list": meat_result}
        return jsonify(result)

    def _get_meat_data(self):
        return self._get_range_meat_data(0, Meat.query.count())["meat_list"]

    def _add_specific_meat_data(self):  # 육류 데이터 추가
        # 1. Data Valid Check
        if not request.json:
            abort(400, description="No data sent for update")
        # 2. 기본 데이터 받아두기
        data = request.get_json()
        id = data.get("id")

        with self.app.app_context():
            meat = Meat.query.get(id)  # DB에 있는 육류 정보
            if id == None:  # 1. 애초에 id가 없는 request
                abort(404, description="No ID data sent for update")
            # 1. 신규 육류 데이터 생성
            try:
                # 1. 육류 데이터 추가
                new_meat = create_meat(rds_db, data)
                rds_db.session.merge(new_meat)

                # 2. Firestore -> S3
                self.transfer_folder_image(id, new_meat, "qr_codes")
                rds_db.session.commit()

            except Exception as e:
                rds_db.session.rollback()
                abort(404, description=e)
            finally:
                rds_db.session.close()
            return jsonify(id)

    def _add_specific_sensory_data(self):
        # 1. Data Valid Check
        if not request.json:
            abort(400, description="No data sent for update")
        # 2. 기본 데이터 받아두기
        data = request.get_json()
        id = data.get("id")
        seqno = data.get("seqno")
        deepAging_data = data.get("deepAging")
        data.pop("deepAging", None)
        with self.app.app_context():
            if id == None:  # 1. 애초에 id가 없는 request
                abort(404, description="No ID data sent for update")
            sensory_eval = SensoryEval.query.filter_by(
                id=id, seqno=seqno
            ).first()  # DB에 있는 육류 정보
            try:
                if deepAging_data is not None:  # 가공육 관능검사
                    if sensory_eval:  # 기존 Deep Aging을 수정하는 경우
                        deepAgingId = sensory_eval.deepAgingId
                    else:  # 새로운 Deep aging을 추가하는 경우
                        new_DeepAging = create_DeepAging(rds_db, deepAging_data)
                        deepAgingId = new_DeepAging.deepAgingId
                        rds_db.session.flush(new_DeepAging)

                    new_SensoryEval = create_SensoryEval(
                        rds_db, data, seqno, id, new_DeepAging.deepAgingId
                    )
                    rds_db.session.merge(new_SensoryEval)
                else:  # 신선육 관능검사
                    deepAgingId = None
                    new_SensoryEval = create_SensoryEval(
                        rds_db, data, seqno, id, deepAgingId
                    )
                    rds_db.session.merge(new_SensoryEval)

                self.transfer_folder_image(
                    f"{id}-{seqno}", new_SensoryEval, "sensory_evals"
                )
                rds_db.session.commit()
            except Exception as e:
                rds_db.session.rollback()
                abort(404, description=e)
            finally:
                rds_db.session.close()
            return jsonify(id)

    def _add_specific_heatedmeat_sensory_data(self):
        # 1. Data Valid Check
        if not request.json:
            abort(400, description="No data sent for update")
        # 2. 기본 데이터 받아두기
        data = request.get_json()
        id = data.get("id")
        seqno = data.get("seqno")
        with self.app.app_context():
            if id == None:  # 1. 애초에 id가 없는 request
                abort(404, description="No ID data sent for update")
            try:
                new_HeatedmeatSensoryEval = create_HeatedmeatSensoryEval(
                    rds_db, data, seqno, id
                )
                rds_db.session.merge(new_HeatedmeatSensoryEval)

                self.transfer_folder_image(
                    f"{id}-{seqno}",
                    new_HeatedmeatSensoryEval,
                    "heatedmeat_sensory_evals",
                )
                rds_db.session.commit()
            except Exception as e:
                rds_db.session.rollback()
                abort(404, description=e)
            finally:
                rds_db.session.close()
            return jsonify(id)

    def _add_specific_probexpt_data(self):
        # 1. Data Valid Check
        if not request.json:
            abort(400, description="No data sent for update")
        # 2. 기본 데이터 받아두기
        data = request.get_json()
        id = data.get("id")
        seqno = data.get("seqno")
        with self.app.app_context():
            if id == None:  # 1. 애초에 id가 없는 request
                abort(404, description="No ID data sent for update")
            try:
                new_ProbexptData = create_ProbexptData(rds_db, data, seqno, id)
                rds_db.session.add(new_ProbexptData)
                rds_db.session.commit()
            except Exception as e:
                rds_db.session.rollback()
                abort(404, description=e)
            finally:
                rds_db.session.close()
            return jsonify(id)

    # 2. User DB API
    # 3. Utils

    def transfer_meat_image(self, id, new_meat):
        """
        Firebase Storage -> S3
        Params
        1. id: meat.id
        2. new_meat: New Meat data object
        Return
        None
        """
        try:
            if not self.firestore_conn.firestorage2server(
                "meats", id
            ) or not self.s3_conn.server2s3("meats", id):
                new_meat.meat_imagePath = None
                raise Exception("Failed to transfer meat image")

            new_meat.meat_imagePath = self.s3_conn.get_image_url(
                self.s3_conn.bucket, f"meats/{id}"
            )

            if not self.firestore_conn.firestorage2server(
                "qr_codes", id
            ) or not self.s3_conn.server2s3("qr_codes", id):
                new_meat.qr_imagePath = None
                raise Exception("Failed to transfer QR code image")

            new_meat.qr_imagePath = self.s3_conn.get_image_url(
                self.s3_conn.bucket, f"qr_codes/{id}"
            )
        except Exception as e:
            rds_db.session.rollback()
            abort(404, description=e)

    def transfer_folder_image(self, id, new_meat, folder):
        """
        Firebase Storage -> S3
        Params
        1. id: meat.id
        2. new_meat: New Meat data object
        Return
        None
        """
        try:
            if not self.firestore_conn.firestorage2server(
                f"{folder}", id
            ) or not self.s3_conn.server2s3(f"{folder}", id):
                new_meat.imagePath = None
                raise Exception("Failed to transfer meat image")

            new_meat.imagePath = self.s3_conn.get_image_url(
                self.s3_conn.bucket, f"{folder}/{id}"
            )
        except Exception as e:
            rds_db.session.rollback()
            abort(404, description=e)

    def _create_sqlalchemy_uri(self):  # uri 생성
        aws_db = self.config["aws_db"]
        return f"postgresql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}"

    def run(self, host="0.0.0.0", port=8080):  # server 구동
        self.app.run(host=host, port=port)


def _make_response(data, url):  # For making response
    response = make_response(data)
    response.headers["Access-Control-Allow-Origin"] = url
    return response


# Init RDS
myApp = MyFlaskApp(db_config.config)

# 1. Login/Register Routing
login_manager = LoginManager()
login_manager.init_app(myApp.app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@myApp.app.route("/user/register", methods=["POST"])
def register():
    data = request.get_json()
    user = create_user(rds_db, data, "new")
    # 3. Session end
    try:
        rds_db.session.add(user)
    except Exception as e:
        return jsonify({"message": f"Error Occur {e}"})
    rds_db.session.commit()
    return jsonify({"message": "Registered successfully"}), 200


@myApp.app.route("/user/update", methods=["POST"])
def update():
    data = request.get_json()
    user = create_user(rds_db, data, "old")
    # 3. Session end
    if user is None:
        return jsonify({"message": "User Update Failed"}), 404
    rds_db.session.commit()
    return jsonify({"message": "User Update successfully"}), 200


@myApp.app.route("/user/duplicate_check", methods=["GET"])
def duplicate_check():
    id = request.args.get("id")
    user = User.query.filter_by(userId=id).first()
    print(user)
    if user is None:
        return jsonify({f"message": f"No duplicated Item (userId:{id})"}), 200
    else:
        return jsonify({"message": f"Duplicated Item (userId:{id}"}), 404


@myApp.app.route("/user/login", methods=["GET"])
def login():
    id = request.args.get("id")
    user = User.query.filter_by(userId=id).first()
    if user is None:
        return jsonify({f"message": "No user data in Database(userId:{id})"}), 404
    user.loginAt = datetime.now()
    rds_db.session.commit()
    user_info = to_dict(user)
    user_info["type"] = UserType.query.filter_by(id=user_info["type"]).first().name

    return jsonify({"message": "Logged in successfully", "user": user_info}), 200


@myApp.app.route("/user/logout", methods=["GET"])
def logout():
    id = request.args.get("id")
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
