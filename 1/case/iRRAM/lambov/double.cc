#include <string>
#include <iostream>
#include <cfenv>
#include "../../../src/points.h"

// lambov
double lambov(int n) {
    double e = exp(1);
    double s = 0;
    for (int i=1;i<n;i++) s = s + 1.0/fac(i);
    return e-s;
}
int main() {
    std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	std::string n_str;
	std::cin >> n_str;
	int n_int = binary2int(n_str);
	double r = lambov(n_int);
	std::cout << double2binary(r) << "\n";
}

