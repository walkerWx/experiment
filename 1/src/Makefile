# Makefile for user_programs

iRRAM_HOME=/home/walker/Projects/iRRAM

CC = clang -std=c11
CFLAGS = -g -O2
CPP = clang -E
CPPFLAGS =  -I$(iRRAM_HOME)/installed/include
CXX = clang++ -std=c++11
CXXCPP = clang++ -E -std=c++11
CXXFLAGS = -g -O2
LDFLAGS = -Xlinker -rpath -Xlinker $(iRRAM_HOME)/installed/lib
LDLIBS =  -L$(iRRAM_HOME)/installed/lib -liRRAM -lmpfr -lgmp -lm -lpthread

all: float real bits_error analysis

float: points.o 

real: points.o

bits_error: points.o

analysis: points.o

points.o: points.cc points.h

clean:
	rm -rf $(EXAMPLES_BIN) float.cpp real.cpp input output float real float_output real_output points.o bits_error analysis

install:
