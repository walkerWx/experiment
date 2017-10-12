/**
 * From "Introduction to Numerical Ordinary and Partial Differential Equation Using" Chapter 5.3, Page 103
 * For computing HarmonicNumber[x, 2], the limitation is 6/pi
 */

#include "iRRAM.h"

using namespace iRRAM;

REAL evaluate(int n, REAL x) {
    int i=1;
    iRRAM::REAL harresult = 0;
    for(i=1;i<n;++i){
        harresult += (x/((REAL)i*i));
    }
    return harresult;
}

void compute() {
    int n = 70712; iRRAM::REAL x=1;
    REAL res = evaluate(n, x);
    cout << setRwidth(26) << res << "\n";
}

