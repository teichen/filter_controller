SHELL = /bin/sh

# make clean
# make all
# make multifilter_run.dylib

OBJS = main.o Controller.o Filter.o HarmonicModel.o Model.o RungeKutta.o VanderPolModel.o
SRC = main.cpp Controller.cpp Filter.cpp HarmonicModel.cpp Model.cpp RungeKutta.cpp VanderPolModel.cpp
CFLAGS = -g -O0
CC = clang++
INCLUDES = -I/usr/local/include
LIBS = -L/usr/local/lib -L/usr/local/Cellar/gperftools/2.10/lib -lgsl -lgslcblas -lprofiler

all:multifilter_run.dylib

multifilter_run.dylib:
	${CC} -dynamiclib -o multifilter_run.dylib ${SRC} ${INCLUDES} ${LIBS}

clean:
	-rm -f *.o core *.core *.dat *.dylib

.cpp.o:
	${CC} ${CFLAGS} ${INCLUDES} -c $<


