# Makefile for user_programs

prefix=/home/walker/Projects/iRRAM/installed
exec_prefix=/home/walker/Projects/iRRAM/installed

CC = clang -std=c11
CFLAGS = -g -O2
CPP = clang -E
CPPFLAGS =     -I/home/walker/Projects/iRRAM/installed/include
CXX = clang++ -std=c++11
CXXCPP = clang++ -E -std=c++11
CXXFLAGS = -g -O2
LDFLAGS = -Xlinker -rpath -Xlinker /home/walker/Projects/iRRAM/installed/lib
LDLIBS =  -L/home/walker/Projects/iRRAM/installed/lib -liRRAM -lmpfr -lgmp -lm -lpthread

KLEEEXEC = /home/walker/Projects/build_klee_dir/Release+Asserts/bin/klee
KLEEFLAGS = -I/home/walker/Projects/klee-expression/include/klee -emit-llvm -c -g


all: float real

clean:
	rm -rf $(EXAMPLES_BIN) float.cpp real.cpp input output float real float_output real_output

install:
