#!/usr/bin/python3

import threading
import time
import sys

# database.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from CTFd.models import db
from CTFd import CTFdFlask
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:ctfd@db/ctfd?charset=utf8mb4"
# sqldb = SQLAlchemy(app)
chal = sys.argv[1]
app = CTFdFlask(__name__)
# sqldb = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:ctfd@db/ctfd?charset=utf8mb4"


db.init_app(app)
app.app_context().push()
db.create_all()
# db.create_all()	


class myThread (threading.Thread):
   def __init__(self, name, team):
      threading.Thread.__init__(self)
      self.name = name
      self.team = team
   def run(self):
      print ("Starting " + self.name)
      updateBinary(self.team,self.name)
      print ("Exiting " + self.name)

def generateFlag(flag,team):
	import hashlib
	import time
	index = flag.find('{')
	flag_format = flag[:index]
	flag = flag[index+1:-1]
	m = (team.name+flag+team.secret+str(time.mktime(team.created.timetuple()))).encode()
	hashflag = hashlib.md5(m).hexdigest()[:6]
	return "%s{%s_%s}" % (flag_format,flag,hashflag)

# def generateBinaryFlag(team):
# 	import subprocess
# 	import base64
# 	from os import system
# 	system("""docker exec server-skr bash -c 'echo "%s" | base64 -d > /home/%s/challenges/%s/flag.txt'""" % (base64.b64encode(generateFlag(flag,team).encode()).decode(),team.name,update_challenge))


# import subprocess
# from CTFd.models import Teams
# from os import system
# existing_user = subprocess.check_output([b"docker",b"exec",b"server-skr",b"cat",b"/ctfuser/group"], stderr=subprocess.STDOUT).decode().split('ssh:x:102:\n')[1].split('\n')[:-1]

# flag = subprocess.check_output([b"docker",b"exec",b"server-skr",b"cat",b"/ctf/challenges/%s/flag.txt"%update_challenge], stderr=subprocess.STDOUT).decode()[:-1]
# for e in existing_user:
# 	team_name = e.split(":x:")[0]
# 	team = Teams.query.filter_by(name=team_name).first_or_404()
# 	t = myThread(team_name,team).start()
# 	t.join()

# def updateBinary(team):
# 	system("docker exec server-skr cp -rp /chal_template/challenges/%s /home/%s/challenges/%s" % (update_challenge,team.name,update_challenge))
# 	# system('''docker exec server-skr bash -c 'chown %s: /home/%s' ''' % (team.name,team.name))
# 	generateBinaryFlag(team)


# print ("Exiting Main Thread")
import subprocess
from CTFd.models import Teams
from os import system
import base64
existing_user = Teams.query.filter(Teams.secret.isnot(None))
flag = subprocess.check_output([b"docker",b"exec",b"server-skr",b"cat",b"/chal_template/challenges/%s/flag.txt"%chal.encode()], stderr=subprocess.STDOUT).decode()[:-1]

def updateBinary(team,team_name):
	system("docker exec server-skr cp -rp /chal_template/challenges/%s/. /home/%s/challenges/%s" % (chal,team_name,chal))
	system("""docker exec server-skr bash -c 'echo "%s" | base64 -d > /home/%s/challenges/%s/flag.txt'""" % (base64.b64encode(generateFlag(flag,team).encode()).decode(),team_name,chal))

for e in existing_user:
	team_name = e.name
	t = myThread(team_name,e)
	t.start()
	t.join()
	
	# system('''docker exec server-skr bash -c 'chown %s: /home/%s' ''' % (team.name,team.name))
	# generateBinaryFlag(team)
print ("Exiting Main Thread")