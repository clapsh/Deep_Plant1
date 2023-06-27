from main import rds_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class UserAuth(UserMixin ,rds_db.Model):
    id = rds_db.Column(rds_db.Integer, nullable = False ,unique=True, primary_key =True, autoincrement=True)
    email = rds_db.Column(rds_db.String(100), nullable = False ,unique=True)
    password_hash = rds_db.Column(rds_db.String(128))
    name = rds_db.Column(rds_db.String(50), nullable = False )
    grade = rds_db.Column(rds_db.Integer)
    confirmed = rds_db.Column(rds_db.Boolean, default=False)
    confirmation_token = rds_db.Column(rds_db.String(100))
        
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