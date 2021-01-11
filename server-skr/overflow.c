#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define FLAGSIZE_MAX 128

char flag[FLAGSIZE_MAX];

void sigsegv_handler(int sig) {
  fprintf(stderr, "Overflowwwww! Here's your flag: %s\n", flag);
  fflush(stderr);
  exit(1);
}

void setup(){
  FILE *f = fopen("flag.txt","r");
  fgets(flag,FLAGSIZE_MAX,f);
  signal(SIGSEGV, sigsegv_handler);
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
}


int main(int argc, char **argv){
  setup();
  char name[16];
  printf("Welcome to our first challenge!\n");
  printf("Please do not enter your name over 24 characters!\n");
  printf("Enter your name: ");
  gets(name);
  printf("Good Bye %s\n",name);
  return 0;
}
