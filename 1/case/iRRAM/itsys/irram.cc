#include "iRRAM.h"
#include "../../../src/points.h"
#include "../../../src/self_math.h"
#include <algorithm>
#include <vector>
#include <sys/time.h>

using namespace iRRAM;


REAL itsyst(int n)
{
    REAL x = 0.5;
    REAL c = 3.75;
    std::vector<bool> record;
    for (int i = 0; i < n; ++i)
    {
        record.push_back(x.as_double()>=0.5); // 根据x与0.5大小来判断取正取负，这里加as_doubel是因为REAL无法判断REAL(0.5)>=0.5
        x = c * x * (REAL("1") - x);
    }
    for (int i = n-1; i >= 0; --i)
    {
        if (record[i]) {
            x = REAL("0.5") + sqrt(REAL("0.25") - REAL(4.0)/REAL(15.0)*x);
        } else {
            x = REAL("0.5") - sqrt(REAL("0.25") - REAL(4.0)/REAL(15.0)*x);
        }
    }
    return x;
}


void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout << iRRAM::setRwidth(30);
	std::string n_str;
	iRRAM::cin >> n_str;
	int n_int = binary2int(n_str);
    struct timeval tstart, tfinish;
    if(gettimeofday(&tstart,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
	iRRAM::REAL r_irram = itsyst(n_int);
    if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
	double r_double = r_irram.as_double();
	iRRAM::cout << usec << "\n";
	iRRAM::cout << double2binary(r_double) << "\n";
}


