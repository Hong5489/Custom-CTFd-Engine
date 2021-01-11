#include <stdio.h>
#include <unistd.h>
#include <string.h>
#define FLAGSIZE_MAX 64

int main(int argc, char const *argv[])
{
	char flag[FLAGSIZE_MAX];
	FILE *f = fopen("flag.txt","r");
  	fgets(flag,FLAGSIZE_MAX,f);
	char buffer[40];
	char* string = "This is a string";
	char* dummy = "Not even close";
	char* dummy2 = dummy;
	char* nothing = dummy;
	char* dunlookhere = dummy;
	char* target = "Y0U M4D3 17!!";
	printf("Time to learn Format String with printf!!\n");
	sleep(1);
	printf("How do you print a string with printf?\n1. printf(\"%%s\",string);\n2. printf(\"%%d\",string);\n3. printf(\"%%f\",string);\n\nSelect option : ");
	while(scanf("\n%39[^\n]",buffer) == 1){
		printf("****************************************************************************************************\n");
		printf("Output: ");
		if(strcmp(buffer,"1") == 0){
			printf("%s",string);
			printf("\n****************************************************************************************************\n");	
			printf("\nCorrect Answer!!\n\n");
			break;
		}else if(strcmp(buffer,"2") == 0){
			printf("%d",string);
			printf("\n****************************************************************************************************\n");
			printf("\nWrong Answer!!\n\n");
		}else if(strcmp(buffer,"3") == 0){
			printf("%f",string);
			printf("\n****************************************************************************************************\n");
			printf("\nWrong Answer!!\n\n");
		}else{
			printf("Invalid option!!\nPlease select 1, 2 or 3: ");
		}
		printf("Select option : ");
	}
	sleep(1);
	printf("What is the output of this printf statement?\nprintf(\"This book cost me RM %%.2f\",666.f);\nOutput: ");
	while(scanf("\n%39[^\n]",buffer) == 1){
		if(strcmp(buffer,"This book cost me RM 666.00") == 0){
			printf("\nCorrect Answer!!\n\n");
			break;
		}else printf("\nWrong Answer!!\n\n");
		printf("Output: ");
	}
	sleep(1);
	printf("Ok, now comes the hard part!\nWhat's the output of this printf statement?\nprintf(\"%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c%%c\",105,108,111,118,101,102,111,114,109,97,116,115,116,114,105,110,103);\nOutput: ");
	while(scanf("\n%39[^\n]",buffer) == 1){
		if(strcmp(buffer,"iloveformatstring") == 0){
			printf("\nCorrect Answer!!\n\n");
			break;
		}else printf("\nWrong Answer!!\n\n");
		printf("Output: ");
	}
	sleep(1);
	printf("Good well done!!\nFinal question,\nWhat format of the format string to print the target variable with the statament below?\nprintf(\"format\",dummy,dummy2,nothing,dunlookhere,target);\nEnter the format: ");
	while(scanf("\n%39[^\n]",buffer) == 1){
		char output[100];
		sprintf(output,buffer,dummy,dummy2,nothing,dunlookhere,target,"You are close",flag); // How to print the flag out?
		printf("****************************************************************************************************\n");
		printf("Output: %s\n",output );
		printf("****************************************************************************************************\n");
		if(strstr(output,target) != 0){
			printf("Congrats!! You have completed all the questions!\nHave you get the flag? (The target is not the flag)\n");
			break;
		}else{
			printf("Just keep trying\nEnter the format: ");
		}
	}
	return 0;
}
