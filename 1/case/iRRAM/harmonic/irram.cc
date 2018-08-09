#include <string>
#include <iostream>
#include "iRRAM.h"
#include <cfenv>
#include "../../../src/points.h"

// Herbie case: float_extension
iRRAM::REAL evaluate(int n) {
    int i=1;
    iRRAM::REAL initval = 0;
    for(i=1;i<n;++i){
        initval += (iRRAM::REAL(1)/iRRAM::REAL(i*i));
    }
    return initval;
}

void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout << iRRAM::setRwidth(30);
	std::string n_str;
	iRRAM::cin >> n_str;
	int n_int = binary2int(n_str);
	iRRAM::REAL r_irram = evaluate(n_int);
	double r_double = r_irram.as_double();
	iRRAM::cout << double2binary(r_double) << "\n";
}
