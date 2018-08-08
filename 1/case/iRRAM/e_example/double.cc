#include <string>
#include <iostream>
#include <cfenv>
#include "../../../src/points.h"

// e_example
double e_example(int n) {
    double z = 1;
    for (int i=1;i<n;i++) z = z + 1.0/fac(i);
    return z;
}
int main() {
    std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	std::string n_str;
	std::cin >> n_str;
	int n_int = binary2int(n_str);
	double r = e_example(n_int);
	std::cout << double2binary(r) << "\n";
}

