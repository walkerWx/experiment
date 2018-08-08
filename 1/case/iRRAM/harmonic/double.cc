#include <string>
#include <iostream>
#include <cfenv>
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
	double r = evaluate(n_int);
	std::cout << double2binary(r) << "\n";
}
