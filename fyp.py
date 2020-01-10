def generateFlag(flag,team):
	import hashlib
	import time
	index = flag.find('{')
	flag_format = flag[:index]
	flag = flag[index+1:-1]
	hashflag = hashlib.md5(team.name+flag+team.secret+str(time.mktime(team.created.timetuple()))).hexdigest()
	return "%s{%s_%s}" % (flag_format,flag,hashflag)

def generateBinaryFlag(team):
	import subprocess
	challenges = subprocess.check_output(["docker","exec","server-skr","ls","/ctf/challenges/"], stderr=subprocess.STDOUT)[:-1].split('\n')
	for c in challenges:
		flag = subprocess.check_output(["docker","exec","server-skr","cat","/ctf/challenges/%s/flag.txt"%c], stderr=subprocess.STDOUT)[:-1]
		from os import system
		system("""docker exec server-skr bash -c 'echo "%s" | base64 -d > /home/%s/challenges/%s/flag.txt'""" % (generateFlag(flag,team).encode("base64"),team.name,c))

def updateBinaryChallenge():
	import subprocess
	from CTFd.models import Teams
	from os import system
	existing_user = subprocess.check_output(["docker","exec","server-skr","cat","/ctfuser/group"], stderr=subprocess.STDOUT).split('ssh:x:102:\n')[1].split('\n')[:-1]
	for e in existing_user:
		team_name = e.split(":x:")[0]
		team = Teams.query.filter_by(name=team_name).first_or_404()
		system("docker exec server-skr cp -rp /ctf/. /home/%s/" % team_name)
        	system('''docker exec server-skr bash -c 'chown %s: /home/%s' ''' % (team_name,team_name))
        	generateBinaryFlag(team)
	return "Success!"

def createBinaryChallenge():
	from os import system


def createPort(challenge,flag,team,port):
	from os import system
	system("docker run -d --name web_%i -e FLAG=%s -p %i:80 --network=\"custom-ctfd-engine_default\" %s" %(port.number,generateFlag(flag,team),port.number,challenge.docker_name))

def closePort(port_number):
	from os import system
	system("docker stop web_%i -t 0; docker rm web_%i" % (port_number,port_number))

def showCategory():
	from CTFd.models import db,Category,Challenges
	categories = Category.query.all()
	categories = [i.name for i in categories]
	challenges = Challenges.query.all()
	for c in challenges:
		for i,name in enumerate(categories):
			if c.category == name:
				c.category_id = i
	db.session.commit()
	response = []
	for c in categories:
	 	response.append(c)
	# if len(categories) == 0:
	# 	total_category = [i[0] for i in db.session.query(Challenges.category)]
	# 	for c in total_category:
	# 		if c not in response:
	# 			response.append(c)
	# 			db.session.add(Category(name=c))
	# 	db.session.commit()
	# else:
	# 	current_category = currentCategory()
	# 	categories = [i.name for i in categories]
	# 	if len(current_category) == len(categories):
	# 		for c in categories:
	# 			response.append(c)
	# 	else:
	# 		response = categories[:]
	# 		if len(current_category) > len(categories):
	# 			for c in current_category:
	# 				if c not in categories:
	# 					response.append(c)
	# 					db.session.add(Category(name=c))
	# 		else:
	# 			for c in categories:
	# 				if c not in current_category:
	# 					response.remove(c)
	# 					db.session.delete(Category.query.filter_by(name=c).one())
	# 		db.session.commit()
	return response

def currentCategory():
	response = []
	from CTFd.models import db,Challenges
	total_category = [i[0] for i in db.session.query(Challenges.category)]
	for c in total_category:
		if c not in response:
			response.append(c)
	return response
