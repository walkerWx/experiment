# Makefile for user_programs

#PROJECTHOME = /home/walker/Projects
PROJECTHOME = /Users/wangxie/Projects

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

KLEEEXEC = $(PROJECTHOME)/build_klee_dir/Release+Asserts/bin/klee
KLEEFLAGS = -I$(PROJECTHOME)/klee-expression/include/klee -emit-llvm -c -g

EXAMPLES_BIN = analytic_r analytic_f analytic_o

all: $(EXAMPLES_BIN)

bytecode: analytic_i.cc
	$(CXX) $(KLEEFLAGS) analytic_i.cc

expr:
	$(KLEEEXEC)	-check-div-zero=false *.bc
		
maintainer-clean: distclean
distclean: clean
	rm -f Makefile

clean:
	rm -rf $(EXAMPLES_BIN) *.bc klee-* expression.txt

install:
