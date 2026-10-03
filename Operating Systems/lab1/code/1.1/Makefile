all: myzing zing2

myzing: myzing.o main.o
                gcc main.o myzing.o -o myzing

zing2: zing2.o main.o
                gcc main.o zing2.o -o zing2

main.o: main.c
                gcc -Wall -c main.c
