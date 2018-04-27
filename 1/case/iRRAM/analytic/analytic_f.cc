#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>

using namespace std;

double evaluate(double x, int degree = 15) {
    double res = 0;
    double powx = 1;
    for (int i = 0; i < degree; ++i) {
        powx = powx*x;  
        res = res + powx;
    }
    return res;
}

int main() {
    double x = 100.5;
    double res = evaluate(x);
    cout << scientific << setprecision(numeric_limits<double>::digits10) << res << endl;
}
