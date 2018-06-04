
#include <iostream>
#include <iomanip>
#include <limits>
#include <cmath>

#include "iRRAM.h"
#include "../../src/gamma.h"

#define euler_gamma (0.57721566490)

using namespace std;
using namespace iRRAM;


double evaluate(int n)
{
	double initval;

	if((true)&&((1000<=n&&n<=1099))) {
		initval = 0;
		{
			int i;
			i = 1;
			while(true) {
				if(i<n) {
					initval = initval+1.0/(i*i);
					i = i+1;
				}
				if(!(i<n)) {
					break;
				}
			}
		}
	}

	return initval;
}

void compute(){
	int n;
	std::cin >> n;
	std::cout << scientific << setprecision(numeric_limits<double>::digits10);
	std::cout << evaluate(n) << endl;
}

