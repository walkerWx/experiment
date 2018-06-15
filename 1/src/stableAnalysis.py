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
import path

logging.basicConfig(format='%(levelname)s %(asctime)s : %(message)s', level=logging.INFO)


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
# def generate_random_double(start=-0.9, end=-1.1):

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
    irram_double = binary2double(irram_res)
    opt_double = binary2double(opt_res)
    if math.isnan(opt_double) or math.isnan(irram_double):
        return 64
    distance = double_distance(irram_double, opt_double)
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
def stable_analysis(path_data):

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
                values.append(int2binary(generate_random_int(1, 10000)))

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

    point_stability_output = [(point, is_point_stable(point), real_output(point)) for point in points]  # 所有输入点及其稳定性信息，结构:[(p1, True), (p2, False)... ]

    # 所有输入点按大小排序，按照输入点的第一个维度的大小
    point_stability_output = sorted(point_stability_output, key=lambda p: binary2double(p[0].values[0]) if p[0].types[0] == 'decimal' else (binary2int(p[0].values[0]) if p[0].types[0] == 'integer' else 0))

    for pso in point_stability_output:
        print("{}\t{}".format(str(pso[0]), str(pso[1])))

    # 对稳定性不同的相邻输入点进行进一步划分

    new_points = list()  # 划分过程中新产生的输入点
    for i in range(len(point_stability_output)-1):

        # 相邻输入点稳定性不同，进一步划分
        if point_stability_output[i][1] != point_stability_output[i+1][1]:
            new_points.extend(divide_stable_unstable(point_stability_output, i))

    # 新产生的输入点加入并排序
    point_stability_output.extend(new_points)
    point_stability_output = sorted(point_stability_output, key=lambda p: binary2double(p[0].values[0]) if p[0].types[0] == 'decimal' else (binary2int(p[0].values[0]) if p[0].types[0] == 'integer' else 0))

    for pso in point_stability_output:
        print("{}\t{}".format(str(pso[0]), str(pso[1])))

    # 对相邻的稳定输入点进一步细化，一直细化到输入点的数量达到一定值
    points_enough = 500  # CONFIG
    while len(point_stability_output) < points_enough:

        print("points number " + str(len(point_stability_output)))

        # 根据权重对相邻的稳定输入点进一步细化，权重主要取决于下述两个值
        w1 = list()
        w2 = list()

        # 相邻稳定输入点 p q, abs((real_output(p)-real_output(q))/(p-q))
        def weight_1(p, q):

            # 只考虑相邻的稳定输入点
            if (not p[1]) or (not q[1]):
                return 0

            delta_out = abs(binary2double(p[2])-binary2double(q[2]))
            delta_in = 1
            if p[0].types[0] == 'decimal':
                delta_in = abs(binary2double(p[0].values[0])-binary2double(q[0].values[0]))
            elif p[0].types[0] == 'integer':
                delta_in = abs(binary2int(p[0].values[0])-binary2int(q[0].values[0]))

            if delta_in == 0:
                delta_in = sys.float_info.min

            return delta_out/delta_in

        # 相邻稳定输入点距离权重
        def weight_2(p, q):

            # 只考虑相邻的稳定输入点
            if (not p[1]) or (not q[1]):
                return 0

            d = 0
            if p[0].types[0] == 'decimal':
                d = double_distance(binary2double(p[0].values[0]), binary2double(q[0].values[0]))
            elif p[0].types[0] == 'integer':
                d = int_distance(binary2int(p[0].values[0]), binary2int(q[0].values[0]))

            if d == 0:
                return 0

            return int(math.log2(d))/64

        w1 = [weight_1(point_stability_output[i], point_stability_output[i+1]) for i in range(len(point_stability_output)-1)]
        w2 = [weight_2(point_stability_output[i], point_stability_output[i+1]) for i in range(len(point_stability_output)-1)]

        # 归一化
        if max(w1) > 0:
            w1 = [w/max(w1) for w in w1]
        if max(w2) > 0:
            w2 = [w/max(w2) for w in w2]

        # 对应权重相加
        w = [sum(x) for x in zip(w1, w2)]

        # 最大权重下标
        max_weight_index = w.index(max(w))

        # 在该下标处细分
        point_stability_output = divide_stable_stable(point_stability_output, max_weight_index)

    for pso in point_stability_output:
        print("{}\t{}".format(str(pso[0]), str(pso[1])))

    return [(pso[0], pso[1]) for pso in point_stability_output]


