SHELL = /bin/sh

# make all
# make controller_test
# make clean

OBJS_CONTROLLER_TEST = controller_test.o ../Controller.o
CFLAGS = -g -O0
CC = clang++
INCLUDES =
LIBS = -L/usr/local/lib -L/usr/local/Cellar/gperftools/2.10/lib -lprofiler

all:controller_test

controller_test:${OBJS_CONTROLLER_TEST}
	${CC} ${CFLAGS} ${INCLUDES} -o $@ ${OBJS_CONTROLLER_TEST} ${LIBS}

clean:
	-rm -f *.o core *.core *.dat

.cpp.o:
	${CC} ${CFLAGS} ${INCLUDES} -c $<


