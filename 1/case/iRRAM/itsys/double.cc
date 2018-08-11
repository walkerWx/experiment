#include <string>
#include <iostream>
#include <cfenv>
#include <sys/time.h>
#include "../../../src/points.h"
#include "../../../src/self_math.h"


double itsyst(int n)
{
    double x = 0.5;
    double c = 3.75;
    std::vector<bool> record;
    for (int i = 0; i < n; ++i)
    {
        record.push_back(x>=0.5); // 根据x与0.5大小来判断取正取负，这里加as_doubel是因为REAL无法判断REAL(0.5)>=0.5
        x = c * x * (1 - x);
    }
    for (int i = n-1; i >= 0; --i)
    {
        if (record[i]) {
            x = 0.5 + sqrt(0.25 - 4.0/15.0*x);
        } else {
            x = 0.5 - sqrt(0.25 - 4.0/15.0*x);
        }
    }
    return x;
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
	double r = itsyst(n_int);
	if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return 1;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    std::cout << usec << "\n";
	std::cout << double2binary(r) << "\n";
}