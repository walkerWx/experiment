#include "iRRAM.h"

using namespace iRRAM;

REAL evaluate(int n) {
    REAL z=2;
    REAL y = 1.0;
    for (int i = 2; i < n; ++i) {
        y=y/i;
        z=z+y;
    }
    return z;
}

int main() {
    int n;
    cin >> n;
    REAL res = evaluate(n);
    cout << setRwidth(45) << res << "\n";
}
