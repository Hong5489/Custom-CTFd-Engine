#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

#define FLAGSIZE_MAX 64

char flag[FLAGSIZE_MAX];

void setup(){
  FILE *f = fopen("flag.txt","r");
  fgets(flag,FLAGSIZE_MAX,f);
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
}

int main(int argc, char **argv){
  setup();
  int authed = 0;
  char user[16];
  printf("Authenticate Me 1.0\n");
  printf("--------------------------------\n");
  printf("Enter your username: ");
  gets(user);
  // Haven't implement login function yet
  if(authed){
    printf("Welcome admin! Here is your flag: %s",flag);
  }else{
    printf("Good Bye %s\n",user);
  }
  return 0;
}
