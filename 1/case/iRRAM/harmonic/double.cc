#include <string>
#include <iostream>
#include <cfenv>
#include <sys/time.h>
#include "../../../src/points.h"


double evaluate(int n) {
    int i=1;
    double initval = 0;
    for(i=1;i<n;++i){
        initval += (double(1)/double(i*i));
    }
    return initval;
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
	double r = evaluate(n_int);
	if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return 1;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    std::cout << usec << "\n";
	std::cout << double2binary(r) << "\n";
}
