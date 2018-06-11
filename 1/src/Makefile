# Makefile for user_programs

# PROJECTHOME = /home/walker/Projects
PROJECTHOME = /Users/walker/Projects

prefix=$(PROJECTHOME)/iRRAM/installed
exec_prefix=$(PROJECTHOME)/iRRAM/installed

CC = clang -std=c11
CFLAGS = -g -O2
CPP = clang -E
CPPFLAGS =     -I$(PROJECTHOME)/iRRAM/installed/include
CXX = clang++ -std=c++11
CXXCPP = clang++ -E -std=c++11
CXXFLAGS = -g -O2
LDFLAGS = -Xlinker -rpath -Xlinker $(PROJECTHOME)/iRRAM/installed/lib
LDLIBS =  -L$(PROJECTHOME)/iRRAM/installed/lib -liRRAM -lmpfr -lgmp -lm -lpthread

all: float real bits_error analysis

float: points.o 

real: points.o

bits_error: points.o

analysis: points.o

points.o: points.cc points.h

clean:
	rm -rf $(EXAMPLES_BIN) float.cpp real.cpp input output float real float_output real_output points.o bits_error analysis

install:
