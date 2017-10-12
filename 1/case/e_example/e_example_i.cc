#include <iostream>
#include <iomanip>
#include <limits>

#include "klee.h"
#include "klee-expression.h"

using namespace std;

int evaluate(int y) {
    int z=2;
    int i=2;
    while (i <= 20) {
        y=y/i;
        z=z+y;
        i+=1;
    }
    return z;
}

int main() {

    int x = 1.0;
    klee_make_symbolic(&x, sizeof(x), "x");
    int res = evaluate(x);
    klee_output("res", res);
    cout << setprecision(numeric_limits<double>::digits10) << res << endl;

}

