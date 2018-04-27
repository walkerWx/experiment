#include "iRRAM.h"

using namespace iRRAM;

/* Compute iteration by J.M.Muller */

REAL evaluate(int count){

  REAL a = REAL(11)/2.0, b=REAL(61)/11.0, c;

  for (long i=0;i<count;i++ ) {
    c=111-(1130-3000/a)/b;
    a=b; b=c;   
  }
  for (long i=0;i<count;i++ ) {
    c=3000/(1130-(111-b)*a);
    b=a; a=c;
  }
  return c;
}

void compute(){
    int count;
    cin >> count;
    REAL res = evaluate(count);
    cout << setRwidth(26) << res << "\n";
}
