import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# db연동 
from db_connect import rds_db
from models.user_auth import UserAuth
from sqlalchemy.exc import IntegrityError


bp = Blueprint('auth', __name__)#, url_prefix='/auth'

@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('auth/login.html')

@bp.route('/confirm/<token>', methods=('GET'))


@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password']
        name = request.form['name']
        #userAuths = UserAuth.query.all()
        error = None
        
        # error haddling 
        if not email:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
            
        if error is None:
            try:
                ua = UserAuth(email=email, pw = password,name=name, grade=0 )
                rds_db.session.add(ua)
                rds_db.session.commit()
            except IntegrityError: # 중복 유저 관리 
                error = f"User {email} is already registered."
                rds_db.session.rollback()
            else:
                return redirect(url_for("auth.login"))
            
        flash(error) # validation 실패시 팝업창 만들기 
        
    return render_template('auth/register.html') 

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()
        
        
        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password): 
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()   #session : dict that stores data across request
            session['user_id'] = user['id'] # users' id is stored in session -> 그 뒤에 request에서 사용 가능 
            return redirect(url_for('index'))
        
        flash(error)
        
    return render_template('auth/login.html')

@bp.before_app_request # 어떤 url가 request되든지 view 함수 실행전에 함수 등록  ->약간 이해 X 
def load_logged_in_user(): 
    user_id = session.get('user_id') # user id 가 session에 저장되어있는지 확인 
    
    if user_id is None:
        g.user = None
    else: # 해당 user의 데이터를 db에서 가져와서 g.user에 저장 
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
        
# logout 하고 블로그 첫 화면으로 ('index') 
@bp.route('/logout')
def logout():
    session.clear() # user id를 session에서 지워야함 -> load_logged_in_user에 남아있지 않게 
    return redirect(url_for('index')) 

# require authentication in other views 
def login_required(view):
    @functools.wraps(view) # https://hongl.tistory.com/250
    def wrapped_view(**kwargs):# new view function that wraps the original view 
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view 