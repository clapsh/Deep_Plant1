from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKeyConstraint
from sqlalchemy.orm import backref
from utils import *
import hashlib  # For password hashing
import uuid  # For making ID


rds_db = SQLAlchemy()


class Species(rds_db.Model):
    __tablename__ = "species"
    id = rds_db.Column(rds_db.Integer, primary_key=True)  # 종 ID
    value = rds_db.Column(rds_db.String(255))  # 종 값(cattle, pig)
    categories = rds_db.relationship("Category", backref="species")


class Category(rds_db.Model):
    __tablename__ = "category"
    id = rds_db.Column(rds_db.Integer, primary_key=True)  # 카테고리 ID
    speciesId = rds_db.Column(rds_db.Integer, rds_db.ForeignKey("species.id"))  # 종 ID
    primalValue = rds_db.Column(rds_db.String(255), nullable=False)  # 부위 대분활 값
    secondaryValue = rds_db.Column(rds_db.String(255), nullable=False)  # 부위 소분할 값
    meats = rds_db.relationship("Meat", backref="category")


class GradeNum(rds_db.Model):
    """
    0: 1++
    1: 1+
    2: 1
    3: 2
    4: 3
    5: None(Null)
    """

    __tablename__ = "gradeNum"
    id = rds_db.Column(rds_db.Integer, primary_key=True)  # 등급 ID
    value = rds_db.Column(rds_db.String(255))  # 등급 값 (1++,1+,1,2,3,null)


class SexType(rds_db.Model):
    """
    0: Male
    1: Female
    2: None(Null)
    """

    __tablename__ = "sexType"
    id = rds_db.Column(rds_db.Integer, primary_key=True)  # 성별 ID
    value = rds_db.Column(rds_db.String(255))  # 성별 값 (수, 암, 거세, null)


class StatusType(rds_db.Model):
    """
    0: 대기중
    1: 반려
    2: 승인
    """

    __tablename__ = "statusType"
    id = rds_db.Column(rds_db.Integer, primary_key=True)  # 승인 여부 ID
    value = rds_db.Column(rds_db.String(255))  # 승인 값 (대기중, 반려, 승인)


class Meat(rds_db.Model):
    __tablename__ = "meat"
    # 1. 육류 관리번호
    id = rds_db.Column(rds_db.String(255), primary_key=True)  # 육류 관리번호
    # 2. 외래키 관리
    userId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("users.userId"), nullable=False
    )  # 생성한 유저 ID
    sexType = rds_db.Column(rds_db.Integer, rds_db.ForeignKey("sexType.id"))  # 성별 ID
    categoryId = rds_db.Column(
        rds_db.Integer, rds_db.ForeignKey("category.id"), nullable=False
    )  # Category ID
    gradeNum = rds_db.Column(rds_db.Integer, rds_db.ForeignKey("gradeNum.id"))  # 등급 ID
    statusType = rds_db.Column(
        rds_db.Integer, rds_db.ForeignKey("statusType.id"), default=0
    )  # 승인 여부 ID

    # 3. Open API 및 관리번호 생성시간
    createdAt = rds_db.Column(DateTime, nullable=False)  # 관리번호 생성 시간
    traceNum = rds_db.Column(rds_db.String(255), nullable=False)  # 이력번호(묶음번호)
    farmAddr = rds_db.Column(rds_db.String(255))  # 농장 주소
    farmerNm = rds_db.Column(rds_db.String(255))  # 농장주 명
    butcheryYmd = rds_db.Column(DateTime, nullable=False)  # 도축일자
    birthYmd = rds_db.Column(DateTime)  # 출생일자

    # 4. QR code image
    imagePath = rds_db.Column(rds_db.String(255))  # QR image path


