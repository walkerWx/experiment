#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from subprocess import call
from decimal import *

import json
import itertools

getcontext().prec = 20

# 待分析输入区间，每个输入范围 [START, END]
FLOATSTART = 1
FLOATEND = 2 

INTSTART = 10000
INTEND = 10100

# 区间拆分粒度，即划分小区间的大小 10^(-PREC)
PREC = 1

# 浮点精度与高精度程序的容许的相对误差，容许误差范围内认为是稳定的
TOLERANCE = 1e-16


# 不同实现对应的不同类型的名称以及需要引入的头文件等
FLOAT = {}
REAL = {}

FLOAT['decimal'] = 'double'
FLOAT['integer'] = 'int'
FLOAT['cin'] = 'cin'
FLOAT['cout'] = 'cout'
FLOAT['header'] = '''
#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
using namespace std;
'''

REAL['decimal'] = 'REAL'
REAL['integer'] = 'INTEGER'
REAL['cin'] = 'cin'
REAL['cout'] = 'cout'
REAL['header'] = '''
#include "iRRAM.h"
using namespace iRRAM;
'''

FLOATCPP = 'float.cpp'
REALCPP = 'real.cpp'

LOGFILE = open('LOG', 'w')


# 以step为步长对输入区间[start, end]进行划分，并将结果输出 
def divideInputSpace(varNum, varType):

    li = range(INTSTART, INTEND)

    ld = []
    step = 10**(-PREC) 
    i = 0
    while (FLOATSTART+i*step < FLOATEND):
        ld.append([round(FLOATSTART+i*step, PREC), round(FLOATSTART+(i+1)*step, PREC)])
        i = i + 1

    l = []

    for t in varType:
        if t == 'integer':
            l.append(li) 
        elif t == 'decimal':
            l.append(ld)

    return [list(x) for x in itertools.product(*l)]

# 计算每个变量的范围表示的N维空间的所有顶点，例如 x = [1, 2], y = [2, 4] 对应二维空间中的4个顶点 (1, 2) (1, 4) (2, 2) (2, 4)
def interval2Points(interval):

    for i in range(len(interval)):
        if isinstance(interval[i], int):
            interval[i] = [interval[i]]
        
    return [list(x) for x in itertools.product(*interval)]

# 对拆分后的区间进行合并  
def mergeInterval(intervals):
    # TODO
    return intervals

# 将变量的区间转化为能直接填写到程序中的约束的字符串 
def interval2Constrain(variables, variablesType, interval):
    constrain = []
    for i in range(len(interval)):
        if variablesType[i] == 'decimal':
            constrain.append((('%.'+str(PREC)+'f') % interval[i][0]) + '<=' + variables[i] + '&&' + variables[i] + '<=' + (('%.'+str(PREC)+'f') % interval[i][1]))
        elif variablesType[i] == 'integer':
            constrain.append(variables[i]+'=='+str(interval[i][0]))
    constrain = '(' + '&&'.join(constrain) + ')'
    return constrain

def intervals2Constrain(variables, variablesType, intervals):
    constrain = [interval2Constrain(variables, variablesType, interval) for interval in intervals]
    constrain = '||'.join(constrain)
    return constrain

# 生成循环cpp代码
def generateLoop(loop, type):

    if (type == 'float'):
        implement = FLOAT
    elif (type == 'real'):
        implement = REAL

    # 临时变量定义与初始化
    cppcode = '{\n'
    for i in range(len(loop['variables'])):
        cppcode += implement[loop['variablesType'][i]] + ' ' + loop['variables'][i] + ';\n' 
    for i in loop['initialize']:
        cppcode += i[0] + ' = ' + i[1] + ';\n'
    
    # 循环体
    cppcode += 'while(true) {\n'
    for lb in loop['loopBody']:

        cppcode += '\tif(' + lb['constrain'] + ') {\n'

        for path in lb['path']:
            cppcode += '\t\t' + path[0] + ' = ' + path[1] + ';\n'

        if (lb['break'] == 'true'):
            cppcode += '\t\tbreak;\n'

        cppcode += '\t}\n'
    cppcode += '}\n'
    cppcode += '}\n'

    return cppcode

