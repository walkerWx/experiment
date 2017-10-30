#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function

import json

FLOATCPP = 'float.cpp'
REALCPP = 'real.cpp'

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

        header += '#include "iRRAM.h"\n'
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
    mainFunc += '\t' + declType + ','.join(variables) + ';\n'
    mainFunc += '\t' + inputStream + ' >> ' + ' >> '.join(variables) + ';\n'
    mainFunc += '\t' + declType + ' res;\n'
    mainFunc += '\t' + 'res = ' + path + ';\n'
    mainFunc += '\t' + outputStream + ' << res;\n'
    mainFunc += '}\n'

    outputFile = {}
    outputFile['float'] = FLOATCPP
    outputFile['real'] = REALCPP 
    f = open(outputFile[type], 'w')
    print (header, file=f)
    print (mainFunc, file=f)

# 稳定性分析主逻辑
def stableAnalysis(variables, path, constrain):
    
    start = 0
    end = 1
    prec = 3 # step = 1e-2 
     
    '''
    intervals = divideInputSpace(len(varNum), start, end, prec)
    points = [interval2Points(interval) for interval in intervals]

    for i in range(len(intervals)):
        print (intervals[i])
        print (points[i])
    '''

    generateCpp(variables, path, constrain)
     
    

variables = ['x', 'y']
path = 'sin(x)*cos(y)'
constrain = '0<x&&x<1&&0<y&&y<1'
stableAnalysis(variables, path, constrain)