class SensoryEval(rds_db.Model):
    __tablename__ = "sensory_eval"
    # 1. 복합키 설정
    id = rds_db.Column(
        rds_db.String(255),
        rds_db.ForeignKey("meat.id"),
        primary_key=True,
    )  # 육류 관리번호
    seqno = rds_db.Column(
        rds_db.Integer, primary_key=True
    )  # 가공 횟수(seqno가 0이면 원육, 1이상인 N일때 N회차 가공육)
    __table_args__ = (rds_db.PrimaryKeyConstraint("id", "seqno"),)

    # 2. 관능검사 메타 데이터
    createdAt = rds_db.Column(DateTime, nullable=False)  # 관능검사 생성 시간
    userId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("users.userId"), nullable=False
    )  # 관능검사 생성한 유저 ID
    period = rds_db.Column(rds_db.Integer, nullable=False)  # 도축일로부터 경과된 시간
    imagePath = rds_db.Column(rds_db.String(255))  # 관능검사 이미지 경로
    deepAgingId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("deep_aging.deepAgingId")
    )  # 원육이면 null, 가공육이면 해당 딥에이징 정보 ID

    # 3. 관능검사 데이터
    marbling = rds_db.Column(rds_db.Float)
    color = rds_db.Column(rds_db.Float)
    texture = rds_db.Column(rds_db.Float)
    surfaceMoisture = rds_db.Column(rds_db.Float)
    overall = rds_db.Column(rds_db.Float)


class AI_SensoryEval(rds_db.Model):
    __tablename__ = "ai_sensory_eval"
    # 1. 복합키 설정
    id = rds_db.Column(
        rds_db.String(255),
        rds_db.ForeignKey("meat.id"),
        primary_key=True,
    )  # 육류 관리번호
    seqno = rds_db.Column(
        rds_db.Integer, primary_key=True
    )  # 가공 횟수(seqno가 0이면 원육, 1이상인 N일때 N회차 가공육)
    __table_args__ = (rds_db.PrimaryKeyConstraint("id", "seqno"),)

    # 2. 관능검사 메타 데이터
    createdAt = rds_db.Column(DateTime, nullable=False)  # 관능검사 생성 시간
    userId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("users.userId"), nullable=False
    )  # 관능검사 생성한 유저 ID
    period = rds_db.Column(rds_db.Integer, nullable=False)  # 도축일로부터 경과된 시간
    imagePath = rds_db.Column(rds_db.String(255))  # xai 관능검사 이미지 경로
    xai_imagePath = rds_db.Column(rds_db.String(255))
    deepAgingId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("deep_aging.deepAgingId")
    )  # 원육이면 null, 가공육이면 해당 딥에이징 정보 ID

    # 3. 관능검사 데이터
    marbling = rds_db.Column(rds_db.Float)
    color = rds_db.Column(rds_db.Float)
    texture = rds_db.Column(rds_db.Float)
    surfaceMoisture = rds_db.Column(rds_db.Float)
    overall = rds_db.Column(rds_db.Float)


class HeatedmeatSensoryEval(rds_db.Model):
    __tablename__ = "heatedmeat_sensory_eval"
    # 1. 복합키 설정
    id = rds_db.Column(rds_db.String(255), primary_key=True)  # 육류 관리번호
    seqno = rds_db.Column(
        rds_db.Integer, primary_key=True
    )  # 가공 횟수(seqno가 0이면 원육, 1이상인 N일때 N회차 가공육)
    __table_args__ = (
        rds_db.PrimaryKeyConstraint("id", "seqno"),
        rds_db.ForeignKeyConstraint(
            ["id", "seqno"], ["sensory_eval.id", "sensory_eval.seqno"]
        ),
    )

    # 2. 관능검사 메타 데이터
    createdAt = rds_db.Column(DateTime, nullable=False)  # 가열육 관능검사 데이터 생성 시간
    userId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("users.userId"), nullable=False
    )  # 가열육 관능검사 데이터 생성 유저 ID
    period = rds_db.Column(rds_db.Integer, nullable=False)  # 도축일로부터 경과된 시간
    imagePath = rds_db.Column(rds_db.String(255))  # 가열육 관능검사 이미지 경로

    # 3. 관능검사 데이터
    flavor = rds_db.Column(rds_db.Float)
    juiciness = rds_db.Column(rds_db.Float)
    tenderness = rds_db.Column(rds_db.Float)
    umami = rds_db.Column(rds_db.Float)
    palability = rds_db.Column(rds_db.Float)


