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

#def updateBinaryChallenge():
#	import subprocess
#	from CTFd.models import Teams
#	from os import system
#	existing_user = subprocess.check_output([b"docker",b"exec",b"server-skr",b"cat",b"/ctfuser/group"], stderr=subprocess.STDOUT).decode().split('ssh:x:102:\n')[1].split('\n')[:-1]
#	for e in existing_user:
#		team_name = e.split(":x:")[0]
#		team = Teams.query.filter_by(name=team_name).first_or_404()
#		system("docker exec server-skr cp -rp /ctf/. /home/%s/" % team_name)
#		system('''docker exec server-skr bash -c 'chown %s: /home/%s' ''' % (team_name,team_name))
#		generateBinaryFlag(team)
#	return "Success!"

def updateBinaryChallenge(chal):
	import os
	from CTFd.utils import get_config
	os.system(f"python3 update_binary_chal.py \"{chal}\" &")
	return "Success"
	# import subprocess
	# from CTFd.models import Teams
	# from os import system
	# import base64
	# existing_user = Teams.query.filter(Teams.secret.isnot(None))

	# flag = subprocess.check_output([b"docker",b"exec",b"server-skr",b"cat",b"/ctf/challenges/%s/flag.txt"%chal.encode()], stderr=subprocess.STDOUT).decode()[:-1]
	# for e in existing_user:
	# 	team_name = e.name

	# 	system("docker exec server-skr cp -rp /chal_template/challenges/%s/. /home/%s/challenges/%s" % (chal,team_name,chal))
	# 	system("""docker exec server-skr bash -c 'echo "%s" | base64 -d > /home/%s/challenges/%s/flag.txt'""" % (base64.b64encode(generateFlag(flag,e).encode()).decode(),team_name,chal))
	# 	# system('''docker exec server-skr bash -c 'chown %s: /home/%s' ''' % (team.name,team.name))
	# 	# generateBinaryFlag(team)
	# return "Success"

def updateTeamBinary(name):
	import subprocess
	from CTFd.models import Teams
	from os import system
	team = Teams.query.filter_by(name=name).first_or_404()
	system("docker exec server-skr cp -rp /chal_template/. /home/%s/" % name)
	system('''docker exec server-skr bash -c 'chown %s: /home/%s' ''' % (name,name))
	generateBinaryFlag(team)



# def createBinaryChallenge():
# 	from os import system


def createPort(challenge,flag,team,port):
	from os import system
	# system("docker run -d --name web_%i -e FLAG=\"%s\" -p %i:80 --network=\"custom-ctfd-engine_default\" %s" %(port.number,generateFlag(flag,team),port.number,challenge.docker_name))
	system(f"docker run -d --rm --name web_{port.url} -e FLAG=\"{generateFlag(flag,team)}\" -p {port.number}:80 --network=\"custom-ctfd-engine_default\" {challenge.docker_name}")
	# system("docker stop web_%i -t 1800 && docker rm web_%i && docker exec custom-ctfd-engine_db_1 bash -c \"mysql -uroot -pctfd ctfd -e 'delete from ports where number = %i;'\" &" % (port.number,port.number,port.number))
	system(f"""docker stop web_{port.url} -t 1800 && docker exec custom-ctfd-engine_db_1 bash -c "mysql -uroot -pctfd ctfd -e 'delete from ports where url = \\"{port.url}\\";'" &""")

def closePort(port_url):
	from os import system
	# system("docker stop web_%i -t 0; docker rm web_%i; docker network disconnect -f custom-ctfd-engine_default web_%i" % (port_number,port_number,port_number))
	system(f"docker stop web_{port_url} -t 0;")


def showCategory():
	from CTFd.models import db,Category,Challenges
	categories = Category.query.all()
	categories_name = [i.name for i in categories]
	# challenges = Challenges.query.all()
	# for c in challenges:
	# 	for i,name in enumerate(categories_name):
	# 		if c.category == name:
	# 			c.category_id = i
	# db.session.commit()
	return categories_name

def showCategoryDesc():
	from CTFd.models import Category
	response = []
	category = Category.query.order_by(Category.number).all()
	for c in category:
		response.append({
		    "id": c.id,
		    "name": c.name,
		    "description": c.description,
		    "number": c.number
		})
	return response

def selectCategory(id):
	from CTFd.models import Category
	c = Category.query.filter_by(id=id).first()
	return c

def currentCategory():
	response = []
	from CTFd.models import db,Challenges
	total_category = [i[0] for i in db.session.query(Challenges.category)]
	for c in total_category:
		if c not in response:
			response.append(c)
	return response

def checkShareFlag(correct_flag,wrong_flag):
	wrong_flag = wrong_flag[:-8] + "}"
	correct_flag = correct_flag[:-8] + "}"
	if wrong_flag == correct_flag:
		return True
	return False

def generateDifficulty(difficulty):
	if difficulty == 0:
		return "<span style='color:#37d63e;'>Beginner</span>"
	if difficulty == 1:
		return "<span style='color:#37d63e;'>Easy</span>"
	elif difficulty == 2:
		return "<span style='color:orange;'>Medium</span>"
	elif difficulty == 3:
		return "<span style='color:red;'>Hard</span>"
	elif difficulty == 4:
		return "<b><span style='color:#d60000;'>EXTREME</span></b>"

def announceDiscord(text):
	from CTFd.utils import get_config
	import os, base64
	os.system(f"python3 bot.py {get_config('token')} {get_config('channel')} {base64.b64encode(text.encode()).decode()}")

def getIPinfo(ip):
	from CTFd.utils import get_config
	import ipinfo
	if get_config('ipinfo_token'):	
		handler = ipinfo.getHandler(get_config('ipinfo_token'))
		details = handler.getDetails(ip)
		return details.country_name
	else:
		return "Missing ipinfo token"