SHELL = /bin/sh

# make clean
# make all
# make corruption_simulation

OBJS = main.o Controller.o Filter.o HarmonicModel.o Model.o RungeKutta.o VanderPolModel.o
CFLAGS =
CC = clang++
INCLUDES = -I/usr/local/include
LIBS = -L/usr/local/lib -lgsl -lgslcblas

all:corruption_simulation

corruption_simulation:${OBJS}
	${CC} ${CFLAGS} ${INCLUDES} -o $@ ${OBJS} ${LIBS}

clean:
	-rm -f *.o core *.core *.dat

.cpp.o:
	${CC} ${CFLAGS} ${INCLUDES} -c $<


