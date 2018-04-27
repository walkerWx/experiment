#include <cmath>
#include <iostream>
#include "klee.h"
#include "klee-expression.h"

using namespace std;

struct Complex {
    double realPart;
    double imaginaryPart;
    Complex() : realPart(0), imaginaryPart(0) {}
    Complex(double r, double i) : realPart(r), imaginaryPart(i) {}
};

double modulo(const Complex& c) {
    return sqrt(c.realPart*c.realPart + c.imaginaryPart*c.imaginaryPart);
}

Complex operator / (const Complex& c, double d) {
    Complex res(c);
    double m = modulo(c);
    res.realPart /= m;
    res.imaginaryPart /= m;
    return res;
}

void unit(Complex& c) {
    double m = modulo(c);
    c = c/m;
}

Complex midPoint(const Complex& a, const Complex& b) {
    Complex mid;
    mid.realPart = a.realPart+b.realPart; 
    mid.imaginaryPart = a.imaginaryPart+b.imaginaryPart;
    mid = mid/modulo(mid);
    return mid;
}

int main() {
    Complex a(3, 4);
    Complex b(5, 6);
    klee_make_symbolic(&a.realPart, sizeof(a.realPart), "ar");
    klee_make_symbolic(&a.imaginaryPart, sizeof(a.imaginaryPart), "ai");
    klee_make_symbolic(&b.realPart, sizeof(b.realPart), "br");
    klee_make_symbolic(&b.imaginaryPart, sizeof(b.imaginaryPart), "bi");
    modulo(a);
    modulo(b);
    Complex mid = midPoint(a, b);
    klee_output("mr", mid.realPart);
    klee_output("mi", mid.imaginaryPart);
}
