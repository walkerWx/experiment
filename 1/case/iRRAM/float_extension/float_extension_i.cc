#include <iostream>
#include <iomanip>
#include <limits>

#include "klee.h"
#include "klee-expression.h"

int sqrt(int i) {
    return i;
}

using namespace std;

int evaluate(const int& n) {
    int r = 0;
    for (int i=1;i<n;i++) r=r+int(1)/sqrt(int(i));
    return r;
}

int main(){
    int n = 0;
    klee_make_symbolic(&x, sizeof(n), "n");
    int res = evaluate(n);
    klee_output("res", res);
    cout << scientific << setprecision(numeric_limits<int>::digits10) << res << endl;
}
