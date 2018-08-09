#include <string>
#include <iostream>
#include "iRRAM.h"
#include <cfenv>
#include "../../../src/points.h"

// Herbie case: float_extension
iRRAM::REAL irram_float_extension(int n) {
    iRRAM::REAL r = 0;
    for (int i=1;i<n;i++) r=r+iRRAM::REAL(1)/sqrt(iRRAM::REAL(i));
    return r;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout << iRRAM::setRwidth(30);
	std::string n_str;
//	iRRAM::cin >> n_str;
//	int n_int = binary2int(n_str);
    int n_int;
    iRRAM::cin >> n_int;
	iRRAM::REAL r_irram = irram_float_extension(n_int);
	double r_double = r_irram.as_double();
	iRRAM::cout << double2binary(r_double) << "\n";
}

