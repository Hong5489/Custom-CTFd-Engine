#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAGSIZE_MAX 128

char flag[FLAGSIZE_MAX];

void setup(){
  FILE *f = fopen("flag.txt","r");
  fgets(flag,FLAGSIZE_MAX,f);
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
}


int main(int argc, char **argv){
  setup();
  int overflowMe = 0;
  char name[16];
  printf("Welcome to our second overflow challenge!\n");
  printf("Please do not enter your name over 28 characters!\n");
  printf("Enter your name: ");
  gets(name);
  if(overflowMe == 0xdeadbeef){
  	printf("Overflowwwww! Here's your flag: %s\n", flag);
  }
  else{
  	printf("Good Bye %s\noverflowMe now is equal 0x%x (Hex) or %i (Decimal)\n",name,overflowMe,overflowMe);
  }
  return 0;
}
