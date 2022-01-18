#!/bin/bash

useradd ctf
chown -R ctf:ctf /challs
useradd ctf2
chown -R ctf2:ctf2 /challs/calculator
chmod -R u-w,g-w,o-r /challs
#useradd -m -s /bin/bash user
#cp -r /challs/linux2/user/* /home/user
#chown -R user: /home/user
cd challs

sudo -u ctf socat TCP-LISTEN:2000,reuseaddr,fork EXEC:'python3 ecb/server.py'&
sudo -u ctf socat TCP-LISTEN:2001,reuseaddr,fork EXEC:'python3 ecb2/server.py'& 
sudo -u ctf socat TCP-LISTEN:2002,reuseaddr,fork EXEC:'/bin/sh netcat/server.sh'& 
sudo -u ctf socat TCP-LISTEN:2003,reuseaddr,fork EXEC:'python3 nimgame/server.py'&
sudo -u ctf socat TCP-LISTEN:2004,reuseaddr,fork EXEC:'python3 ecb3/server.py'&
sudo -u ctf socat TCP-LISTEN:2005,reuseaddr,fork EXEC:'python3 quickmaths/server.py'&
sudo -u ctf socat TCP-LISTEN:2006,reuseaddr,fork EXEC:'python3 quickmaths64/server.py'&
sudo -u ctf socat TCP-LISTEN:2007,reuseaddr,fork EXEC:'python3 cat/server.py'&
sudo -u ctf socat TCP-LISTEN:2008,reuseaddr,fork EXEC:'python3 xor/server.py'&
sudo -u ctf socat TCP-LISTEN:2009,reuseaddr,fork EXEC:'python3 hex_to_ascii/server.py'&
cd calculator
sudo -u ctf2 socat TCP-LISTEN:2010,fork,reuseaddr EXEC:"python2.7 server.py",pty,echo=0,stderr &
cd ../
sudo -u ctf socat TCP-LISTEN:2011,reuseaddr,fork EXEC:'python3 linux1/server.py',pty,echo=0,stderr &
sudo -u ctf socat TCP-LISTEN:2012,reuseaddr,fork EXEC:'python3 linux3/server.py',pty,echo=0,stderr &
sudo -u ctf socat TCP-LISTEN:2013,reuseaddr,fork EXEC:'python3 linux4/server.py',pty,echo=0,stderr &
sudo -u ctf socat TCP-LISTEN:2014,reuseaddr,fork EXEC:'python3 cat2/server.py'&

while true; do sleep 1000; done
