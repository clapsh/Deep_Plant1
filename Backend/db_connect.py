from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, DateTime
from sqlalchemy.orm import backref


rds_db = SQLAlchemy()


class Species(rds_db.Model):
    __tablename__ = "species"
    id = rds_db.Column(rds_db.Integer, primary_key=True)
    value = rds_db.Column(rds_db.String(255))
    categories = rds_db.relationship("Category", backref="species")


class Category(rds_db.Model):
    __tablename__ = "category"
    id = rds_db.Column(rds_db.Integer, primary_key=True)
    speciesId = rds_db.Column(
        rds_db.Integer, rds_db.ForeignKey("species.id")
    )  # 0: Cattle, 1: Pig
    primalValue = rds_db.Column(rds_db.String(255), nullable=False)
    secondaryValue = rds_db.Column(rds_db.String(255), nullable=False)
    meats = rds_db.relationship("Meat", backref="category")


class GradeNum(rds_db.Model):
    __tablename__ = "gradeNum"
    id = rds_db.Column(rds_db.Integer, primary_key=True)
    value = rds_db.Column(rds_db.String(255))


class Meat(rds_db.Model):
    __tablename__ = "meat"
    id = rds_db.Column(rds_db.String(255), primary_key=True)
    userId = rds_db.Column(rds_db.String(255))
    createdAt = rds_db.Column(DateTime)
    traceNum = rds_db.Column(rds_db.String(255))
    farmAddr = rds_db.Column(rds_db.String(255))
    butcheryPlaceNum = rds_db.Column(rds_db.String(255))
    butcheryYmd = rds_db.Column(DateTime)
    birthYmd = rds_db.Column(DateTime)
    sexType = rds_db.Column(rds_db.Integer)
    categoryId = rds_db.Column(rds_db.Integer, rds_db.ForeignKey("category.id"))
    gradeNum = rds_db.Column(rds_db.Integer, rds_db.ForeignKey("gradeNum.id"))

    freshmeat_seqno = rds_db.Column(rds_db.Integer)
    heatedmeat_seqno = rds_db.Column(rds_db.Integer)
    probexpt_seqno = rds_db.Column(rds_db.Integer)
    __table_args__ = (
        rds_db.ForeignKeyConstraint(
            ["freshmeat_seqno", "id"],
            ["historyFreshmeatSenseval.id", "historyFreshmeatSenseval.freshMeatId"],
        ),
        rds_db.ForeignKeyConstraint(
            ["heatedmeat_seqno", "id"],
            ["historyHeatedmeatSenseval.id", "historyHeatedmeatSenseval.heatedMeatId"],
        ),
        rds_db.ForeignKeyConstraint(
            ["heatedmeat_seqno", "id"],
            ["historyProbexptSenseval.id", "historyProbexptSenseval.probexptId"],
        ),
    )


class HistoryFreshmeatSenseval(rds_db.Model):
    __tablename__ = "historyFreshmeatSenseval"
    id = rds_db.Column(rds_db.Integer, primary_key=True)
    createdAt = rds_db.Column(DateTime)
    userId = rds_db.Column(rds_db.String(255), rds_db.ForeignKey("users.userId"))
    freshMeatId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("meat.id"), primary_key=True
    )
    period = rds_db.Column(rds_db.Integer)
    marbling = rds_db.Column(rds_db.Float)
    color = rds_db.Column(rds_db.Float)
    texture = rds_db.Column(rds_db.Float)
    surfaceMoisture = rds_db.Column(rds_db.Float)
    overall = rds_db.Column(rds_db.Float)


class HistoryHeatedmeatSenseval(rds_db.Model):
    __tablename__ = "historyHeatedmeatSenseval"
    id = rds_db.Column(rds_db.Integer, primary_key=True)
    createdAt = rds_db.Column(DateTime)
    userId = rds_db.Column(rds_db.String(255), rds_db.ForeignKey("users.userId"))
    period = rds_db.Column(rds_db.Integer)
    heatedMeatId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("meat.id"), primary_key=True
    )
    flavor = rds_db.Column(rds_db.Float)
    juiciness = rds_db.Column(rds_db.Float)
    tenderness = rds_db.Column(rds_db.Float)
    umami = rds_db.Column(rds_db.Float)
    palability = rds_db.Column(rds_db.Float)


