#include <cmath>
#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

double evaluate(const int& n) {
    double r = 0;
    for (int i=1;i<n;i++) r=r+double(1)/sqrt(double(i));
    return r;
}

int main(){
    double x = 0;
    double res = evaluate(x);
    cout << scientific << setprecision(numeric_limits<double>::digits10) << res << endl;
}
