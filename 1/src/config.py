#!/usr/bin/python
# -*- coding:utf-8 -*-

# Configuration file

PROJECT_HOME = '/home/walker/Projects/experiment'
iRRAM_HOME = '/home/walker/Projects/iRRAM'

# 优化后程序两种不同的实现类型：浮点数实现、高精度实现
FLOATTYPE = 'float'
REALTYPE = 'real'


# 浮点精度与高精度程序的容许的比特误差，容许误差范围内认为是稳定的
TOLERANCE = 4

# 不同实现对应的不同类型的名称以及需要引入的头文件等
FLOAT = dict()
REAL = dict()

FLOAT['decimal'] = 'double'
FLOAT['integer'] = 'int'
FLOAT['cin'] = 'std::cin'
FLOAT['cout'] = 'std::cout'
FLOAT['header'] = '''
#include "points.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
#include <string>

#define euler_gamma 0.57721566490

using namespace std;
'''

REAL['decimal'] = 'REAL'
REAL['integer'] = 'int'
REAL['cin'] = 'iRRAM::cin'
REAL['cout'] = 'iRRAM::cout'
REAL['header'] = '''
#include "points.h"
#include "iRRAM.h"
#include "gamma.h"
#include <string>

#define euler_gamma REAL(0.57721566490)

using namespace iRRAM;

'''

REAL['convert_func'] = {'decimal': 'as_double(53)', 'integer': ''}

# 二进制表示转换数值表示的函数名
TRANSFUNC = dict()
TRANSFUNC['decimal'] = 'binary2double'
TRANSFUNC['integer'] = 'binary2int'

FLOATCPP = 'float.cpp'
REALCPP = 'real.cpp'

LOGFILE = open('LOG', 'a')

