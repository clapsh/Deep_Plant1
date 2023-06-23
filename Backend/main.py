from flask import Flask  # Flask Server import
from routes import main  # Flask Server Routing pages
from db_connect import rds_db  # RDS Connection Check
import db_config  # RDS Configuration
import os  # Port Number assignment
from apscheduler.schedulers.background import BackgroundScheduler # Background running function
import firebase_connect # Firebase Connect

app = Flask(__name__)
app.register_blueprint(main) # Register the BluePrint

# 1. RDS & Server Connection
def create_app(test_config=None):
    # Config 설정
    if test_config is None:
        app.config.from_object(db_config)
    else:
        app.config.update(test_config)
    rds_db.init_app(app)

# 2. FireStore & Server Connection 
firestore_conn = firebase_connect.FireBase_()

# Server 구동
if __name__ == "__main__":
    # 1. 서버 포트 지정
    port = int(os.environ.get("PORT", 8080))

    # 2. Background Fetch Data (FireStore -> Flask Server) , 30sec 주기
    scheduler = BackgroundScheduler(daemon=True,timezone='Asia/Seoul')
    scheduler.add_job(firestore_conn.transferDbData,'interval',minutes=0.5)
    scheduler.start()

    # 2. Flask 서버 실행
    create_app()
    app.run(host="0.0.0.0", port=port)
