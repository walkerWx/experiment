/**
 * From "Introduction to Numerical Ordinary and Partial Differential Equation Using" Chapter 5.3, Page 103
 * For computing HarmonicNumber[x, 2], the limitation is 6/pi
 */

#include <iostream>
#include <iomanip>
#include <limits>
#include <cmath>

using namespace std;

double evaluate(int n) {
    double initval = 0;
    for (int i=1; i<n; ++i) {
        //initval += (1/((double)i*i));
        initval += (1/sqrt(i));
    }
    return initval;
}

int main() {
    int n=70712;
    cin >> n;
    double res = evaluate(n);
    cout << scientific << setprecision(numeric_limits<double>::digits10) << res << endl;
}


