#include <string>
#include <iostream>
#include <cfenv>
#include "../../../src/points.h"

// Herbie case: float_extension
double float_extension(int n) {
    double r = 0;
    for (int i=1;i<n;i++) r=r+double(1)/sqrt(double(i));
    return r;
}
int main() {
    std::fesetround(FE_TONEAREST);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	std::string n_str;
	std::cin >> n_str;
	int n_int = binary2int(n_str);
	double r = float_extension(n_int);
	std::cout << double2binary(r) << "\n";
}

