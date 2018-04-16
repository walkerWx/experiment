#!/usr/bin/env sage
# -*- coding: utf-8 -*-

from .path import *
from .config import *

import json
import random
import itertools
from copy import deepcopy
from copy import copy


# load rules from file
rules_file = 'rules.json'
with open(rules_file) as f:
    rules = json.load(f)["expr_rules"]


# 判断两个计算路径是否等价
def is_expr_equal(vars1, path1, vars2, path2):

    # 变量数量一致
    if len(vars1) != len(vars2):
        return False

    var(' '.join(vars1))
    var(' '.join(vars2))

    exec 'expr1 = ' + path1
    exec 'expr2 = ' + path2

    # substitute variables with random numbers, if the result of the paths are always the same, they are equal paths
    try_num = 10
    for _ in range(try_num):

        # 初始化随机输入
        random_nums = []
        for _ in range(len(vars1)):
            random_nums.append(random.uniform(-10, 10))

        exec_stmt1 = 'res1 = expr1.subs('
        variables = copy(vars1)
        for j in range(len(vars1)):
            variables[j] += '=' + '{:.9f}'.format(random_nums[j])
        exec_stmt1 += ','.join(variables) + ')'
        exec exec_stmt1

        exec_stmt2 = 'res2 = expr2.subs('
        variables = copy(vars2)
        for j in range(len(vars2)):
            variables[j] += '=' + '{:.9f}'.format(random_nums[j])
        exec_stmt2 += ','.join(variables) + ')'
        exec exec_stmt2

        epsi = 1e-10
        print res1-res2
        if (abs(res1-res2) > epsi):
            return False

    return True


def generate_gamma_approx_expr(var_str):
    up = '(8-4*euler_gamma+(3-2*euler_gamma)*('+var_str+'))'
    down = '(8+4*('+var_str+'))'
    return up+'/'+down


# 输入一个分式。返回一个分式的随机拆分
def get_random_denominator(f):
    if(not is_simple(f.numerator())):
        return f
    length = f.numerator().number_of_operands()
    return denominator(f,get_random_list(length))


# 输入一个0-（length-1）的数组，返回一个该数组的随机拆分
def get_random_list(length):
    if(length<=1):
        return [0]
    number_of_list = random.randint(1,length)
    list = []
    temp_list = []
    if(number_of_list==1):
        for i in range(0,length):
            temp_list.append(i)
        list.append(temp_list)
        return list
    list_1 = []
    randid=1
    while(randid==1 and length-len(list_1)>0):
        length_i = random.randint(1,length-len(list_1))
        a = 0
        list_2 = []
        while(a<length_i):
            j = random.randint(0,length-1)
            if j in list_1:
                a = a-1
            else:
                list_2.append(j)
                list_1.append(j)
            a = a+1
        list.append(list_2)
        randid = random.randint(0,2)
    last_list = []
    for i in range(0,length):
        if i not in list_1:
            last_list.append(i)
    if(len(last_list)>0):
        list.append(last_list)
    return list


# 根据list来随机拆分分式f
def denominator(f,list):
    den = f.denominator()
    num = f.numerator()
    res = 0
    for sublist in list:
        temp = 0
        for i in sublist:
            temp = temp + num.op[i]
        res = res + temp/den
    return res


# 主函数
def transform(f,num):
    res_list = []
    num_of_result = num
    exp = f.expand().normalize()
    #denominator for expression
    repeat_time = 0
    i=0
    while(i<num_of_result and repeat_time < num_of_result + 100):
        temp = repr(get_random_transform(exp))
        if(temp in res_list):
            repeat_time = repeat_time + 1
            i = i - 1
        else:
            res_list.append(temp)
            repeat_time = 0
        i = i + 1
    return res_list


# 判断是否是分式，是分式就对分式进行拆分后再变形
def get_random_transform(f):
    #random divide first time
    if(is_simple(f)):
        return transform_exp(f)
    elif(is_fraction(f)):
        exp = get_random_denominator(f)
        res = 0
        if(is_simple(exp)):
            for term in exp.op:
                term = random_dif_of_sqr(term)
                numerator = transform_exp(term.numerator())
                denominator = transform_exp(term.denominator())
                res = res + numerator/denominator
        else:
            exp = random_dif_of_sqr(exp)
            numerator = transform_exp(exp.numerator())
            denominator = transform_exp(exp.denominator())
            res = numerator/denominator
        return res
    else:
        return transform_exp(f)


# 对一个非分式进行变形
def transform_exp(f):
    if(not is_expression(f)):
        return transform_exp_implements(f)
    if(not is_simple(f)):
        return transform_exp_implements(f)
    #get a random divide
    length = f.number_of_operands()
    # a little chance not to divide
    random_list = simple_get_random_list(length)
    f1 = 0
    for j in random_list[0]:
        f1 = f1 + f.op[j]
    f2 = f - f1
    f1 = transform_exp_implements(f1)
    f2 = transform_exp_implements(f2)
    res = f1 + f2
    return res


# 随机选择变换规则
def transform_exp_implements(f):
    #random rectfrom expression
    if(not bool(f.imag_part().rectform()==0)):
        if(random.randint(0,1)==1):
            f = f.rectform()
    if(not is_expression(f)):
        randid = random.randint(0,1)
    else:
        randid = random.randint(0,4)
    if(randid==3):
        #factor the expression
        f = f.factor()
    elif(randid==1):
        f = random_expand_trig(f)
    elif(randid==2):
        f = f.reduce_trig()
    elif(randid==4):
        variable = get_random_variable(f)
        f = my_horner(f,random.randint(1,len(f.coefficients(variable,sparse = False))),variable)
    elif(randid==0):
        #expand the expression
        f = f.expand()
    return f


