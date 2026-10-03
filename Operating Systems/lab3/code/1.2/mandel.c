int n;
sem_t *sems;

void *compute_and_output_mandel_line(void *arg)
{
	/*
	 * A temporary array, used to hold color values for the line being drawn
	 */

	volatile int *help = arg;	/*
					 * volatile int* p; is a pointer to an int that the compiler will treat as volatile.
					 * This means that the compiler will assume that it is possible for the variable that p
					 * is pointing at to have changed even if there is nothing in the source code to suggest
					 * that this might occur.
					 * The only effect of volatile is to warn the compiler that the value of x might be changed
					 * from another thread.
					 */

	int line = *help;
	int color_val[x_chars];
	int j;

	for (j = line; j < y_chars; j = j + n) {

		signal(SIGINT, sigintHandler);

		compute_mandel_line(j, color_val);

		int mod = j % n;		// shows the thread that is currently running

		if (mod == 0) {

			sem_wait(&sems[n - 1]);
			output_mandel_line(1, color_val);
			sem_post(&sems[0]);
		}
		/*
		else if(mod == n-1) {

			sem_wait(&sems[n-2]);
			output_mandel_line(1, color_val);
			sem_post(&sems[n-1]);
		}
		*/

		else {
			sem_wait(&sems[mod - 1]);
			output_mandel_line(1, color_val);
			sem_post(&sems[mod]);
		}
	}
}

int main(int argc, char *argv[])
{
	//int n = argv[1];
	n = atoi(argv[1]);
	pthread_t t[n];

	sems = (sem_t *) malloc(sizeof(sem_t) * (n));

	// sem_init(&sem1, 0, 0); // initialize sem1 to 0
	// sem_init(&sem2, 0, 1); // initialize sem2 to 1

	int lines[n], i, ret;

	xstep = (xmax - xmin) / x_chars;
	ystep = (ymax - ymin) / y_chars;

	for (i = 0; i < n - 1; i++) {

		//printf("%d \n", n);
		sem_init(&sems[i], 0, 0);
	}
	sem_init(&sems[n - 1], 0, 1);

	/*
	 * draw the Mandelbrot Set, one line at a time.
	 * Output is sent to file descriptor '1', i.e., standard output.
	 */

	for (i = 0; i < n; i++) {

		lines[i] = i;
		//printf("%d \n", line);
		ret = pthread_create(&t[i], NULL, compute_and_output_mandel_line, &lines[i]);
		if (ret) {
			perror_pthread(ret, "pthread_create");
			exit(1);
		}

	}

	reset_xterm_color(1);

	for (i = 0; i < n; i++) pthread_join(t[i], NULL);

	/*
	for (line = 0; line < y_chars; line++) {
		compute_and_output_mandel_line(1, line);
	}
	*/
	reset_xterm_color(1);

	return 0;
}
