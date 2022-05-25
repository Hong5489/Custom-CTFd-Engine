#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

int main(int argc, char **argv){
  char name[32];
  setvbuf(stdout, NULL, _IONBF, 0);
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  printf("Welcome to the fourth challenge!\n");
  printf("Can you get the flag now?\n");
  printf("Hint: %p\n",name);
  printf("Enter your name: ");
  gets(name);
  printf("Good Bye %s\n",name);
  return 0;
}
