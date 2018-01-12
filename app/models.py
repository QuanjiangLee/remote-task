# coding=UTF-8

from app import db


class UserInf(db.Model):
    
    userId = db.Column(db.Integer, primary_key=True) #主键userId
    userName = db.Column(db.String(64), index=True, unique=True) #可索引，字段名唯一
    userPassword = db.Column(db.String(120)) 
    userEmail = db.Column(db.String(120), index=True, unique=True) #可索引，字段名唯一
    logs = db.relationship('LogsInf', backref='user', lazy='dynamic')
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.userId)
        except NameError:
            return str(self.userId)

    def __repr__(self):
        return '<UserInf %r>' % (self.userName) #格式化打印字符串，同def __str__(self)类似


# from app import db,models
# u = models.UserInf.query.get(1)
# import datetime
# log = models.LogsInf(logTime=datetime.datetime.utcnow(), logType=0, logMsg='test2',retStatus=True, logStatus=True, user=u)
# db.session.add(log)
# db.session.commit()
class LogsInf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logTime = db.Column(db.DateTime)
    logType = db.Column(db.Integer)
    logMsg = db.Column(db.String(64))
    retStatus = db.Column(db.Boolean,  default=False) 
    logStatus = db.Column(db.Boolean,  default=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user_inf.userId'))
    
    def __repr__(self):
        return '<LogsInf %r>' % (self.logMsg)