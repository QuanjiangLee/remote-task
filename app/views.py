# coding=UTF-8
import sys
import os
import time 
import json
import datetime 
import subprocess
reload(sys)  
sys.setdefaultencoding('utf8')
#sys.setdefaultencoding('ISO-8859-1')

from flask import jsonify
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, LoginMa
from forms import loginForm, serviceForm
from models import UserInf, LogsInf
from sqlalchemy import desc

@app.before_first_request


def top_run():
    args = 'top -i -b -n1 -d 1 > test.top'
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdout, stderr) = p.communicate()
    if stderr:
        return False
    return True

@app.before_request
def before_request():
    g.user = current_user  
    print(g.user)
    top_run()

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
        print(userName, passWord, rem_me)
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
    dataTitle = '当前主机信息:'
    cmd1 = ["uname", "-ior"]
    cmd2 = ["uname", '-v']
    cmd3 = ['hostname']
    cmd4 = 'cat /proc/cpuinfo | grep name | cut -f2 -d: | uniq -c'
    data = more_exec(False, cmd1, cmd2, cmd3)
    data.append(cmd_exec(cmd4, True))
    data[0]["info"] = "内核版本"
    data[1]["info"] = "系统版本"
    data[2]["info"] = "主机名"
    data[3]["info"] = "CPU型号"
    return render_template('host.html', user=user, title=title, dataTitle=dataTitle, data=data, infoType='hostInfo')

@app.route('/getMsgCount', methods=['GET','POST'])
@login_required
def getMsgCount():
        cur_user = UserInf.query.filter_by(userName = current_user.userName).first()
        logsCount = LogsInf.query.filter_by(user_id=cur_user.userId, logStatus=False).count()
        print logsCount
        ret = {'msgCount': logsCount}
        return jsonify(ret) 

@app.route('/otherInfo')
def host_info():
    title = "其他信息"
    cmd = ['w', '-u']
    ret = more_exec(False, cmd)
    if ret[0]['is_exec']:
        data = ret[0]['cmdret'].split('\n')[:-1]
    else:
        data = []
    dataTitle="当前用户登录信息:"
    return render_template('host.html', title=title, data=data,dataTitle=dataTitle, infoType='otherInfo')


@app.route('/serviceManage')
def service_info():
    form = serviceForm()
    cmdret = []
    title = "服务信息"
    dataTitle = "服务信息:" 
    cmd = ['netstat', '-ntlp']
    info = more_exec(False, cmd)
    #data[0]["info"]="服务信息"
    data = info[0]['cmdret'].split('\n')
    #print data
    is_exec = info[0]['is_exec']
    if is_exec:
        for d in data[2:]:
            cmdret.append(d.split()) 
    #print cmdret
    return render_template('manageServ.html', title=title, dataTitle=dataTitle, cmdret=cmdret, is_exec=is_exec, form=form,infoType='service')


@app.route('/sourceInfo')
def source_Info():
    title = "资源信息"
    dataTitle = "资源信息:"  
    listData = []
    tableData = []
    with open('test.top', 'r') as f:
        lines = f.read()
    linesList = lines.split('\n')
    for list in linesList[:5]:
        listData.append(list)
    for data in linesList[6:]:
        tableData.append(data)
    return render_template('host.html', title=title, dataTitle=dataTitle, listData=listData, tableData=tableData, infoType='source')

@app.route('/getSourceInfo', methods=['GET', 'POST'])
def getSourceInfo():
    listData = []
    tableData = []
    with open('test.top', 'r') as f:
        lines = f.read()
    linesList = lines.split('\n')
    for list in linesList[:5]:
        listData.append(list)
    for data in linesList[6:]:
        tableData.append(data.split())
    return jsonify(listData=listData, tableData=tableData)


@app.route('/manageService', methods=['GET','POST'])
def manageService():
    form = serviceForm()
    if form.is_submitted():                   
        serviceName = request.form.get('serviceName', '')
        customCmd = request.form.get('customCmd', '')
        manageType = request.form.get('manageType', '')
        print('=========',serviceName, manageType,customCmd)
        if serviceName == '' and customCmd == '' and manageType == '':
            flash("The form is not should all null ")
            return redirect(request.args.get('next') or url_for('service_info'))
        if customCmd != '':
            type = customCmd.split()
            if len(type) > 2:
                if type[1] == 'start' or type[2] == 'start':
                    logType = 0
                elif type[1] == 'stop' or type[2] == 'stop':
                    logType = 1
                elif type[1] == 'restart' or type[2] == 'restart':
                    logType = 2
                else:
                    logType = 'unknow'
            else:
                logType = 'unknow'
            try:
                ret = cmd_exec(customCmd, False)
            except Exception :
                ret = cmd_exec(customCmd, True)
                if ret['is_exec'] is False:
                    msg = 'No such this service to Manage! The custom command is  error!'
                    flash(msg)
                    db_insert_logs(logType, msg, retStatus=False, logStatus=False)
                else:
                    msg = 'The custom command is success!'
                    flash(msg)
                    db_insert_logs(logType, msg, retStatus=True, logStatus=False)
        else:
            if serviceName != '' and manageType != '':
                cmd = 'systemctl' + ' ' + manageType +' '+ serviceName
                if manageType == 'start':
                    logType = 0
                elif manageType == 'stop':
                    logType = 1
                elif manageType == 'restart':
                    logType =2
                else:
                    logType = 'unknow'
                try:
                    ret = cmd_exec(cmd, False)
                except Exception :
                    ret = cmd_exec(cmd, True)
                if ret['is_exec'] is True:
                    msg = 'The ' +serviceName+ ' is '+ manageType + ' success!'
                    flash(msg)
                    db_insert_logs(logType, msg, retStatus=True, logStatus=False)
                    return redirect(request.args.get('next') or url_for('service_info'))
                else:
                    cmd = 'service' + ' ' + serviceName +' '+ manageType
                    if manageType == 'start':
                        logType = 0
                    elif manageType == 'stop':
                        logType = 1
                    elif manageType == 'restart':
                        logType = 2
                    try:
                        ret = cmd_exec(cmd, False)
                    except Exception :
                        ret = cmd_exec(cmd, True)
                    if ret['is_exec'] is False:
                        msg = 'No such this service to Manage! The ' +serviceName+ 'is '+ manageType + ' Failed!'
                        flash(msg)
                        db_insert_logs(logType, msg, retStatus=False, logStatus=False)
                    else:
                        msg = 'The ' +serviceName+ ' is '+ manageType + ' success!'
                        flash(msg)
                        db_insert_logs(logType, msg, retStatus=True, logStatus=False)
            else:
                flash("serviceName or manageType is not should null ")
    return redirect(request.args.get('next') or url_for('service_info')) 

