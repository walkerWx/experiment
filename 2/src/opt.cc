#include <cmath>

// Herbie Case: 2log
double opt_2log(double N) {
    return log(N+1) - log(N);
}

// Herbie Case: cos2
double opt_cos2(double x) {
    return (1-cos(x))/(x*x);
}

// Herbie case: exp2
double opt_exp2(double x) {
    return (exp(x) - 2 ) + exp(-x);
}

// Herbie case: expax
double opt_expax(double a, double x) {
    return exp(a*x) - 1;
}

// Herbie case: expm1
double opt_expm1(double x) {
    return exp(x) - 1;
}

// Herbie case: expq2
double opt_expq2(double x) {
    if((true)&&((0.0000100<=x&&x<=0.0000201)))
		return 1/x + 1.0/2 + x/12 - (pow(x, 3))/720 + (pow(x, 5))/30240 - (pow(x, 7))/1209600 ;
    return exp(x)/(exp(x)-1);
}

// Herbie case: invcot
double opt_invcot(double x) {
    return 1/x-1/tan(x);
}

// Herbie case: quad2m
double opt_quad2m(double a, double b, double c) {
    return ((-b/2)-sqrt(b*b/4-a*c))/a;
}

// Herbie case: quadp
double opt_quadp(double a, double b, double c) {
    double d = -b + sqrt(b*b-4*a*c);
    return d/(2*a);
}

// Herbie case: quadm
double opt_quadm(double a, double b, double c) {
    double d = -b - sqrt(b*b-4*a*c);
    return d/(2*a);
}

// Herbie case: sintan
double opt_sintan(double x) {
    double a = x - sin(x);
    double b = x - tan(x);
    return a/b;
}

// Herbie case: sqrtexp
double opt_sqrtexp(double x) {
    return sqrt(exp(x)+1);
}

// Herbie case: quad2p
double opt_quad2p(double a, double b, double c) {
    return ((-b/2)+sqrt(b*b/4-a*c))/a;
}

// Herbie case: 2nthrt 
double opt_2nthrt(double x, double n) {
    double a = pow(x+1, 1/n);
    double b = pow(x, 1/n);
    return a - b;
}

// Herbie case: 2frac
double opt_2frac(double x) {
    double a = 1/(x+1);
    double b = 1/x;
    return a - b;
}

// Herbie case: 2cos
double opt_2cos(double x, double eps) {
    return cos(x+eps) - cos(x);
}

// Herbie case: 2cbrt
double opt_2cbrt(double x) {
    double n = double(1)/double(3);
    double a = pow(x+1, n);
    double b = pow(x, n);
    return a - b;
}

// Herbie case: tanhf
double opt_tanhf(double x) {
    return (1-cos(x))/sin(x);
}

// Herbie case: qlog
double opt_qlog(double x) {
    double a = log(1-x);
    double b = log(1+x);
    return a/b;
}

// Herbie case: logq
double opt_logq(double eps) {
    double a = 1 - eps;
    double b = 1 + eps;
    return log(a/b);
    
}

// Herbie case: logs
double opt_logs(double n) {
    return (n+1)*log(n+1) - n*log(n) - 1;
}

// Herbie case: expq3
double opt_expq3(double a, double b, double eps) {
    double abe = eps*(exp((a+b)*eps)-1);
    double ae = exp(a*eps) - 1;
    double be = exp(b*eps) - 1;
    return abe/(ae*be);
}

// Herbie case: 3frac
double opt_3frac(double x) {
    return 1/(x+1) - 2/x + 1/(x-1);
}

// Herbie case: 2tan
double opt_2tan(double x, double eps) {
    return tan(x+eps) - tan(x);
}

// Herbie case: 2sqrt
double opt_2sqrt(double x) {
    return sqrt(x+1) - sqrt(x);
}

// Herbie case: 2sin
double opt_2sin(double x, double eps) {
    return sin(x+eps) - sin(x);
}

// Herbie case: 2isqrt
double opt_2isqrt(double x) {
    return 1/sqrt(x) - 1/sqrt(x+1);
}

// Herbie case: 2atan
double opt_2atan(double N) {
    return atan(N+1) - atan(N);
}


