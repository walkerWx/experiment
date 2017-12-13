#include <cmath>
#include <iostream>

#include "iRRAM.h"

using namespace iRRAM;

REAL evaluate(const int& n) {
    REAL r = 0;
    for (int i=1;i<n;i++) r=r+REAL(1)/sqrt(REAL(i));
    return r;
}

void compute(){
    int n = 10000;
    REAL res = evaluate(x);
    cout << setRwidth(24) << res << "\n";
}
