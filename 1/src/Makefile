# Makefile for user_programs

iRRAM_HOME=/home/whj/iRRAM_improved

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

float: points.o self_math.o

float_origin: points.o self_math.o

real: points.o self_math.o

bits_error: points.o self_math.o

analysis: points.o self_math.o

analysis_irram: points.o self_math.o

points.o: points.cc points.h

self_math.o: self_math.cc self_math.h

clean:
	rm -rf $(EXAMPLES_BIN) float.cpp real.cpp input output float real float_output points.o bits_error analysis

install:
