#include "iRRAM.h"

iRRAM::REAL irram_cos2(iRRAM::REAL x) {
    iRRAM::REAL r = (1-iRRAM::cos(x))/(x*x);
    return r;
}
