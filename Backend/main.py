from flask import Flask # Flask Server import 
import firebase_admin # Firestore init

app = Flask(__name__)

# Firestore 연동
cred = firebase_admin.credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firebase_admin.client()

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