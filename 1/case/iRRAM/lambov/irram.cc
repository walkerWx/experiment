#include <string>
#include <iostream>
#include "iRRAM.h"
#include <cfenv>
#include "../../../src/points.h"

// e_example
iRRAM::REAL lambov(int n) {
    iRRAM::REAL e = iRRAM::exp(1);
    iRRAM::REAL s = 0;
    for (int i=1;i<n;i++) s = s+iRRAM::REAL(1)/fac_real(i);
    return e-s;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout << iRRAM::setRwidth(30);
	std::string n_str;
	iRRAM::cin >> n_str;
	int n_int = binary2int(n_str);
	iRRAM::REAL n_irram(n_int);
	iRRAM::REAL r_irram = lambov(n_irram);
	double r_double = r_irram.as_double();
	iRRAM::cout << double2binary(r_double) << "\n";
}
