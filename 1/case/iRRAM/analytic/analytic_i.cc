#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>

#include "klee.h"
#include "klee-expression.h"

using namespace std;

int evaluate(int x, int degree = 15) {
    int res = 0;
    int powx = 1;
    for (int i = 0; i < degree; ++i) {
        powx = powx*x;  
        res = res + powx;
    }
    return res;
}

int main() {
    int x = 0.5;
    klee_make_symbolic(&x, sizeof(x), "x");
    int res = evaluate(x);
    klee_output("res", res);
    cout << scientific << setprecision(numeric_limits<int>::digits10) << res << endl;
}
