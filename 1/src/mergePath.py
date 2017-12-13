
from __future__ import print_function

from transform import convert_expr

import json

# TODO
# different type implemention && loop implemention
# merge paths in pth file to a C program
def mergePath(pthFile):

    with open(pthFile) as f:
        data = json.load(f)

    variables = data['variables']
    types = data['types']
    paths = data['paths']
    constrains = data['constrains']

    header = '''
#include "iRRAM.h"
#include <iostream>
#include <iomanip> 
#include <cmath>
#include <limits>
using namespace std;
using namespace iRRAM;
             '''
            
    declType = ''
    returnType = ''
    if ('real' in data['types']):
        declType = 'REAL'
        returnType = 'REAL'
    else:
        declType = 'double'
        returnType = 'double'

    # function declare
    funcBody = returnType + ' ' + data['functionName'] + '(' + ', '.join([declType+' '+v for v in data['variables']]) +  ') { \n'

    # double variables declare and initialize
    variables_double = [v + '_double' for v in data['variables']]
    funcBody += '\tdouble ' + ', '.join(variables_double) + ';\n'
    for i in range(len(variables)):
        if (declType == 'double'):
            funcBody += '\t' + variables_double[i] + ' = ' + variables[i] + ';\n'
        elif (declType == 'REAL'):
            funcBody += '\t' + variables_double[i] + ' = ' + variables[i] + '->as_double();\n'
    funcBody += '\n'
         
    # real variables declare and initialize
    variables_real = [v + '_real' for v in data['variables']]
    funcBody += '\tREAL ' + ', '.join(variables_real) + ';\n'
    for i in range(len(variables)):
        funcBody += '\t' + variables_real[i] + ' = ' + variables[i] + ';\n'
    funcBody += '\n'

    # return value declare
    funcBody += '\t' + 'double res_double;\n'
    funcBody += '\t' + 'REAL res_real;\n'
    funcBody += '\n'
        
    # paths implemention
    for i in range(len(data['paths'])):


        funcBody += '\tif(' + constrains[i] + ') {\n' 

        # float implemention
        if (types[i] == 'float'):
            funcBody += '\t\tres_double  = ' + convert_expr(paths[i], variables, variables_double) + ';\n'

            # return statement
            if (returnType == 'double'):
                funcBody += '\t\treturn res_double;\n'
            elif (returnType == 'REAL'):
                funcBody += '\t\treturn REAL(res_double);\n'

        # real implemention
        elif (types[i] == 'real'):
            funcBody += '\t\tres_real = ' + convert_expr(paths[i], variables, variables_real)  + ';\n'

            # return statement
            if (returnType == 'double'):
                funcBody += '\t\treturn res_real->as_double();\n' 
            elif (returnType == 'REAL'):
                funcBody += '\t\treturn res_real;\n' 

        funcBody += '\t}\n\n'

    funcBody += '\treturn 0;\n'
    funcBody += '}\n'

    # output to file
    outputDirectory = ''
    if (pthFile.rfind('/') != -1):
        outputDirectory = pthFile[:pthFile.rfind('/')+1]

    outputFile = open(outputDirectory+data['programName']+'_o.cc', 'w')

    print (header, file=outputFile)
    print (funcBody, file=outputFile)


