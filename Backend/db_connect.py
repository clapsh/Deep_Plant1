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
    deepAging = rds_db.Column(rds_db.String, nullable=True)  # as JSON string
    fresh = rds_db.Column(rds_db.JSON, nullable=True)  # as JSON string
    heated = rds_db.Column(rds_db.JSON, nullable=True)  # as JSON string
    tongue = rds_db.Column(rds_db.JSON, nullable=True)  # as JSON string
    lab_data = rds_db.Column(rds_db.JSON, nullable=True)  # as JSON string


class User1(rds_db.Model):
    id = rds_db.Column(rds_db.String, primary_key=True)
    meatList = rds_db.Column(rds_db.String,nullable=True)
    lastLogin = rds_db.Column(rds_db.String,nullable=False)
    name = rds_db.Column(rds_db.String,nullable=False)
    company = rds_db.Column(rds_db.String,nullable=True)
    position = rds_db.Column(rds_db.String,nullable=True)


class User2(rds_db.Model):
    id = rds_db.Column(rds_db.String, primary_key=True)
    meatList = rds_db.Column(rds_db.String,nullable=True)
    lastLogin = rds_db.Column(rds_db.String,nullable=False)
    name = rds_db.Column(rds_db.String,nullable=False)
    company = rds_db.Column(rds_db.String,nullable=True)
    position = rds_db.Column(rds_db.String,nullable=True)
    revisionMeatList = rds_db.Column(rds_db.String,nullable=True)


class User3(rds_db.Model):
    id = rds_db.Column(rds_db.String, primary_key=True)
    lastLogin = rds_db.Column(rds_db.String,nullable=False)
    name = rds_db.Column(rds_db.String,nullable=False)
    company = rds_db.Column(rds_db.String,nullable=True)
    position = rds_db.Column(rds_db.String,nullable=True)
    pwd = rds_db.Column(rds_db.String,nullable=False) # 암호화 완료
