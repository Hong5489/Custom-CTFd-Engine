#include <stdio.h>                                                                                                                    
#include <stdlib.h>                                                                                                                   
#include <string.h>                                                                                                                   
#include <unistd.h>                                                                                                                   
#include <sys/types.h> 

#define FLAGSIZE 128
#define BUFSIZE 64

void vuln()
{
	char flag[FLAGSIZE];                                                                                                                 
	FILE *f = fopen("flag.txt","r");                                                                                                    
	fgets(flag,FLAGSIZE,f);
	char buffer[BUFSIZE];

  	printf("What's is your name? ");
  	fgets(buffer, BUFSIZE, stdin);
  	printf("Welcome! ");
  	printf(buffer);
  	printf("Now what?");
}

int main(int argc, char **argv)
{
	setvbuf(stdout, NULL, _IONBF, 0);
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	printf("Format String is also a common vulnerability\n");
	printf("Now I give you a vulnerable function\n");
	printf("Can you leak the flag out?\n");

	vuln();
}