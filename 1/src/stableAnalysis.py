#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from subprocess import call
from decimal import *
from path import *

import json
import itertools

getcontext().prec = 20

# 待分析输入区间，每个输入范围 [START, END]
FLOATSTART = 1
FLOATEND = 2 

INTSTART = 1
INTEND = 500

# 区间拆分粒度，即划分小区间的大小 10^(-PREC)
PREC = 1

# 浮点精度与高精度程序的容许的相对误差，容许误差范围内认为是稳定的
TOLERANCE = 1e-16

# 不同实现对应的不同类型的名称以及需要引入的头文件等
FLOAT = dict()
REAL = dict()

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
def divide_input_space(var_type):

    li = range(INTSTART, INTEND)

    ld = []
    step = 10**(-PREC) 
    i = 0
    while FLOATSTART+i*step < FLOATEND:
        ld.append([round(FLOATSTART+i*step, PREC), round(FLOATSTART+(i+1)*step, PREC)])
        i = i + 1

    lst = []

    for t in var_type:
        if t == 'integer':
            lst.append(li)
        elif t == 'decimal':
            lst.append(ld)

    return [list(x) for x in itertools.product(*lst)]


# 计算每个变量的范围表示的N维空间的所有顶点，例如 x = [1, 2], y = [2, 4] 对应二维空间中的4个顶点 (1, 2) (1, 4) (2, 2) (2, 4)
def interval2points(interval):

    for i in range(len(interval)):
        if isinstance(interval[i], int):
            interval[i] = [interval[i]]
        
    return [list(x) for x in itertools.product(*interval)]


# 对拆分后的区间进行合并  
def merge_interval(intervals):
    # TODO
    return intervals


# 将变量的区间转化为能直接填写到程序中的约束的字符串 
def interval2constrain(variables, variables_type, interval):
    constrain = []
    for i in range(len(interval)):
        if variables_type[i] == 'decimal':
            constrain.append((('%.'+str(PREC)+'f') % interval[i][0]) + '<=' + variables[i] + '&&' + variables[i] + '<=' + (('%.'+str(PREC)+'f') % interval[i][1]))
        elif variables_type[i] == 'integer':
            constrain.append(variables[i]+'=='+str(interval[i][0]))
    constrain = '(' + '&&'.join(constrain) + ')'
    return constrain


def intervals2constrain(variables, variables_type, intervals):
    constrain = [interval2constrain(variables, variables_type, interval) for interval in intervals]
    constrain = '||'.join(constrain)
    return constrain


# generate runable cpp file according to path, constrain and type
def generate_cpp(path_data, path, implement_type='all'):
    
    if implement_type == 'all':
        generate_cpp(path_data, path, 'float')
        generate_cpp(path_data, path, 'real')
        return
        
    # according to different implement type, we should include different header files and use different things

    precision_setting = ''
    main_func = ''

    if implement_type == 'float':

        implement = FLOAT

        main_func += 'int main(){\n'

        precision_setting = implement['cout'] + ' << scientific << setprecision(numeric_limits<double>::digits10);\n'

    elif implement_type == 'real':

        implement = REAL
        
        main_func += 'void compute(){\n'

        precision_setting = implement['cout'] + ' << setRwidth(45);\n'

    main_func += '\t' + precision_setting
    for var in path_data.get_variables():
        main_func += '\t' + implement[path_data.get_variable_type(var)] + ' ' + var + ';\n'

    # variables initialize
    for var in path_data.get_input_variables():
        main_func += '\t' + implement['cin'] + ' >> ' + var + ';\n'

    for m in path.get_path_list():
        main_func += m.to_cpp_code(indent=1)

    main_func += '\t' + implement['cout'] + ' << ' + path_data.get_return_expr() + ' << "\\n";\n'
    main_func += '}\n'

    output_file = {'float': FLOATCPP, 'real': REALCPP}
    f = open(output_file[implement_type], 'w')
    print (implement['header'], file=f)
    print (main_func, file=f)


# 稳定性分析主逻辑
def stable_analysis(path_data, path):

    variables = path_data.get_variables()
    print ('VARIABLES:\t', variables, file=LOGFILE)
    print ('PATH:\t', path, file=LOGFILE)
    print ('CONSTRAIN:\t',  file=LOGFILE)

    # 只关心用户输入的变量
    input_variables = path_data.get_input_variables()
    input_variables_type = [path_data.get_variable_type(var) for var in input_variables]
    intervals = divide_input_space(input_variables_type)
    points = [interval2points(interval) for interval in intervals]

    generate_cpp(path_data, path)
    call(['make'], shell=True)

    stable_interval = []
    unstable_interval = []

    for i in range(len(intervals)):

        stable = True   # interval stable
        pstable = True  # point stable

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

            print (' '.join(point), file=open('input', 'w'))
            
            call(['./float < input > float_output'], shell=True)
            call(['./real < input > real_output'], shell=True)

            float_res = Decimal([line.rstrip('\n') for line in open('float_output')][0])
            real_res = Decimal([line.rstrip('\n') for line in open('real_output')][0])

            if real_res == Decimal(0):
                relative_error = abs((float_res-real_res)/Decimal(1))
            else:
                relative_error = abs((float_res-real_res)/real_res)

            if relative_error >= TOLERANCE:
                pstable = False
                stable = False
            
            print ('', file=LOGFILE)
            print ('POINT:\t', point, file=LOGFILE) 
            print ('FLOAT RESUTL:\t', '%.20E' % float_res, file=LOGFILE)
            print ('REAL RESUTL:\t', '%.20E' % real_res, file=LOGFILE)
            print ('RELATVIE ERROR:\t','%.20E' % relative_error, file=LOGFILE )
            print ('STABLE:\t', str(stable), file=LOGFILE )

            '''
            print ('')
            print ('POINT:\t', point) 
            print ('FLOAT RESUTL:\t', '%.20E' % float_res)
            print ('REAL RESUTL:\t', '%.20E' % real_res)
            print ('RELATVIE ERROR:\t','%.20E' % relative_error)
            print ('STABLE:\t', str(stable))
            '''

        if stable:
            stable_interval.append(intervals[i])
        else:
            unstable_interval.append(intervals[i])

    print (' ', file=LOGFILE)
    print ('STABLE INTERVAL:\t', len(stable_interval), file=LOGFILE)
    print ('UNSTABLE INTERVAL:\t', len(unstable_interval), file=LOGFILE)

    # call(['make clean'], shell=True)

    stable_interval = merge_interval(stable_interval)
    unstable_interval = merge_interval(unstable_interval)

    stable_interval = intervals2constrain(input_variables, input_variables_type, stable_interval)
    unstable_interval = intervals2constrain(input_variables, input_variables_type, unstable_interval)

    return {'stable': stable_interval, 'unstable': unstable_interval}

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

pd = PathData('../case/harmonic/harmonic.pth')
path = pd.get_paths()[0]
generate_cpp(pd, path)
