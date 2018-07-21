#ifndef SELF_MATH_H
#define SELF_MATH_H

#include <cmath>

inline double get_arc(double a, double b)
{
    const double pi = 3.14159265358979323846;
//    if(a == 0)
//    {
//        if(b == 0) return 0;
//        else return b < 0 ? -pi/2 : pi/2;
//    }
//    else
//        return a > 0 ? atan(b/a) : (atan(b/a) + pi);
    return (a == 0 ? (b == 0 ? 0 : (b < 0 ? -pi/2 : pi/2)) : (a > 0 ? atan(b/a) : (atan(b/a) + pi)));
}

#endif
