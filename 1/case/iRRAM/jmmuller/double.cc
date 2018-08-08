#include <string>
#include <iostream>
#include <cfenv>
#include "../../../src/points.h"

// e_example
double jmmuller(int count) {
    double a = double(11)/2.0, b=double(61)/11.0, c;

    for (long i=0;i<count;i++ ) {
        c=111-(1130-3000/a)/b;
        a=b; b=c;
    }
    for (long i=0;i<count;i++ ) {
        c=3000/(1130-(111-b)*a);
        b=a; a=c;
    }
    return a;
}
int main() {
    std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	std::string n_str;
	std::cin >> n_str;
	int n_int = binary2int(n_str);
	double r = jmmuller(n_int);
	std::cout << double2binary(r) << "\n";
}

