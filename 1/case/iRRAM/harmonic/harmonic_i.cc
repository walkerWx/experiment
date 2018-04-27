/**
 * From "longroduction to Numerical Ordinary and Partial Differential Equation Using" Chapter 5.3, Page 103
 * For computing HarmonicNumber[x, 2], the limitation is 6/pi
 */

#include <iostream>
#include <iomanip>
#include <limits>

#include "klee.h"
#include "klee-expression.h"

using namespace std;

long evaluate(long n, long x) {
    long i=1;
    long harresult=0;
    for (i=1; i<n; ++i) {
        harresult += (x/((long)i*i));
    }
    return harresult;
}

int main() {
    long n=70712; long x=0;
    klee_make_symbolic(&x, sizeof(x), "x");
    long res = evaluate(n, x);
    klee_output("res", res);
    cout << scientific << setprecision(numeric_limits<long>::digits10) << res << endl;
}


