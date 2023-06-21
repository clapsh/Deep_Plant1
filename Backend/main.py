from flask import Flask  # Flask Server import
from db_connect import rds_db  # RDS Connection Check
from firebase_connect import firebase_db  # Firebase Firestore Connection
import db_config  # RDS Configuration
import os  # Port Number assignment


app = Flask(__name__)
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
   primary_key => 육류이력코드 (OPEN API) , String
   Field => 
3. [heatedMeats] table 
	 primary_key => 
"""


# RDS Server Configuration
def create_app(test_config=None):
    # Config 설정
    if test_config is None:
        app.config.from_object(db_config)
    else:
        app.config.update(test_config)
    rds_db.init_app(app)


# Server 구동
if __name__ == "__main__":
    # 1. 서버 포트 지정
    port = int(os.environ.get("PORT", 8080))

    # 2. Flask 서버 실행
    create_app().run(host="0.0.0.0", port=port)
