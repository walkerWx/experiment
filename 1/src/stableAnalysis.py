#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from subprocess import call
from decimal import *
from config import *

import itertools

getcontext().prec = 20


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
        
    points = [list(x) for x in itertools.product(*interval)]

    # 格式化输入
    for point in points:
        for i in range(len(point)):
            if isinstance(point[i], int):
                point[i] = str(point[i])
            else:
                point[i] = ('%.'+str(PREC)+'f') % point[i]

    return points


# 对拆分后的区间进行合并  
def merge_interval(intervals):

    merged = list()

    # 单变量情况
    dimension = len(intervals[0])

    if dimension == 1:
        # 变量为浮点数
        if len(intervals[0][0]) == 2:
            t = [x[0] for x in intervals]
            i = 0
            while i < len(t):
                start = t[i][0]
                while i+1 < len(t):
                    if t[i][1] != t[i+1][0]:
                        break
                    i = i + 1
                end = t[i][1]
                merged.append([[start, end]])
                i = i + 1
        # 变量为整数
        elif len(intervals[0][0]) == 1:
            t = [x[0] for x in intervals]
            i = 0
            while i < len(t):
                start = t[i][0]
                while i+1 < len(t):
                    if t[i][0] + 1 != t[i+1][0]:
                        break
                    i = i + 1
                end = t[i][0]
                merged.append([[start, end]])
                i = i + 1

    return merged


# 将变量的区间转化为能直接填写到程序中的约束的字符串 
def interval2constrain(variables, variables_type, interval):
    constrain = []
    for i in range(len(interval)):
        if variables_type[i] == 'decimal':
            constrain.append((('%.'+str(PREC)+'f') % interval[i][0]) + '<=' + variables[i] + '&&' + variables[i] + '<=' + (('%.'+str(PREC)+'f') % interval[i][1]))
        elif variables_type[i] == 'integer':
            constrain.append(str(interval[i][0]) + '<=' + variables[i] + '&&' + variables[i] + '<=' + str(interval[i][1]))
    constrain = '(' + '&&'.join(constrain) + ')'
    return constrain


def intervals2constrain(variables, variables_type, intervals):
    intervals = merge_interval(intervals)
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
        main_func += m.to_cpp_code(implement_type, indent=1)

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
    print ('PATH:\t', path.to_json(), file=LOGFILE)
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
            
            print (' '.join(point), file=open('input', 'w'))
            call(['./float < input > float_output'], shell=True)
            call(['./real < input > real_output'], shell=True)

            float_res = [line.rstrip('\n') for line in open('float_output')][0]
            real_res = [line.rstrip('\n') for line in open('real_output')][0]

            if float_res.startswith('-'):
                float_res = str(float_res).split('e')[1][1:18].replace('.', '')
            else:
                float_res = str(float_res).split('e')[0][:17].replace('.', '')
            real_res = str(real_res).split('E')[0][1:18].replace('.', '')

            error = abs(int(float_res)-int(real_res))

            if error >= TOLERANCE:
                pstable = False
                stable = False

            print ('', file=LOGFILE)
            print ('POINT:\t', point, file=LOGFILE) 
            print ('FLOAT RESUTL:\t', float_res, file=LOGFILE)
            print ('REAL RESUTL:\t', real_res, file=LOGFILE)
            print ('RELATVIE ERROR:\t', error, file=LOGFILE )
            print ('STABLE:\t', str(pstable), file=LOGFILE )

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

    return {'stable': stable_interval, 'unstable': unstable_interval}


# 判断一条路径在给定区间上是否稳定
def is_stable(path_data, path, interval):

    # 输入区间对应边界点
    points = interval2points(interval)

    for point in points:

        print (' '.join(point), file=open('input', 'w'))
        call(['./float < input > float_output'], shell=True)
        call(['./real < input > real_output'], shell=True)

        float_res = [line.rstrip('\n') for line in open('float_output')][0]
        real_res = [line.rstrip('\n') for line in open('real_output')][0]

        if float_res.startswith('-'):
            float_res = str(float_res).split('e')[1][1:18].replace('.', '')
        else:
            float_res = str(float_res).split('e')[0][:17].replace('.', '')
        real_res = str(real_res).split('E')[0][1:18].replace('.', '')

        error = abs(int(float_res)-int(real_res))

        if error >= TOLERANCE:
            return False

    return True


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

pd = PathData('../case/harmonic/harmonic.pth')
path = pd.get_paths()[0]
generate_cpp(pd, path)
'''