# 三角函数变换
def random_expand_trig(f):
    randid_trig = random.randint(0,1)
    if(randid_trig == 0):
        f = f.expand_trig()
    elif(randid_trig == 1):
        f = f.expand_trig(full = true)
    return f


# horner形式变换
def my_horner(f,times,variable = x):
    coef = f.coefficients(x,sparse = False)
    no_horner_part = coef[0]
    length = len(coef)
    i = 1
    while(i+times<length):
        no_horner_part = no_horner_part + coef[i]*x**i
        i = i + 1
    f = (f - no_horner_part).horner(variable) + no_horner_part
    return f


# 分子分母乘同一个因式
def random_dif_of_sqr(f):
    if(is_simple(f.numerator()) and len(f.numerator()) == 2):
        if(random.randint(0,1)==1):
            f = dif_of_sqr_simple(f).collect_common_factors()
    elif(is_simple(f.denominator()) and len(f.denominator()) == 2 and not f.numerator() == 0):
        if(random.randint(0,1)==1):
            f = dif_of_sqr_simple(f.denominator()/f.numerator())
            f = (f.denominator()/f.numerator()).collect_common_factors()
    return f


def dif_of_sqr_simple(f):
    temp = dif_of_sqr(f.numerator())
    numerator = f.numerator()*temp
    numerator = numerator.expand()
    dinominator = f.denominator()*temp
    dinominator = dinominator.expand()
    result = numerator/dinominator
    return result


def dif_of_sqr(self):
    return self.op[0]-self.op[1]


# 随机选择一个变量
def get_random_variable(f):
    variables = f.variables()
    randid = random.randint(0,len(variables)-1)
    return variables[randid]


# 将一个列表随机拆分成两个列表
def simple_get_random_list(length):
    if(length<=1):
        return [[0]]
    length_1 = random.randint(1,length)
    a = 0
    list_1 = []
    list_2 = []
    while(a<length_1):
        i = random.randint(0,length-1)
        if(i in list_1):
            a = a - 1
        else:
            list_1.append(i)
        a = a + 1
    for i in range(0,length):
        if i not in list_1:
            list_2.append(i)
    return [list_1,list_2]


# 判断是一个符号还是表达式
def is_expression(f):
    var('test_variable_a')
    if(f.operator()==test_variable_a.operator()):
        return False
    return True


# 判断一个表达式优先级最低的符号是不是+或者-
def is_simple(f):
    var('test_variable_a,test_variable_b')
    if(f.operator()==(test_variable_a+test_variable_b).operator()):
        return True
    return False


# 判断一个表达式是不是分式
def is_fraction(f):
    var('test_variable_a,test_variable_b')
    if(f.operator()==(test_variable_a/test_variable_b).operator()):
        return True
    return False


def accumulationTransform(expr):
    expr = expr.expand()
    return expr


# Horner form 转换，将path_data中所涉及到的所有的计算过程均进行转换
def horner_transform(path_data):

    # 声明所涉及到的所有变量
    for v in path_data.get_all_variables():
        var(v)

    # 对于所有的过程语句
    for _, procedure in path_data.get_procedures().items():
        # 对于所有的变量更新表达式
        for variable, update_expr in procedure.get_procedure().items():
            expr = update_expr
            for v in path_data.get_all_variables():
                exec 'expr = ' + str(expr)
                if isinstance(expr, Expression):
                    exec 'expr = str(expr.horner('+ v + '))'
            procedure.set_update_expr(variable, expr)



'''
#variables = ['ar', 'ai', 'br', 'bi']
variables = ['a', 'b', 'c', 'd']
variables2 = ['s', 't', 'a', 'b']
path1 = "(a/sqrt(a*a+b*b)+c/sqrt(c*c+d*d))/sqrt(2+2*(a*c+b*d)/sqrt((a*a+b*b)*(c*c+d*d)))"
path2 = convertPath(path1, variables, variables2) 
print path1
print path2

var('x')
var('y')
var('z')

f = x*x + x*x*x + y
print(f.horner(x).horner(z))

path_file = '../case/analytic/analytic.pth'
path_data = PathData(path_file)
horner_transform(path_data)

path = path_data.get_paths()[0]

eps = generate_equal_path(path)
for ep in eps:
    print (ep.to_json())

# is_expr_equal() test cases
vars1 = ['ar', 'ai', 'br', 'bi']
path1 = '(ar/sqrt(ar*ar+ai*ai)+br/sqrt(br*br+bi*bi))/sqrt(2+2*(ar*br+ai*bi)/sqrt((ar*ar+ai*ai)*(br*br+bi*bi)))'

vars2 = ["a", "b", "c", "d"]
path2 = '(a/sqrt(a*a+b*b)+c/sqrt(c*c+d*d))/sqrt(2+2*(a*c+b*d)/sqrt((a*a+b*b)*(c*c+d*d)))'

equal_path = '-sgn(abs(atan2(b,a)-atan2(d,c))-pi)*cos(0.5*(atan2(b,a)+atan2(d,c)))'

print(is_expr_equal(vars1, path1, vars2, path2))
print(convert_expr(equal_path, vars2, vars1))

path_file = '../case/midarc/midarc.pth'
path_data = PathData(path_file5

p = path_data.get_procedure('p1')
print (p.to_json())

eps = generate_equal_procedure(path_data, p)

print(path_data.to_json())

# reduce loop test case
path_file = '../case/jmmuller/jmmuller.pth'
path_data = PathData(path_file)

l1 = path_data.get_loop('l1')
l2 = path_data.get_loop('l2')

# gamma example test
path_file = '../case/gamma/gamma.pth'
path_data = PathData(path_file)

path = path_data.get_paths()[0]
eps = generate_equal_path(path_data, path)

for ep in eps:
    print(ep.to_json())

print(path_data.to_json())
'''
