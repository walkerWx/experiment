CXX = clang++ -std=c++11
CXXFLAGS = -g -O2 -I.

DEPS = points.h
OBJS = points.o

all: points analysis

%.o: %.cc $(DEPS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

points: $(OBJS) main.cc
	$(CXX) -o $@ $^ $(CXXFLAGS)

analysis: $(OBJS) analysis.cc
	$(CXX) -o $@ $^ $(CXXFLAGS)
		
maintainer-clean: distclean
distclean: clean
	rm -f Makefile

clean:
	rm -rf points points.txt $(OBJS) *.dSYM

install:
