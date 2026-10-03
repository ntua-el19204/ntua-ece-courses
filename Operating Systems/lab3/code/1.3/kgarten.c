void child_enter(struct thread_info_struct *thr)
{
	if (!thr->is_child) {
		fprintf(stderr, "Internal error: %s called for a Teacher thread.\n",
			__func__);
		exit(1);
	}

	fprintf(stderr, "THREAD %d: CHILD ENTER\n", thr->thrid);

	pthread_mutex_lock(&thr->kg->mutex);

	while (1){
		int children;
		children = thr->kg->vc;

		int teachers;
		teachers = thr->kg->vt;

		int ratio;
		ratio = thr->kg->ratio;

		if ((teachers)*(ratio) < (children + 1))
			pthread_cond_wait(&thr->kg->cond1, &thr->kg->mutex);

		else{
			++(thr->kg->vc);
			break;
		}
	}

	pthread_mutex_unlock(&thr->kg->mutex);
}

void child_exit(struct thread_info_struct *thr)
{
	if (!thr->is_child) {
		fprintf(stderr, "Internal error: %s called for a Teacher thread.\n",
			__func__);
		exit(1);
	}

	fprintf(stderr, "THREAD %d: CHILD EXIT\n", thr->thrid);

	pthread_mutex_lock(&thr->kg->mutex);
	--( thr->kg->vc);

	int children;
	children = thr->kg->vc;

	int teachers;
	teachers = thr->kg->vt;

	int ratio;
	ratio = thr->kg->ratio;

	if (((teachers-1)*(ratio)) >= (children))
		pthread_cond_signal(&thr->kg->cond2);

	pthread_mutex_unlock(&thr->kg->mutex);
}

void teacher_enter(struct thread_info_struct *thr)
{
	if (thr->is_child) {
		fprintf(stderr, "Internal error: %s called for a Child thread.\n",
			__func__);
		exit(1);
	}

	fprintf(stderr, "THREAD %d: TEACHER ENTER\n", thr->thrid);

	pthread_mutex_lock(&thr->kg->mutex);
	++(thr->kg->vt);

	pthread_cond_broadcast(&thr->kg->cond1);

	pthread_mutex_unlock(&thr->kg->mutex);
}

void teacher_exit(struct thread_info_struct *thr)
{
	if (thr->is_child) {
		fprintf(stderr, "Internal error: %s called for a Child thread.\n",
			__func__);
		exit(1);
	}

	fprintf(stderr, "THREAD %d: TEACHER EXIT\n", thr->thrid);

	pthread_mutex_lock(&thr->kg->mutex);
	int children;
	children = thr->kg->vc;

	int teachers;
	teachers = thr->kg->vt;

	int ratio;
	ratio = thr->kg->ratio;

	if ((((teachers - 1) * (ratio)) < (children)))
		pthread_cond_wait(&thr->kg->cond2, &thr->kg->mutex);
	--(thr->kg->vt);
	pthread_mutex_unlock(&thr->kg->mutex);
}
