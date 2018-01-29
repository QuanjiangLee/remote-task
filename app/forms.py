from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, RadioField
from wtforms.validators import DataRequired

class loginForm(Form):
	userName = StringField('userName', validators=[DataRequired()])
	passWord = PasswordField('passWord', validators=[DataRequired()])
	rem_me = BooleanField('rem_me', default=False)


class serviceForm(Form):
	serviceName = StringField('serviceName', default='')
	manageType = RadioField('manageType', choices=[('start','start server'),('stop','stop server'),('restart','restart server')])
	customCmd = StringField('customCmd',default='')