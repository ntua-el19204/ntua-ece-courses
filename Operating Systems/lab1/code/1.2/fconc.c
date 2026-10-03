#include "write_file.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

int main (int argc , char **argv){
        if (argc < 3 || argc > 4){
                printf("we need 2 or 3 files! \n");
        }
        if (argc == 4){
                int fd, oflags, mode;
                oflags = O_CREAT | O_WRONLY | O_TRUNC;
                mode = S_IRUSR | S_IWUSR;
                fd = open(argv[3], oflags, mode);
                if (fd == -1){perror("open");exit(1);}

                write_file(fd,argv[1]);
                write_file(fd,argv[2]);
                close(fd);
                return 0;
        }
        if (argc == 3){
                int fd, oflags, mode;
                oflags = O_CREAT | O_WRONLY | O_TRUNC;
                mode = S_IRUSR | S_IWUSR;
                fd = open("fconc.out", oflags, mode);
                if (fd == -1){perror("open");exit(1);}

                write_file(fd,argv[1]);
                write_file(fd,argv[2]);
                close(fd);
                return 0;

        }

}
