#!/usr/bin/env sage
# -*- coding: utf-8 -*-

from sage.all import *
import json

import random

var('a b c d e f g h i j k l m n o p q r s t u v w x y z')

# load rules from file
rulesFile = 'rules.json' 
with open(rulesFile) as f:
    rules = json.load(f)["rules"]

# variables substitution in path. e.g x+y --> a+b
def convertPath(originPath, originVars, newVars):

    m = {}
    for i in range(len(originVars)):
        m[originVars[i]] = newVars[i]

    newPath = ''
    i = 0
    while i < len(originPath):
        if (not originPath[i].isalpha()):
            newPath += originPath[i]
            i += 1
        else:
            j = i  
            while (j < len(originPath) and originPath[j].isalpha()):
                j += 1
            var = originPath[i:j]
            if (var in m):
                newPath += m[var]
            else:
                newPath += var
            i = j

    return newPath

class Path:

    def __init__(self, variables, path):
        self.varNum = len(variables)
        self.variables = variables
        self.path = path


# 判断两个计算路径是否等价
def isEqual(path1, path2):

    # 变量数量一致
    if (path1.varNum != path2.varNum):
        return False

    var(' '.join(path1.variables))  
    var(' '.join(path2.variables))  

    exec 'expr1 = ' + path1.path
    exec 'expr2 = ' + path2.path

    # substitute variables with random numbers, if the result of the paths are always the same, they are equal paths
    TryNum = 10
    for _ in range(TryNum):
        randomNumbers = [] 
        for _ in range(path1.varNum):
            randomNumbers.append(random.uniform(-10, 10))

        execStr1 = 'res1 = expr1.subs('
        variables = list(path1.variables)
        for j in range(len(variables)):
            variables[j] += '=' + '{:.9f}'.format(randomNumbers[j])
        execStr1 += ','.join(variables) + ')'
        exec execStr1

        execStr2 = 'res2 = expr2.subs('
        variables = list(path2.variables)
        for j in range(len(variables)):
            variables[j] += '=' + '{:.9f}'.format(randomNumbers[j])
        execStr2 += ','.join(variables) + ')'
        exec execStr2

        epsi = 1e-10
        print res1-res2
        if (abs(res1-res2) > epsi):
            return False

    return  True

#输入一个分式。返回一个分式的随机拆分
def get_random_denominator(f):
    if(not is_simple(f.numerator())):
        return f
    length = f.numerator().number_of_operands()
    return denominator(f,get_random_list(length))

#输入一个0-（length-1）的数组，返回一个该数组的随机拆分
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

#根据list来随机拆分分式f
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

#主函数
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

#判断是否是分式，是分式就对分式进行拆分后再变形
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

#对一个非分式进行变形
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

#随机选择变换规则
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

#三角函数变换
def random_expand_trig(f):
    randid_trig = random.randint(0,1)
    if(randid_trig == 0):
        f = f.expand_trig()
    elif(randid_trig == 1):
        f = f.expand_trig(full = true)
    return f

#horner形式变换
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

#分子分母乘同一个因式
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

#随机选择一个变量
def get_random_variable(f):
    variables = f.variables()
    randid = random.randint(0,len(variables)-1)
    return variables[randid]

#将一个列表随机拆分成两个列表
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

#判断是一个符号还是表达式
def is_expression(f):
    var('test_variable_a')
    if(f.operator()==test_variable_a.operator()):
        return False
    return True

#判断一个表达式优先级最低的符号是不是+或者-
def is_simple(f):
    var('test_variable_a,test_variable_b')
    if(f.operator()==(test_variable_a+test_variable_b).operator()):
        return True
    return False

#判断一个表达式是不是分式
def is_fraction(f):
    var('test_variable_a,test_variable_b')
    if(f.operator()==(test_variable_a/test_variable_b).operator()):
        return True
    return False

# 
def accumulationTransform(expr):
    expr = expr.expand()
    return expr

