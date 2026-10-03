#include <unistd.h>
#include <stdio.h>
#include <string.h>


void doWrite(int fd, const char *buff, int len)
{
        size_t idx = 0;
        ssize_t wcnt;
                do
                {
                        wcnt = write(fd,buff + idx, len + idx);
                        if (wcnt == -1){ perror("write"); return;}
                        idx += wcnt;
                } while (idx < len);
}
