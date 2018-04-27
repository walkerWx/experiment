
#include <iostream>
#include <iomanip>
#include <limits>
#include <cmath>

#include "iRRAM.h"
#include "../../src/gamma.h"

#define euler_gamma (0.57721566490)

using namespace std;
using namespace iRRAM;


double evaluate(double x)
{
	double res;

	if((true)&&((0.0<=x&&x<=1.0))) {
		res = ((((((((((((((x+(x*x))+((x*x)*x))+(((x*x)*x)*x))+((((x*x)*x)*x)*x))+(((((x*x)*x)*x)*x)*x))+((((((x*x)*x)*x)*x)*x)*x))+(((((((x*x)*x)*x)*x)*x)*x)*x))+((((((((x*x)*x)*x)*x)*x)*x)*x)*x))+(((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x))+((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+(((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+((((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+(((((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+((((((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x));
	}

	return res;
}

void compute(){
	double x;
	std::cin >> x;
	std::cout << scientific << setprecision(numeric_limits<double>::digits10);
	std::cout << evaluate(x) << endl;
}

