/**
 * From "Introduction to Numerical Ordinary and Partial Differential Equation Using" Chapter 5.3, Page 103
 * For computing HarmonicNumber[x, 2], the limitation is 6/pi
 */

#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

double evaluate(int n, double initval) {
    for (int i=1; i<n; ++i) {
        initval += (1/((double)i*i));
    }
    return initval;
}

int main() {
    int n=70712; double initval=0;
    double res = evaluate(n, initval);
    cout << scientific << setprecision(numeric_limits<double>::digits10) << res << endl;
}


