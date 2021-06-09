FROM debian:stable-slim
RUN apt-get update && apt-get -y install gcc socat nano openssh-server python3 netcat

COPY config /etc/ssh/sshd_config
RUN mkdir /var/run/sshd
RUN mkdir /root/.ssh

RUN mkdir /ctf
RUN mkdir /ctfuser
RUN chmod 755 /ctf /ctfuser

RUN mkdir /ctf/challenges

COPY *.c /
COPY setup.sh /
RUN chmod +x setup.sh && ./setup.sh

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
