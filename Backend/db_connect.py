from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import Pool

rds_db = SQLAlchemy()


class Meat(rds_db.Model):
    id = rds_db.Column(rds_db.String, primary_key=True)
    email = rds_db.Column(rds_db.String, nullable=False)
    saveTime = rds_db.Column(rds_db.String, nullable=False)
    traceNumber = rds_db.Column(rds_db.String, nullable=False)
    species = rds_db.Column(rds_db.String, nullable=False)
    l_division = rds_db.Column(rds_db.String, nullable=False)
    s_division = rds_db.Column(rds_db.String, nullable=False)
    gradeNm = rds_db.Column(rds_db.String, nullable=False)
    farmAddr = rds_db.Column(rds_db.String, nullable=False)
    butcheryPlaceNm = rds_db.Column(rds_db.String, nullable=False)
    butcheryYmd = rds_db.Column(rds_db.String, nullable=False)

    deepAging = rds_db.relationship(
        "DeepAging", backref="meat", lazy=True, uselist=False
    )
    fresh = rds_db.relationship("Fresh", backref="meat", lazy=True, uselist=False)
    heated = rds_db.relationship("Heated", backref="meat", lazy=True, uselist=False)
    tongue = rds_db.relationship("Tongue", backref="meat", lazy=True, uselist=False)
    lab_data = rds_db.relationship("LabData", backref="meat", lazy=True, uselist=False)


class DeepAging(rds_db.Model):  # Deep Aging Table
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("meat.id"), primary_key=True)
    period = rds_db.Column(rds_db.PickleType, nullable=True)


class Fresh(rds_db.Model):  # 신선육 관능 데이터
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("meat.id"), primary_key=True)
    marbling = rds_db.Column(rds_db.Float, nullable=True)
    color = rds_db.Column(rds_db.Float, nullable=True)
    texture = rds_db.Column(rds_db.Float, nullable=True)
    surfaceMoisture = rds_db.Column(rds_db.Float, nullable=True)
    total = rds_db.Column(rds_db.Float, nullable=True)


class Heated(rds_db.Model):  # 가열육 관능 데이터
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("meat.id"), primary_key=True)
    flavor = rds_db.Column(rds_db.Float, nullable=True)
    juiciness = rds_db.Column(rds_db.Float, nullable=True)
    tenderness = rds_db.Column(rds_db.Float, nullable=True)
    umami = rds_db.Column(rds_db.Float, nullable=True)
    palability = rds_db.Column(rds_db.Float, nullable=True)


class Tongue(rds_db.Model):  # 전자혀 데이터
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("meat.id"), primary_key=True)
    sourness = rds_db.Column(rds_db.Float, nullable=True)
    bitterness = rds_db.Column(rds_db.Float, nullable=True)
    umami = rds_db.Column(rds_db.Float, nullable=True)
    richness = rds_db.Column(rds_db.Float, nullable=True)


class LabData(rds_db.Model):  # 실험데이터
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("meat.id"), primary_key=True)
    L = rds_db.Column(rds_db.Float, nullable=True)
    a = rds_db.Column(rds_db.Float, nullable=True)
    b = rds_db.Column(rds_db.Float, nullable=True)
    DL = rds_db.Column(rds_db.Float, nullable=True)
    CL = rds_db.Column(rds_db.Float, nullable=True)
    RW = rds_db.Column(rds_db.Float, nullable=True)
    ph = rds_db.Column(rds_db.Float, nullable=True)
    WBSF = rds_db.Column(rds_db.Float, nullable=True)
    cardepsin_activity = rds_db.Column(rds_db.Float, nullable=True)
    MFI = rds_db.Column(rds_db.Float, nullable=True)


class User(rds_db.Model):
    __tablename__ = "user"
    id = rds_db.Column(rds_db.String, primary_key=True)
    lastLogin = rds_db.Column(rds_db.String, nullable=False)
    name = rds_db.Column(rds_db.String, nullable=False)
    company = rds_db.Column(rds_db.String, nullable=True)
    position = rds_db.Column(rds_db.String, nullable=True)
    type = rds_db.Column(rds_db.String(50))

    __mapper_args__ = {"polymorphic_identity": "user", "polymorphic_on": type}


# associate table for many-to-many relationship between Meat and Normal
meat_user = rds_db.Table(
    "meat_user",
    rds_db.Column("meat_id", rds_db.String, rds_db.ForeignKey("meat.id")),
    rds_db.Column("user_id", rds_db.String, rds_db.ForeignKey("normal.id")),
)

# associate table for many-to-many relationship between Meat and Researcher
meat_user2 = rds_db.Table(
    "meat_user2",
    rds_db.Column("meat_id", rds_db.String, rds_db.ForeignKey("meat.id")),
    rds_db.Column("user_id", rds_db.String, rds_db.ForeignKey("researcher.id")),
)


class Normal(User):
    __tablename__ = "normal"
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("user.id"), primary_key=True)
    meatList = rds_db.relationship("Meat", secondary=meat_user, backref="normals")

    __mapper_args__ = {
        "polymorphic_identity": "normal",
    }


class Researcher(User):
    __tablename__ = "researcher"
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("user.id"), primary_key=True)
    meatList = rds_db.relationship(
        "Meat",
        secondary=meat_user,
        primaryjoin=id == meat_user.c.user_id,
        secondaryjoin=Meat.id == meat_user.c.meat_id,
        backref="researchers",
        lazy="dynamic",
    )
    revisionMeatList = rds_db.relationship(
        "Meat",
        secondary=meat_user2,
        primaryjoin=id == meat_user2.c.user_id,
        secondaryjoin=Meat.id == meat_user2.c.meat_id,
        backref="revision_researchers",
        lazy="dynamic",
    )

    __mapper_args__ = {
        "polymorphic_identity": "researcher",
    }


class Manager(User):
    __tablename__ = "manager"
    id = rds_db.Column(rds_db.String, rds_db.ForeignKey("user.id"), primary_key=True)
    pwd = rds_db.Column(rds_db.String, nullable=False)  # 암호화 완료

    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }
