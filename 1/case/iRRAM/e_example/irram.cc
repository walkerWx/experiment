#include <string>
#include <iostream>
#include <cfenv>
#include <sys/time.h>
#include "iRRAM.h"
#include "../../../src/points.h"
#include "../../../src/self_math.h"

// e_example
iRRAM::REAL e_example(int n) {
    iRRAM::REAL z = 1;
    for (int i=1;i<n;i++) z = z+1.0/fac(i);
    return z;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout.real_w=50;
	std::string n_str;
	iRRAM::cin >> n_str;
	int n_int = binary2int(n_str);
    struct timeval tstart, tfinish;
    if(gettimeofday(&tstart,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
	iRRAM::REAL r_irram = e_example(n_int);
	double r_double = r_irram.as_double();
    if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    iRRAM::cout << usec << "\n";
	iRRAM::cout << double2binary(r_double) << "\n";
}
