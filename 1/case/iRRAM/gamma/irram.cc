#include <string>
#include <iostream>
#include <cfenv>
#include <sys/time.h>
#include "iRRAM.h"
#include "../../../src/points.h"
#include "../../../src/self_math.h"
#include "../../../src/gamma.h"

#undef euler_gamma
#define euler_gamma REAL("0.57721566490153286060651209008240243104215933593992359880576723488486772677766467093694706329174674951463144724980708248096050401448654283622417399764492353625350033374293733773767394279259525824709491600873520394816567085323315177661152862119950150798479374508570574002992135478614669402960432542151905877553526733139925401296742051375413954911168510280798423487758720503843109399736137255306088933126760017247953783675927135157722610273492913940798430103417771778088154957066107501016191663340152279")


iRRAM::REAL evaluate(iRRAM::REAL x) {
    iRRAM::REAL r = 0;
    r = gamma((iRRAM::REAL(2)-iRRAM::REAL(euler_gamma)+x)/(iRRAM::REAL(euler_gamma)-iRRAM::REAL(1)-x)-1);
    return r;
}
void compute() {
	std::fesetround(FE_DOWNWARD);
	std::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);
	iRRAM::cout << iRRAM::setRwidth(30);
	std::string x_str;
	iRRAM::cin >> x_str;
	double x_double = binary2double(x_str);
	iRRAM::REAL x_irram(x_double);
    struct timeval tstart, tfinish;
    if(gettimeofday(&tstart,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
	iRRAM::REAL r_irram = evaluate(x_irram);
    if(gettimeofday(&tfinish,NULL)!=0){
        printf("Get time error!\n");
        return;
    }
    double usec=(tfinish.tv_sec-tstart.tv_sec)*1000000+tfinish.tv_usec-tstart.tv_usec;
    iRRAM::cout << usec << "\n";
	double r_double = r_irram.as_double();
	iRRAM::cout << double2binary(r_double) << "\n";
}