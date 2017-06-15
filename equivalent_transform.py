#!/home/walker/Projects/SageMath/sage -python
#encoding:utf-8

from sage.all import *
import math
import random
import sys

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

# Check whether two expressions are equal 
def is_expression_equal(expression1, varlist1, expression2, varlist2):

    if (len(varlist1) != len(varlist2)):
        return False

    var_num = len(varlist1)
    expression2 = expression2.subs(dict(zip(varlist2, varlist1)))

    if bool(expression1 == expression2):
        return True

    for i in range(10):
        random_input = []    
        for _ in range(var_num):
            random_input.append(random.uniform(-1,1))
        output1 = expression1.subs(dict(zip(varlist1, random_input))).n()
        output2 = expression2.subs(dict(zip(varlist1, random_input))).n()
        print random_input
        print output1
        print output2
        if (not isclose(output1, output2)):
            return False

    return True

def stability_analysis(var_list, expression_list, constrain):

    """ Given a list of equivalent expressions and a constrain, find stable interval of the expressions under the constrain.

    Args:
        var_list: variable list in the expression
        expression_list: equivalent expressions to analysis
        constain: constain
    
    Returns:
        List<expression, constrain>: <expression, constrain> pair list which guarantee the expression under the constrain is stable


    """

    # TODO: implenemt stablity analysis
    if (not expression_list):
        return [(None, constrain)]

    return [(expression_list[0], constrain)]

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
        #f = my_horner(f,random.randint(1,len(f.coefficients(variable,sparse = False))),variable)
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

'''
#horner形式变换
def my_horner(f,times,variable = x):
    coef = f.coefficients(x,sparse = False)
    no_horner_part = coef[0]
    length = len(coef)
    i = 1
    while(i+times<length):
        no_horner_part = no_horner_part + coef[i]*x^i
        i = i + 1
    f = (f - no_horner_part).horner(variable) + no_horner_part
    return f
'''

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


path_file = sys.argv[1]

with open(path_file, 'r') as f:

    path_num = int(f.readline())
    input_var_num = int(f.readline())
    input_var_list = f.readline().rstrip()
    ouput_var_num = int(f.readline())
    output_var_list = f.readline().rstrip()

    exec("var('" + input_var_list + "')")
    exec("var('" + output_var_list + "')")
    input_var_list = input_var_list.split()
    output_var_list = output_var_list.split()

    for i in range(0, path_num):
        for j in range(0, ouput_var_num):
            exec(f.readline().rstrip())
            print("exec:" + "transform(" + output_var_list[j] + ", 2)")
            exec("print transform(" + output_var_list[j] + ", 2)")
            


cr2 = -sgn(abs(atan2(ai,ar)-atan2(bi,br))-pi)*cos(0.5*(atan2(ai,ar)+atan2(bi,br)))
ci2 = -sgn(abs(atan2(ai,ar)-atan2(bi,br))-pi)*sin(0.5*(atan2(ai,ar)+atan2(bi,br)))

varlist1 = []
varlist1.append(ar)
varlist1.append(br)
varlist1.append(ai)
varlist1.append(bi)

##print is_expression_equal(ci, varlist1, ci2, varlist1)

ci = (ai+bi)/sqrt((ar+br)**2+(ai+bi)**2)



