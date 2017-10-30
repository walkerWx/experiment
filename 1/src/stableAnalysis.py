#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from subprocess import call
from decimal import *

import json

FLOATCPP = 'float.cpp'
REALCPP = 'real.cpp'

LOGFILE = open('LOG', 'w')

getcontext().prec = 20

# 以step为步长对输入区间[start, end]进行划分，并将结果输出 
def divideInputSpace(varNum, start, end, prec):

    d1 = []
    dn = []

    i = 0
    step = 10**(-prec) 
    while (start+i*step < end):
        d1.append([[round(start+i*step, prec), round(start+(i+1)*step, prec)]])
        i = i + 1
        
    dn = list(d1)
    for _ in range(varNum-1):
        dt = []
        for i in dn:
            for j in d1:
                dt.append(list(i) + j)
        dn = list(dt)


    '''
    output = {}
    output['varNum'] = varNum 
    output['intervals'] = dn

    with open(outputFile, 'w') as f:
        json.dump(output, f, indent=4)
    '''

    return dn


# 计算每个变量的范围表示的N维空间的所有顶点，例如 x = [1, 2], y = [2, 4] 对应二维空间中的4个顶点 (1, 2) (1, 4) (2, 2) (2, 4)
def interval2Points(interval):

    varNum = len(interval)
    points = [[interval[0][0]], [interval[0][1]]]
    i = 1
    while (i < len(interval)):
        t = []
        for point in points:
            t.append(point + [interval[i][0]])
            t.append(point + [interval[i][1]])
        points = list(t)
        i += 1
        
    return points

# generate runable cpp file according to path, constrain and type
def generateCpp(variables, path, constrain, type = 'all'):
    
    if (type == 'all'):
        generateCpp(variables, path, constrain, 'float')
        generateCpp(variables, path, constrain, 'real')
        return
        
    # according to different implement type, we should include different header files and use different things

    header = ''
    declType = ''
    inputStream = ''
    outputStream = ''
    precisionSetting = ''
    mainFunc = ''

    if (type == 'float'):

        header += '#include <iostream>\n'
        header += '#include <iomanip>\n'
        header += '#include <cmath>\n'
        header += '#include <limits>\n'
        header += 'using namespace std;\n'

        mainFunc += 'int main(){\n'

        declType = 'double'
        inputStream = 'cin'
        outputStream = 'cout'

        precisionSetting = outputStream + ' << scientific << setprecision(numeric_limits<double>::digits10);\n'

    elif (type == 'real'):

        header += '#include "iRRAM.h"\n'
        header += 'using namespace iRRAM;\n'
        
        mainFunc += 'void compute(){\n'

        declType = 'REAL'
        inputStream = 'cin'
        outputStream = 'cout'

        precisionSetting = outputStream + ' << setRwidth(45);\n'

    elif (type == 'interval'):
        # TODO
        header += ''
        declType = ''

    mainFunc += '\t' + precisionSetting
    mainFunc += '\t' + declType + ' ' +  ','.join(variables) + ';\n'
    mainFunc += '\t' + inputStream + ' >> ' + ' >> '.join(variables) + ';\n'
    mainFunc += '\t' + declType + ' res;\n'
    mainFunc += '\t' + 'res = ' + path + ';\n'
    mainFunc += '\t' + outputStream + ' << res << "\\n";\n'
    mainFunc += '}\n'

    outputFile = {}
    outputFile['float'] = FLOATCPP
    outputFile['real'] = REALCPP 
    f = open(outputFile[type], 'w')
    print (header, file=f)
    print (mainFunc, file=f)


# 稳定性分析主逻辑
def stableAnalysis(variables, path, constrain):

    print ('VARIABLES:\t', variables, file=LOGFILE)
    print ('PATH:\t', path, file=LOGFILE)
    print ('CONSTRAIN:\t', constrain, file=LOGFILE)
    

    # 待分析输入区间，每个输入都范围 [START, END]
    START = 1e10 
    END = 1e10+1 

    # 区间拆分粒度，即划分小区间的大小 10^(-PREC)
    PREC = 3 

    # 浮点精度与高精度程序的容许的相对误差，容许误差范围内认为是稳定的
    TOLERANCE = 1e-16
    
    intervals = divideInputSpace(len(variables), START, END, PREC)
    points = [interval2Points(interval) for interval in intervals]


    generateCpp(variables, path, constrain)
    call(['make'], shell=True)

    stableInterval = []
    unstableInterval = []

    for i in range(len(intervals)):

        stable = True

        print ('', file=LOGFILE)
        print ('----------------------------------------------', file=LOGFILE)
        print ('INTERVAL:\t', intervals[i], file=LOGFILE)

        # 对待分析区间中所有点，计算其相对误差   
        for point in points[i]:
            
            point = [('%.'+str(PREC)+'f') % x for x in point]

            print (' '.join(point), file = open('input', 'w'))
            
            call(['./float < input > float_output'], shell=True)
            call(['./real < input > real_output'], shell=True)

            floatRes = Decimal([line.rstrip('\n') for line in open('float_output')][0])
            realRes = Decimal([line.rstrip('\n') for line in open('real_output')][0])

            if (realRes == Decimal(0)):
                relativeError = abs((floatRes-realRes)/Decimal(1))
            else:
                relativeError = abs((floatRes-realRes)/realRes)

            if (relativeError >= TOLERANCE):
                stable = False
            
            print ('', file=LOGFILE)
            print ('POINT:\t', point, file=LOGFILE) 
            print ('FLOAT RESUTL:\t', '%.20E' % floatRes, file=LOGFILE)
            print ('REAL RESUTL:\t', '%.20E' % realRes, file=LOGFILE)
            print ('RELATVIE ERROR:\t','%.20E' % relativeError, file=LOGFILE )
            print ('STABLE:\t', str(stable), file=LOGFILE )
            
            

        if (stable):
            stableInterval.append(intervals[i])
        else:
            unstableInterval.append(intervals[i])

    print (' ', file=LOGFILE)
    print ('STABLE INTERVAL:\t', len(stableInterval), file=LOGFILE)
    print ('UNSTABLE INTERVAL:\t', len(unstableInterval), file=LOGFILE)

    return {'stable': stableInterval, 'unstable': unstableInterval} 

variables = ['x']
path = 'sqrt(x+1)-sqrt(x)'
stablepath = '1.0/(sqrt(x+1)+sqrt(x))'
constrain = '0<x&&x<1&&0<y&&y<1'
res = stableAnalysis(variables, stablepath, constrain)
#res = stableAnalysis(variables, path, constrain)