class HistoryProbexptSenseval(rds_db.Model):
    __tablename__ = "historyProbexptSenseval"
    id = rds_db.Column(rds_db.Integer, primary_key=True)
    createdAt = rds_db.Column(DateTime)
    userId = rds_db.Column(rds_db.String(255), rds_db.ForeignKey("users.userId"))
    period = rds_db.Column(rds_db.Integer)
    probexptId = rds_db.Column(
        rds_db.String(255), rds_db.ForeignKey("meat.id"), primary_key=True
    )
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
    sourness = rds_db.Column(rds_db.Float)
    bitterness = rds_db.Column(rds_db.Float)
    umami = rds_db.Column(rds_db.Float)
    richness = rds_db.Column(rds_db.Float)


class UserType(rds_db.Model):
    __tablename__ = "userType"
    id = rds_db.Column(rds_db.Integer, primary_key=True)
    name = rds_db.Column(rds_db.String(255))


class User(rds_db.Model):
    __tablename__ = "users"
    userId = rds_db.Column(rds_db.String(255), primary_key=True)
    createdAt = rds_db.Column(DateTime)
    updatedAt = rds_db.Column(DateTime)
    loginAt = rds_db.Column(DateTime)
    password = rds_db.Column(rds_db.String(255))
    name = rds_db.Column(rds_db.String(255))
    company = rds_db.Column(rds_db.String(255))
    jobTitle = rds_db.Column(rds_db.String(255))
    type = rds_db.Column(rds_db.Integer, rds_db.ForeignKey("userType.id"))


species = ["cattle", "pig"]
cattleLarge = [
    "tenderloin",
    "sirloin",
    "striploin",
    "chuck",
    "blade",
    "round",
    "bottom_round",
    "brisket",
    "shank",
    "rib",
]
pigLarge = [
    "tenderloin",
    "loin",
    "boston_shoulder",
    "picnic_shoulder",
    "spare_ribs",
    "belly",
    "ham",
]
cattleSmall = {
    0: ["tenderloin"],
    1: [
        "chuck_roll",
        "ribeye_roll",
        "lower sirloin",
        "chuck_flap_tail",
    ],
    2: ["strip_loin"],
    3: ["chuck"],
    4: [
        "chuck_tender",
        "top_blade_muscle",
        "blade",
        "blade_meat",
        "top_blade_meat",
    ],
    5: [
        "inside_round",
        "eye_of_round",
    ],
    6: [
        "rump_round",
        "top_sirloin",
        "top_sirloin_cap",
        "knuckle",
        "tri_tip",
    ],
    7: [
        "brisket",
        "brisket_point",
        "plate",
        "inside_skirt",
        "flank",
        "flap_meat",
        "apron",
    ],
    8: [
        "fore_shank",
        "hind_shank",
        "heel_muscle",
    ],
    9: [
        "chuck_short_rib",
        "boneless_short_rib",
        "short_rib",
        "interconstal",
        "tirmmed_rib",
        "hanging_tender",
        "outside_skirt",
        "neck_chain",
    ],
}
pigSmall = {
    0: ["tenderloin"],
    1: [
        "loin",
        "sirloin",
    ],
    2: ["boston_shoulder"],
    3: [
        "picnic_shoulder",
        "foreshank",
        "pork_jowl",
        "chuck_tender",
        "top_blade_muscle",
        "spatula_meat",
    ],
    4: ["rib", "ribs", "tirmmed_rib"],
    5: [
        "belly",
        "skirt_meat",
        "back_rib",
        "hanging_tender",
        "odol_belly",
    ],
    6: [
        "buttok",
        "top_sirloin",
        "knuckle",
        "eye_of_round",
        "rump_round",
        "hind_shank",
    ],
}
usrType = {0: "Normal", 1: "Researcher", 2: "Manager"}
CATTLE = 0
PIG = 1


def load_initial_data(db):
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
    for id, Type in enumerate(usrType.items()):
        if not UserType.query.get(id):
            temp = UserType(id=id, name=Type[1])
            db.session.add(temp)
    db.session.commit()


def calId(id, s_id, type):
    return 100 * type + 10 * id + s_id
