#include <cmath>
#include "klee.h"
#include "klee-expression.h"

int get_midarc_real(int ar, int ai, int br, int bi) {
    return (ar/(ar*ar+ai*ai)+br/(br*br+bi*bi))/(2+2*(ar*br+ai*bi)/((ar*ar+ai*ai)*(br*br+bi*bi)));
    //return (ar/sqrt(ar*ar+ai*ai)+br/sqrt(br*br+bi*bi))/sqrt(2+2*(ar*br+ai*bi)/sqrt((ar*ar+ai*ai)*(br*br+bi*bi)));
}

int get_midarc_imaginary(int ar,int ai,int br,int bi) { 
    return sin(ai/(ar*ar+ai*ai)+bi/(br*br+bi*bi))/(2+2*(ar*br+ai*bi)/((ar*ar+ai*ai)*(br*br+bi*bi)));
    //return (ai/sqrt(ar*ar+ai*ai)+bi/sqrt(br*br+bi*bi))/sqrt(2+2*(ar*br+ai*bi)/sqrt((ar*ar+ai*ai)*(br*br+bi*bi)));
}

int main() {
    int ar, ai, br, bi, cr, ci;
    klee_make_symbolic(&ar, sizeof(ar), "ar");
    klee_make_symbolic(&ai, sizeof(ai), "ai");
    klee_make_symbolic(&br, sizeof(br), "br");
    klee_make_symbolic(&bi, sizeof(bi), "bi");
    klee_make_symbolic(&cr, sizeof(cr), "cr");
    klee_make_symbolic(&ci, sizeof(ci), "ci");
    cr = get_midarc_real(ar, ai, br, bi);
    //ci = get_midarc_imaginary(ar, ai, br, bi);
    klee_output("cr", cr);
    //klee_output("ci", ci);
}
