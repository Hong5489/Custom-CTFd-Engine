#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#define BUFSIZE 32
#define FLAGSIZE 128

void printFlag() {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  fgets(buf,FLAGSIZE,f);
  printf("Congrats!\nYou deserve your flag: %s",buf);
}

void vuln(){
  char buf[BUFSIZE];
  gets(buf);
  printf("Going to address 0x%x\n",__builtin_return_address(0));
}

int main(int argc, char **argv){
  setvbuf(stdout, NULL, _IONBF, 0);
  gid_t gid = getegid();
  setresgid(gid, gid, gid);
  printf("Welcome to the third challenge!\n");
  puts("In last challenge, you overflow a variable become 0xdeadbeef");
  puts("In this challenge, you have to overflow return address become the address at printFlag!");
  printf("The printFlag function address is at 0x%x\n",  __builtin_extract_return_addr(printFlag));
  puts("Overflow me to go to the printFlag function!");
  printf("\nPayload: ");
  vuln();
  printf("Your payload is not loooooong enough\n");
  printf("You failed =(\n");
  return 0;
}
