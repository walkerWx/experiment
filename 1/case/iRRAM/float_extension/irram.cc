#include <string>
#include <iostream>
#include <cfenv>
#include <sys/time.h>

#include "iRRAM.h"
#include "../../../src/points.h"
#include "../../../src/self_math.h"

#define RECORDING_TIME 1

// Herbie case: float_extension
iRRAM::REAL irram_float_extension(int n) {
    iRRAM::REAL r = 0;
    for (int i=1;i<n;i++) r=r+1.0/sqrt(i);
    return r;
}
void compute() {
	std::string n_str;
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout.real_w=50;
	iRRAM::cin >> n_str;
	int n_int = binary2int(n_str);
    struct timeval tstart, tfinish;
    if(gettimeofday(&tstart,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
	iRRAM::REAL r_irram = irram_float_extension(n_int);
	double r_double = r_irram.as_double();
    if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    iRRAM::cout << usec << "\n";
	iRRAM::cout << double2binary(r_double) << "\n";
}