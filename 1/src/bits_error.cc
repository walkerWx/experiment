// 计算两个二进制表示的浮点数的比特误差

#include "points.h"
#include <iostream>
#include <string>

using namespace std;

int main() {
    /*
    string d1, d2;
    cin >> d1 >> d2;
    cout << herbie_error(d1, d2) << endl;
    */
    string s;
    int i;
    cin >> i;
    s = int2binary(i);
    cout << s << endl;
    cout << binary2int(s) << endl;
}

