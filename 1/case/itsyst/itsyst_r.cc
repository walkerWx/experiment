#include "iRRAM.h"

using namespace iRRAM;

using std::setw;

/* Compute iterated system x=3.75*x*(1-x) (Kulisch) */

REAL evaluate(REAL x, int count) {
    REAL c = 3.75;
    for (int i = 0; i < count; ++i) {
        x = c*x*(1-x);
    }
    return x;
}

void compute(){
    int count = 80;
    REAL x = 0.5;
    REAL res = evaluate(x, count);
    cout << setRwidth(24) << res << "\n";
}
