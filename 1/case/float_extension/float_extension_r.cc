#include <cmath>
#include <iostream>

#include "iRRAM.h"

using namespace iRRAM;

REAL evaluate(const REAL& x) {
    REAL r; 
    r=x;
    for (int i=1;i<100000;i++) r=r+REAL(1)/sqrt(REAL(i));
    return r;
}

void compute(){
    REAL x = 0;
    REAL res = evaluate(x);
    cout << setRwidth(24) << res << "\n";
}
