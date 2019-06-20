# Custom CTFd engine
First run this:
```
pip install -r requirements.txt
```
Then install `docker` and `docker-compose` (For Debian):
```
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
echo 'deb https://download.docker.com/linux/debian stretch stable' > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get install docker-ce
pip install docker-compose
```

After that, run this and you're done!
```
docker-compose up
```