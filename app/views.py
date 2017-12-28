# coding=UTF-8
import sys  
import subprocess
reload(sys)  
sys.setdefaultencoding('utf8')
#sys.setdefaultencoding('ISO-8859-1')

from flask import jsonify
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, LoginMa
from forms import loginForm
from models import UserInf

@app.before_request
def before_request():
    g.user = current_user  
    print(g.user)

@LoginMa.user_loader
def load_User(userId):
    return UserInf.query.get(int(userId))

@app.route('/', methods=['GET', 'POST'])
def root():
    form = loginForm()
    return render_template('login.html', title='登录', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():                   
        userName = request.form.get('userName', '')
        passWord = request.form.get('passWord', '')
        rem_me = request.form.get('rem_me', False)
        print(userName, passWord, '--------')
        user = UserInf.query.filter_by(userName = userName).first()
        if  not user  or user.userPassword != passWord:
            flash("用户名或密码错误!")
            return render_template('login.html', title='登录', form=form)
        else:
            login_user(user, remember=rem_me)
            flash("登录成功!")
            return redirect(request.args.get('next') or url_for('index'))
        #flash('login requested for id="%s", rmember_me = %s' % (form.id_me.data, str(form.rem_me.data)))
        #return redirect('/index')
    else:
        flash("用户名或密码不能为空!")
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
@login_required
def logout():
    form = loginForm()
    logout_user()
    return redirect('/')


@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    user = g.user
    title = "主页"
    cmd1 = ["uname", "-ior"]
    cmd2 = ['hostname']
    cmd3 = ['crontab', '-l']
    data = more_exec(cmd1, cmd2, cmd3)
    data[0]["info"]="系统版本"
    data[1]["info"]="主机名"
    data[2]["info"]="任务列表"
    return render_template('index.html', user=user, title=title,data=data)

@app.route('/serviceInfo')
def host_info():
    title = "服务信息"
    cmd = ['netstat', '-ntlp']
    data = more_exec(cmd)
    data[0]["info"]="TCP服务"
    return render_template('index.html', title=title,data=data)

def more_exec(*args):
    more_ret=[]
    for arg in args:
        ret = cmd_exec(arg)
        more_ret.append(ret)
    return more_ret

def cmd_exec(cmd):
    is_exec, cmdout = cmd_run(cmd)
    if is_exec is True:
        ret = {
            "is_exec": True,
            "cmdret": cmdout  # 命令执行成功返回的数据
        }
        return ret
    else:
        ret = {
            "is_exec": False,
            "cmdret": cmdout,   # 命令错误信息
            "retopt": "Unkown"  # 结果替代信息
        }
        return ret

@app.route('/tcpServices')
def tcp_service():
    cmd = ['netstat', '-ntlp']
    data = cmd_exec(cmd)
    return jsonify(data)


def cmd_run(args):
    is_exec = False
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    (stdout, stderr) = p.communicate()
    if stdout:
        is_exec = True
        return is_exec, stdout
    return is_exec, stderr