from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    MetaData,
    create_engine,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Species(Base):
    __tablename__ = "species"
    id = Column(Integer, primary_key=True)
    value = Column(String(255))


class PrimalCuts(Base):
    __tablename__ = "primalCuts"
    id = Column(Integer, primary_key=True)
    speciesId = Column(Integer,ForeignKey("species.id"),primary_key=True)
    value = Column(String(255))


class SecondaryCuts(Base):
    __tablename__ = "secondaryCuts"
    id = Column(Integer, primary_key=True)
    primalId = Column(Integer,ForeignKey("primalCuts.id"),primary_key=True)
    value = Column(String(255))

class GradeNum(Base):
    __tablename__ = "gradeNum"
    id = Column(Integer, primary_key=True)
    value = Column(String(255))


class Meat(Base):
    __tablename__ = "meat"
    id = Column(String(255), primary_key=True)
    userId = Column(String(255))
    createdAt = Column(DateTime)
    traceNum = Column(String(255))
    farmAddr = Column(String(255))
    butcheryPlaceNum = Column(String(255))
    butcheryYmd = Column(DateTime)
    birthYmd = Column(DateTime)
    sexType = Column(Integer)

    species = Column(Integer, ForeignKey("species.id"))
    primalCuts = Column(Integer, ForeignKey("primalCuts.id"))
    secondaryCuts = Column(Integer, ForeignKey("secondaryCuts.id"))
    gradeNum = Column(Integer,ForeignKey("gradeNum.id"))

    freshmeat_seqno = Column(Integer)
    heatedmeat_seqno = Column(Integer)
    probexpt_seqno = Column(Integer)


class HistoryFreshmeatSenseval(Base):
    __tablename__ = "historyFreshmeatSenseval"
    id = Column(Integer, ForeignKey("meat.freshmeat_seqno"), primary_key=True)
    createdAt = Column(DateTime)
    userId = Column(String(255),ForeignKey("users.userId"))
    freshMeatId = Column(
        String(255), ForeignKey("meat.id"), primary_key=True
    )
    period = Column(Integer)
    marbling = Column(Float)
    color = Column(Float)
    texture = Column(Float)
    surfaceMoisture = Column(Float)
    overall = Column(Float)


class HistoryHeatedmeatSenseval(Base):
    __tablename__ = "historyHeatedmeatSenseval"
    id = Column(Integer, ForeignKey("meat.heatedmeat_seqno"), primary_key=True)
    createdAt = Column(DateTime)
    userId = Column(String(255),ForeignKey("users.userId"))
    period = Column(Integer)
    heatedMeatId = Column(
        String(255), ForeignKey("meat.id"), primary_key=True
    )
    flavor = Column(Float)
    juiciness = Column(Float)
    tenderness = Column(Float)
    umami = Column(Float)
    palability = Column(Float)


class HistoryProbexptSenseval(Base):
    __tablename__ = "historyProbexptSenseval"
    id = Column(Integer, ForeignKey("meat.probexpt_seqno"), primary_key=True)
    createdAt = Column(DateTime)
    userId = Column(String(255),ForeignKey("users.userId"))
    period = Column(Integer)
    probexptId = Column(String(255), ForeignKey("meat.id"), primary_key=True)
    L = Column(Float)
    a = Column(Float)
    b = Column(Float)
    DL = Column(Float)
    CL = Column(Float)
    RW = Column(Float)
    ph = Column(Float)
    WBSF = Column(Float)
    cardepsin_activity = Column(Float)
    MFI = Column(Float)
    Collagen = Column(Float)
    sourness = Column(Float)
    bitterness = Column(Float)
    umami = Column(Float)
    richness = Column(Float)


class UserType(Base):
    __tablename__ = "userType"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class User(Base):
    __tablename__ = "users"
    userId = Column(String(255), primary_key=True)
    createdAt = Column(DateTime)
    updatedAt = Column(DateTime)
    loginAt = Column(DateTime)
    password = Column(String(255))
    name = Column(String(255))
    company = Column(String(255))
    jobTitle = Column(String(255))
    type = Column(Integer, ForeignKey("userType.id"))
