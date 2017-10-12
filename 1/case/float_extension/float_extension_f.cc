#include <cmath>
#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

double evaluate(const double& x) {
    double r; 
    r=x;
    for (int i=1;i<100000;i++) r=r+double(1)/sqrt(double(i));
    return r;
}

int main(){
    double x = 0;
    double res = evaluate(x);
    cout << scientific << setprecision(numeric_limits<double>::digits10) << res << endl;
}
