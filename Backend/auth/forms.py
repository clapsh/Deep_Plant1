from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

email_regex = "([\.0-9a-zA-Z_-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}"

class LoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Length(1, 200), 
        Email('이메일 주소가 아닙니다.'), Regexp(email_regex, 0, '이메일 주소가 아닙니다.')])
    password = PasswordField('비밀번호', validators=[DataRequired()])
    remember_me = BooleanField('로그인 상태 유지')
    submit = SubmitField('로그인')


class SignupForm(FlaskForm):        
    email = StringField('이메일', validators=[DataRequired('이메일을 입력하세요.'), Length(1,200), Email('이메일 주소가 아닙니다.'),
        Regexp(email_regex, 0, '이메일 주소가 아닙니다.')])
    username = StringField('이름', validators=[DataRequired('이름을 입력하세요.'), Length(1, 20)])
    password = PasswordField('비밀번호', validators=[
        DataRequired('비밀번호를 입력하세요.'), EqualTo('password2', message='비밀번호가 일치하지 않습니다.'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
        '비밀번호는 문자, 숫자, 점, 밑줄만 사용할 수 있습니다.'), Length(10,16, '비밀번호는 10~16자리여야 합니다.')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호 확인을 입력하세요.')])
    submit = SubmitField('회원가입')