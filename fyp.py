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
		system("""docker exec server-skr bash -c 'echo "%s" > /home/%s/challenges/%s/flag.txt'""" % (generateFlag(flag,team),team.name,c))

def createPort(challenge,flag,team,port):
	from os import system
	system("docker run -d --name %s_%i -e FLAG=%s -p %i:80 %s" %(challenge.docker_name,port.id,generateFlag(flag,team),port.number,challenge.docker_name))

def closePort(docker_name,port_id):
	from os import system
	system("docker stop %s_%i -t 0; docker rm %s_%i" % (docker_name,port_id,docker_name,port_id))

def showCategory():
	from CTFd.models import db,Category,Challenges
	categories = Category.query.all()
	response = []
	if len(categories) == 0:
		total_category = [i[0] for i in db.session.query(Challenges.category)]
		for c in total_category:
			if c not in response:
				response.append(c)
				db.session.add(Category(name=c))
		db.session.commit()
	else:
		current_category = currentCategory()
		categories = [i.name for i in categories]
		if len(current_category) == len(categories):
			for c in categories:
				response.append(c)
		else:
			response = categories[:]
			if len(current_category) > len(categories):
				for c in current_category:
					if c not in categories:
						response.append(c)
						db.session.add(Category(name=c))
			else:
				for c in categories:
					if c not in current_category:
						response.remove(c)
						db.session.delete(Category.query.filter_by(name=c).one())
			db.session.commit()
	return response

def currentCategory():
	response = []
	from CTFd.models import db,Challenges
	total_category = [i[0] for i in db.session.query(Challenges.category)]
	for c in total_category:
		if c not in response:
			response.append(c)
	return response
