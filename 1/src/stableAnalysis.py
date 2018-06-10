#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from decimal import *
from config import *

import itertools
import copy
import subprocess
import struct
import sys
import random
import functools
import re
import sympy
import math
import logging

logging.basicConfig(format='%(levelname)s %(asctime)s : %(message)s', level=logging.INFO)

import path

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
def generate_cpp(path_data, paths, implement_type='all'):

    if implement_type == 'all':
        generate_cpp(path_data, paths, 'float')
        generate_cpp(path_data, paths, 'real')
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

    main_func += '\t' + precision_setting + '\n'

    for var in path_data.get_variables():
        main_func += '\t' + implement[path_data.get_variable_type(var)] + ' ' + var + ';\n'
    main_func += '\n'

    # 输入对应字符串变量声明
    # main_func += '//输入对应字符串变量声明\n'
    main_func += '\tstd::string ' + ','.join([iv + '_str' for iv in path_data.get_input_variables()]) + ';\n'

    # 用户输入
    # main_func += '//用户输入\n'
    main_func += '\t' + implement['cin'] + ' >> ' + ' >> '.join([iv + '_str' for iv in path_data.get_input_variables()]) + ';\n\n'

    # 字符串变量转换为数值变量
    # main_func += '//字符串变量转换为数值变量\n'
    for iv in path_data.get_input_variables():
        main_func += '\t' + iv + ' = ' + TRANSFUNC[path_data.get_variable_type(iv)] + '(' + iv + '_str);\n'
    main_func += '\n'

    for path in paths:
        main_func += '\tif(' + path.get_constrain() + '){\n'
        for m in path.get_path_list():
            main_func += m.to_cpp_code(implement_type, indent=2)
        main_func += '\t}\n\n'

    if implement == FLOAT:
        main_func += '\t' + implement['cout'] + ' << double2binary(' + path_data.get_return_expr() + ') << "\\n";\n'
    elif implement == REAL:
        main_func += '\t' + implement['cout'] + ' << double2binary(' + path_data.get_return_expr() + '.as_double()) << "\\n";\n'

    main_func += '}\n'

    output_file = {'float': FLOATCPP, 'real': REALCPP}
    f = open(output_file[implement_type], 'w')
    print(implement['header'], file=f)
    print(main_func, file=f)


# 稳定性分析主逻辑
def stable_analysis(path_data, path):

    variables = path_data.get_variables()
    print('VARIABLES:\t', variables, file=LOGFILE)
    print('PATH:\t', path.to_json(), file=LOGFILE)
    print('CONSTRAIN:\t',  file=LOGFILE)

    # 只关心用户输入的变量
    input_variables = path_data.get_input_variables()
    input_variables_type = [path_data.get_variable_type(var) for var in input_variables]
    intervals = divide_input_space(input_variables_type)
    points = [interval2points(interval) for interval in intervals]

    generate_cpp(path_data, path)
    subprocess.call(['make'], shell=True)

    stable_interval = []
    unstable_interval = []

    for i in range(len(intervals)):

        stable = True   # interval stable
        pstable = True  # point stable

        print('', file=LOGFILE)
        print('----------------------------------------------', file=LOGFILE)
        print('INTERVAL:\t', intervals[i], file=LOGFILE)

        # 对待分析区间中所有点，计算其比特误差
        for point in points[i]:

            pstable = True

            float_res = subprocess.run(['./float'], stdout=subprocess.PIPE, input=' '.join(point), encoding='ascii').stdout
            real_res = subprocess.run(['./real'], stdout=subprocess.PIPE, input=' '.join(point), encoding='ascii').stdout
            bits_error = int(subprocess.run(['./bits_error'], stdout=subprocess.PIPE, input=float_res+' '+real_res, encoding='ascii').stdout)

            if bits_error >= TOLERANCE:
                pstable = False
                stable = False

            print('', file=LOGFILE)
            print('POINT:\t', point, file=LOGFILE)
            print('FLOAT RESULT:\t', float_res, file=LOGFILE)
            print('REAL RESULT:\t', real_res, file=LOGFILE)
            print('BITS ERROR:\t', bits_error, file=LOGFILE)
            print('STABLE:\t', str(pstable), file=LOGFILE)

        if stable:
            stable_interval.append(intervals[i])
        else:
            unstable_interval.append(intervals[i])

    print(' ', file=LOGFILE)
    print('STABLE INTERVAL:\t', len(stable_interval), file=LOGFILE)
    print('UNSTABLE INTERVAL:\t', len(unstable_interval), file=LOGFILE)

    return {'stable': stable_interval, 'unstable': unstable_interval}


