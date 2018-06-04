#include "iRRAM.h"

iRRAM::REAL irram_invcot(iRRAM::REAL x) {
    iRRAM::REAL r = 1/x-1/iRRAM::tan(x);
    return r;
}
