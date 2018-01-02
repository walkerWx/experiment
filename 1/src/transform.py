#!/usr/bin/env sage
# -*- coding: utf-8 -*-

from sage.all import *
from path import *
from config import *

import json
import random
import itertools
from copy import deepcopy
from copy import copy

var('a b c d e f g h i j k l m n o p q r s t u v w x y z')

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


# 生成等价过程模块
def generate_equal_procedure(path_data, procedure):

    equal_procedures = list()

    for v in path_data.get_all_variables():
        var(v)

    # Horner规则
    ep = deepcopy(procedure)
    ep.set_id(ep.get_id() + '_HORNER')  # 设置新id

    for i in range(len(procedure.get_procedure())):
        variable = procedure.get_procedure()[i][0]
        update_expr = procedure.get_procedure()[i][1]
        expr = update_expr
        for v in path_data.get_all_variables():

            # 表达式字符串中指数标记为 '^' 会报错，需替换为'**'
            expr = str(expr)
            if '^' in expr:
                expr = expr.replace('^', '**')

            exec 'expr = ' + expr
            if isinstance(expr, Expression):
                exec 'expr = str(expr.horner('+ v + '))'
        ep.set_update_expr(variable, expr)

    path_data.add_procedure(ep)         # 记得将新产生的procedure加入到path_data
    equal_procedures.append(ep)

    # 规则列表匹配规则
    ep = deepcopy(procedure)

    origin_vars = path_data.get_input_variables()
    for i in range(len(procedure.get_procedure())):

        # 这个procedure中被更新的变量
        updated_var = procedure.get_procedure()[i][0]

        # 更新表达式
        update_expr = procedure.get_procedure()[i][1]

        # 规则列表中去匹配是否为等价表达式，若发现匹配到了便转换
        for j in range(len(rules)):
            rule = rules[j]
            if is_expr_equal(origin_vars, update_expr, rule['variables'], rule['origin_expr']):
                update_expr = convert_expr(rule['equal_expr'], rule['variables'], origin_vars)
                ep = deepcopy(ep)
                ep.set_id(ep.get_id() + '_RULE_' + rule['name'])  # 设置新id
                ep.set_update_expr(updated_var, update_expr)
                equal_procedures.append(ep)
                # 记得将生成的等价procedure加入到path_data中
                path_data.add_procedure(ep)

    return equal_procedures


# 生成等价循环模块
def generate_equal_loop(path_data, loop):

    equal_loops = list()

    # 累加累乘规则，针对类似于for(i=0;i<n;++i)这样的循环判定是否为累加或者累乘，然后逆序操作

    # 单循环变量
    if len(loop.get_variables()) == 1:
        # 循环体中仅两条路径
        if len(loop.get_loop_body()) == 2:
            p1 = loop.get_loop_body()[0]
            p2 = loop.get_loop_body()[1]

            # 两条路径约束互补
            if ('!('+p1.get_constrain()+')' == p2.get_constrain()) or (p1.get_constrain() == '!('+p2.get_constrain()+')'):
                # 循环体中临时变量更新方法为+1
                tv = loop.get_variables()[0]
                loop_body_path = p1 if len(p1.get_path_list()) == 1 else p2
                if len(loop_body_path.get_path_list()) == 1:
                    loop_body_procedure = loop_body_path.get_path_list()[0]
                    if loop_body_procedure.get_update_expr(tv) == tv+'+1':
                        print("+1")
                        # 判断其他变量是否为累加、累乘的更新形式
                        can_transform = True

                        for i in range(len(loop_body_procedure.get_procedure())):
                            v = loop_body_procedure.get_procedure()[i][0]
                            e = loop_body_procedure.get_procedure()[i][1]

                            if not e.startswith(v):
                                can_transform = False
                                break
                            if e[len(v)] not in "+*":
                                can_transform = False
                                break
                            if v in e[len(v):]:
                                can_transform = False
                                break

                        if can_transform:
                            el = deepcopy(loop)
                            el.set_id(el.get_id() + '_REVERSE')
                            vstart =  el.get_initialize_expr(tv)
                            vend = loop_body_path.get_constrain().split('<')[1]

                            el.set_initialize_expr(tv, vend+'-1')

                            p1 = el.get_loop_body()[0]
                            p2 = el.get_loop_body()[1]
                            loop_body_path = p1 if len(p1.get_path_list()) == 1 else p2
                            loop_body_path.set_constrain(tv+'>='+vstart)
                            loop_body_procedure = loop_body_path.get_path_list()[0]
                            loop_body_procedure.set_id(loop_body_procedure.get_id()+'_SUM')
                            loop_body_procedure.set_update_expr(tv, tv+'-1')
                            path_data.add_procedure(loop_body_procedure)

                            loop_body_path = p1 if len(p1.get_path_list()) == 0 else p2
                            loop_body_path.set_constrain("!("+tv+">="+vstart+")")
                            equal_loops.append(el)
                            path_data.add_loop(el)

    return equal_loops