# 判断一条路径在给定区间上是否稳定
def filter_stable_interval(path_data, original_path, opt_path, intervals):

    # 根据path生成可执行文件并编译
    generate_cpp(path_data, original_path, implement_type='real')
    generate_cpp(path_data, opt_path, implement_type='float')
    subprocess.call(['make > /dev/null'], shell=True)

    stable_intervals = list()
    for interval in intervals:

        # 输入区间对应边界点
        points = interval2points(interval)

        # TODO 判断输入域上的点是否均满足路径约束

        pstable = True
        for point in points:

            float_res = subprocess.run(['./float'], stdout=subprocess.PIPE, input=' '.join(point), encoding='ascii').stdout
            real_res = subprocess.run(['./real'], stdout=subprocess.PIPE, input=' '.join(point), encoding='ascii').stdout
            bits_error = int(subprocess.run(['./bits_error'], stdout=subprocess.PIPE, input=float_res+' '+real_res, encoding='ascii').stdout)

            if bits_error >= TOLERANCE:
                pstable = False
                break

        if pstable:
            stable_intervals.append(interval)

    return stable_intervals


# 将双精度浮点数转换为其二进制表示
def double2binary(d):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!d', d))


# 将整型转换为其二进制表示
def int2binary(i):
    return ''.join('{:0>8b}'.format(c) for c in struct.pack('!i', i))


# 将二进制表示的双精度浮点数转换为数值形式
def binary2double(b):
    return struct.unpack('d', struct.pack('Q', int('0b'+b, 0)))[0]


# 将二进制表示表示的有符号整型转换为数值形式
def binary2int(b):
    return struct.unpack('i', struct.pack('I', int('0b'+b, 0)))[0]


# 计算begin与end在双精度浮点数数轴上的距离，即中间隔间多少个浮点数+1
def double_distance(begin, end):

    if begin == end:
        return 0
    if end < begin:
        return double_distance(end, begin)
    if begin == 0:
        return int('0b'+double2binary(end), 0)
    if begin < 0 < end:
        return double_distance(0, -begin)+double_distance(0, end)
    if 0 < begin:
        return double_distance(0, end)-double_distance(0, begin)
    if end <= 0:
        return double_distance(0, -begin)-double_distance(0, -end)
    return 0


# 计算两个有符号整型的距离
def int_distance(begin, end):
    return abs(begin-end)


# 生成双精度浮点数d后面第offset个浮点数
def generate_double_by_offset(d, offset):
    if d == 0:
        if offset >= 0:
            return struct.unpack('d', struct.pack('Q', offset))[0]
        else:
            return -struct.unpack('d', struct.pack('Q', -offset))[0]
    if d > 0:
        return generate_double_by_offset(0, offset+double_distance(0, d))
    if d < 0:
        if offset >= double_distance(d, 0.0):
            return generate_double_by_offset(0.0, offset - double_distance(d, 0.0))
        else:
            return -generate_double_by_offset(0.0, double_distance(0.0, -d) - offset)


# 生成随机的双精度浮点数
def generate_random_double(start=-sys.float_info.max, end=sys.float_info.max):

    if start == end:
        return start
    if start > end:
        return generate_random_double(end, start)

    distance = double_distance(start, end)

    offset = random.randrange(distance)
    return generate_double_by_offset(start, offset)


# 生成随机整型，默认c++ int范围
# def generate_random_int(start=1, end=1100):
def generate_random_int(start=-2147483647, end=2147483647):
    if start > end:
        return generate_random_int(end, start)
    return random.randint(start, end)


# 在point附近+-range范围内随机生成其他的点
def generate_random_point(point, rge):
    values = list()
    types = copy.copy(point.types)
    for i in range(point.dimension):
        if types[i] == 'decimal':
            d = binary2double(point.values[i])
            s = generate_double_by_offset(d, -rge)
            e = generate_double_by_offset(d, rge)
            values.append(double2binary(generate_random_double(s, e)))
        if types[i] == 'integer':
            i = binary2int(point.values[i])
            values.append(int2binary(generate_random_int(i-rge, i+rge)))
    return Point(values, types)


# 计算两个二进制表示的浮点数的相对误差
def relative_error(irram_res, opt_res):
    irram = binary2double(irram_res)
    opt = binary2double(opt_res)
    if irram == 0:
        if opt == 0:
            return 0
        return float('inf')
    return abs((irram-opt)/irram)


# 计算两个二进制表示的浮点数的比特误差
def bits_error(irram_res, opt_res):
    distance = double_distance(binary2double(irram_res), binary2double(opt_res))
    if distance == 0:
        return 0
    return int(math.log2(distance))


# 生成两个浮点数的中位数mid，满足double_distance(left, mid) == double_distance(mid, right) +- 1
def get_middle_double(left, right):
    distance = double_distance(left, right)
    return generate_double_by_offset(left, int(distance/2))


