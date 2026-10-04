#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include "../helpers/tree.h"
#include "../helpers/proc-common.h"

#define READ_END 0
#define WRITE_END 1

int create_fork_tree(struct tree_node *root)
{

	pid_t pid_child, p, array[root->nr_children];
	int i,j,status;
	change_pname(root->name);
	// if (root->nr_children == 0) raise(SIGSTOP);
	if (root->nr_children == 0){

		printf("Terminated node %s \n", root->name);
		return (atoi(root->name));
	}
	else {
		int values[2];

		for(i=0; i < 2; i++) {

			printf("i = %d \n",i);
			int pfd[2];
			if (pipe(pfd) < 0){ perror("pipe"); exit(1); }

			pid_child = fork();

			if (pid_child < 0){perror("fork"); exit(1);}

			else if (pid_child == 0){

				close(pfd[READ_END]);
				int x = create_fork_tree(root->children + i);
				printf("x = %d \n", x);
				char str[16];
				sprintf(str, "%d", x); // int to string
				write(pfd[WRITE_END], str, sizeof(str));
				printf("before exit \n");
				exit(1);
			}
			close(pfd[WRITE_END]);
			p = wait(&status);
			explain_wait_status(p,status);
			char value[16];
			read(pfd[READ_END], &value, sizeof(value));

			printf("%d READ : %s \n", i, value);
			values[i] = atoi(value);
		}

		printf("%d \n", sizeof(root->name)); //root name is an array
		char new[3];
		for(j=0; j<3; j++) new[j] = (root->name)[j];
		printf("%d \n", sizeof(new));
		printf("%c \n \n", new[1]);

		if (new[1] == '+') {

			printf("+ Execution \n");
			int sum = values[0] + values[1];
			return sum;
			exit(1);
		}
		if (new[1] == '*') {

			printf("* Execution \n");
			int product = values[0] * values[1];
			return product;
			exit(1);
		}
	}
}

int main(int argc, char *argv[]) {

	int status, value;
	int fd[2];
	pid_t p, pid_root;
	if (argc != 2) {
		fprintf(stderr, "Usage: %s <input_tree_file>\n\n", argv[0]);
		exit(1);
	}
	struct tree_node *root;
	root = get_tree_from_file(argv[1]);

	if (pipe(fd) < 0) {
		perror("pipe");
		exit(1);
	}
	pid_root = fork();

	if (pid_root < 0) {perror("fork"); exit(1);}
	else if (pid_root == 0){

		printf("%s \n", root->name);
		printf("Start fork \n");
		int x = create_fork_tree(root);
		printf("%d \n", x);
		exit(1);
	}

	return 0;
}
