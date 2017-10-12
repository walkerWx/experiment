#include <iostream>
#include <iomanip>
#include <limits>

#include "klee.h"
#include "klee-expression.h"

using namespace std;

/* Compute iterated system x=3.75*x*(1-x) (Kulisch) */

int evaluate(int x, int count) {
    int c = 3.75;
    for (int i = 0; i < count; ++i) {
        x = c*x*(1-x);
    }
    return x;
}

int main() {
    int count = 10;
    int x = 0.5;
    klee_make_symbolic(&x, sizeof(x), "x");
    int res = evaluate(x, count);
    klee_output("res", res);
    cout << scientific << setprecision(numeric_limits<int>::digits10);
    cout << res << endl;
}
