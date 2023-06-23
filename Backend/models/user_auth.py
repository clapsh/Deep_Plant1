from db_connect import rds_db

class UserAuth(rds_db.Model):
    id = rds_db.Column(rds_db.Integer, primary_key =True)
    email = rds_db.Column(rds_db.String(100), nullable = False )
    pw = rds_db.Column(rds_db.String(50), nullable = False )
    name = rds_db.Column(rds_db.String(50), nullable = False )
    grade = rds_db.Column(rds_db.Integer)
    
    
    def __init__(self ,email, pw, name, grade):
        self.email = email
        self.pw = pw
        self.name = name
        self.grade = grade