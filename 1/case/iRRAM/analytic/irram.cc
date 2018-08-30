#include <string>
#include <iostream>
#include <sys/time.h>
#include "iRRAM.h"
#include <cfenv>
#include "../../../src/points.h"

using namespace iRRAM;

REAL evaluate(REAL x, int degree = 15) {
    REAL res = 0;
    REAL powx = 1;
    for (int i = 0; i < degree; ++i) {
        powx = powx*x;
        res = res + powx;
    }
    return res;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout.real_w=50;
	std::string x_str;
	iRRAM::cin >> x_str;
	REAL x_double = binary2double(x_str);
    struct timeval tstart, tfinish;
    if(gettimeofday(&tstart,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
	iRRAM::REAL r_irram = evaluate(x_double);
	double r_double = r_irram.as_double();
    if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    iRRAM::cout << usec << "\n";
	iRRAM::cout << double2binary(r_double) << "\n";
}
