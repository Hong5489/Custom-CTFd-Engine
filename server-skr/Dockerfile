FROM debian:stable-slim
RUN apt-get update && apt-get -y install gcc socat nano openssh-server

COPY config /etc/ssh/sshd_config
RUN mkdir /var/run/sshd
RUN mkdir /root/.ssh

RUN mkdir /ctf
RUN mkdir /ctfuser
RUN chmod 700 /ctf /ctfuser

RUN mkdir /ctf/challenges
RUN mkdir /ctf/challenges/simple_overflow

WORKDIR /ctf/challenges/simple_overflow
COPY overflow.c ./
RUN echo "SKR{Ss1mple_0verfl0wW}" > flag.txt
RUN gcc -o overflow overflow.c -fno-stack-protector
RUN chmod 4755 overflow
RUN chmod 644 overflow.c
RUN chmod 400 flag.txt

RUN mkdir /ctf/challenges/auth_me
WORKDIR /ctf/challenges/auth_me
COPY auth.c ./
RUN echo "SKR{OveRWr1te_loc4l_vAr14bLe}" > flag.txt
RUN gcc -o auth auth.c -fno-stack-protector
RUN chmod 4755 auth
RUN chmod 644 auth.c
RUN chmod 400 flag.txt

RUN mkdir /ctf/challenges/auth_me2
WORKDIR /ctf/challenges/auth_me2
COPY auth2.c ./
RUN echo "SKR{C_St0p_rE4dinG_untIL_nuLL}" > flag.txt
RUN gcc -o auth2 auth2.c -fno-stack-protector
RUN chmod 4755 auth2
RUN chmod 644 auth2.c
RUN chmod 400 flag.txt

RUN mkdir /ctf/challenges/guess_num
WORKDIR /ctf/challenges/guess_num
COPY guess_num.c ./
RUN echo "SKR{Y0u're_sooo_D4mn_Luckyyyy}" > flag.txt
RUN gcc -o guess_num guess_num.c -fno-stack-protector
RUN chmod 4755 guess_num
RUN chmod 644 guess_num.c
RUN chmod 400 flag.txt

RUN mkdir /ctf/challenges/overflow2
WORKDIR /ctf/challenges/overflow2
COPY overflow2.c ./
RUN echo "SKR{Overfl0ww_Bin4ry_Byt35}" > flag.txt
RUN gcc -o overflow2 overflow2.c -fno-stack-protector
RUN chmod 4755 overflow2
RUN chmod 644 overflow2.c
RUN chmod 400 flag.txt

RUN mkdir /ctf/challenges/overflow3
WORKDIR /ctf/challenges/overflow3
COPY overflow3.c ./
RUN echo "SKR{Overfl0ww_R3turn_4ddre\$\$}" > flag.txt
RUN gcc -o overflow3 overflow3.c -fno-stack-protector -no-pie
RUN chmod 4755 overflow3
RUN chmod 644 overflow3.c
RUN chmod 400 flag.txt

RUN mkdir /ctf/beginner_reverse
WORKDIR /ctf/beginner_reverse
COPY beginner_reverse/beginner5.c .
RUN gcc -o beginner5 beginner5.c -std=c99

COPY beginner_reverse/beginner6.c .
RUN gcc -o beginner6 beginner6.c -std=c99

RUN cp -rp /ctf/. /chal_template/
WORKDIR /chal_template/challenges/simple_overflow
RUN rm overflow && ln -s /ctf/challenges/simple_overflow/overflow overflow 

WORKDIR /chal_template/challenges/auth_me
RUN rm auth && ln -s /ctf/challenges/auth_me/auth auth 

WORKDIR /chal_template/challenges/auth_me2
RUN rm auth2 && ln -s /ctf/challenges/auth_me2/auth2 auth2

WORKDIR /chal_template/challenges/overflow2
RUN rm overflow2 && ln -s /ctf/challenges/overflow2/overflow2 overflow2

WORKDIR /chal_template/challenges/overflow3
RUN rm overflow3 && ln -s /ctf/challenges/overflow3/overflow3 overflow3

WORKDIR /chal_template/challenges/guess_num
RUN rm guess_num && ln -s /ctf/challenges/guess_num/guess_num guess_num

WORKDIR /ctf
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
