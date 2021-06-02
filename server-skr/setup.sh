#!/bin/bash
mkdir /ctf/challenges/simple_overflow

cd /ctf/challenges/simple_overflow
cp /overflow.c ./
echo "SKR{Ss1mple_0verfl0wW}" > flag.txt
gcc -o overflow overflow.c -fno-stack-protector
chmod 4755 overflow
chmod 644 overflow.c
chmod 400 flag.txt

mkdir /ctf/challenges/auth_me
cd /ctf/challenges/auth_me
cp /auth.c ./
echo "SKR{OveRWr1te_loc4l_vAr14bLe}" > flag.txt
gcc -o auth auth.c -fno-stack-protector
chmod 4755 auth
chmod 644 auth.c
chmod 400 flag.txt

mkdir /ctf/challenges/auth_me2
cd /ctf/challenges/auth_me2
cp /auth2.c ./
echo "SKR{C_St0p_rE4dinG_untIL_nuLL}" > flag.txt
gcc -o auth2 auth2.c -fno-stack-protector
chmod 4755 auth2
chmod 644 auth2.c
chmod 400 flag.txt

mkdir /ctf/challenges/guess_num
cd /ctf/challenges/guess_num
cp /guess_num.c ./
echo "SKR{Y0u're_sooo_D4mn_Luckyyyy}" > flag.txt
gcc -o guess_num guess_num.c -fno-stack-protector
chmod 4755 guess_num
chmod 644 guess_num.c
chmod 400 flag.txt

mkdir /ctf/challenges/overflow2
cd /ctf/challenges/overflow2
cp /overflow2.c ./
echo "SKR{Overfl0ww_Bin4ry_Byt35}" > flag.txt
gcc -o overflow2 overflow2.c -fno-stack-protector
chmod 4755 overflow2
chmod 644 overflow2.c
chmod 400 flag.txt

mkdir /ctf/challenges/overflow3
cd /ctf/challenges/overflow3
cp /overflow3.c ./
echo "SKR{Overfl0ww_R3turn_4ddre\$\$}" > flag.txt
gcc -o overflow3 overflow3.c -fno-stack-protector -no-pie
chmod 4755 overflow3
chmod 644 overflow3.c
chmod 400 flag.txt

mkdir /ctf/challenges/format_string
cd /ctf/challenges/format_string
cp /format.c ./
echo "SKR{L34k_7h3_Fl4G_fr0m_St4cK}" > flag.txt
gcc -o format format.c
chmod 4755 format
chmod 644 format.c
chmod 400 flag.txt

mkdir /ctf/beginner_reverse
cd /ctf/beginner_reverse
cp /beginner5.c .
gcc -o beginner5 beginner5.c -std=c99

cp /beginner6.c .
gcc -o beginner6 beginner6.c -std=c99

cp -rp /ctf/. /chal_template/
cd /chal_template/challenges/simple_overflow
rm overflow && ln -s /ctf/challenges/simple_overflow/overflow overflow 

cd ../auth_me
rm auth && ln -s /ctf/challenges/auth_me/auth auth 

cd ../auth_me2
rm auth2 && ln -s /ctf/challenges/auth_me2/auth2 auth2

cd ../overflow2
rm overflow2 && ln -s /ctf/challenges/overflow2/overflow2 overflow2

cd ../overflow3
rm overflow3 && ln -s /ctf/challenges/overflow3/overflow3 overflow3

cd ../guess_num
rm guess_num && ln -s /ctf/challenges/guess_num/guess_num guess_num

cd ../format_string
rm format && ln -s /ctf/challenges/format_string/format format

cd /ctf
apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /*.c