# 尝试将两个循环进行规约，成功则返回规约后的结果(一个Loop或者Procedure)，否则返回None
def reduce_loop(l1, l2):

    # 两个循环能够规约的必要条件是循环结构相同
    if l1.get_variables() != l2.get_variables():
        return None

    l1_loop_body = l1.get_loop_body()
    l2_loop_body = l2.get_loop_body()
    if len(l1_loop_body) != len(l2_loop_body):
        return None

    for i in range(len(l1_loop_body)):
        if l1_loop_body[i].get_constrain() != l2_loop_body[i].get_constrain():
            return None
        if l1_loop_body[i].get_constrain() != l2_loop_body[i].get_constrain():
            return None

    l1_path_list = list()
    l2_path_list = list()
    for i in range(len(l1_loop_body)):
        l1_path_list = l1_loop_body[i].get_path_list()
        if l1_path_list:
            break

    for i in range(len(l2_loop_body)):
        l2_path_list = l2_loop_body[i].get_path_list()
        if l2_path_list:
            break

    if len(l1_path_list) > 1 or len(l2_path_list) > 1:
        return None

    l1_procedure = l1_path_list[0].get_procedure()
    l2_procedure = l2_path_list[0].get_procedure()

    # 去掉循环临时变量
    l1_procedure = [x for x in l1_procedure if x[0] not in l1.get_variables()]
    l2_procedure = [x for x in l2_procedure if x[0] not in l2.get_variables()]

    variables = list(set([x[0] for x in l1_procedure + l2_procedure]))

    init_values = ['init_'+x for x in variables]

    exec_stmts = list()
    exec_stmts.append("var('" + ' '.join(init_values) + "')")
    exec_stmts += [x+'=init_'+x for x in variables]
    exec_stmts += [x[0]+'='+x[1] for x in l1_procedure+l2_procedure]

    print (variables)

    for x in exec_stmts:
        exec x

    exec_res = [[x, str(eval(str(x)))] for x in variables]
    exec_res = [x for x in exec_res if str('init_'+x[0]) != x[1]]

    if len(exec_res) == 0:
        # 循环相当于啥都没做，返回一个空的Procedure
        p = Procedure('empty_procedure', [])
        return p
    elif len(exec_res) == 1 and exec_res[0][1] in init_values:
        # 循环在对一个变量不停的赋值，循环n次的效果与一次赋值相同
        p = Procedure('REDUCE_'+l1.get_id()+'_'+l2.get_id(), [[exec_res[0][0], exec_res[0][1][5:]]])
        return p

    return None


# 生成等价路径
def generate_equal_path(path_data, path):

    equal_paths = list()

    # 循环规约规则，连续的两个相互为逆过程的循环可规约
    path_list = deepcopy(path.get_path_list())
    i = 0
    while i+1 < len(path_list):
        if isinstance(path_list[i], Loop) and isinstance(path_list[i+1], Loop):
            reduce_res = reduce_loop(path_list[i], path_list[i+1])
            if reduce_res:
                del path_list[i:i+2]
                path_list.insert(i, reduce_res)
        i += 1

    ep = deepcopy(path)
    ep.set_path_list(path_list)
    print ('reduce generate path')
    print (ep.to_json())
    equal_paths.append(ep)

    # gamma近似规则
    path_list = deepcopy(path.get_path_list())
    if len(path_list) == 1 and isinstance(path_list[0], Procedure) and len(path_list[0].get_procedure()) == 1:
        update_var = path_list[0].get_procedure()[0][0]
        update_expr = path_list[0].get_procedure()[0][1]
        if update_expr.startswith('gamma(') and update_expr.endswith(')'):
            gamma_input = update_expr[6:-1]
            ep = deepcopy(path)
            ep.add_constrain('abs(('+gamma_input+')+2)<1e-5')
            gamma_procedure = Procedure(path_list[0].get_id()+'_GAMMA_APPROX', [[update_var, generate_gamma_approx_expr(gamma_input)]])
            path_data.add_procedure(gamma_procedure)
            ep.set_path_list([gamma_procedure])
            ep.set_implement(REALTYPE)
            equal_paths.append(ep)

    # 生成等价的Loop以及Procedure后排列组合成新的path
    equal_list = list()
    for t in path.get_path_list():
        if isinstance(t, Procedure):
            equal_list.append(generate_equal_procedure(path_data, t))
        elif isinstance(t, Loop):
            equal_list.append(generate_equal_loop(path_data, t))

    print('product generate path')
    for t in [list(x) for x in itertools.product(*equal_list)]:
        ep = deepcopy(path)
        ep.set_path_list(t)
        print (ep.to_json())
        equal_paths.append(ep)

    return equal_paths


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