@app.route('/serviceLog', methods=['GET', 'POST'])
def serviceLog():
    title = "logsInf"
    dataTitle = '进程操作日志:'
    logsRead = []
    try:
        cur_user = UserInf.query.filter_by(userName = current_user.userName).first()
        logs = LogsInf.query.filter_by(user_id=cur_user.userId).order_by(desc(LogsInf.logTime))
        for log in logs:
            logsRead.append(log.logStatus)
        print logsRead
        tmpLogs = LogsInf.query.filter_by(user_id=cur_user.userId)
        tmpLogs.update(dict(logStatus=True))
        db.session.commit()
    except Exception as err:
        print err
        flash('it\'s no logs in here ')
        return render_template('logsInf.html', title=title, dataTitle=dataTitle, logs=logs, logsRead=logsRead, infoType='logsInf')
    #logsLen = len(logs)
    return render_template('logsInf.html', title=title, dataTitle=dataTitle, logs=logs, logsRead=logsRead, infoType='logsInf')



def db_insert_logs(logType, logMsg, retStatus=False, logStatus=False):
    #cur_user = UserInf.query.filter_by(userName = cur_user.userName).first()
    try:
        log = LogsInf(logTime=datetime.datetime.utcnow(), logType=logType, logMsg=logMsg,retStatus=retStatus, logStatus=logStatus, user=current_user)
        db.session.add(log)
        db.session.commit()
    except Exception as err:
        print 'err is %s' % (err)
        return False
    return True

@app.route('/del_that_log', methods=['GET', 'POST'])
def db_delete_logs():
    if request.method == "GET":
        item = request.args.get('id', '')
    if request.method == "POST":
        data = request.get_json(force=False)
        item = data['item']
    try:
        print item
        cur_user = UserInf.query.filter_by(userName = current_user.userName).first()
        del_log = LogsInf.query.filter_by(id=int(item), user_id=cur_user.userId).first()
        db.session.delete(del_log)
        db.session.commit()
    except Exception as err:
        print err
        flash('delete log error!')
        #ret = {'ret': False}
        return redirect(request.args.get('next') or url_for('serviceLog'))
    #ret = {'ret': True} 
    #return jsonify(ret)
    flash('delete log success!')
    return redirect(request.args.get('next') or url_for('serviceLog'))

@app.route('/getProcessInfo', methods=['GET', 'POST'])
@app.route('/getProcessInfo/<int:page>', methods=['GET', 'POST'])
def getProcessInfo(page = 1):
    #if request.method == "GET":
    #    page = request.args.get('page', '')
    dataTitle = '进程管理:'
    start = (page-1) * 15 +1
    end = start + 15
    lineCount = -1 
    lines = []
    tableData = []
    with open('test.ps', 'r') as f:
        for line in f:
            lineCount += 1
            if lineCount < start:
                continue
            lines.append(line)
            if len(lines) >= 15:
                break  
    for line in lines:
        list = line.split()
        if len(list) > 11:
            print len(list)
            for i in range(11, len(list)):
                list[10] += ' '+list[i]
            print list[10]
        tableData.append(list[:11])
    return render_template('manageServ.html', dataTitle=dataTitle, tableData = tableData, infoType='processManage')



# R, S -> T: 
# kill -STOP PID
# T -> S, R:
# kill -CONT PID

# get process source info to file
def process_info():
    cmd = 'ps -aux > test.ps'
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except Exception as err:
        print('error is ' + err)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    (stdout, stderr) = p.communicate()
    if stderr:
        return False
    return True


# R,S -> T
def process_stop(pid):
    cmd = 'kill -STOP %s' % pid
    try:
        ret = cmd_exec(cmd)
    except Exception :
        ret = cmd_exec(cmd, True)
    return ret

# T -> S,R
def process_start(pid):
    cmd = 'kill -CONT %s' % pid 
    try:
        ret = cmd_exec(cmd)
    except Exception :
        ret = cmd_exec(cmd, True)
    return ret

# search process via pNmae
def process_search(pName):
    cmd = 'ps -aux | grep %s | grep -v grep' % pName
    try:
        ret = cmd_exec(cmd)
    except Exception :
        ret = cmd_exec(cmd, True)
    return ret


def cmd_run(args, option=False) :
    is_exec = True
    print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=option)
    (stdout, stderr) = p.communicate()
    if stderr:
        is_exec = False
        return is_exec, stderr
    return is_exec, stdout

def cmd_exec(cmd, option=False):
    is_exec, cmdout = cmd_run(cmd, option)
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

def more_exec(option=False, *args):
    more_ret=[]
    for arg in args:
        ret = cmd_exec(arg, option)
        more_ret.append(ret)
    return more_ret


