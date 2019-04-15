#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<netinet/in.h>
#include<error.h>
#include<string.h>
#include<unistd.h>
#include<arpa/inet.h>

#define MAX_CLIENTS 2
#define MAX_DATA 1024

void main(int argc, char **argv)
{
	struct sockaddr_in remote_server;
	int sock, len;
	char input[MAX_DATA];
	char output[MAX_DATA];

	if(argc != 3)
	{
		printf("Too few arguments \n");
		printf("Usage: %s <IP address> <port number> \n", argv[0]);
		exit(1);
	}

	if((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		perror("server socket: ");
		exit(-1);
	}

	remote_server.sin_family = AF_INET;
	remote_server.sin_port = htons(atoi(argv[2]));
	remote_server.sin_addr.s_addr = inet_addr(argv[1]);
	bzero(&remote_server.sin_zero, 8);

	if((connect(sock, (struct sockaddr *)&remote_server, sizeof(struct sockaddr_in))) == -1)
	{
		perror("connect");
		exit(-1);
	}

	while(1)
	{
		fgets(input, MAX_DATA, stdin);

		send(sock, input, strlen(input), 0);

		len = recv(sock, output, MAX_DATA, 0);
		output[len] = '\0';
		printf("%s \n", output);

	}

	close(sock);
}