# generate runable cpp file according to path, constrain and type
def generateCpp(data, path, constrain, type = 'all'):
    
    if (type == 'all'):
        generateCpp(data, path, constrain, 'float')
        generateCpp(data, path, constrain, 'real')
        return
        
    # according to different implement type, we should include different header files and use different things

    precisionSetting = ''
    mainFunc = ''

    if (type == 'float'):

        implement = FLOAT

        mainFunc += 'int main(){\n'

        precisionSetting = implement['cout'] + ' << scientific << setprecision(numeric_limits<double>::digits10);\n'

    elif (type == 'real'):

        implement = REAL
        
        mainFunc += 'void compute(){\n'

        precisionSetting = implement['cout'] + ' << setRwidth(45);\n'


    mainFunc += '\t' + precisionSetting

    for i in range(len(data['variables'])):
        mainFunc += '\t' + implement[data['variablesType'][i]] + ' ' + data['variables'][i]+ ';\n'
    mainFunc += '\t' + implement['cin'] + ' >> ' + ' >> '.join(data['variables']) + ';\n'

    statements = path.split(';')
    for s in statements:
        # loop statement
        if (s[0] == '{' and s[-1] == '}'):
            mainFunc += generateLoop(data['loops'][s[1:-1]], type)  
        else:
            mainFunc += s + ';\n'
        mainFunc += '\n'

    mainFunc += '\t' + implement['cout'] + ' << ' + data['return']  + ' << "\\n";\n'
    mainFunc += '}\n'

    outputFile = {}
    outputFile['float'] = FLOATCPP
    outputFile['real'] = REALCPP 
    f = open(outputFile[type], 'w')
    print (implement['header'], file=f)
    print (mainFunc, file=f)


# 稳定性分析主逻辑
def stableAnalysis(data, path, constrain):

    variables = data['variables']
    print ('VARIABLES:\t', variables, file=LOGFILE)
    print ('PATH:\t', path, file=LOGFILE)
    print ('CONSTRAIN:\t', constrain, file=LOGFILE)
    

    intervals = divideInputSpace(len(variables), data['variablesType'])
    points = [interval2Points(interval) for interval in intervals]

    generateCpp(data, path, constrain)
    #call(['make'], shell=True)

    stableInterval = []
    unstableInterval = []

    for i in range(len(intervals)):

        stable = True # interval stable
        pstable = True # point stable

        print ('', file=LOGFILE)
        print ('----------------------------------------------', file=LOGFILE)
        print ('INTERVAL:\t', intervals[i], file=LOGFILE)

        # 对待分析区间中所有点，计算其相对误差   
        for point in points[i]:

            pstable = True
            
            for i in range(len(point)):
                if isinstance(point[i], int):
                    point[i] = str(point[i])
                else:
                    point[i] = ('%.'+str(PREC)+'f') % point[i] 

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
                pstable = False
                stable = False
            
            print ('', file=LOGFILE)
            print ('POINT:\t', point, file=LOGFILE) 
            print ('FLOAT RESUTL:\t', '%.20E' % floatRes, file=LOGFILE)
            print ('REAL RESUTL:\t', '%.20E' % realRes, file=LOGFILE)
            print ('RELATVIE ERROR:\t','%.20E' % relativeError, file=LOGFILE )
            print ('STABLE:\t', str(stable), file=LOGFILE )

            '''
            print ('')
            print ('POINT:\t', point) 
            print ('FLOAT RESUTL:\t', '%.20E' % floatRes)
            print ('REAL RESUTL:\t', '%.20E' % realRes)
            print ('RELATVIE ERROR:\t','%.20E' % relativeError)
            print ('STABLE:\t', str(stable))
            '''
            

        if (stable):
            stableInterval.append(intervals[i])
        else:
            unstableInterval.append(intervals[i])

    print (' ', file=LOGFILE)
    print ('STABLE INTERVAL:\t', len(stableInterval), file=LOGFILE)
    print ('UNSTABLE INTERVAL:\t', len(unstableInterval), file=LOGFILE)

    #call(['make clean'], shell=True)

    stableInterval = mergeInterval(stableInterval)
    unstableInterval = mergeInterval(unstableInterval)

    stableInterval = intervals2Constrain(variables, data['variablesType'], stableInterval)
    unstableInterval = intervals2Constrain(variables, data['variablesType'], unstableInterval)

    return {'stable': stableInterval, 'unstable': unstableInterval} 

'''
variables = ['x']
path = 'sqrt(x+1)-sqrt(x)'
stablepath = '1.0/(sqrt(x+1)+sqrt(x))'
constrain = '0<x&&x<1&&0<y&&y<1'
res = stableAnalysis(variables, stablepath, constrain)
print (res)
#res = stableAnalysis(variables, path, constrain)

variables = [ "ar", "ai", "br", "bi"]
path = "(ar/sqrt(ar*ar+ai*ai)+br/sqrt(br*br+bi*bi))/sqrt(2+2*(ar*br+ai*bi)/sqrt((ar*ar+ai*ai)*(br*br+bi*bi)))"
constrain = "true"
res = stableAnalysis(variables, path, constrain)
'''

with open('../case/harmonic/harmonic.pth') as f:
    data = json.load(f)

stableAnalysis(data, data['paths'][0], '')

