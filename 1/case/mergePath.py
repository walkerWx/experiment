# merge paths in pth file to a C program

import json

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
        for i in range(len(data['variableNames'])):
            data['variableNames'][i] = 'double '+data['variableNames'][i]
        argumentList = '('+' ,'.join(data['variableNames'])+')'
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


mergePath('./analytic/analytic.pth') 

