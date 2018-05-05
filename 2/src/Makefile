# Makefile for user_programs

#PROJECTHOME = /home/walker/Projects
PROJECTHOME = /Users/wangxie/Projects

prefix=$(PROJECTHOME)/iRRAM/installed
exec_prefix=$(PROJECTHOME)/iRRAM/installed

CC = clang -std=c11
CFLAGS = -g -O2
CPP = clang -E
CXX = clang++ -std=c++11
CXXCPP = clang++ -E -std=c++11
CXXFLAGS = -g -O2

EXAMPLES_BIN = points

all: $(EXAMPLES_BIN)
		
maintainer-clean: distclean
distclean: clean
	rm -f Makefile

clean:
	rm -rf $(EXAMPLES_BIN) points.txt

install:
