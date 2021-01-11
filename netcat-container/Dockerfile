FROM python:3.7-slim
RUN apt-get update
RUN apt-get install socat gcc -y 
RUN pip install pycrypto
RUN apt-get install python2.7 sudo -y
RUN mkdir /challs
COPY challs/. /challs	
COPY setup.sh /setup.sh
RUN chmod +x /setup.sh

ENTRYPOINT /setup.sh
