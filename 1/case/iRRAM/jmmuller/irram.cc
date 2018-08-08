#include <string>
#include <iostream>
#include "iRRAM.h"
#include <cfenv>
#include "../../../src/points.h"

using namespace iRRAM;
// jmmuller
iRRAM::REAL jmmuller(int count) {
  REAL a = REAL(11)/REAL(2.0), b=REAL(61)/REAL(11.0), c;

  for (long i=0;i<count;i++ ) {
    c=REAL(111)-(REAL(1130)-REAL(3000)/a)/b;
    a=b; b=c;
  }
  for (long i=0;i<count;i++ ) {
    c=REAL(3000)/(REAL(1130)-(REAL(111)-b)*a);
    b=a; a=c;
  }
  return c;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout << iRRAM::setRwidth(30);
	std::string n_str;
	iRRAM::cin >> n_str;
	int n_int = binary2int(n_str);
	iRRAM::REAL n_irram(n_int);
	iRRAM::REAL r_irram = jmmuller(n_irram);
	double r_double = r_irram.as_double();
	iRRAM::cout << double2binary(r_double) << "\n";
}