from flask import Flask, make_response  # Flask Server import
import os  # Port Number assignment
from apscheduler.schedulers.background import (
    BackgroundScheduler,
)  # Background running function
import firebase_connect  # Firebase Connect
import s3_connect  # S3 Connect
import keyId  # Key data in this Backend file
from flask_sqlalchemy import SQLAlchemy  # For implement RDS database in server
from sqlalchemy import func, case, nullslast

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
from datetime import datetime, timedelta  # 시간 출력용
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
        @self.app.route("/data", methods=["GET"])
        def get_db_data():
            return _make_response(jsonify(get_db_data_()), "http://localhost:3000")

        @self.app.route("/meat/get", methods=["GET"])  # 1. 전체 meat data 요청
        def get_meat_data():
            id = request.args.get("id")
            offset = request.args.get("offset")
            count = request.args.get("count")
            part_id = request.args.get("part_id")
            start = request.args.get("start")
            end = request.args.get("end")
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
                    self._get_range_meat_data(offset, count, start, end),
                    "http://localhost:3000",
                )

            else:
                return _make_response(self._get_meat_data(), "http://localhost:3000")

        @self.app.route("/meat/statistic", methods=["GET"])
        def get_statistic_meat_data():
            id = request.args.get("id")
            statisticType = safe_int(request.args.get("type"))
            if id:  # 1. 특정 육류 정보에 대한 통계
                pass
            else:  # 2. 전체에 대한 통계
                if statisticType == 0:  # 1. 신선육, 숙성육 비율(소,돼지,전체)
                    return _make_response(
                        self._get_num_of_processed_raw(),
                        "http://localhost:3000",
                    )
                elif statisticType == 1:  # 2. 소, 돼지 개수
                    return _make_response(
                        self._get_num_of_cattle_pig(),
                        "http://localhost:3000",
                    )
                elif statisticType == 2:  # 3. 대분류 부위 별 개수(소, 돼지)
                    return _make_response(
                        self._get_num_of_primal_part(),
                        "http://localhost:3000",
                    )
                elif statisticType == 3:  # 4. 농장 지역 별 개수(소,돼지)
                    return _make_response(
                        self._get_num_by_farmAddr(),
                        "http://localhost:3000",
                    )
                else:
                    return _make_response(
                        abort(404, description="Wrong data in type params"),
                        "http://localhost:3000",
                    )

        @self.app.route("/meat/user", methods=["GET"])
        def get_user_meat_data():
            userId = request.args.get("userId")
            userType = request.args.get("userType")
            if userId:
                return _make_response(
                    self._get_userId_meat_data(userId), "http://localhost:3000"
                )
            elif userType:
                return _make_response(
                    self._get_userType_meat_data(userType), "http://localhost:3000"
                )
            else:
                return _make_response(
                    self._get_user_meat_data(), "http://localhost:3000"
                )

        @self.app.route("/meat/status", methods=["GET"])
        def get_status_meat_data():
            statusType_value = request.args.get("statusType")
            offset = request.args.get("offset")
            count = request.args.get("count")
            start = request.args.get("start")
            end = request.args.get("end")

            if statusType_value:
                if offset and count:
                    return _make_response(
                        self._get_range_status_meat_data(
                            statusType_value, offset, count, start, end
                        ),
                        "http://localhost:3000",
                    )
                else:
                    return _make_response(
                        self._get_status_meat_data(statusType_value),
                        "http://localhost:3000",
                    )
            else:
                return _make_response(
                    self._get_all_status_meat_data(),
                    "http://localhost:3000",
                )

        @self.app.route("/meat/add", methods=["POST"])  # 3. meat db 추가(OpenAPI 정보)
        def add_specific_meat_data():
            return _make_response(
                self._add_specific_meat_data(), "http://localhost:3000"
            )

        @self.app.route("/meat/add/deep_aging_data", methods=["POST"])
        def add_specific_deep_aging_data():
            return _make_response(
                self._add_specific_deep_aging_meat_data(), "http://localhost:3000"
            )

        @self.app.route("/meat/confirm", methods=["GET"])
        def confirm_specific_meat_data():
            id = request.args.get("id")
            return _make_response(
                self._confirm_specific_meat_data(id), "http://localhost:3000"
            )

        @self.app.route("/meat/reject", methods=["GET"])
        def reject_specific_meat_data():
            id = request.args.get("id")
            return _make_response(
                self._reject_specific_meat_data(id), "http://localhost:3000"
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

        @self.app.route("/meat/delete", methods=["POST", "GET"])  # 5. meat data 삭제
        def delete_meat_data():
            id = request.args.get("id")
            if id:  # 특정 id 삭제
                return _make_response(
                    self._delete_specific_meat_data(id), "http://localhost:3000"
                )
            else:  # 전체 육류 데이터 삭제
                return _make_response(
                    self._delete_range_meat_data(), "http://localhost:3000"
                )

    # 1. Meat DB API
    def _get_specific_meat_data(self, id):
        result = get_meat(rds_db, id)
        if result:
            return jsonify(get_meat(rds_db, id))
        else:
            return abort(404, description=f"No Meat data found for {id}")

    def _get_specific_meat_data_part(self, part_id):  # part_id가 id에 해당하는 육류 id 목록 반환
        meats_with_statusType_2 = Meat.query.filter_by(statusType=2).all()

        meat_list = []
        for meat in meats_with_statusType_2:
            meat_list.append(meat.id)

        # Using list comprehension to filter meat_list
        part_id_meat_list = [meat for meat in meat_list if part_id in meat]
        return jsonify({part_id: part_id_meat_list})

    def _get_range_meat_data(self, offset, count, start, end):
        offset = int(offset)
        count = int(count)
        start = convert2datetime(start, 1)
        end = convert2datetime(end, 1)
        query = (
            Meat.query.options()
            .order_by(Meat.createdAt.desc())
            .offset(offset * count)
            .limit(count)
        )
        if start is not None and end is not None:
            query = query.filter(Meat.createdAt.between(start, end))

        meat_data = query.all()
        meat_result = {}
        id_result = [data.id for data in meat_data]
        for id in id_result:
            meat_result[id] = get_meat(rds_db, id)
            userTemp = get_User(rds_db, meat_result[id].get("userId"))
            if userTemp:
                meat_result[id]["name"] = userTemp.get("name")
                meat_result[id]["company"] = userTemp.get("company")
                meat_result[id]["type"] = userTemp.get("type")
            else:
                meat_result[id]["name"] = userTemp
                meat_result[id]["company"] = userTemp
                meat_result[id]["type"] = userTemp
            del meat_result[id]["processedmeat"]
            del meat_result[id]["rawmeat"]

        result = {
            "DB Total len": Meat.query.count(),
            "meat_id_list": id_result,
            "meat_dict": meat_result,
        }

        return jsonify(result)

    def _get_meat_data(self):
        response = self._get_range_meat_data(0, Meat.query.count())
        data = response.get_json()
        return jsonify(data["meat_dict"])

    def _get_status_meat_data(self, varified):
        try:
            varified = int(varified)
        except Exception as e:
            abort(404, description=e)
        meats_db = Meat.query.all()
        meat_list = []
        if varified == 2:  # 승인
            varified = "승인"
        elif varified == 1:  # 반려
            varified = "반려"
        elif varified == 0:
            varified = "대기중"
        for meat in meats_db:
            temp = get_meat(rds_db, meat.id)
            del temp["processedmeat"]
            del temp["rawmeat"]
            if temp.get("statusType") == varified:
                meat_list.append(temp)
        return jsonify({f"{varified}": meat_list}), 200

    def _get_range_status_meat_data(self, varified, offset, count, start, end):
        offset = int(offset)
        count = int(count)
        varified = int(varified)
        start = convert2datetime(start, 1)
        end = convert2datetime(end, 1)
        # Base query
        query = (
            Meat.query.options()
            .filter_by(statusType=varified)
            .order_by(Meat.createdAt.desc())
            .offset(offset * count)
            .limit(count)
        )

        # Date Filter
        if start is not None and end is not None:
            query = query.filter(Meat.createdAt.between(start, end))

        result = []
        meat_data = query.all()

        for meat in meat_data:
            temp = get_meat(rds_db, meat.id)
            userTemp = get_User(rds_db, temp.get("userId"))
            if userTemp:
                temp["name"] = userTemp.get("name")
                temp["company"] = userTemp.get("company")
                temp["type"] = userTemp.get("type")
            else:
                temp["name"] = userTemp
                temp["company"] = userTemp
                temp["type"] = userTemp
            del temp["processedmeat"]
            del temp["rawmeat"]
            result.append(temp)
        if varified == 2:
            varified = "승인"
        elif varified == 1:
            varified = "반려"
        else:
            varified = "대기중"
        return (
            jsonify({f"{varified}": result}),
            200,
        )

    def _get_all_status_meat_data(self):
        result = {}
        result["승인"] = self._get_status_meat_data("2")[0].get_json().get("승인")
        result["반려"] = self._get_status_meat_data("1")[0].get_json().get("반려")
        result["대기중"] = self._get_status_meat_data("0")[0].get_json().get("대기중")
        return jsonify(result), 200

    def _get_userId_meat_data(self, userId):
        try:
            meats = Meat.query.filter_by(userId=userId).all()
            if meats:
                result = []
                for meat in meats:
                    temp = get_meat(rds_db, meat.id)
                    del temp["processedmeat"]
                    del temp["rawmeat"]
                    result.append(temp)
                return jsonify(result), 200
            else:
                return jsonify({"message": "No meats found for the given userId."}), 404
        except Exception as e:
            abort(404, description=str(e))

    def _get_userType_meat_data(self, userType):
        try:
            userType_value = UserType.query.filter_by(name=userType).first()
            if userType_value:
                userType = userType_value.id
            else:
                raise Exception(
                    "No userType in DB  (Normal, Researcher, Manager, None)"
                )
            # First, get all users of the given user type
            users = User.query.filter_by(type=userType).all()
            user_ids = [user.userId for user in users]

            # Then, get all meats that were created by the users of the given user type
            meats = Meat.query.filter(Meat.userId.in_(user_ids)).all()

            if meats:
                result = []
                for meat in meats:
                    temp = get_meat(rds_db, meat.id)
                    del temp["processedmeat"]
                    del temp["rawmeat"]
                    result.append(temp)
                return jsonify(result), 200
            else:
                return (
                    jsonify({"message": "No meats found for the given userType."}),
                    404,
                )
        except Exception as e:
            abort(404, description=str(e))

    def _get_user_meat_data(self):
        try:
            users = User.query.all()

            user_meats = {}
            for user in users:
                response, _ = self._get_userId_meat_data(user.userId)
                user_meats[user.userId] = response.get_json()
            return jsonify(user_meats), 200
        except Exception as e:
            abort(404, description=str(e))

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
            if meat:
                if meat.statusType == 2:
                    abort(404, description="Already confirmed meat data")
            # 1. 신규 육류 데이터 생성
            try:
                # 1. 육류 데이터 추가
                new_meat = create_meat(rds_db, data)
                new_meat.statusType = 0
                rds_db.session.merge(new_meat)
                # 2. Firestore -> S3
                self.transfer_folder_image(id, new_meat, "qr_codes")
                rds_db.session.commit()

            except Exception as e:
                rds_db.session.rollback()
                abort(404, description=e)
            finally:
                rds_db.session.close()
            return jsonify(id), 200

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
            meat = Meat.query.get(id)  # DB에 있는 육류 정보
            if id == None:  # 1. 애초에 id가 없는 request
                abort(404, description="No ID data sent for update")

            sensory_eval = SensoryEval.query.filter_by(
                id=id, seqno=seqno
            ).first()  # DB에 있는 육류 정보
            try:
                if deepAging_data is not None:  # 가공육 관능검사
                    if meat:  # 승인 정보 확인
                        if meat.statusType != 2:
                            abort(404, description="Not confirmed meat data")
                    if sensory_eval:  # 기존 Deep Aging을 수정하는 경우
                        deepAgingId = sensory_eval.deepAgingId
                        new_SensoryEval = create_SensoryEval(
                            rds_db, data, seqno, id, deepAgingId
                        )
                        rds_db.session.merge(new_SensoryEval)
                    else:  # 새로운 Deep aging을 추가하는 경우
                        new_DeepAging = create_DeepAging(rds_db, deepAging_data)
                        deepAgingId = new_DeepAging.deepAgingId
                        rds_db.session.add(new_DeepAging)
                        rds_db.session.commit()
                        new_SensoryEval = create_SensoryEval(
                            rds_db, data, seqno, id, deepAgingId
                        )
                        rds_db.session.merge(new_SensoryEval)
                else:  # 신선육 관능검사
                    if meat:  # 수정하는 경우
                        if meat.statusType == 2:
                            abort(404, description="Already confirmed meat data")
                    deepAgingId = None
                    new_SensoryEval = create_SensoryEval(
                        rds_db, data, seqno, id, deepAgingId
                    )
                    rds_db.session.merge(new_SensoryEval)
                    meat.statusType = 0
                    rds_db.session.merge(meat)

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
            meat = Meat.query.get(id)  # DB에 있는 육류 정보
            if meat:  # 승인 정보 확인
                if meat.statusType != 2:
                    abort(404, description="Not confirmed meat data")
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
            meat = Meat.query.get(id)  # DB에 있는 육류 정보
            if meat:  # 승인 정보 확인
                if meat.statusType != 2:
                    abort(404, description="Not confirmed meat data")
            if id == None:  # 1. 애초에 id가 없는 request
                abort(404, description="No ID data sent for update")
            try:
                new_ProbexptData = create_ProbexptData(rds_db, data, seqno, id)
                rds_db.session.merge(new_ProbexptData)
                rds_db.session.commit()
            except Exception as e:
                rds_db.session.rollback()
                abort(404, description=e)
            finally:
                rds_db.session.close()
            return jsonify(id)

    def _add_specific_deep_aging_meat_data(self):
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
            meat = Meat.query.get(id)  # DB에 있는 육류 정보
            if id == None:  # 1. 애초에 id가 없는 request
                abort(404, description="No ID data sent for update")
            sensory_eval = SensoryEval.query.filter_by(
                id=id, seqno=seqno
            ).first()  # DB에 있는 육류 정보
            try:
                if deepAging_data is not None:
                    if meat:  # 승인 정보 확인
                        if meat.statusType != 2:
                            abort(404, description="Not confirmed meat data")
                    if sensory_eval:  # 기존 Deep Aging을 수정하는 경우
                        deepAgingId = sensory_eval.deepAgingId
                        existing_DeepAging = DeepAging.query.get(deepAgingId)
                        if existing_DeepAging:
                            for key, value in deepAging_data.items():
                                setattr(existing_DeepAging, key, value)
                        else:
                            abort(
                                404, description="No deep aging data found for update"
                            )
                    else:  # 새로운 Deep aging을 추가하는 경우
                        new_DeepAging = create_DeepAging(rds_db, deepAging_data)
                        deepAgingId = new_DeepAging.deepAgingId
                        rds_db.session.add(new_DeepAging)
                        rds_db.session.commit()
                        new_SensoryEval = create_SensoryEval(
                            rds_db, data, seqno, id, deepAgingId
                        )
                        rds_db.session.merge(new_SensoryEval)
                    rds_db.session.commit()
                else:
                    abort(404, description="No deepaging data in request")
            except Exception as e:
                rds_db.session.rollback()
                abort(404, description=e)
            finally:
                rds_db.session.close()
            return jsonify(id)

    def _confirm_specific_meat_data(self, id):
        meat = Meat.query.get(id)  # DB에 있는 육류 정보
        if meat:
            meat.statusType = 2
            rds_db.session.merge(meat)
            rds_db.session.commit()
            return jsonify(id), 200
        else:
            abort(404, description="No data in Meat DB")

    def _reject_specific_meat_data(self, id):
        meat = Meat.query.get(id)  # DB에 있는 육류 정보
        if meat:
            meat.statusType = 1
            rds_db.session.merge(meat)
            rds_db.session.commit()
            return jsonify(id), 200
        else:
            abort(404, description="No data in Meat DB")

    def _delete_specific_meat_data(self, id):
        with self.app.app_context():
            # 1. 육류 DB 체크
            meat = Meat.query.get(id)

            if meat is None:
                return f"No meat data found with the given ID: {id}"
            try:
                sensory_evals = SensoryEval.query.filter_by(id=id).all()
                heatedmeat_evals = HeatedmeatSensoryEval.query.filter_by(id=id).all()
                probexpt_datas = ProbexptData.query.filter_by(id=id).all()
                for heatedmeat_eval in heatedmeat_evals:
                    seqno = heatedmeat_eval.seqno
                    rds_db.session.delete(heatedmeat_eval)
                    self.s3_conn.delete_image(
                        "heatedmeat_sensory_evals", f"{id}-{seqno}"
                    )
                    rds_db.session.commit()

                for probexpt_data in probexpt_datas:
                    rds_db.session.delete(probexpt_data)
                rds_db.session.commit()

                for sensory_eval in sensory_evals:
                    seqno = sensory_eval.seqno
                    rds_db.session.delete(sensory_eval)
                    self.s3_conn.delete_image("sensory_evals", f"{id}-{seqno}")
                    rds_db.session.commit()

                rds_db.session.delete(meat)
                self.s3_conn.delete_image("qr_codes", f"{id}")
                rds_db.session.commit()
                return id
            except Exception as e:
                rds_db.session.rollback()
                return str(e)

    def _delete_range_meat_data(self):
        # 1. Data Valid Check
        if not request.json:
            abort(400, description="No data sent for Deletion")
        # 2. 기본 데이터 받아두기
        data = request.get_json()
        delete_list = list(data.get("delete_id"))
        delete_success = []
        delete_failed = []
        try:
            for data in delete_list:
                result = self._delete_specific_meat_data(data)
                if isinstance(
                    result, int
                ):  # if the deletion was successful, result would be the id
                    delete_success.append(result)
                else:  # if the deletion failed, result would be an error message
                    delete_failed.append({"id": id, "reason": result})
            return (
                jsonify(
                    {"delete_success": delete_list, "delete_failed": delete_failed}
                ),
                200,
            )
        except Exception as e:
            abort(404, description=3)

    # 2. Statistic API
    def _get_num_of_processed_raw(self):
        # Subquery to find meats which have processed data
        processed_meats_subquery = (
            rds_db.session.query(Meat.id)
            .join(SensoryEval)
            .filter(SensoryEval.seqno > 0)
            .subquery()
        )
        processed_meats_select = processed_meats_subquery.select()
        # 1. Category.specieId가 0이면서 SensoryEval.seqno 값이 0인 데이터, 1인 데이터
        fresh_cattle_count = (
            Meat.query.join(Category)
            .filter(Category.speciesId == 0, ~Meat.id.in_(processed_meats_select))
            .count()
        )
        processed_cattle_count = (
            Meat.query.join(Category)
            .filter(Category.speciesId == 0, Meat.id.in_(processed_meats_select))
            .count()
        )

        # 2. Category.specieId가 1이면서 SensoryEval.seqno 값이 0인 데이터, 1인 데이터
        fresh_pig_count = (
            Meat.query.join(Category)
            .filter(Category.speciesId == 1, ~Meat.id.in_(processed_meats_select))
            .count()
        )
        processed_pig_count = (
            Meat.query.join(Category)
            .filter(Category.speciesId == 1, Meat.id.in_(processed_meats_select))
            .count()
        )

        # 3. 전체 데이터에서 SensoryEval.seqno 값이 0인 데이터, 1인 데이터
        fresh_meat_count = Meat.query.filter(
            ~Meat.id.in_(processed_meats_select)
        ).count()
        processed_meat_count = Meat.query.filter(
            Meat.id.in_(processed_meats_select)
        ).count()
        # Returning the counts in JSON format
        return (
            jsonify(
                {
                    "cattle_counts": {
                        "raw": fresh_cattle_count,
                        "processed": processed_cattle_count,
                    },
                    "pig_counts": {
                        "raw": fresh_pig_count,
                        "processed": processed_pig_count,
                    },
                    "total_counts": {
                        "raw": fresh_meat_count,
                        "processed": processed_meat_count,
                    },
                }
            ),
            200,
        )

    def _get_num_of_cattle_pig(self):
        cow_count = Meat.query.join(Category).filter(Category.speciesId == 0).count()
        pig_count = Meat.query.join(Category).filter(Category.speciesId == 1).count()
        return jsonify({"cattle_count": cow_count, "pig_count": pig_count}), 200

    def _get_num_of_primal_part(self):
        # 1. Category.specieId가 0일때 해당 Category.primalValue 별로 육류의 개수를 추출
        count_by_primal_value_beef = (
            rds_db.session.query(Category.primalValue, func.count(Meat.id))
            .join(Meat, Meat.categoryId == Category.id)
            .filter(Category.speciesId == 0)
            .group_by(Category.primalValue)
            .all()
        )

        # 2. Category.specieId가 1일때 해당 Category.primalValue 별로 육류의 개수를 추출
        count_by_primal_value_pork = (
            rds_db.session.query(Category.primalValue, func.count(Meat.id))
            .join(Meat, Meat.categoryId == Category.id)
            .filter(Category.speciesId == 1)
            .group_by(Category.primalValue)
            .all()
        )

        # Returning the counts in JSON format
        return (
            jsonify(
                {
                    "beef_counts_by_primal_value": dict(count_by_primal_value_beef),
                    "pork_counts_by_primal_value": dict(count_by_primal_value_pork),
                }
            ),
            200,
        )

    def _get_num_by_farmAddr(self):
        regions = [
            "강원",
            "경기",
            "경남",
            "경북",
            "광주",
            "대구",
            "대전",
            "부산",
            "서울",
            "세종",
            "울산",
            "인천",
            "전남",
            "전북",
            "제주",
            "충남",
            "충북",
        ]
        result = {}

        for speciesId in [0, 1]:  # 0 for cattle, 1 for pig
            region_counts = {}
            for region in regions:
                count = (
                    Meat.query.join(Category)
                    .filter(
                        Category.speciesId == speciesId,
                        Meat.farmAddr.like(f"%{region}%"),
                    )
                    .count()
                )
                region_counts[region] = count
            if speciesId == 0:
                result["cattle_counts_by_region"] = region_counts
            else:
                result["pig_counts_by_region"] = region_counts

        # For total data
        total_region_counts = {}
        for region in regions:
            count = Meat.query.filter(Meat.farmAddr.like(f"%{region}%")).count()
            total_region_counts[region] = count
        result["total_counts_by_region"] = total_region_counts

        return jsonify(result), 200

    # 3. Utils

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
            rds_db.session.merge(new_meat)
            rds_db.session.commit()
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


# 2. User DB API
@myApp.app.route("/user", methods=["GET"])
def get_user_data():
    userId = request.args.get("userId")
    if userId:
        return _make_response(_get_users_by_userId(userId), "http://localhost:3000")
    else:
        return _make_response(_get_users_by_type(), "http://localhost:3000")


def _get_users_by_userId(userId):
    result = get_User(rds_db, userId)
    if result is None:
        abort(404, description=f"No user data about user Id({userId})")
    else:
        return jsonify(result), 200


def _get_users_by_type():
    # UserType 별로 분류될 유저 정보를 담을 딕셔너리
    user_dict = {}

    # 모든 유저 정보를 조회
    users = User.query.all()

    # 조회된 유저들에 대하여
    for user in users:
        # 해당 유저의 UserType을 조회
        user_type = UserType.query.get(user.type).name

        # user_dict에 해당 UserType key가 없다면, 새로운 리스트 생성
        if user_type not in user_dict:
            user_dict[user_type] = []

        # UserType에 해당하는 key의 value 리스트에 유저 id 추가
        user_dict[user_type].append(user.userId)

    return jsonify(user_dict)


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
    if user is None:
        return 200
    else:
        return 404


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

    return jsonify(user_info), 200


@myApp.app.route("/user/logout", methods=["GET"])
def logout():
    id = request.args.get("id")
    return 200


def scheduler_function():  # 일정 주기마다 실행하는 함수
    myApp.firestore_conn.transferDbData()  # (FireStore -> Flask Server)
    myApp.s3_conn.transferImageData("meats")  # (Flask server(images folder) -> S3)
    myApp.s3_conn.transferImageData("qr_codes")  # (Flask server(images folder) -> S3)
    myApp.transfer_data_to_rds()  #  (FireStore -> RDS)


# Server 구동
if __name__ == "__main__":
    # 2. Flask 서버 실행
    myApp.run()
