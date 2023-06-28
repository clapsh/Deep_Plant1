import keyId

# RDS Configuration
config = {
    "aws_db": {
        "user": "postgres",
        "password": "qwer1234",
        "host": keyId.rds_host,
        "port": "5432",  # Maria DB의 포트
        "database": "flask_db",
    }
}
