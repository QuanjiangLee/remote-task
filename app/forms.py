from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class loginForm(FlaskForm):
	userName = StringField('userName', validators=[DataRequired()])
	passWord = PasswordField('passWord', validators=[DataRequired()])
	rem_me = BooleanField('rem_me', default=False)
