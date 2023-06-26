from flask import Flask  # Flask Server import
from routes import main  # Flask Server Routing pages
from db_connect import rds_db  # RDS Connection Check
import db_config  # RDS Configuration
import os  # Port Number assignment
from apscheduler.schedulers.background import (
    BackgroundScheduler,
)  # Background running function
import firebase_connect  # Firebase Connect
import s3_connect  # S3 Connect
import keyId  # Key data in this Backend file
from flask_sqlalchemy import SQLAlchemy  # For implement RDS database in server
import db_config  # For implement RDS database in server


class MyFlaskApp:
    def __init__(self, config):
        self.app = Flask(__name__)

        # 1. Route Connection
        self.app.register_blueprint(main)

        # 2. RDS Config
        self.config = config
        self.app.config["SQLALCHEMY_DATABASE_URI"] = self._create_sqlalchemy_uri()
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = SQLAlchemy(self.app)

        # 3. Firebase Config
        self.firestore_conn = firebase_connect.FireBase_()

        # 4. S3 Database Config
        self.s3_conn = s3_connect.S3Bucket(keyId.s3_folder_name)

    def transfer_data_to_rds(self):
        """
        Firebase에서 새로 저장된 데이터들은 각각 다음의 변수에 저장됩니다.
        self.firestore_conn.temp_user1_data <= user1 database
        self.firestore_conn.temp_user2_data <= user2 database
        self.firestore_conn.temp_user3_data <= user3 database
        self.firestore_conn.temp_meat_data <= meat database
        """
        pass

    def _create_sqlalchemy_uri(self):  # uri 생성
        aws_db = self.config["aws_db"]
        return f"mysql+pymysql://{aws_db['user']}:{aws_db['password']}@{aws_db['host']}:{aws_db['port']}/{aws_db['database']}?charset=utf8"

    def run(self, host="0.0.0.0", port=8080):  # server 구동
        self.app.run(host=host, port=port)


# Server 구동
if __name__ == "__main__":
    app = MyFlaskApp(db_config.config)
    # 1. Background Fetch Data (FireStore -> Flask Server) , 30sec 주기
    scheduler = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
    scheduler.add_job(
        app.firestore_conn.transferDbData, "interval", minutes=0.5
    )  # 주기적 데이터 전송 firebase -> flask server

    # 2. Send data to S3 storage (Flask server(images folder) -> S3), 30sec
    scheduler.add_job(
        app.s3_conn.transferImageData, "interval", minutes=0.5
    )  # 주기적 이미지 데이터 전송 flask server -> S3

    # 3. Send data to RDS (FireStore -> RDS), 30sec
    scheduler.add_job(
        app.transfer_data_to_rds, "interval", minutes=0.5
    )  # 주기적 Json Data 전송 flask server -> RDS
    scheduler.start()

    # 3. Flask 서버 실행
    app.run()
