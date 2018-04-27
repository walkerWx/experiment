
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
	double z;

	if((true)&&((1<=n&&n<=9999))) {
		z = 1;
		{
			int i;
			double y;
			i = 1;
			y = 1.0;
			while(true) {
				if(i<n) {
					y = y/i;
					z = z+y;
					i = i+1;
				}
				if(!(i<n)) {
					break;
				}
			}
		}
	}

	return z;
}

void compute(){
	int n;
	std::cin >> n;
	std::cout << scientific << setprecision(numeric_limits<double>::digits10);
	std::cout << evaluate(n) << endl;
}

