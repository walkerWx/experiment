#ifndef SELF_MATH_H
#define SELF_MATH_H

#include <cmath>

/**
input (a, b) represents a vector
get the angle between vector (a, b) and vector (1, 0)
the return value is in [-pi/2, 3*pi/2)
**/
inline double get_arc(double a, double b)
{
    const double pi = 3.14159265358979323846;
    if(a == 0)
    {
        if(b == 0) return 0;
        else return b < 0 ? -pi/2 : pi/2;
    }
    else
    {
        if(a > 0)
        {
            return atan(b/a);
        }
        else
        {
            if(b > 0) return atan(b/a) + pi;
            else return atan(b/a) - pi;
        }
    }
//    return (a == 0 ? (b == 0 ? 0 : (b < 0 ? -pi/2 : pi/2)) : (a > 0 ? atan(b/a) : (atan(b/a) + pi)));
}

//#include "iRRAM/lib.h"
//
//namespace iRRAM
//{
//    inline REAL get_arc(REAL a, REAL b)
//    {
//    //    if(a == 0)
//    //    {
//    //        if(b == 0) return 0;
//    //        else return b < 0 ? -pi/2 : pi/2;
//    //    }
//    //    else
//    //        return a > 0 ? atan(b/a) : (atan(b/a) + pi);
//        return (a == 0 ? (b == 0 ? REAL(0) : (b < 0 ? -pi()/2 : pi()/2)) : (a > 0 ? atan(b/a) : (atan(b/a) + pi())));
//    }
//}

#endif
