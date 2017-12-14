#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

/* Compute iteration by J.M.Muller */

double evaluate(int count){

  double a = double(11)/2.0, b=double(61)/11.0, c;

  for (long i=0;i<count;i++ ) {
    c=111-(1130-3000/a)/b;
    a=b; b=c;   
  }
  return a;
}

int main() {
    int count;
    cin >> count;
    double res = evaluate(count);
    cout << scientific << setprecision(numeric_limits<double>::digits10) << res << endl;
}

