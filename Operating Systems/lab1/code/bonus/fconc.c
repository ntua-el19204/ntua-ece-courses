#include "write_file.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

int main (int argc , char **argv){
        if (argc < 3){
                printf("we need at least 2files! \n");
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
	  
	  if(argc >= 4){
                int fd, oflags, mode;
                oflags = O_CREAT | O_WRONLY | O_TRUNC;
                mode = S_IRUSR | S_IWUSR;
                fd = open(argv[argc-1], oflags, mode);
                if (fd == -1){perror("open");exit(1);}
		    for(int i = 1; i < argc - 1; i++) write_file(fd, argv[i]);
                close(fd);
                return 0;
	  }

}
