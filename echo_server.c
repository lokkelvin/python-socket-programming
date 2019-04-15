#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<netinet/in.h>
#include<error.h>
#include<strings.h>
#include<unistd.h>
#include<arpa/inet.h>

#define MAX_CLIENTS 2
#define MAX_DATA 1024

void main(int argc, char **argv)
{
	struct sockaddr_in server;
	struct sockaddr_in client;
	int sock, new, data_len;
	int sockaddr_len = sizeof(struct sockaddr_in);
	char data[MAX_DATA];

	if(argc != 2)
	{
		printf("Too few arguments \n");
		printf("Usage: %s <port number> \n", argv[0]);
		exit(1);
	}

	if((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		perror("server socket: ");
		exit(-1);
	}

	server.sin_family = AF_INET;
	server.sin_port = htons(atoi(argv[1]));
	server.sin_addr.s_addr = INADDR_ANY;
	bzero(&server.sin_zero, 8);

	if((bind(sock, (struct sockaddr *)&server, sockaddr_len)) == -1)
	{
		perror("bind");
		exit(-1);
	}

	if((listen(sock, MAX_CLIENTS)) == -1)
	{
		perror("listen");
		exit(-1);
	}

	while(1)
	{
		if((new = accept(sock, (struct sockaddr *)&client, &sockaddr_len)) == -1)
		{
			perror("accept");
			exit(-1);
		}

		printf("New client connected from port number %d and IP address %s \n", ntohs(client.sin_port), inet_ntoa(client.sin_addr));

		data_len = 1;

		while(data_len)
		{
			data_len = recv(new, data, MAX_DATA, 0);

			if(data_len > 0)
			{
				send(new, data, data_len, 0);
				data[data_len] = '\0';
				printf("Sent message: %s", data);
			}
		}

		printf("Client disconnected \n");

		close(new);
	}
}