# 生成两个有符号整型的均值
def get_middle_int(left, right):
    return left + int((right-left)/2)


# 生成两个输入点的中间的点
def get_middle_point(left, right):

    values = list()
    types = copy.copy(left.types)

    for i in range(len(types)):
        if types[i] == 'decimal':
            lv = binary2double(left.values[i])
            rv = binary2double(right.values[i])
            mv = get_middle_double(lv, rv)
            values.append(double2binary(mv))
        if types[i] == 'integer':
            lv = binary2int(left.values[i])
            rv = binary2int(right.values[i])
            mv = get_middle_int(lv, rv)
            values.append(int2binary(mv))

    return Point(values, types)


class Point:

    """输入点封装类"""

    # values为一个list，双精度浮点数使用一个64位的01串来表示，整数类型即使用普通数值形式表示
    # types与values相对应，有'decimal'与'integer'两种类型
    def __init__(self, values, types):
        if len(values) != len(types):
            sys.exit("Initialize point error, len(values) != len(types)")
        self.dimension = len(values)
        self.values = values
        self.types = types

    def __str__(self):
        s = ''
        for i in range(self.dimension):
            if self.types[i] == 'decimal':
                s += '{:.25e}\t'.format(binary2double(self.values[i]))
            if self.types[i] == 'integer':
                s += '{:0>10d}\t'.format(binary2int(self.values[i]))
        return s

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        if not self.dimension == other.dimension:
            return False
        return self.types == other.types and self.values == other.values

    def __hash__(self):
        return hash(' '.join(self.types) + ' ' + str(self))


# 稳定性分析
def stable_analysis_new(path_data):

    paths = path_data.get_paths()
    input_variables = path_data.get_input_variables()

    points = list()  # 输入点
    while len(points) < 300:  # 300个随机输入

        values = list()
        types = list()
        for v in input_variables:
            t = path_data.get_variable_type(v)
            types.append(t)
            if t == 'decimal':
                values.append(double2binary(generate_random_double()))
            elif t == 'integer':
                values.append(int2binary(generate_random_int()))

        point = Point(values, types)

        # 排除不满足任意一条路径约束的输入
        constrains = [p.get_constrain() for p in paths]
        if not functools.reduce(lambda x, y: x or y, [satisfy(point, input_variables, c) for c in constrains]):
            continue

        points.append(point)

    logging.info("Random sampling points")
    for point in points:
        logging.info(str(point))

    # 判断输入稳定性
    generate_cpp(path_data, paths)  # 根据路径生成cpp文件
    subprocess.call(['make > /dev/null'], shell=True)  # 编译

    point_stablility = [(point, is_point_stable(point)) for point in points]  # 所有输入点及其稳定性信息，结构:[(p1, True), (p2, False)... ]

    # 所有输入点按大小排序，按照输入点的第一个维度的大小
    point_stablility = sorted(point_stablility, key=lambda p: binary2double(p[0].values[0]) if p[0].types[0] == 'decimal' else (binary2int(p[0].values[0]) if p[0].types[0] == 'integer' else 0))

    for ps in point_stablility:
        print(ps[0], end='\t')
        print(ps[1])

    # 对稳定性不同的相邻输入点进行进一步划分

    new_points = list() # 划分过程中新产生的输入点
    for i in range(len(point_stablility)-1):

        # 相邻输入点稳定性不同，进一步划分
        if point_stablility[i][1] != point_stablility[i+1][1]:
            new_points.extend(divide_stable_unstable(point_stablility, i))

    # 新产生的输入点加入并排序
    point_stablility.extend(new_points)
    point_stablility = sorted(point_stablility, key=lambda p: binary2double(p[0].values[0]) if p[0].types[0] == 'decimal' else (binary2int(p[0].values[0]) if p[0].types[0] == 'integer' else 0))

    for ps in point_stablility:
        print(ps[0], end='\t')
        print(ps[1])

    # TODO 对相邻的稳定输入点进一步细化

    return point_stablility


# 根据index对相邻的两个稳定性不同的输入点进一步划分，通过二分查找的方式大致定位稳定与不稳定的分界点，并将新产生的分界点返回
def divide_stable_unstable(point_stablility, index):

    left_point = point_stablility[index][0]
    right_point = point_stablility[index+1][0]

    lsi = point_stablility[index][1]
    rsi = point_stablility[index+1][1]

    mid_point = get_middle_point(left_point, right_point)  # FIXME mid_point是有可能不在输入域上的，如何处理？

    # 相距1000个输入点认为足够近，退出循环，参数可调
    close_enough = 1000  # CONFIG

    while True:

        d = double_distance(binary2double(left_point.values[0]), binary2double(right_point.values[0]))
        print('L:', end='')
        print(left_point)
        print('M:', end='')
        print(mid_point)
        print('R:', end='')
        print(right_point)
        print('D::' + str(d))
        print('')

        if left_point.types[0] == 'decimal' and double_distance(binary2double(left_point.values[0]), binary2double(right_point.values[0])) < close_enough:
            break
        if left_point.types[0] == 'integer' and int_distance(binary2int(left_point.values[0]), binary2int(right_point.values[0])) < close_enough:
            break

        msi = is_point_stable(mid_point)

        if msi == lsi:
            left_point = mid_point
        elif msi == rsi:
            right_point = mid_point

        mid_point = get_middle_point(left_point, right_point)  # FIXME 同上

    # 返回划分过程中新产生的点
    return [(left_point, lsi), (right_point, rsi)]