class AI_HeatedmeatSensoryEval(rds_db.Model):
    __tablename__ = "ai_heatedmeat_sensory_eval"
    # 1. 복합키 설정
    id = rds_db.Column(rds_db.String(255), primary_key=True)  # 육류 관리번호
    seqno = rds_db.Column(
        rds_db.Integer, primary_key=True
    )  # 가공 횟수(seqno가 0이면 원육, 1이상인 N일때 N회차 가공육)
    __table_args__ = (rds_db.PrimaryKeyConstraint("id", "seqno"),)

    # 2. 관능검사 메타 데이터
    createdAt = rds_db.Column(DateTime, nullable=False)  # 가열육 관능검사 데이터 생성 시간
    userId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("users.userId"), nullable=False
    )  # 가열육 관능검사 데이터 생성 유저 ID
    period = rds_db.Column(rds_db.Integer, nullable=False)  # 도축일로부터 경과된 시간
    imagePath = rds_db.Column(rds_db.String(255))  # 가열육 관능검사 이미지 경로
    xai_imagePath = rds_db.Column(rds_db.String(255))

    # 3. 관능검사 데이터
    flavor = rds_db.Column(rds_db.Float)
    juiciness = rds_db.Column(rds_db.Float)
    tenderness = rds_db.Column(rds_db.Float)
    umami = rds_db.Column(rds_db.Float)
    palability = rds_db.Column(rds_db.Float)


class ProbexptData(rds_db.Model):
    __tablename__ = "probexpt_data"
    # 1. 복합키 설정
    id = rds_db.Column(rds_db.String(255), primary_key=True)  # 육류 관리번호
    seqno = rds_db.Column(
        rds_db.Integer, primary_key=True
    )  # 가공 횟수(seqno가 0이면 원육, 1이상인 N일때 N회차 가공육)
    __table_args__ = (
        rds_db.PrimaryKeyConstraint("id", "seqno"),
        rds_db.ForeignKeyConstraint(
            ["id", "seqno"], ["sensory_eval.id", "sensory_eval.seqno"]
        ),
        rds_db.CheckConstraint("0 <= DL AND DL <= 100", name="check_DL_percentage"),
        rds_db.CheckConstraint("0 <= CL AND CL <= 100", name="check_CL_percentage"),
        rds_db.CheckConstraint("0 <= RW AND RW <= 100", name="check_RW_percentage"),
    )

    # 2. 연구실 메타 데이터
    updatedAt = rds_db.Column(DateTime, nullable=False)  # 실험실 데이터 업데이트(수정 혹은 생성) 시간
    userId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("users.userId"), nullable=False
    )  # 실험실 데이터 업데이트(수정 혹은 생성)한 유저 ID
    period = rds_db.Column(rds_db.Integer, nullable=False)  # 도축일로부터 경과된 시간

    # 3. 실험 데이터
    L = rds_db.Column(rds_db.Float)
    a = rds_db.Column(rds_db.Float)
    b = rds_db.Column(rds_db.Float)
    DL = rds_db.Column(rds_db.Float)
    CL = rds_db.Column(rds_db.Float)
    RW = rds_db.Column(rds_db.Float)
    ph = rds_db.Column(rds_db.Float)
    WBSF = rds_db.Column(rds_db.Float)
    cardepsin_activity = rds_db.Column(rds_db.Float)
    MFI = rds_db.Column(rds_db.Float)
    Collagen = rds_db.Column(rds_db.Float)

    # 4. 전자혀 데이터
    sourness = rds_db.Column(rds_db.Float)
    bitterness = rds_db.Column(rds_db.Float)
    umami = rds_db.Column(rds_db.Float)
    richness = rds_db.Column(rds_db.Float)


class DeepAging(rds_db.Model):
    __tablename__ = "deep_aging"
    # 1. 기본키
    deepAgingId = rds_db.Column(rds_db.String(255), primary_key=True)  # 딥에이징 이력 ID

    # 2. 딥에이징 데이터
    date = rds_db.Column(DateTime, nullable=False)  # 딥에이징 실시 일자
    minute = rds_db.Column(rds_db.Integer, nullable=False)  # 딥에이징 진행 시간(분)


class UserType(rds_db.Model):
    """
    (id, name)
    = (0,"Normal"),(1,"Researcher"),(2,"Manager"),(3,None)
    """

    __tablename__ = "userType"
    id = rds_db.Column(rds_db.Integer, primary_key=True)  # 유저 Type ID
    name = rds_db.Column(
        rds_db.String(255)
    )  # 유저 종류 이름 (Normal, Researcher, Manager, None)