# 根据index对相邻的两个稳定性不同的输入点进一步划分，通过二分查找的方式大致定位稳定与不稳定的分界点，并将新产生的分界点返回
def divide_stable_unstable(point_stability_output, index):

    left_point = point_stability_output[index][0]
    right_point = point_stability_output[index+1][0]

    logging.info("divide stable unstable: {} --- {}".format(str(left_point), str(right_point)))

    lsi = point_stability_output[index][1]
    rsi = point_stability_output[index+1][1]

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
        # 当前输入为整数的用例均为循环次数，因此这里设置的间隔较小
        if left_point.types[0] == 'integer' and int_distance(binary2int(left_point.values[0]), binary2int(right_point.values[0])) < 2:
            break

        msi = is_point_stable(mid_point)

        if msi == lsi:
            left_point = mid_point
        elif msi == rsi:
            right_point = mid_point

        mid_point = get_middle_point(left_point, right_point)  # FIXME 同上

    # 返回划分过程中新产生的点
    return [(left_point, lsi, real_output(left_point)), (right_point, rsi, real_output(right_point))]


# 根据index对相邻的两个稳定的输入点形成的区间进行划分，去中点判定稳定性，稳定则将新的分界点加入到point_stability_output并返回，不稳定则使用divide_stable_unstable进一步划分
def divide_stable_stable(point_stability_output, index):

    left_point = point_stability_output[index][0]
    right_point = point_stability_output[index+1][0]

    logging.info("divide stable stable: {} --- {}".format(str(left_point), str(right_point)))

    mid_point = get_middle_point(left_point, right_point)
    point_stability_output.insert(index+1, (mid_point, is_point_stable(mid_point), real_output(mid_point)))

    # 中点不稳定，细分
    if not point_stability_output[index+1][1]:

        new_points = list()
        new_points.extend(divide_stable_unstable(point_stability_output, index))
        new_points.extend(divide_stable_unstable(point_stability_output, index+1))

        # 新产生的输入点加入并排序
        point_stability_output.extend(new_points)
        point_stability_output = sorted(point_stability_output, key=lambda p: binary2double(p[0].values[0]) if p[0].types[0] == 'decimal' else (binary2int(p[0].values[0]) if p[0].types[0] == 'integer' else 0))

    return point_stability_output


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


# 输入点在任意精度下输出，注意当前的real是否为对应的任意精度程序
def real_output(point):
    return subprocess.run(['./real'], stdout=subprocess.PIPE, input=' '.join(point.values), encoding='ascii').stdout


# 判断输入点是否稳定，注意调用前必须保证对应路径已经生成可执行程序float与real
def is_point_stable(point):

    stable = True

    # 在稳定输入域与不稳定输入域的交界处，稳定输入点越靠近稳定输入域越密集，不稳定输入点越靠近不稳定输入域越密集
    # 因此，如果只通过单个点来判定稳定性有可能选取到不稳定输入域附近孤立的稳定点，这里采取的策略是在point附近多次采点，均稳定则稳定，出现不稳定则不稳定

    # 首先确认选取的点时稳定的
    float_res = subprocess.run(['./float'], stdout=subprocess.PIPE, input=' '.join(point.values), encoding='ascii').stdout
    real_res = subprocess.run(['./real'], stdout=subprocess.PIPE, input=' '.join(point.values), encoding='ascii').stdout
    bits_err = bits_error(real_res, float_res)
    if bits_err >= TOLERANCE:
        return False

    # 参数类型为整数时，直接以该点的稳定性作为判断依据
    if point.types[0] == "integer":
        return bits_err < TOLERANCE

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

    pth = '../case/herbie/sqrtexp/sqrtexp.pth'

    path_data = path.PathData(pth)

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

    stable_analysis(path_data)



