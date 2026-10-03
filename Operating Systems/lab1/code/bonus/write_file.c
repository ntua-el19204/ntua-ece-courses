#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include <string.h>

#include "doWrite.h"

void  write_file(int fd, const char *infile)
{
        char buff[1024]; // may go in for
        ssize_t rcnt;
        int fd_source = open(infile, O_RDONLY);
        if (fd_source == -1) { perror("open"); exit(1); }

        for (;;) // copy infile to buffer and then to fd
        {
                rcnt = read(fd_source,buff,sizeof(buff)-1); // copy infile to buffer
                if (rcnt == 0) return;
                if (rcnt == -1){ perror("read"); return ; }
                buff[rcnt] = '\0';
                int len = strlen(buff);
                doWrite(fd, buff, len); // copy buffer to fd
        }

        close(fd);
        return;
}
