#include <string>
#include <iostream>
#include "iRRAM.h"
#include <cfenv>
#include <sys/time.h>
#include "../../../src/points.h"
#include "../../../src/self_math.h"

// e_example
//iRRAM::REAL lambov(int n) {
//    iRRAM::REAL e = iRRAM::exp((iRRAM::REAL)1);
//    iRRAM::REAL s = 0;
//    for (int i=0;i<=n;i++) s = s+iRRAM::REAL(1)/fac_real(i);
//    return e-s;
//}
iRRAM::REAL lambov(int n) {
    iRRAM::REAL s = "2.718281828459045235360287471352662497757";
    for (int i=n;i>=0;--i) s -= 1.0/fac(i);
    return s;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
    iRRAM::cout.real_w=50;
    std::string n_str;
    iRRAM::cin >> n_str;
    int n = binary2int(n_str);
    struct timeval tstart, tfinish;
    if(gettimeofday(&tstart,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
	iRRAM::REAL r_irram = lambov(n);
	double r_double = r_irram.as_double();
    if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    iRRAM::cout << usec << "\n";
	iRRAM::cout << double2binary(r_double) << "\n";
}