# Horner form transformation
def hornerTransform(v, e):
    v = var(v)
    exec 'expr = ' + e
    return str(expr.horner(x))

# 判断一个表达式在给定区间是否稳定
def isStable(expr, interval):
    return True

# 生成等价计算语句, stmt可以是一个赋值语句或者是一个由loopid所表示的循环
def generateEqualStmt(data, stmt):
    # loop
    if (stmt[0] == '{' and stmt[-1] == '}'):
        return generateEqualLoop(data, stmt[1:-1])
    # assignment
    elif ('=' in stmt):
        # TODO
        return [stmt]
    return []

# 生成等价计算路径
def generateEqualPath(data, path):

    statements = path.split(';')
    estatements = [generateEqualStmt(data, stmt) for stmt in statements]

    epaths = ['']
    for i in range(len(statements)):
        t = []
        for estatement in estatements[i]:
            for j in range(len(epaths)):
                t.append(epaths[j] + estatement + ';')
        epaths = t
    return epaths


# 生成等价循环
LOOPID = 0
def generateEqualLoop(data, loopid):

    global LOOPID
    
    # 规则1，针对类似于for(i=0;i<n;++i)这样的循环制定转化规则

    eloops = []
    eloops.append('{'+loopid+'}')

    loop = data['loops'][loopid]

    # 单循环变量
    if (len(loop['variables']) == 1):
        # 循环体中仅两条路径
        if (len(loop['loopBody']) == 2):
            # 两条路径约束互补
            if (('!('+loop['loopBody'][0]['constrain']+')') == (loop['loopBody'][1]['constrain'])):
                # 一条路径为循环体，另一条为循环退出条件 
                if (loop['loopBody'][0]['break'] == 'false' and loop['loopBody'][1]['break'] == 'true'):
                    # 循环体中变量更新方法为+1
                    variable = loop['variables'][0]
                    for p in loop['loopBody'][0]['path']:
                        if (p[0] == variable):
                            update = p[1]
                    if (update == (variable+'+1')):
                        # 判断其他变量是否为累加、累乘的更新形式 
                        canTransform = True
                        for update in loop['loopBody'][0]['path']:
                            updateVar = update[0]
                            updateExpr = update[1]
                            if (not updateExpr.startswith(updateVar)):
                                canTransform = False
                                break
                            if (updateExpr[len(updateVar)] not in "+-*/"):
                                canTransform = False
                                break
                            if (updateVar in updateExpr[len(updateVar):]):
                                canTransform = False
                                break
                        if (canTransform):
                            newLoop = dict(loop) 
                            vstart = loop['initialize'][0][1]
                            vend = loop['loopBody'][0]['constrain'].split('<')[1]
                            newLoop['initialize'][0][1] = vend + '-1'
                            newLoop['loopBody'][0]['constrain'] = loop['variables'][0] + '>=' + vstart
                            newLoop['loopBody'][1]['constrain'] = '!(' + loop['variables'][0] + '>=' + vstart + ')'
                            for update in newLoop['loopBody'][0]['path']:
                                if (update[0] == newLoop['variables'][0]):
                                    update[1] = update[0] + '-1'
                                    break

                            newLoopId = 'eloop' + str(LOOPID)
                            LOOPID += 1
                            data['loops'][newLoopId] = newLoop
                            eloops.append('{'+newLoopId+'}')

    return eloops

                            

#variables = ['ar', 'ai', 'br', 'bi']
'''
variables = ['a', 'b', 'c', 'd']
variables2 = ['s', 't', 'a', 'b']
path1 = "(a/sqrt(a*a+b*b)+c/sqrt(c*c+d*d))/sqrt(2+2*(a*c+b*d)/sqrt((a*a+b*b)*(c*c+d*d)))"
path2 = convertPath(path1, variables, variables2) 
print path1
print path2

'''

with open('../case/loop/loop.pth') as f:
    data = json.load(f)

path = data['paths'][0]
print (generateEqualPath(data, path))
print (data)



