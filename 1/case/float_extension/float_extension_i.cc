#include <iostream>
#include <iomanip>
#include <limits>

#include "klee.h"
#include "klee-expression.h"

int sqrt(int i) {
    return i;
}

using namespace std;

int evaluate(const int& x) {
    int r; 
    r=x;
    for (int i=1;i<100000;i++) r=r+int(1)/sqrt(int(i));
    return r;
}

int main(){
    int x = 0;
    klee_make_symbolic(&x, sizeof(x), "x");
    int res = evaluate(x);
    klee_output("res", res);
    cout << scientific << setprecision(numeric_limits<int>::digits10) << res << endl;
}
