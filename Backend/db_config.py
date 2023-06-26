import keyId
# RDS Configuration
config = {
    "aws_db": {
        "user": "admin",
        "password": "qwer1234",
        "host": keyId.rds_host,
        "port": "3306",  # Maria DB의 포트
        "database": "users",
    }
}