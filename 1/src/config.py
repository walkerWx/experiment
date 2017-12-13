#!/usr/bin/python
# -*- coding:utf-8 -*-

# Configuration file

# 待分析输入区间，每个输入范围 [START, END]
FLOATSTART = 1
FLOATEND = 2

INTSTART = 50000
INTEND = 50100

# 区间拆分粒度，即划分小区间的大小 10^(-PREC)
PREC = 1

# 浮点精度与高精度程序的容许的相对误差，容许误差范围内认为是稳定的
TOLERANCE = 2

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
REAL['integer'] = 'int'
REAL['cin'] = 'cin'
REAL['cout'] = 'cout'
REAL['header'] = '''
#include "iRRAM.h"
using namespace iRRAM;
'''

FLOATCPP = 'float.cpp'
REALCPP = 'real.cpp'

LOGFILE = open('LOG', 'w')

