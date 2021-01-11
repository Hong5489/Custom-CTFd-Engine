#include <stdio.h>
#include <string.h>

int checkPassword(char* pass){
	size_t length = strlen(pass);
	if(length != 14){
		return 0;
	}
	char* correct_pass = "BTDJJ`Qmvt`1o4";
	for (int i = 0; i < length; i++){
		if(pass[i] != correct_pass[i]-1){
			return 0;
		}
	}
	return 1;
}


int main () {
	char password[20];
	printf("Enter password: ");
	scanf("%19s",password);
	if (checkPassword(password))
	{
		printf("Welcome admin!\nFlag: SKR{%s}",password);
	}else{
		printf("Login failed!");
	}
}
