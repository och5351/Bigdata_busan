from flask_wtf import FlaskForm
<<<<<<< Updated upstream
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('이름', validators=[DataRequired(), Length(min=3, max=25)])
=======
from wtforms import StringField, TextAreaField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    userid = StringField('ID', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired(), EqualTo('password1', '비밀번호가 일치하지 않습니다')])
    username = StringField('Name', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    number = IntegerField('Number',validators=[DataRequired()])

class UserLoginForm(FlaskForm):
    userid = StringField('이름', validators=[DataRequired(), Length(min=3, max=25)])
>>>>>>> Stashed changes
    password = PasswordField('비밀번호', validators=[DataRequired()])