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
from flask_cors import CORS
import requests

"""
flask run --host=0.0.0.0 --port=8080
 ~/.pyenv/versions/deep_plant_backend/bin/python app.py
"""
UPDATE_IMAGE_FOLDER_PATH = "./update_images/"


class MyFlaskApp:
    def __init__(self, app, config):
        self.app = app
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

        @self.app.route("/predict", methods=["POST"])
        def predict_db_data():
            return _make_response(self._predict_db_data(), "http://localhost:3000")
        
        @self.app.route("/predict/get", methods=["GET"])
        def get_predict_db_data():
            id = request.args.get("id")
            seqno = request.args.get("seqno")
            return _make_response(self._get_predict_db_data(id,seqno), "http://localhost:3000")
        

        @self.app.route("/meat/get", methods=["GET"])  # 1. 전체 meat data 요청
        def get_meat_data():
            id = request.args.get("id")
            offset = request.args.get("offset")
            count = request.args.get("count")
            part_id = request.args.get("part_id")
            start = request.args.get("start")
            end = request.args.get("end")
            # filter
            farmAddr = safe_bool(request.args.get("farmAddr"))
            userId = safe_bool(request.args.get("userId"))
            type = safe_bool(request.args.get("type"))
            createdAt = safe_bool(request.args.get("createdAt"))
            statusType = safe_bool(request.args.get("statusType"))
            company = safe_bool(request.args.get("company"))
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
                    self._get_range_meat_data(
                        offset,
                        count,
                        start,
                        end,
                        farmAddr,
                        userId,
                        type,
                        createdAt,
                        statusType,
                        company,
                    ),
                    "http://localhost:3000",
                )

            else:
                return _make_response(self._get_meat_data(), "http://localhost:3000")

        @self.app.route("/meat/statistic", methods=["GET"])
        def get_statistic_meat_data():
            id = request.args.get("id")
            statisticType = safe_int(request.args.get("type"))
            seqno = request.args.get("seqno")
            start = safe_str(request.args.get("start"))
            end = safe_str(request.args.get("end"))
            if id:  # 1. 특정 육류 정보에 대한 통계
                return _make_response(
                    abort(404, description="Wrong data in type params"),
                    "http://localhost:3000",
                )
            else:  # 2. 전체에 대한 통계
                if statisticType == 0:  # 1. 신선육, 숙성육 비율(소,돼지,전체)
                    return _make_response(
                        self._get_num_of_processed_raw(start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 1:  # 2. 소, 돼지 개수
                    return _make_response(
                        self._get_num_of_cattle_pig(start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 2:  # 3. 대분류 부위 별 개수(소, 돼지)
                    return _make_response(
                        self._get_num_of_primal_part(start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 3:  # 4. 농장 지역 별 개수(소,돼지)
                    return _make_response(
                        self._get_num_by_farmAddr(start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 4:  # 5. 신선육 맛데이터 항목 별 평균, 최대, 최소치
                    return _make_response(
                        self._get_probexpt_of_rawmeat(start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 5:  # 6. 처리육 맛데이터 항목 별 평균, 최대, 최소치
                    return _make_response(
                        self._get_probexpt_of_processedmeat(seqno, start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 6:  # 6. 신선육에 따라 관능 데이터 각 항목 별 평균, 최대, 최소치
                    return _make_response(
                        self._get_senseval_of_rawmeat(start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 7:  # 6. 처리육에 따라 관능 데이터 각 항목 별 평균, 최대, 최소치
                    return _make_response(
                        self._get_senseval_of_processedmeat(seqno, start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 8:  # 7. 가열한 원육에 따라 관능 데이터 각 항목 별 평균, 최대, 최소치
                    return _make_response(
                        self._get_senseval_of_raw_heatedmeat(start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 9:  # 8. 가열한 처리육에 따라 관능 데이터 각 항목 별 평균, 최대, 최소치
                    return _make_response(
                        self._get_senseval_of_processed_heatedmeat(seqno, start, end),
                        "http://localhost:3000",
                    )
                elif statisticType == 10:  # 8. 가열한 처리육에 따라 맛 데이터 각 항목 별 평균, 최대, 최소치
                    return _make_response(
                        self._get_tongue_of_processedmeat(start, end),
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

        @self.app.route(
            "/meat/delete/deep_aging", methods=["POST", "GET"]
        )  # 5. meat data 삭제
        def delete_deep_aging_data():
            id = request.args.get("id")
            seqno = request.args.get("seqno")
            if id and seqno:
                return _make_response(
                    self._delete_specific_seqno_meat_data(id, seqno),
                    "http://localhost:3000",
                )
            else:
                return _make_response(
                    abort(404, description="Invalid id or seqno in URL"),
                    "http://localhost:3000",
                )

    # 1. Meat DB API
    def _get_specific_meat_data(self, id):
        result = get_meat(rds_db, id)
        if result:
            try:
                result["rawmeat_data_complete"] = (
                    all(
                        v is not None
                        for v in result["rawmeat"]["heatedmeat_sensory_eval"].values()
                    )
                    and all(
                        v is not None
                        for v in result["rawmeat"]["probexpt_data"].values()
                    )
                    and all(
                        v is not None
                        for v in result["rawmeat"]["sensory_eval"].values()
                    )
                )
            except:
                result["rawmeat_data_complete"] = False

            result["processedmeat_data_complete"] = {}
            for k, v in result["processedmeat"].items():
                try:
                    result["processedmeat_data_complete"][k] = all(
                        all(vv is not None for vv in inner_v.values())
                        for inner_v in v.values()
                    )
                except:
                    result["processedmeat_data_complete"][k] = False
            if not result["processedmeat_data_complete"]:
                result["processedmeat_data_complete"] = False

            return jsonify(result)
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

    def _get_range_meat_data(
        self,
        offset,
        count,
        start=None,
        end=None,
        farmAddr=None,
        userId=None,
        type=None,
        createdAt=None,
        statusType=None,
        company=None,
    ):
        offset = int(offset)
        count = int(count)
        start = convert2datetime(start, 1)
        end = convert2datetime(end, 1)
        # Base Query
        query = Meat.query.join(User, User.userId == Meat.userId)  # Join with User

        # Sorting and Filtering
        if farmAddr is not None:
            if farmAddr:  # true: 가나다순 정렬
                query = query.order_by(Meat.farmAddr.asc())
            else:  # false: 역순
                query = query.order_by(Meat.farmAddr.desc())
        if userId is not None:
            if userId:  # true: 알파벳 오름차순 정렬
                query = query.order_by(Meat.userId.asc())
            else:  # false: 알파벳 내림차순 정렬
                query = query.order_by(Meat.userId.desc())
        if type is not None:
            if type:  # true: 숫자 오름차순 정렬
                query = query.order_by(User.type.asc())
            else:  # false: 숫자 내림차순 정렬
                query = query.order_by(User.type.desc())
        if company is not None:
            if company:  # true: 가나다순 정렬
                query = query.order_by(User.company.asc())
            else:  # false: 역순
                query = query.order_by(User.company.desc())
        if createdAt is not None:
            if createdAt:  # true: 최신순
                query = query.order_by(Meat.createdAt.desc())
            else:  # false: 역순
                query = query.order_by(Meat.createdAt.asc())
        if statusType is not None:
            if statusType:  # true: 숫자 오름차순 정렬
                query = query.order_by(Meat.statusType.asc())
            else:  # false: 숫자 내림차순 정렬
                query = query.order_by(Meat.statusType.desc())

        # 기간 설정 쿼리
        if start is not None and end is not None:
            query = query.filter(Meat.createdAt.between(start, end))
        query = query.offset(offset * count).limit(count)

        # 탐색
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
            "id_list": id_result,
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

    def _get_range_status_meat_data(
        self, varified, offset, count, start=None, end=None
    ):
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
        )

        # Date Filter
        if start is not None and end is not None:
            query = query.filter(Meat.createdAt.between(start, end))

        query = query.offset(offset * count).limit(count)

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
        varified_id = varified
        if varified == 2:
            varified = "승인"
        elif varified == 1:
            varified = "반려"
        else:
            varified = "대기중"
        return (
            jsonify(
                {
                    "DB Total len": Meat.query.filter_by(
                        statusType=varified_id
                    ).count(),
                    f"{varified}": result,
                }
            ),
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
                    userTemp = get_User(rds_db, temp.get("userId"))
                    if userTemp:
                        temp["name"] = userTemp.get("name")
                    else:
                        temp["name"] = userTemp
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
                return jsonify({"delete Id": id})
            except Exception as e:
                rds_db.session.rollback()
                return e

    def _delete_specific_seqno_meat_data(self, id, seqno):
        with self.app.app_context():
            # 1. 육류 DB 체크
            meat = Meat.query.get(id)

            if meat is None:
                return f"No meat data found with the given ID: {id}"
            try:
                sensory_evals = SensoryEval.query.filter_by(id=id, seqno=seqno).all()
                heatedmeat_evals = HeatedmeatSensoryEval.query.filter_by(
                    id=id, seqno=seqno
                ).all()
                probexpt_datas = ProbexptData.query.filter_by(id=id, seqno=seqno).all()
                for heatedmeat_eval in heatedmeat_evals:
                    rds_db.session.delete(heatedmeat_eval)
                    self.s3_conn.delete_image(
                        "heatedmeat_sensory_evals", f"{id}-{seqno}"
                    )
                    rds_db.session.commit()

                for probexpt_data in probexpt_datas:
                    rds_db.session.delete(probexpt_data)
                rds_db.session.commit()

                for sensory_eval in sensory_evals:
                    rds_db.session.delete(sensory_eval)
                    self.s3_conn.delete_image("sensory_evals", f"{id}-{seqno}")
                    rds_db.session.commit()

                return jsonify({"delete Id": id, "delete Seqno": seqno})
            except Exception as e:
                rds_db.session.rollback()
                return e

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
                result = self._delete_specific_meat_data(data).get_json()
                if not isinstance(
                    result, str
                ):  # if the deletion was successful, result would be the id
                    delete_success.append(result.get("delete Id"))
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
    def _get_num_of_processed_raw(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

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
            .filter(
                Category.speciesId == 0,
                ~Meat.id.in_(processed_meats_select),
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .count()
        )
        processed_cattle_count = (
            Meat.query.join(Category)
            .filter(
                Category.speciesId == 0,
                Meat.id.in_(processed_meats_select),
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .count()
        )

        # 2. Category.specieId가 1이면서 SensoryEval.seqno 값이 0인 데이터, 1인 데이터
        fresh_pig_count = (
            Meat.query.join(Category)
            .filter(
                Category.speciesId == 1,
                ~Meat.id.in_(processed_meats_select),
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .count()
        )
        processed_pig_count = (
            Meat.query.join(Category)
            .filter(
                Category.speciesId == 1,
                Meat.id.in_(processed_meats_select),
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .count()
        )

        # 3. 전체 데이터에서 SensoryEval.seqno 값이 0인 데이터, 1인 데이터
        fresh_meat_count = Meat.query.filter(
            ~Meat.id.in_(processed_meats_select),
            Meat.createdAt.between(start, end),
            Meat.statusType == 2,
        ).count()

        processed_meat_count = Meat.query.filter(
            Meat.id.in_(processed_meats_select),
            Meat.createdAt.between(start, end),
            Meat.statusType == 2,
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

    def _get_num_of_cattle_pig(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

        cow_count = (
            Meat.query.join(Category)
            .filter(
                Category.speciesId == 0,
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .count()
        )
        pig_count = (
            Meat.query.join(Category)
            .filter(
                Category.speciesId == 1,
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .count()
        )
        return jsonify({"cattle_count": cow_count, "pig_count": pig_count}), 200

    def _get_num_of_primal_part(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")
        # 1. Category.specieId가 0일때 해당 Category.primalValue 별로 육류의 개수를 추출
        count_by_primal_value_beef = (
            rds_db.session.query(Category.primalValue, func.count(Meat.id))
            .join(Meat, Meat.categoryId == Category.id)
            .filter(
                Category.speciesId == 0,
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .group_by(Category.primalValue)
            .all()
        )

        # 2. Category.specieId가 1일때 해당 Category.primalValue 별로 육류의 개수를 추출
        count_by_primal_value_pork = (
            rds_db.session.query(Category.primalValue, func.count(Meat.id))
            .join(Meat, Meat.categoryId == Category.id)
            .filter(
                Category.speciesId == 1,
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
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

    def _get_num_by_farmAddr(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")
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
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
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
            count = Meat.query.filter(
                Meat.farmAddr.like(f"%{region}%"),
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            ).count()
            total_region_counts[region] = count
        result["total_counts_by_region"] = total_region_counts

        return jsonify(result), 200

    def _get_probexpt_of_rawmeat(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")
        # 각 필드의 평균값, 최대값, 최소값 계산
        stats = {}
        for field in ["sourness", "bitterness", "umami", "richness"]:
            avg = (
                rds_db.session.query(func.avg(getattr(ProbexptData, field)))
                .join(Meat, Meat.id == ProbexptData.id)
                .filter(
                    ProbexptData.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )
            max_value = (
                rds_db.session.query(func.max(getattr(ProbexptData, field)))
                .join(Meat, Meat.id == ProbexptData.id)
                .filter(
                    ProbexptData.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )
            min_value = (
                rds_db.session.query(func.min(getattr(ProbexptData, field)))
                .join(Meat, Meat.id == ProbexptData.id)
                .filter(
                    ProbexptData.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )

            # 실제로 존재하는 값들 찾기
            unique_values_query = (
                rds_db.session.query(getattr(ProbexptData, field))
                .join(Meat, Meat.id == ProbexptData.id)
                .filter(
                    ProbexptData.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .distinct()
            )
            unique_values = [value[0] for value in unique_values_query.all()]

            stats[field] = {
                "avg": avg,
                "max": max_value,
                "min": min_value,
                "unique_values": unique_values,
            }

        return jsonify(stats)

    def _get_probexpt_of_processedmeat(self, seqno, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

        # 각 필드의 평균값, 최대값, 최소값 계산
        stats = {}
        seqno = safe_int(seqno)
        if seqno:
            for field in ["sourness", "bitterness", "umami", "richness"]:
                avg = (
                    rds_db.session.query(func.avg(getattr(ProbexptData, field)))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                max_value = (
                    rds_db.session.query(func.max(getattr(ProbexptData, field)))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                min_value = (
                    rds_db.session.query(func.min(getattr(ProbexptData, field)))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )

                # 실제로 존재하는 값들 찾기
                unique_values_query = (
                    rds_db.session.query(getattr(ProbexptData, field))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .distinct()
                )
                unique_values = [value[0] for value in unique_values_query.all()]

                stats[field] = {
                    "avg": avg,
                    "max": max_value,
                    "min": min_value,
                    "unique_values": unique_values,
                }
        else:
            for field in ["sourness", "bitterness", "umami", "richness"]:
                avg = (
                    rds_db.session.query(func.avg(getattr(ProbexptData, field)))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                max_value = (
                    rds_db.session.query(func.max(getattr(ProbexptData, field)))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                min_value = (
                    rds_db.session.query(func.min(getattr(ProbexptData, field)))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )

                # 실제로 존재하는 값들 찾기
                unique_values_query = (
                    rds_db.session.query(getattr(ProbexptData, field))
                    .join(Meat, Meat.id == ProbexptData.id)
                    .filter(
                        ProbexptData.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .distinct()
                )
                unique_values = [value[0] for value in unique_values_query.all()]

                stats[field] = {
                    "avg": avg,
                    "max": max_value,
                    "min": min_value,
                    "unique_values": unique_values,
                }

        return jsonify(stats)

    def _get_senseval_of_rawmeat(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

        # 각 필드의 평균값, 최대값, 최소값 계산
        stats = {}
        for field in ["marbling", "color", "texture", "surfaceMoisture", "overall"]:
            avg = (
                rds_db.session.query(func.avg(getattr(SensoryEval, field)))
                .join(Meat, Meat.id == SensoryEval.id)
                .filter(
                    SensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )
            max_value = (
                rds_db.session.query(func.max(getattr(SensoryEval, field)))
                .join(Meat, Meat.id == SensoryEval.id)
                .filter(
                    SensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )
            min_value = (
                rds_db.session.query(func.min(getattr(SensoryEval, field)))
                .join(Meat, Meat.id == SensoryEval.id)
                .filter(
                    SensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )

            # 실제로 존재하는 값들 찾기
            unique_values_query = (
                rds_db.session.query(getattr(SensoryEval, field))
                .join(Meat, Meat.id == SensoryEval.id)
                .filter(
                    SensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .distinct()
            )
            unique_values = [value[0] for value in unique_values_query.all()]

            stats[field] = {
                "avg": avg,
                "max": max_value,
                "min": min_value,
                "unique_values": sorted(unique_values),
            }

        return jsonify(stats)

    def _get_senseval_of_processedmeat(self, seqno, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

        stats = {}
        seqno = safe_int(seqno)
        if seqno:
            # 각 필드의 평균값, 최대값, 최소값 계산
            for field in ["marbling", "color", "texture", "surfaceMoisture", "overall"]:
                avg = (
                    rds_db.session.query(func.avg(getattr(SensoryEval, field)))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                max_value = (
                    rds_db.session.query(func.max(getattr(SensoryEval, field)))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                min_value = (
                    rds_db.session.query(func.min(getattr(SensoryEval, field)))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )

                # 실제로 존재하는 값들 찾기
                unique_values_query = (
                    rds_db.session.query(getattr(SensoryEval, field))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .distinct()
                )
                unique_values = [
                    value[0]
                    for value in unique_values_query.all()
                    if value[0] is not None
                ]

                stats[field] = {
                    "avg": avg,
                    "max": max_value,
                    "min": min_value,
                    "unique_values": sorted(unique_values)
                    if unique_values
                    else unique_values,
                }
        else:
            # 각 필드의 평균값, 최대값, 최소값 계산
            for field in ["marbling", "color", "texture", "surfaceMoisture", "overall"]:
                avg = (
                    rds_db.session.query(func.avg(getattr(SensoryEval, field)))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                max_value = (
                    rds_db.session.query(func.max(getattr(SensoryEval, field)))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                min_value = (
                    rds_db.session.query(func.min(getattr(SensoryEval, field)))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )

                # 실제로 존재하는 값들 찾기
                unique_values_query = (
                    rds_db.session.query(getattr(SensoryEval, field))
                    .join(Meat, Meat.id == SensoryEval.id)
                    .filter(
                        SensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .distinct()
                )
                unique_values = [
                    value[0]
                    for value in unique_values_query.all()
                    if value[0] is not None
                ]

                stats[field] = {
                    "avg": avg,
                    "max": max_value,
                    "min": min_value,
                    "unique_values": sorted(unique_values),
                }

        return jsonify(stats)

    def _get_senseval_of_raw_heatedmeat(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

        # 각 필드의 평균값, 최대값, 최소값 계산
        stats = {}
        for field in ["flavor", "juiciness", "tenderness", "umami", "palability"]:
            avg = (
                rds_db.session.query(func.avg(getattr(HeatedmeatSensoryEval, field)))
                .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                .filter(
                    HeatedmeatSensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )
            max_value = (
                rds_db.session.query(func.max(getattr(HeatedmeatSensoryEval, field)))
                .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                .filter(
                    HeatedmeatSensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )
            min_value = (
                rds_db.session.query(func.min(getattr(HeatedmeatSensoryEval, field)))
                .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                .filter(
                    HeatedmeatSensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .scalar()
            )

            # 실제로 존재하는 값들 찾기
            unique_values_query = (
                rds_db.session.query(getattr(HeatedmeatSensoryEval, field))
                .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                .filter(
                    HeatedmeatSensoryEval.seqno == 0,
                    Meat.createdAt.between(start, end),
                    Meat.statusType == 2,
                )
                .distinct()
            )
            unique_values = [
                value[0] for value in unique_values_query.all() if value[0] is not None
            ]

            stats[field] = {
                "avg": avg,
                "max": max_value,
                "min": min_value,
                "unique_values": sorted(unique_values),
            }

        return jsonify(stats)

    def _get_senseval_of_processed_heatedmeat(self, seqno, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

        # 각 필드의 평균값, 최대값, 최소값 계산
        stats = {}
        seqno = safe_int(seqno)
        if seqno:
            for field in ["flavor", "juiciness", "tenderness", "umami", "palability"]:
                avg = (
                    rds_db.session.query(
                        func.avg(getattr(HeatedmeatSensoryEval, field))
                    )
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(
                        HeatedmeatSensoryEval.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                max_value = (
                    rds_db.session.query(
                        func.max(getattr(HeatedmeatSensoryEval, field))
                    )
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(
                        HeatedmeatSensoryEval.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                min_value = (
                    rds_db.session.query(
                        func.min(
                            getattr(HeatedmeatSensoryEval, field),
                            Meat.createdAt.between(start, end),
                            Meat.statusType == 2,
                        )
                    )
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(HeatedmeatSensoryEval.seqno == seqno)
                    .scalar()
                )

                # 실제로 존재하는 값들 찾기
                unique_values_query = (
                    rds_db.session.query(getattr(HeatedmeatSensoryEval, field))
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(
                        HeatedmeatSensoryEval.seqno == seqno,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .distinct()
                )
                unique_values = [
                    value[0]
                    for value in unique_values_query.all()
                    if value[0] is not None
                ]

                stats[field] = {
                    "avg": avg,
                    "max": max_value,
                    "min": min_value,
                    "unique_values": sorted(unique_values),
                }
        else:
            for field in ["flavor", "juiciness", "tenderness", "umami", "palability"]:
                avg = (
                    rds_db.session.query(
                        func.avg(getattr(HeatedmeatSensoryEval, field))
                    )
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(
                        HeatedmeatSensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                max_value = (
                    rds_db.session.query(
                        func.max(getattr(HeatedmeatSensoryEval, field))
                    )
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(
                        HeatedmeatSensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )
                min_value = (
                    rds_db.session.query(
                        func.min(getattr(HeatedmeatSensoryEval, field))
                    )
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(
                        HeatedmeatSensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .scalar()
                )

                # 실제로 존재하는 값들 찾기
                unique_values_query = (
                    rds_db.session.query(getattr(HeatedmeatSensoryEval, field))
                    .join(Meat, Meat.id == HeatedmeatSensoryEval.id)
                    .filter(
                        HeatedmeatSensoryEval.seqno != 0,
                        Meat.createdAt.between(start, end),
                        Meat.statusType == 2,
                    )
                    .distinct()
                )
                unique_values = [
                    value[0]
                    for value in unique_values_query.all()
                    if value[0] is not None
                ]

                stats[field] = {
                    "avg": avg,
                    "max": max_value,
                    "min": min_value,
                    "unique_values": sorted(unique_values),
                }

        return jsonify(stats)

    def _get_tongue_of_processedmeat(self, start, end):
        # 기간 설정
        start = convert2datetime(start, 1)  # Start Time
        end = convert2datetime(end, 1)  # End Time
        if start is None or end is None:
            abort(404, description="Wrong start or end data")

        # Get all SensoryEval records
        sensory_evals = (
            SensoryEval.query.join(Meat, Meat.id == SensoryEval.id)
            .filter(
                Meat.createdAt.between(start, end),
                Meat.statusType == 2,
            )
            .order_by(SensoryEval.id, SensoryEval.seqno)
            .all()
        )

        result = {}

        # Keep track of the accumulated minutes for each id
        accumulated_minutes = {}

        for sensory_eval in sensory_evals:
            deep_aging = DeepAging.query.filter_by(
                deepAgingId=sensory_eval.deepAgingId
            ).first()

            # If no matching DeepAging record was found, skip this SensoryEval

            # Get the corresponding ProbexptData record
            probexpt_data = ProbexptData.query.filter_by(
                id=sensory_eval.id, seqno=sensory_eval.seqno
            ).first()

            # If no matching ProbexptData record was found, skip this SensoryEval
            if not probexpt_data:
                continue

            # Create a dictionary of ProbexptData fields
            probexpt_data_dict = {
                "sourness": probexpt_data.sourness,
                "bitterness": probexpt_data.bitterness,
                "umami": probexpt_data.umami,
                "richness": probexpt_data.richness,
            }

            # If the seqno is 0, set the minute to 0, otherwise, add the current DeepAging minute to the accumulated minutes
            if sensory_eval.seqno == 0:
                accumulated_minutes[sensory_eval.id] = 0
            else:
                # If the id is not yet in the accumulated_minutes dictionary, initialize it to the current minute
                if sensory_eval.id not in accumulated_minutes:
                    accumulated_minutes[sensory_eval.id] = deep_aging.minute
                else:
                    accumulated_minutes[sensory_eval.id] += deep_aging.minute

            # Add the ProbexptData fields to the result under the accumulated minutes
            if accumulated_minutes[sensory_eval.id] not in result:
                result[accumulated_minutes[sensory_eval.id]] = {}

            result[accumulated_minutes[sensory_eval.id]][
                f"({sensory_eval.id},{sensory_eval.seqno})"
            ] = probexpt_data_dict

        return result

    # 3. AI API
    def _predict_db_data(self):
        # 1. Data Valid Check
        if not request.json:
            abort(400, description="No data sent for update")
        # 2. 기본 데이터 받아두기
        data = request.get_json()
        id = data.get("id")
        seqno = data.get("seqno")
        # Find SensoryEval data
        sensory_eval = SensoryEval.query.filter_by(id=id, seqno=seqno).first()

        # If no SensoryEval found, abort
        if not sensory_eval:
            abort(404, description="No SensoryEval found with given id and seqno")

        # Call 2nd team's API
        response = requests.post(
            f"{keyId.ML_server_base_url}/predict",
            data=json.dumps({"image_path": sensory_eval.imagePath}),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        # If the response was unsuccessful, abort
        if response.status_code != 200:
            print(response)
            abort(500, description="Failed to get data from team 2's API")

        # Decode the response data
        response_data = response.json()
        print(response_data)
        # Merge the response data with the existing data
        data.update(response_data)
        
        # Change the key name from 'gradeNum' to 'xai_gradeNum'
        if "gradeNum" in data:
            data["xai_gradeNum"] = data.pop("gradeNum")
        data["createdAt"] = datetime.now()
        try:
            # Create a new SensoryEval
            new_sensory_eval = create_AI_SensoryEval(rds_db, data, seqno, id)

            # Add new_sensory_eval to the session
            rds_db.session.merge(new_sensory_eval)

            # Commit the session to save the changes
            rds_db.session.commit()
        except Exception as e:
            rds_db.session.rollback()
            abort(404, description=e)

        # Return the new data
        return jsonify(data), 200
        # 의문점1 : 이거 시간 오바 안 뜨려나?
        # 의문점2 : 로딩창 안 뜨나

    def _get_predict_db_data(self,id,seqno):
        id = safe_str(id)
        seqno = safe_int(seqno)
        if id is None or seqno is None:
            abort(404,description="Wrong id or seqno")
        try:
            result = get_AI_SensoryEval(rds_db,id,seqno)
        except Exception as e:
            abort(401,description = e)
        if result is not None:
            return jsonify(result),200
        else:
            abort(404,description="No data in AI Sensory Evaluate DB")
    # 4. Utils

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


def _make_response(data, url):  # For making response
    response = make_response(data)
    response.headers["Access-Control-Allow-Origin"] = url
    return response


# Init RDS
app = Flask(__name__)
myApp = MyFlaskApp(app, db_config.config)
CORS(myApp.app)

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
        return jsonify({"message": f"Error Occur {e}"}), 404
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
        return jsonify({"message": "None Duplicated id"}), 200
    else:
        return jsonify({"message": "Duplicated id"}), 404


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


@myApp.app.route("/user/delete", methods=["GET"])
def delete():
    id = request.args.get("id")
    user = User.query.filter_by(userId=id).first()
    # 해당 유저가 데이터베이스에 없을 경우
    if user is None:
        return jsonify({f"message": f"No user data in Database (userId: {id})"}), 404

    # 해당 유저가 데이터베이스에 있을 경우 삭제
    try:
        rds_db.session.delete(user)
        rds_db.session.commit()
        return jsonify({f"message": f"User with userId {id} has been deleted"}), 200

    except Exception as e:
        rds_db.session.rollback()
        return jsonify({f"error": str(e)}), 500


@myApp.app.route("/user/pwd_check", methods=["POST"])
def pwd_check():
    data = request.get_json()
    id = data.get("id")
    password = data.get("password")

    user = User.query.filter_by(userId=id).first()
    if user is None:
        return jsonify({"message": f"No user data in Database(userId:{id})"}), 404
    if user.password != hashlib.sha256(password.encode()).hexdigest():
        print(user.password, hashlib.sha256(password.encode()).hexdigest())
        return jsonify({"message": f"Invalid password for userId:{id}"}), 401

    return jsonify({"message": f"Valid password for userId:{id}"}), 200


def scheduler_function():  # 일정 주기마다 실행하는 함수
    myApp.firestore_conn.transferDbData()  # (FireStore -> Flask Server)
    myApp.s3_conn.transferImageData("meats")  # (Flask server(images folder) -> S3)
    myApp.s3_conn.transferImageData("qr_codes")  # (Flask server(images folder) -> S3)
    myApp.transfer_data_to_rds()  #  (FireStore -> RDS)


# Server 구동
if __name__ == "__main__":
    # 2. Flask 서버 실행
    myApp.app.run(host="0.0.0.0", port=8080)
