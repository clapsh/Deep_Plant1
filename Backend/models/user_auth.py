#import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#import login_manager
class UserAuth(UserMixin ):#,db.Model):
    # id = db.Column(db.Integer, nullable = False ,unique=True, primary_key =True, autoincrement=True)
    # email = db.Column(db.String(100), nullable = False ,unique=True)
    # password_hash = db.Column(db.String(128))
    # name = db.Column(db.String(50), nullable = False )
    # grade = db.Column(db.Integer)
    # confirmed = db.Column(db.Boolean, default=False)
    # confirmation_token = db.Column(db.String(100))#, unique=True)
    
    # def __init__(self ,email, pw, name, grade):
    #     self.email = email
    #     self.pw = pw
    #     self.name = name
    #     self.grade = grade
    #     self.confirmed = 0
    #     self.confirmation_token = 'string'
        
    @property 
    def password(self):
        raise AttributeError('비밀번호는 읽을 수 없습니다.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# @login_manager.user_loader
# def load_user(id):
#     print(id)
#     return UserAuth.query.get(int(id))  