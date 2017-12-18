#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

double euler_constant = double(0.57721566490);

double gamma_approx_2(const double& x) {
    return (8-4*euler_constant+3*x-2*euler_constant*x)/(8+4*x);
}

int main() {

  cout << scientific << setprecision(numeric_limits<double>::digits10);

  double x;
  cin >> x;

  double res = gamma_approx_2((2-euler_constant+x)/(euler_constant-1-x)-1);

  cout << res <<"\n";

}


