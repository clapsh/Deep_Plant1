import keyId

# RDS Configuration
config = {
    "aws_db": {
        "user": keyId.rds_username,
        "password": "qwer1234",
        "host": keyId.rds_host,
        "port": "5432",  # Maria DB의 포트
        "database": keyId.rds_db_name,
    }
}
