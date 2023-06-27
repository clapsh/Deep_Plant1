import functools
from flask import (
   flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, logout_user, login_required, current_user
from models.user_auth import UserAuth
from sqlalchemy.exc import IntegrityError
from .forms import SignupForm, LoginForm
import auth
# db연동 
from main import app


# 시작화면 : 로그인 페이지
@auth.route('/', methods=['GET', 'POST'])
def index():
    return 'hello'#render_template('../auth/login.html')

@auth.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    user = UserAuth.query.filter_by(confirmation_token=token).first()
    if user:
        user.confirmed = True
        app.db.session.commit()
        return 'Email confirmed successfully.'
    else:
        return 'Invalid token.'

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = SignupForm()
    # POST 일 때 form validation 을 trigger함 
    if form.validate_on_submit():
        # 중복 가입 확인 (이름으로)
        ua = UserAuth.query.filter_by(name=form.username.data).first()
        if not ua:
            # UserAuth 생성
            ua = UserAuth(email=form.email.data, password = form.password.data,name=form.username.data, grade=0,confirmed= 0, confirmation_token="string" )
            print("id :",ua.id)
            try:
                # DB에 저장 및 로그인 화면으로 redirect
                app.db.session.add(ua)
                app.db.session.commit()
                flash('가입되었습니다. 로그인 하세요.')
                return redirect(url_for("auth.login"))
            except IntegrityError: 
                # DB규칙에 맞지 않는 경우, DB rollback
                print(ua)
                print('password', ua.password_hash)
                flash("규칙에 맞지 않는 데이터입니다.")
                app.db.session.rollback()
        # 중복 가입된 경우 (이름)
        else:
            flash('이미 등록된 사용자입니다.')
    
    # GET 메소드이거나 validation에 문제가 있을 경우 회원가입 화면 render  
    return render_template('auth/register.html', form = form) 

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # email로 UserAuth에서 사용자 정보 찾아오기
        ua = UserAuth.query.filter_by(email=form.email.data.lower()).first()
        # 정상적인 로그인
        if ua is not None and ua.verify_password(form.password.data):
            login_user(ua, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('../auth.register') # change to index 
            return redirect(next)
        # 로그인 정보가 틀린 경우
        flash('이메일 또는 비밀번호를 확인하세요.')

    return render_template('../auth/login.html', form = form)      

# @bp.before_app_request # 어떤 url가 request되든지 view 함수 실행전에 함수 등록  -
# def load_logged_in_user(): 
#     user_id = session.get('user_id') # user id 가 session에 저장되어있는지 확인 
    
#     if user_id is None:
#         g.user = None
#     else: # 해당 user의 데이터를 db에서 가져와서 g.user에 저장 
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()
        
        
# logout 하고 블로그 첫 화면으로 ('index') 
@auth.route('/logout')
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