class User(rds_db.Model):
    __tablename__ = "users"
    userId = rds_db.Column(rds_db.String(255), primary_key=True)  # 유저 ID -> 이메일
    createdAt = rds_db.Column(DateTime, nullable=False)  # 유저 ID 생성 시간
    updatedAt = rds_db.Column(DateTime)  # 유저 정보 수정 시간
    loginAt = rds_db.Column(DateTime)  # 유저 로그인 시간
    password = rds_db.Column(rds_db.String(255), nullable=False)  # 유저 비밀번호 (암호화)
    name = rds_db.Column(rds_db.String(255))  # 유저명
    company = rds_db.Column(rds_db.String(255))  # 직장명
    jobTitle = rds_db.Column(rds_db.String(255))  # 직위명
    homeAddr = rds_db.Column(rds_db.String(255))  # 유저 주소
    alarm = rds_db.Column(rds_db.Boolean, default=False)  # 유저 알람 허용 여부
    type = rds_db.Column(
        rds_db.Integer, rds_db.ForeignKey("userType.id"), nullable=False
    )  # 유저 Type ID


def load_initial_data(db):
    """
    초기 데이터 셋업 function
    Params
    1. db: 초기 데이터 셋업 db
    # 이거 나중에는 merge로 바꾸자.....!! add -> merge TEST!!!!
    """

    # 1. Specie
    for id, specie in enumerate(species):
        if not Species.query.get(id):
            temp = Species(id=id, value=specie)  # 0: Cattle, 1: Pig
            db.session.add(temp)
    db.session.commit()

    # 2. Cattle
    for id, large in enumerate(cattleLarge):
        for s_id, small in enumerate(cattleSmall[id]):
            index = calId(id, s_id, CATTLE)
            if not Category.query.get(index):
                temp = Category(
                    id=index,
                    speciesId=CATTLE,
                    primalValue=large,
                    secondaryValue=small,
                )
                db.session.add(temp)
    db.session.commit()

    # 3. Pig
    for id, large in enumerate(pigLarge):
        for s_id, small in enumerate(pigSmall[id]):
            index = calId(id, s_id, PIG)
            if not Category.query.get(index):
                temp = Category(
                    id=index,
                    speciesId=PIG,
                    primalValue=large,
                    secondaryValue=small,
                )
                db.session.add(temp)
    db.session.commit()

    # 4. User
    for id, Type in usrType.items():
        if not UserType.query.get(id):
            temp = UserType(id=id, name=Type)
            db.session.add(temp)
    db.session.commit()

    # 5. GradeNum
    for id, Type in gradeNum.items():
        if not GradeNum.query.get(id):
            temp = GradeNum(id=id, value=Type)
            db.session.add(temp)
    db.session.commit()

    # 6. SexType
    for id, Type in sexType.items():
        if not SexType.query.get(id):
            temp = SexType(id=id, value=Type)
            db.session.add(temp)
    db.session.commit()

    # 7. StatusType
    for id, Type in statusType.items():
        if not StatusType.query.get(id):
            temp = StatusType(id=id, value=Type)
            db.session.add(temp)
    db.session.commit()


def find_id(specie_value, primal_value, secondary_value, db):
    """
    category id 지정 function
    Params
    1. specie_value: "cattle" or "pig
    2. primal_value: "대분할 부위"
    3. secondary_value: "소분할 부위"
    4. db: 세션 db

    Return
    1. Category.id
    """
    # Find specie using the provided specie_value
    specie = db.session.query(Species).filter_by(value=specie_value).first()

    # If the specie is not found, return an appropriate message
    if not specie:
        raise Exception("Invalid specie data")

    # Find category using the provided primal_value, secondary_value, and the specie id
    category = (
        db.session.query(Category)
        .filter_by(
            primalValue=primal_value,
            secondaryValue=secondary_value,
            speciesId=specie.id,
        )
        .first()
    )

    # If the category is not found, return an appropriate message
    if not category:
        raise Exception("Invalid primal or secondary value")

    # If everything is fine, return the id of the found category
    return category.id


