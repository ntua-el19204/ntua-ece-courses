/*
 * mandel.c
 *
 * A program to draw the Mandelbrot Set on a 256-color xterm.
 *
 */

#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <pthread.h>

#include "../helpers/mandel-lib.h"

#define MANDEL_MAX_ITERATION 100000

/***************************
 * Compile-time parameters *
 ***************************/

/*
 * Output at the terminal is x_chars wide by y_chars long
*/
int y_chars = 50;
int x_chars = 90;

/*
 * The part of the complex plane to be drawn:
 * upper left corner is (xmin, ymax), lower right corner is (xmax, ymin)
*/
double xmin = -1.8, xmax = 1.0;
double ymin = -1.0, ymax = 1.0;

/*
 * Every character in the final output is
 * xstep x ystep units wide on the complex plane.
 */
double xstep;
double ystep;

/*
 * Shared state for process synchronization using Condition Variables
 */
struct shared_state {
	pthread_mutex_t mutex;
	pthread_cond_t cond;
	int current_line;
};

/*
 * This function computes a line of output
 * as an array of x_char color values.
 */
void compute_mandel_line(int line, int color_val[])
{
	/*
	 * x and y traverse the complex plane.
	 */
	double x, y;

	int n;
	int val;

	/* Find out the y value corresponding to this line */
	y = ymax - ystep * line;

	/* and iterate for all points on this line */
	for (x = xmin, n = 0; n < x_chars; x += xstep, n++) {

		/* Compute the point's color value */
		val = mandel_iterations_at_point(x, y, MANDEL_MAX_ITERATION);
		if (val > 255)
			val = 255;

		/* And store it in the color_val[] array */
		val = xterm_color(val);
		color_val[n] = val;
	}
}

/*
 * This function outputs an array of x_char color values
 * to a 256-color xterm.
 */
void output_mandel_line(int fd, int color_val[])
{
	int i;

	char point = '@';
	char newline = '\n';

	for (i = 0; i < x_chars; i++) {
		/* Set the current color, then output the point */
		set_xterm_color(fd, color_val[i]);
		if (write(fd, &point, 1) != 1) {
			perror("compute_and_output_mandel_line: write point");
			exit(1);
		}
	}

	/* Now that the line is done, output a newline character */
	if (write(fd, &newline, 1) != 1) {
		perror("compute_and_output_mandel_line: write newline");
		exit(1);
	}
}

void compute_and_output_mandel_line(int fd, int line)
{
	/*
	 * A temporary array, used to hold color values for the line being drawn
	 */
	int color_val[x_chars];

	compute_mandel_line(line, color_val);
	output_mandel_line(fd, color_val);
}

/*
 * Create a shared memory area, usable by all descendants of the calling
 * process.
 */
void *create_shared_memory_area(unsigned int numbytes)
{
	int pages;
	void *addr;

	if (numbytes == 0) {
		fprintf(stderr, "%s: internal error: called for numbytes == 0\n", __func__);
		exit(1);
	}

	/*
	 * Determine the number of pages needed, round up the requested number of
	 * pages
	 */
	pages = (numbytes - 1) / sysconf(_SC_PAGE_SIZE) + 1;

	/* Create a shared, anonymous mapping for this number of pages */
	addr = mmap(NULL, pages * sysconf(_SC_PAGE_SIZE), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	if (addr == MAP_FAILED) {
		perror("create_shared_memory_area: mmap failed");
		exit(1);
	}

	return addr;
}

void destroy_shared_memory_area(void *addr, unsigned int numbytes) {
	int pages;

	if (numbytes == 0) {
		fprintf(stderr, "%s: internal error: called for numbytes == 0\n", __func__);
		exit(1);
	}

	/*
	 * Determine the number of pages needed, round up the requested number of
	 * pages
	 */
	pages = (numbytes - 1) / sysconf(_SC_PAGE_SIZE) + 1;

	if (munmap(addr, pages * sysconf(_SC_PAGE_SIZE)) == -1) {
		perror("destroy_shared_memory_area: munmap failed");
		exit(1);
	}
}

int main(int argc, char *argv[])
{
	int line, N = 1;
	pid_t pid;

	if (argc > 1) {
		N = atoi(argv[1]);
		if (N <= 0) N = 1;
	}

	xstep = (xmax - xmin) / x_chars;
	ystep = (ymax - ymin) / y_chars;

	/* Allocate shared state structure containing mutex, condition variable, and current line counter */
	struct shared_state *state = create_shared_memory_area(sizeof(struct shared_state));

	/* Configure attributes for process-shared mutex and condition variable */
	pthread_mutexattr_t mattr;
	pthread_condattr_t cattr;

	pthread_mutexattr_init(&mattr);
	pthread_mutexattr_setpshared(&mattr, PTHREAD_PROCESS_SHARED);
	pthread_mutex_init(&state->mutex, &mattr);

	pthread_condattr_init(&cattr);
	pthread_condattr_setpshared(&cattr, PTHREAD_PROCESS_SHARED);
	pthread_cond_init(&state->cond, &cattr);

	state->current_line = 0;

	/* Fork N child processes */
	for (int i = 0; i < N; i++) {
		pid = fork();
		if (pid < 0) {
			perror("fork");
			exit(1);
		}

		if (pid == 0) {
			/* Child process i handles lines i, i+N, i+2N, ... */
			for (line = i; line < y_chars; line += N) {
				int color_val[x_chars];

				/* Compute Mandelbrot points in parallel without holding any lock */
				compute_mandel_line(line, color_val);

				/* Acquire lock to print sequentially */
				pthread_mutex_lock(&state->mutex);

				/* Wait until it's this line's turn to print */
				while (state->current_line != line) {
					pthread_cond_wait(&state->cond, &state->mutex);
				}

				/* Output the computed line */
				output_mandel_line(1, color_val);

				/* Increment counter to next line and broadcast to all waiting children */
				state->current_line++;
				pthread_cond_broadcast(&state->cond);

				pthread_mutex_unlock(&state->mutex);
			}
			exit(0);
		}
	}

	/* Parent process waits for all child processes */
	for (int i = 0; i < N; i++) {
		wait(NULL);
	}

	/* Clean up synchronization attributes and shared memory */
	pthread_mutex_destroy(&state->mutex);
	pthread_cond_destroy(&state->cond);
	pthread_mutexattr_destroy(&mattr);
	pthread_condattr_destroy(&cattr);

	destroy_shared_memory_area(state, sizeof(struct shared_state));

	reset_xterm_color(1);
	return 0;
}