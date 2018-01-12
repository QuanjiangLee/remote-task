from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, RadioField
from wtforms.validators import DataRequired

class loginForm(FlaskForm):
	userName = StringField('userName', validators=[DataRequired()])
	passWord = PasswordField('passWord', validators=[DataRequired()])
	rem_me = BooleanField('rem_me', default=False)


class serviceForm(FlaskForm):
	serviceName = StringField('serviceName', default='')
	manageType = RadioField('manageType', choices=[('start','start server'),('stop','stop server'),('restart','restart server')])
	customCmd = StringField('customCmd',default='')