def decode_id(id, db):
    result = {"specie_value": None, "primal_value": None, "secondary_value": None}
    category = db.session.query(Category).filter_by(id=id).first()
    specie = db.session.query(Species).filter_by(id=category.speciesId).first()
    result["specie_value"] = specie.value
    result["primal_value"] = category.primalValue
    result["secondary_value"] = category.secondaryValue
    return result["specie_value"], result["primal_value"], result["secondary_value"]


def calId(id, s_id, type):
    """
    category id 계산 함수
    Params
    1. id: 대분할 인덱스
    2. s_id: 소분할 인덱스
    3. type: 종 인덱스

    """
    return 100 * type + 10 * id + s_id


def create_meat(
    db,
    meat_data: dict,
):
    """
    db: SQLAlchemy db
    meat_data: 모든 필드의 데이터가 문자열로 들어왔다고 가정!!
    """
    if meat_data is None:
        raise Exception("Invalid meat data")
    # 1. Get the ID of the record in the SexType table
    sex_type = (
        db.session.query(SexType).filter_by(value=meat_data.get("sexType")).first()
    )
    # 2. Get the ID of the record in the GradeNum table
    grade_num = (
        db.session.query(GradeNum).filter_by(value=meat_data.get("gradeNum")).first()
    )
    # 3. meat_data에 없는 필드 추가

    # 4, meat_data에 있는 필드 수정
    for field in list(meat_data.keys()):
        if field == "sexType":
            try:
                item_encoder(meat_data, field, sex_type.id)
            except Exception as e:
                raise Exception("Invalid sex_type id")
        elif field == "gradeNum":
            try:
                item_encoder(meat_data, field, grade_num.id)
            except Exception as e:
                raise Exception("Invalid grade_num id")
        elif (
            field == "specieValue"
            or field == "primalValue"
            or field == "secondaryValue"
        ):
            item_encoder(
                meat_data,
                "categoryId",
                find_id(
                    meat_data.get("specieValue"),
                    meat_data.get("primalValue"),
                    meat_data.get("secondaryValue"),
                    db,
                ),
            )
        else:
            item_encoder(meat_data, field)
    # 5. meat_data에 없어야 하는 필드 삭제
    meat_data.pop("specieValue")
    meat_data.pop("primalValue")
    meat_data.pop("secondaryValue")
    # Create a new Meat object
    try:
        new_meat = Meat(**meat_data)
    except Exception as e:
        raise Exception("Wrong meat DB field items" + str(e))
    return new_meat


def create_SensoryEval(db, meat_data: dict, seqno: int, id: str, deepAgingId: int):
    """
    db: SQLAlchemy db
    freshmeat_data: 모든 필드의 데이터가 문자열로 들어왔다고 가정!!
    seqno: 신선육 관능검사 seqno
    freshmeatId: 가열육 관능검사 seqno
    probexpt_seqno: 실험(전자혀) 관능 검사 seqno
    type: 0(신규 생성) or 1(기존 수정)
    """
    if meat_data is None:
        raise Exception("Invalid Sensory_Evaluate data")
    # 1. freshmeat_data에 없는 필드 추가
    item_encoder(meat_data, "seqno", seqno)
    item_encoder(meat_data, "id", id)
    item_encoder(meat_data, "deepAgingId", deepAgingId)
    # 2. freshmeat_data에 있는 필드 수정
    for field in meat_data.keys():
        if field == "seqno":  # 여기 있어도 걍 입력된걸 써라~
            pass
        elif field == "freshmeatId":  # 여기 있어도 걍 입력된걸 써라~
            pass
        elif field == "deepAgingId":
            pass
        else:
            item_encoder(meat_data, field)
    # Create a new Meat object
    try:
        new_SensoryEval = SensoryEval(**meat_data)
        print(to_dict(new_SensoryEval))
    except Exception as e:
        raise Exception("Wrong sensory eval DB field items" + str(e))
    return new_SensoryEval


def create_DeepAging(db, data: dict):
    if data is None:
        raise Exception("Invalid Deep Aging data")
    for field in data.keys():
        item_encoder(data, field)
    data["deepAgingId"] = str(uuid.uuid4())
    try:
        new_deepAging = DeepAging(**data)
        print(to_dict(new_deepAging))
    except Exception as e:
        raise Exception("Wrong DeepAging DB field items: " + str(e))
    return new_deepAging


