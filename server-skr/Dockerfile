FROM debian:stable-slim
RUN apt-get update && apt-get -y install gcc socat nano openssh-server netcat python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential gdb

COPY config /etc/ssh/sshd_config
RUN mkdir /var/run/sshd
RUN mkdir /root/.ssh

RUN mkdir /ctf
RUN mkdir /ctfuser
RUN chmod 755 /ctf /ctfuser

RUN mkdir /ctf/challenges
RUN mkdir /ctf/linux_tutorials
COPY linux_tutorials /ctf/linux_tutorials

COPY *.c /
COPY setup.sh /
RUN chmod +x setup.sh && ./setup.sh
RUN pip install pwntools

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
