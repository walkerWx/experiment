
from __future__ import print_function

import json

# merge paths in pth file to a C program
def mergePath(pthFile):

    with open(pthFile) as f:
        data = json.load(f)

        outputDirectory = ''
        if (pthFile.rfind('/') != -1):
            outputDirectory = pthFile[:pthFile.rfind('/')+1]

        outputFile = open(outputDirectory+data['programName']+'_o.cc', 'w')
    
        # function declaration
        print ('double ' + data['functionName'], end='', file=outputFile)        

        # construct argument list
        for i in range(len(data['variables'])):
            data['variables'][i] = 'double '+data['variables'][i]
        argumentList = '('+' ,'.join(data['variables'])+')'
        print (argumentList, file=outputFile)

        # function body
        print ('{', file=outputFile)
        
        # return value declaration
        print ('\tdouble res = 0;', file=outputFile)
        for i in range(len(data['constrains'])):
            print ('\tif('+data['constrains'][i]+')', file=outputFile)
            print ('\t{', file=outputFile)
            print ('\t\t res = ' + data['paths'][i] + ';', file=outputFile)
            print ('\t}', file=outputFile)

        # return statement
        print ('\treturn res;', file=outputFile)

        print ('}', file=outputFile)

# generate runable cpp file according to path, constrain and type
def generateCpp(variabels, constrain, path, type):
    
    # according to different implement type, we should include different header files and use different things

    header = ''
    declType = ''
    inputStream = ''
    outputStream = ''
    precisionSetting = ''

    if (type == 'float'):

        header += '#include <iostream>\n'
        header += '#include <iomanip>\n'
        header += '#include <cmath>\n'
        header += '#include <limits>\n'
        header += 'using namespace std;\n'

        declType = 'double'
        inputStream = 'cin'
        outputStream = 'cout'

        precisionSetting = outputStream + ' << scientific << setprecision(numeric_limits<double>::digit10)\n'

    elif (type == 'real'):

        header += '"iRRAM.h"\n'
        header += 'using namespace iRRAM;\n'

        declType = 'REAL'
        inputStream = 'cin'
        outputStream = 'cout'

        precisionSetting = outputStream + ' << setRwidth(45)\n'

    elif (type == 'interval'):
        # TODO
        header += ''
        declType = ''

    mainFunc = ''
    mainFunc += 'int main(){\n'
    mainFunc += '\t' + precisionSetting
    mainFunc += '\t' + declType + ','.join(variabels) + ';\n'
    mainFunc += '\t' + inputStream + ' >> ' + ' >> '.join(variabels) + ';\n'
    mainFunc += '\t' + declType + ' res;\n'
    mainFunc += '\t' + 'res = ' + path + ';\n'
    mainFunc += '\t' + outputStream + ' << res;\n'
    mainFunc += '}\n'

    print (header)
    print (mainFunc)

# generate all types of runable cpp file
def generateCpp(variabels, constrain, path):
    generateEqualPath(variable, constrain, path, 'float')
    generateEqualPath(variable, constrain, path, 'real')

