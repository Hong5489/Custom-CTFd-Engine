#!/usr/bin/python3

import threading
import time

# database.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
sqldb = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = sys.argv[1]


sqlDB = SQLAlchemy(app)
sqlDB.init_app(app)
sqlDB.create_all()


class myThread (threading.Thread):
   def __init__(self, name, team):
      threading.Thread.__init__(self)
      self.name = name
      self.team = team
   def run(self):
      print ("Starting " + self.name)
      updateBinary(self.team)
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

def generateBinaryFlag(team):
	import subprocess
	import base64
	challenges = subprocess.check_output([b"docker",b"exec",b"server-skr",b"ls",b"/ctf/challenges/"], stderr=subprocess.STDOUT)[:-1].split(b'\n')
	for c in challenges:
		flag = subprocess.check_output([b"docker",b"exec",b"server-skr",b"cat",b"/ctf/challenges/%s/flag.txt"%c], stderr=subprocess.STDOUT).decode()[:-1]
		from os import system
		system("""docker exec server-skr bash -c 'echo "%s" | base64 -d > /home/%s/challenges/%s/flag.txt'""" % (base64.b64encode(generateFlag(flag,team).encode()).decode(),team.name,c.decode()))


import subprocess
from CTFd.models import Teams
from os import system
existing_user = subprocess.check_output([b"docker",b"exec",b"server-skr",b"cat",b"/ctfuser/group"], stderr=subprocess.STDOUT).decode().split('ssh:x:102:\n')[1].split('\n')[:-1]
for e in existing_user:
	team_name = e.split(":x:")[0]
	team = Teams.query.filter_by(name=team_name).first_or_404()
	t = myThread(team_name,team).start()
	t.join()

def updateBinary(team):
	system("docker exec server-skr cp -rp /ctf/. /home/%s/" % team.name)
	system('''docker exec server-skr bash -c 'chown %s: /home/%s' ''' % (team.name,team.name))
	generateBinaryFlag(team)


print ("Exiting Main Thread")
