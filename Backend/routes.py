from flask import Blueprint, request, jsonify # For web request
from flask_login import login_user, logout_user, current_user, LoginManager # For Login 
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing
import hashlib # For password hashing
from db_connect import User3,rds_db
from app import app

# 1. Login Routing
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User3.query.get(user_id)

auth = Blueprint('auth', __name__)

