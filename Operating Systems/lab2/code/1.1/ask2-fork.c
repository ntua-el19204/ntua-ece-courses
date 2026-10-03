#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "proc-common.h"

#define SLEEP_PROC_SEC  10
#define SLEEP_TREE_SEC  3

/*
 * Create this process tree:
 * A-+-B---D
 *   `-C
 */
void fork_procs(void)
{
        /*
         * initial process is A.
         */

        change_pname("A");
        printf("A: Sleeping...\n");
        sleep(SLEEP_PROC_SEC);

        /* Create B */

        pid_t p_b;
        int status_b;
        p_b = fork();

        if(p_b < 0){

                /* fork B failed */
                perror("Fork failed in B creation");
                exit(1);
        }

        else if(p_b == 0){

                /* We are in node B! */

                change_pname("B");
                printf("B: Starting...\n");

                /* Create C */

                pid_t p_d;
                int status_d;

                p_d = fork();

                if(p_d < 0){

                        /* fork D failed */
                        perror("Fork failed in D creation");
                        exit(1);
                }

                if(p_d == 0){

                        /* We are in node D! */
                        change_pname("D");
                        printf("D: Starting...\n");

                        printf("D: Sleeping...\n");
                        sleep(SLEEP_PROC_SEC);

                        printf("D: Awake!\n");

                        printf("D: Exiting.\n");
                        exit(13);
                }

                /* We are in node B right now */
                printf("B: Waiting for D...\n");
                p_d = wait(&status_d);
                explain_wait_status(p_d, status_d);
                exit(19);

        }

        else if(p_b > 0){

                /* We are in node A right now */

                /* Creation of C */
                pid_t p_c;
                int status_c;
                p_c = fork();

                if(p_c < 0){

                        /* fork C failed */
                        perror("Fork failed in C creation");

                        exit(1);
                }

                if(p_c == 0){

                        /* We are in node C */
                        change_pname("C");
                        printf("We are in C node!\n");

                        printf("C: Sleeping...\n");
                        sleep(SLEEP_PROC_SEC);

                        printf("C: Awake!\n");

                        printf("C: Exiting.\n");
                        exit(17);
                }

        printf("Waiting for B\n");

        p_b = wait(&status_b);
        explain_wait_status(p_b, status_b);

        printf("Waiting for C\n");

        p_c = wait(&status_c);
        explain_wait_status(p_c, status_c);

        printf("A: Exiting...\n");
        exit(16);
        }




}

/*
 * The initial process forks the root of the process tree,
 * waits for the process tree to be completely created,
 * then takes a photo of it using show_pstree().
 *
 * How to wait for the process tree to be ready?
 * In ask2-{fork, tree}:
 *      wait for a few seconds, hope for the best.
 * In ask2-signals:
 *      use wait_for_ready_children() to wait until
 *      the first process raises SIGSTOP.
 */
int main(void)
{
        pid_t pid;
        int status;

        /* Fork root of process tree */
        pid = fork();
        if (pid < 0) {
                perror("main: fork");
                exit(1);
        }
        if (pid == 0) {
                /* Child */
                fork_procs();
                exit(1);
        }

        /*
         * Father
         */
        /* for ask2-signals */
        /* wait_for_ready_children(1); */

        /* for ask2-{fork, tree} */
        sleep(SLEEP_TREE_SEC);

        /* Print the process tree root at pid */
        show_pstree(pid);

        /* for ask2-signals */
        /* kill(pid, SIGCONT); */

        /* Wait for the root of the process tree to terminate */
        pid = wait(&status);
        explain_wait_status(pid, status);

        return 0;
}