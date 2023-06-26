from flask import Flask  # Flask Server import
<<<<<<< HEAD:Backend/app.py
from db_connect import rds_db
#from db_connect import rds_db  # RDS Connection Check
#from .firebase_connect import firebase_db  # Firebase Firestore Connection
#from . import db_config  # RDS Configuration
import os  # Port Number assignment
from flask_sqlalchemy import SQLAlchemy

"""
Firebase DB 구조 설계
1. [users] collection 
   document key => firebase authication userID
   Field => lastLogin: String, freshMeats: List<String>, heatedMeats: List<String>
2. [freshMeats] collection
   document key => 육류이력코드 (OPEN API) , String
   Field => 
3. [heatedMeats] collection

AWS S3 DB 구조 설계 - MySQL 사용
1. [users] table 
   primary_key => firebase authication userID
   Field => lastLogin: String, freshMeats: List<String>, heatedMeats: List<String>
2. [freshMeats] table 
   primary_key => 관리번호, String
   Field => 
3. [heatedMeats] table 
	 primary_key => 
"""
# @app.before_first_request
# def create_database():
#    rds_db.create_all()

# RDS Server Configuration

=======
from routes import main  # Flask Server Routing pages
from db_connect import rds_db  # RDS Connection Check
import db_config  # RDS Configuration
import os  # Port Number assignment
from apscheduler.schedulers.background import BackgroundScheduler # Background running function
import firebase_connect # Firebase Connect
import s3_connect

app = Flask(__name__)
app.register_blueprint(main) # Register the BluePrint

# 1. RDS & Server Connection
>>>>>>> upstream/main:Backend/main.py
def create_app(test_config=None):
   
    app = Flask(__name__)
    # Config 설정
    if test_config is None:
         app.config['SQLALCHEMY_DATABASE_URI']= "mysql://root:psh32451@localhost:3306/flaskaws"
         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        #app.config.from_object(db_config)
    else:
        app.config.update(test_config)
        
    @app.route('/test/')
    def test_page():
       return '<h1>Testing the Flask Application Factory Pattern</h1>'
    
    rds_db.init_app(app)
    #경로 
    import auth
    app.register_blueprint(auth.bp)
    
    from models import user_auth
    #app.register_blueprint(users.bp)
    
    import data_mgnt
    #app.response_class(data_mgnt.bp)
    
    return app

# 2. FireStore & Server Connection 
firestore_conn = firebase_connect.FireBase_()

# 3. S3 Connection
s3_conn = s3_connect.S3Bucket()

#Server 구동
if __name__ == "__main__":
    # 1. 서버 포트 지정
    port = int(os.environ.get("PORT", 8080))

    # 2. Background Fetch Data (FireStore -> Flask Server) , 30sec 주기
    scheduler = BackgroundScheduler(daemon=True,timezone='Asia/Seoul')
    scheduler.add_job(firestore_conn.transferDbData,'interval',minutes=0.5) # 주기적 데이터 전송 firebase -> flask server 
    scheduler.add_job(s3_conn.transferImageData,'interval',minutes=0.5) # 주기적 이미지 데이터 전송 flaks server -> S3 
    scheduler.start()

    # 2. Flask 서버 실행
    create_app()
    app.run(host="0.0.0.0", port=port)
