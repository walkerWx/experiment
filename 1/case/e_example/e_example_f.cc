#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

double e(double y) {
    double z=2;
    int i=2;
    while (i <= 20) {
        y=y/i;
        z=z+y;
        i+=1;
    }
    return z;
}

int main() {

    double y = 1.0;
    double res = e(y);
    cout << setprecision(numeric_limits<double>::digits10) << res << endl;

}

