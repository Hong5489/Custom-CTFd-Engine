#!/bin/bash
cd beginner_reverse
socat -dd TCP4-LISTEN:"4005",fork,reuseaddr EXEC:"./beginner5",pty,echo=0,raw &
socat -dd TCP4-LISTEN:"4006",fork,reuseaddr EXEC:"./beginner6",pty,echo=0,raw &
/usr/sbin/sshd -D
