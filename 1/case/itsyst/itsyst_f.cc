#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

/* Compute iterated system x=3.75*x*(1-x) (Kulisch) */

double evaluate(double x, int count) {
    double c = 3.75;
    for (int i = 0; i < count; ++i) {
        x = c*x*(1-x);
    }
    return x;
}

int main() {
    int count = 80;
    double x = 0.5;
    double res = evaluate(x, count);
    cout << scientific << setprecision(numeric_limits<double>::digits10);
    cout << res << endl;
}