def create_HeatedmeatSensoryEval(db, meat_data: dict, seqno: int, id: str):
    """
    db: SQLAlchemy db
    heatedmeat_data: 모든 필드의 데이터가 문자열로 들어왔다고 가정!!
    seqno: 신선육 관능검사 seqno
    heatedMeatId: 가열육 관능검사 seqno
    probexpt_seqno: 실험(전자혀) 관능 검사 seqno
    type: 0(신규 생성) or 1(기존 수정)
    """
    if meat_data is None:
        raise Exception("Invalid Heatedmeat Sensory Evaluate data")
    # 1. heatedmeat_data에 없는 필드 추가
    item_encoder(meat_data, "seqno", seqno)
    item_encoder(meat_data, "id", id)
    # 2. heatedmeat_data에 있는 필드 수정
    for field in meat_data.keys():
        if field == "seqno":
            pass
        elif field == "id":
            pass
        else:
            item_encoder(meat_data, field)
    # Create a new Meat object
    try:
        new_heatedmeat = HeatedmeatSensoryEval(**meat_data)
    except Exception as e:
        raise Exception("Wrong heatedmeat sensory eval DB field items" + str(e))
    return new_heatedmeat


def create_ProbexptData(db, meat_data: dict, seqno: int, id: str):
    """
    db: SQLAlchemy db
    probexpt_data: 모든 필드의 데이터가 문자열로 들어왔다고 가정!!
    seqno: 신선육 관능검사 seqno
    probexptId: 가열육 관능검사 seqno
    probexpt_seqno: 실험(전자혀) 관능 검사 seqno
    type: 0(신규 생성) or 1(기존 수정)
    """
    if meat_data is None:
        raise Exception("Invalid Probexpt data")
    # 1. heatedmeat_data에 없는 필드 추가
    item_encoder(meat_data, "seqno", seqno)
    item_encoder(meat_data, "id", id)
    # 2. heatedmeat_data에 있는 필드 수정
    for field in meat_data.keys():
        if field == "seqno":
            pass
        elif field == "id":
            pass
        else:
            item_encoder(meat_data, field)
    # Create a new Meat object
    try:
        new_Probexpt = ProbexptData(**meat_data)
    except Exception as e:
        raise Exception("Wrong Probexpt DB field items" + str(e))
    return new_Probexpt


def create_user(db, user_data: dict, type):
    """
    유저 생성 함수
    type: "new", "old"
    """
    if type == "new":  # 신규 유저 생성
        for field, value in user_data.items():
            if field == "password":
                item_encoder(
                    user_data, field, hashlib.sha256(value.encode()).hexdigest()
                )
            elif field == "type":
                user_type = UserType.query.filter_by(name=value).first()
                if user_type:  # check if user_type exists
                    item_encoder(user_data, field, user_type.id)
                else:
                    item_encoder(user_data, field, 3)
            else:
                item_encoder(user_data, field)
        try:
            new_user = User(**user_data)
        except Exception as e:
            raise Exception("Wrong User DB field items" + str(e))
        return new_user
    else:  # 기존 유저 정보 수정
        history = User.query.filter_by(
            userId=user_data.get("userId"),
        ).first()
        if history == None:
            return None
        for field, value in user_data.items():
            if field == "password":
                item_encoder(
                    user_data, field, hashlib.sha256(value.encode()).hexdigest()
                )
            elif field == "type":
                user_type = UserType.query.filter_by(name=value).first()
                if user_type:  # check if user_type exists
                    item_encoder(user_data, field, user_type.id)
                else:
                    item_encoder(user_data, field, 3)
            else:
                item_encoder(user_data, field)

        for attr, value in user_data.items():
            setattr(history, attr, value)
        return history


