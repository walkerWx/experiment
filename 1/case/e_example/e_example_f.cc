#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

double e(int n) {
    double z=2;
    double y = 1.0;
    for (int i = 2; i < n; ++i) {
        y=y/i;
        z=z+y;
    }
    return z;
}

int main() {

    int n;
    cin >> n;
    double res = e(n);
    cout << setprecision(numeric_limits<double>::digits10) << res << endl;

}

