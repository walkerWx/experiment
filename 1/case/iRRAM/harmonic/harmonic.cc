/**
 * From "Introduction to Numerical Ordinary and Partial Differential Equation Using" Chapter 5.3, Page 103
 * For computing HarmonicNumber[x, 2], the limitation is 6/pi
 */

#include "iRRAM.h"

using namespace iRRAM;

REAL evaluate(int n) {
    int i=1;
    iRRAM::REAL initval = 0;
    for(i=1;i<n;++i){
        initval += (REAL(1)/REAL(i*i));
        //initval += (REAL(1)/sqrt(i));
    }
    return initval;
}