def get_meat(db, id):
    meat = db.session.query(Meat).filter(Meat.id == id).first()

    if meat is None:
        return None
    result = to_dict(meat)
    sexType = db.session.query(SexType).filter(SexType.id == result["sexType"]).first()
    gradeNum = (
        db.session.query(GradeNum).filter(GradeNum.id == result["gradeNum"]).first()
    )
    statusType = (
        db.session.query(StatusType)
        .filter(StatusType.id == result["statusType"])
        .first()
    )
    # 이미 있는거 변환
    result["sexType"] = sexType.value
    (
        result["specieValue"],
        result["primalValue"],
        result["secondaryValue"],
    ) = decode_id(result["categoryId"], db)
    result["gradeNum"] = gradeNum.value
    result["statusType"] = statusType.value
    result["createdAt"] = convert2string(result["createdAt"], 1)
    result["butcheryYmd"] = convert2string(result["butcheryYmd"], 2)
    result["birthYmd"] = convert2string(result["birthYmd"], 2)

    # 6. freshmeat , heatedmeat, probexpt
    result["rawmeat"] = {
        "sensory_eval": get_SensoryEval(db, id, 0),
        "heatedmeat_sensory_eval": get_HeatedmeatSensoryEval(db, id, 0),
        "probexpt_data": get_ProbexptData(db, id, 0),
    }
    sensory_data = (
        SensoryEval.query.filter_by(id=id).order_by(SensoryEval.seqno.desc()).first()
    )  # DB에 있는 육류 정보
    if sensory_data:
        N = sensory_data.seqno
    else:
        N = 0

    result["processedmeat"] = {
        f"{i}회": {
            "sensory_eval": {},
            "heatedmeat_sensory_eval": {},
            "probexpt_data": {},
        }
        for i in range(1, N + 1)
    }
    for index in range(1, N + 1):
        result["processedmeat"][f"{index}회"]["sensory_eval"] = get_SensoryEval(
            db, id, index
        )
        result["processedmeat"][f"{index}회"][
            "heatedmeat_sensory_eval"
        ] = get_HeatedmeatSensoryEval(db, id, index)
        result["processedmeat"][f"{index}회"]["probexpt_data"] = get_ProbexptData(
            db, id, index
        )

    # remove field
    del result["categoryId"]
    return result


def get_SensoryEval(db, id, seqno):
    sensoryEval_data = (
        db.session.query(SensoryEval)
        .filter(
            SensoryEval.id == id,
            SensoryEval.seqno == seqno,
        )
        .first()
    )
    if sensoryEval_data:
        sensoryEval = to_dict(sensoryEval_data)
        sensoryEval["createdAt"] = convert2string(sensoryEval["createdAt"], 1)
        if seqno != 0:  # 가공육인 경우
            sensoryEval["deepaging_data"] = get_DeepAging(
                db, sensoryEval["deepAgingId"]
            )
            del sensoryEval["deepAgingId"]
        return sensoryEval
    else:
        return None


def get_DeepAging(db, id):
    deepAging_data = (
        db.session.query(DeepAging)
        .filter(
            DeepAging.deepAgingId == id,
        )
        .first()
    )
    if deepAging_data:
        deepAging_history = to_dict(deepAging_data)
        deepAging_history["date"] = convert2string(deepAging_history.get("date"), 2)
        return deepAging_history
    else:
        return None


def get_HeatedmeatSensoryEval(db, id, seqno):
    heated_meat = (
        db.session.query(HeatedmeatSensoryEval)
        .filter(
            HeatedmeatSensoryEval.id == id,
            HeatedmeatSensoryEval.seqno == seqno,
        )
        .first()
    )
    if heated_meat:
        heated_meat_history = to_dict(heated_meat)
        heated_meat_history["createdAt"] = convert2string(
            heated_meat_history["createdAt"], 1
        )
        return heated_meat_history
    else:
        return None


def get_ProbexptData(db, id, seqno):
    probexpt = (
        db.session.query(ProbexptData)
        .filter(
            ProbexptData.id == id,
            ProbexptData.seqno == seqno,
        )
        .first()
    )
    if probexpt:
        probexpt_history = to_dict(probexpt)
        probexpt_history["updatedAt"] = convert2string(probexpt_history["updatedAt"], 1)
        return probexpt_history
    else:
        return None


def get_User(db, userId):
    userData = db.session.query(User).filter(User.userId == userId).first()
    if userData:
        userData_dict = to_dict(userData)
        userData_dict["createdAt"] = convert2string(userData_dict.get("createdAt"), 1)
        userData_dict["updatedAt"] = convert2string(userData_dict.get("updatedAt"), 1)
        userData_dict["loginAt"] = convert2string(userData_dict.get("loginAt"), 1)
        userData_dict["type"] = (
            db.session.query(UserType)
            .filter(UserType.id == userData_dict.get("type"))
            .first()
            .name
        )
        return userData_dict
    else:
        return None
