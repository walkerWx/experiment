#include <string>
#include <iostream>
#include <cfenv>
#include <sys/time.h>
#include "../../../src/points.h"
#include "../../../src/self_math.h"

// Herbie case: float_extension
double float_extension(int n) {
    double r = 0;
    for (int i=1;i<n;i++) r=r+double(1)/sqrt(double(i));
    return r;
}
int main() {
    std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	std::string n_str;
	std::cin >> n_str;
	int n_int = binary2int(n_str);
    struct timeval tstart, tfinish;
    if(gettimeofday(&tstart,NULL)!=0){
        printf("Get time error!\n");
        return 1;
    }
	double r = float_extension(n_int);
	if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return 1;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    iRRAM::cout << usec << "\n";
	std::cout << double2binary(r) << "\n";
}