# 根据index对相邻的两个稳定的输入点形成的区间进行划分，去中点判定稳定性，稳定则将新的分界点加入到point_stability并返回，不稳定则使用divide_stable_unstable进一步划分 TODO
def divide_stable_stable(point_stability, index):
    return


# 判断输入是否满足约束
def satisfy(point, variables, constrain):

    if constrain == 'true':
        return True

    values = list()
    for i in range(point.dimension):
        if point.types[i] == 'decimal':
            values.append(str(binary2double(point.values[i])))
        if point.types[i] == 'integer':
            values.append(str(binary2int(point.values[i])))

    stmt1 = ','.join(variables) + " = sympy.symbols('" + ' '.join(variables) + "')"
    exec(stmt1)

    stmt2 = 'constrain_expr=' + constrain

    stmt2 = re.sub(r'\s+', '', stmt2)  # 去空格
    stmt2 = re.sub(r'&&', '&', stmt2)  # && -> &
    stmt2 = re.sub(r'\|\|', '|', stmt2)  # || -> |
    stmt2 = re.sub(r'!', '~', stmt2)  # ! -> ~

    # 加括号
    stmt2 = re.sub(r'=(.*?)([&|])', r'=(\1)\2', stmt2)
    stmt2 = re.sub(r'([&|])(.*?)([&|])', r'\1(\2)\3', stmt2)
    stmt2 = re.sub(r'([&|])([^&|]*?)$', r'\1(\2)', stmt2)
    stmt2 = re.sub(r'~([^&|~]*)', r'~(\1)', stmt2)

    exec(stmt2)

    stmt3 = 'constrain_expr.subs({' + ','.join([variables[i] + ':' + values[i] for i in range(len(values))]) + '})'

    return eval(stmt3)


# 判断输入点是否稳定，注意调用前必须保证对应路径已经生成可执行程序float与real
def is_point_stable(point):

    stable = True

    # 在稳定输入域与不稳定输入域的交界处，稳定输入点越靠近稳定输入域越密集，不稳定输入点越靠近不稳定输入域越密集
    # 因此，如果只通过单个点来判定稳定性有可能选取到不稳定输入域附近孤立的稳定点，这里采取的策略是在point附近多次采点，均稳定则稳定，出现不稳定则不稳定

    # 当前策略为+-50范围内选10个点，参数可调整
    points_num = 10  # CONFIG
    points_range = 50  # CONFIG

    count = 0
    for _ in range(points_num):

        # 距离50范围内采点
        random_point = generate_random_point(point, points_range)

        # logging.info('Call subprocess float with parameter {}'.format(' '.join(random_point.values)))
        float_res = subprocess.run(['./float'], stdout=subprocess.PIPE, input=' '.join(random_point.values), encoding='ascii').stdout
        # logging.info('Call subprocess real  with parameter {}'.format(' '.join(random_point.values)))
        real_res = subprocess.run(['./real'], stdout=subprocess.PIPE, input=' '.join(random_point.values), encoding='ascii').stdout

        bits_err = bits_error(real_res, float_res)
        # stable = (stable and (bits_err < TOLERANCE))
        if bits_err < TOLERANCE:
            count += 1
        else:
            count -= 1

    return count >= 4  # 稳定不稳定73开认为稳定，后续调整


if __name__ == "__main__":

    point = [1, 200, 3.0]
    # variables = [['x', 'decimal'], ['y', 'integer'], ['z', 'decimal']]
    variables = [['x', 'decimal']]

    pth = '../case/herbie/logq/logq.pth'

    path_data = path.PathData(pth)
    paths = path_data.get_paths()

    # start = 0.1
    # end = 0.25
    #
    # N = 1000
    #
    # points = [[generate_random_double(0.1, 0.25)] for _ in range(N)]
    # points = sorted(points, key=lambda p: p[0])
    # points = [[double2binary(p[0])] for p in points]
    # for p in points:
    #     print(binary2double(p[0]), end='\t')
    #     print(is_point_stable(p))

    stable_analysis_new(path_data)



