#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include "../helpers/tree.h"
#include "../helpers/proc-common.h"

static void create_fork_tree(struct tree_node *root)
{
	pid_t pid_child, p, array[root->nr_children];
	int i,j,status;
	change_pname(root->name);
	// if (root->nr_children == 0) raise(SIGSTOP);

	for(i=0; i < root->nr_children; i++) {

		pid_child = fork();
		if (pid_child < 0){perror("fork"); exit(1);}

		else if (pid_child == 0){
			//array[i] = getpid();
			create_fork_tree(root->children + i);
			exit(2);
		}
		array[i] = pid_child; // #arrays = #parrents
	}
	wait_for_ready_children(root->nr_children);
	raise(SIGSTOP); // last stop is A

	for(i=0; i < root->nr_children; i++) {
		struct tree_node *help = root->children + i;
		printf("PID = %ld, name = %s is awake\n", (long)array[i], help->name);
		kill(array[i], SIGCONT);
		p = wait(&status);
		//p = waitpid(array[i], &status, WIFEXITED(status) | WUNTRACED);
		//explain_wait_status(p,status);

	}
	//raise(SIGCONT);
	exit(3);
}

int main(int argc, char *argv[]) {

	int status;
	pid_t p, pid_root;

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
	}
	else{

		wait_for_ready_children(1);
		show_pstree(pid_root);
		printf("PID = %ld, name = %s is awake\n", (long)getpid(), root->name);
		kill(pid_root, SIGCONT);
		p = wait(&status);
		//wait(&status);
		//explain_wait_status(pid_root, status);
	}

	return 0;
}
