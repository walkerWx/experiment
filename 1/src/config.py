#!/usr/bin/python
# -*- coding:utf-8 -*-

# Configuration file

# 优化后程序两种不同的实现类型：浮点数实现、高精度实现
FLOATTYPE = 'float'
REALTYPE = 'real'

# 待分析输入区间，每个输入范围 [START, END]
FLOATSTART = 0.4
FLOATEND = 0.6

INTSTART = 1
INTEND = 100

# 区间拆分粒度，即划分小区间的大小 10^(-PREC)
PREC = 3

# 浮点精度与高精度程序的容许的相对误差，容许误差范围内认为是稳定的
TOLERANCE = 5

# 使用规则进行等价转化尝试次数
TRANSFORM_NUM = 1

# 不同实现对应的不同类型的名称以及需要引入的头文件等
FLOAT = dict()
REAL = dict()

FLOAT['decimal'] = 'double'
FLOAT['integer'] = 'int'
FLOAT['cin'] = 'std::cin'
FLOAT['cout'] = 'std::cout'
FLOAT['header'] = '''
#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>

#define euler_gamma 0.57721566490

using namespace std;
'''

REAL['decimal'] = 'REAL'
REAL['integer'] = 'int'
REAL['cin'] = 'iRRAM::cin'
REAL['cout'] = 'iRRAM::cout'
REAL['header'] = '''
#include "iRRAM.h"
#include "gamma.h"

#define euler_gamma REAL(0.57721566490)

using namespace iRRAM;
'''

REAL['convert_func'] = {'decimal': 'as_double()', 'integer': 'as_double()'}

FLOATCPP = 'float.cpp'
REALCPP = 'real.cpp'

LOGFILE = open('LOG', 'a')

