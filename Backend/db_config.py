import keyId

# RDS Configuration
aws_db = {
    "user": "admin",
    "password": "qwer1234",
<<<<<<< HEAD
    "host": "mysql-flaskserver.chd2ahxsforg.ap-northeast-2.rds.amazonaws.com",
    "port": "3306", # Maria DB의 포트
    "database": "flaskDatabase",
=======
    "host": keyId.rds_host,
    "port": "3306",  # Maria DB의 포트
    "database": "users",
>>>>>>> upstream/main
}

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}?charset=utf8"
