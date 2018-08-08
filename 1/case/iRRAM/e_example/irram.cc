#include <string>
#include <iostream>
#include "iRRAM.h"
#include <cfenv>
#include "../../../src/points.h"

// e_example
iRRAM::REAL e_example(int n) {
    iRRAM::REAL z = 1;
    for (int i=1;i<n;i++) z = z+iRRAM::REAL(1)/fac_real(i);
    return z;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout << iRRAM::setRwidth(30);
	std::string n_str;
	iRRAM::cin >> n_str;
	int n_int = binary2int(n_str);
	iRRAM::REAL n_irram(n_int);
	iRRAM::REAL r_irram = e_example(n_irram);
	double r_double = r_irram.as_double();
	iRRAM::cout << double2binary(r_double) << "\n";
}
