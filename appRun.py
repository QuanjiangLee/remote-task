#set FLASK_APP=microblog.py 
import subprocess
from app import app
app.run(host='0.0.0.0', debug=True) 
#cmd = "kill -9 $(ps -ef | grep 'top -i -d 1' | grep -v grep | awk '{print $2}')"
#p = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)