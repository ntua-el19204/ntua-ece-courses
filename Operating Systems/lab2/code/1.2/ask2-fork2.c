#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include "../helpers/tree.h"
#include "../helpers/proc-common.h"

static void create_fork_tree(struct tree_node *root)
{
	printf("%s Starting... \n", root->name);
	pid_t pid_child;
	int i,j,status;
	change_pname(root->name);
	if (root->nr_children == 0) sleep(5);

	for(i=0; i < root->nr_children; i++) {

		pid_child = fork();
		if (pid_child < 0) {perror("fork"); exit(1);}

		else if (pid_child == 0){

			create_fork_tree(root->children + i);
			exit(1);
		}
	}
	for (j=0; j < root->nr_children; j++) pid_child = wait(&status);
	printf("%s Exiting... \n", root->name);
}

int main(int argc, char *argv[]) {

	pid_t pid_root;
	if (argc != 2) {
		fprintf(stderr, "Usage: %s <input_tree_file>\n\n", argv[0]);
		exit(1);
	}
	struct tree_node *root;
	root = get_tree_from_file(argv[1]);

	pid_root = fork();
	if (pid_root < 0) {perror("fork"); exit(1);}
	else if (pid_root == 0){

		create_fork_tree(root);
		exit(1); // to vazo tora
	}
	else{
		sleep(1);
		show_pstree(pid_root);
	}

	return 0;
}
