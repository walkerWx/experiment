#!/usr/bin/env sage
# -*- coding: utf-8 -*-

import codecs
import random
import copy
import itertools

from sympy import *
from sympy.parsing.sympy_parser import *

from expr_parser.parseTree import *
from expr_parser.exprParser import exprParser
from expr_parser.exprLexer import exprLexer

from path import Procedure, Loop


class TransformationRule:

    def __init__(self, rule_name, origin_parse_tree, transformed_parse_tree, constrain_parse_tree=None):
        self.rule_name = rule_name
        self.origin_parse_tree = origin_parse_tree
        self.transformed_parse_tree = transformed_parse_tree
        self.constrain_parse_tree = constrain_parse_tree


class SympyRule:

    def __init__(self, rule_name):
        self.rule_name = rule_name


# 在路径上使用规则进行等价转换
def apply_rule_path(path, rule):

    # 在Path中随机选取一个表达式，使用规则对其进行等价变换并返回

    random_procedure = random.choice(path.get_path_list())

    while not isinstance(random_procedure, Procedure):

        if not isinstance(random_procedure, Loop):
            raise TypeError
        random_procedure = random.choice(random_procedure.get_loop_body())  # 在循环体中随机选取一条路径
        random_procedure = random.choice(random_procedure.get_path_list())  # 路径中递归地随机选

    return None


# 在表达式上使用规则进行等价转换
def apply_rule_expr(expr_str, rule):

    if isinstance(rule, TransformationRule):
        data = codecs.decode(bytes(expr_str, 'utf-8'), 'ascii', 'strict')
        input = InputStream(data)
        lexer = exprLexer(input)
        stream = CommonTokenStream(lexer)
        parser = exprParser(stream)

        expr_parse_tree = ParseTree(parser.expression())

        '''
        dfs(rule.origin_parse_tree.root)
        print('')
        dfs(expr_parse_tree.root)
        '''

        candidates = find_match(rule.origin_parse_tree, expr_parse_tree)
        if not candidates:
            return None

        candidate = random.choice(candidates)

        s_rule = [rule.origin_parse_tree.root]
        s_expr = [candidate]

        # 找到匹配规则中变量所对应的节点
        m = dict()
        while s_rule:
            n_rule = s_rule.pop()
            n_expr = s_expr.pop()
            if isinstance(n_rule, VariableNode):
                m[n_rule.getText()] = n_expr
                continue
            s_rule.extend(n_rule.children)
            s_expr.extend(n_expr.children)

        # 生成转换后的节点
        transformed_node = copy.deepcopy(rule.transformed_parse_tree.root)
        s_rule = [transformed_node]
        while s_rule:
            n_rule = s_rule.pop()
            for i in range(len(n_rule.children)):
                if isinstance(n_rule.children[i], VariableNode) and n_rule.children[i].getText() in m:
                    n_rule.children[i] = m[n_rule.children[i].getText()]
                else:
                    s_rule.append(n_rule.children[i])

        # 在原计算式中做对应的替换
        if expr_parse_tree.root == candidate:
            expr_parse_tree.root = transformed_node
        else:
            s_expr = [expr_parse_tree.root]
            while s_expr:
                n_expr = s_expr.pop()
                for i in range(len(n_expr.children)):
                    if n_expr.children[i] == candidate:
                        n_expr.children[i] = transformed_node
                    else:
                        s_expr.append(n_expr.children[i])

        return expr_parse_tree.getText()

    if isinstance(rule, SympyRule):

        transformations = standard_transformations + (convert_xor, )
        expr = parse_expr(expr_str, transformations=transformations)

        if rule.rule_name == 'Simplify':
            expr = str(simplify(expr))

        if rule.rule_name == 'Expand':
            expr = str(expand(expr))

        if rule.rule_name == 'Horner':
            expr = str(horner(expr))

        expr = expr.replace('**', '^')
        return expr


def find_match(origin_parse_tree, expr_parse_tree):
    '''
    :param origin_parse_tree: 等价转换规则原计算形式对应的解析树
    :param expr_parse_tree: 欲进行转换的表达式对应的解析树
    :return: 返回表达式解析树中的与原计算形式相同的子树节点
    '''

    matched_nodes = list()

    s = [expr_parse_tree.root]
    while s:
        n = s.pop()
        if match(origin_parse_tree.root, n):
            matched_nodes.append(n)
        s.extend(n.children)

    return matched_nodes


def match(rule_tree_node, expr_tree_node):
    '''
    判断两棵解析树是否match
    :param rule_tree_node:
    :param expr_tree_node:
    :return:
    '''
    vdict = dict()
    return match_recursive(rule_tree_node, expr_tree_node, vdict)


def match_recursive(rule_tree_node, expr_tree_node, vdict):

    if isinstance(rule_tree_node, OperatorNode):
        if not isinstance(expr_tree_node, OperatorNode):
            return False
        if not rule_tree_node.operator == expr_tree_node.operator:
            return False
        if not len(rule_tree_node.children) == len(expr_tree_node.children):
            return False
        return all(match_recursive(rule_tree_node.children[i], expr_tree_node.children[i], vdict) for i in range(len(rule_tree_node.children)))

    if isinstance(rule_tree_node, VariableNode):
        if rule_tree_node.getText() in vdict and vdict[rule_tree_node.getText()] != expr_tree_node.getText():
            return False
        vdict[rule_tree_node.getText()] = expr_tree_node.getText()
        return True

    if isinstance(rule_tree_node, FunctionNode):
        if not isinstance(expr_tree_node, FunctionNode):
            return False
        if not rule_tree_node.funcname == expr_tree_node.funcname:
            return False
        if not len(rule_tree_node.children) == len(expr_tree_node.children):
            return False
        return all(match_recursive(rule_tree_node.children[i], expr_tree_node.children[i], vdict) for i in range(len(rule_tree_node.children)))

    if isinstance(rule_tree_node, AtomNode):
        if not isinstance(expr_tree_node, AtomNode):
            return False
        if not len(rule_tree_node.children) == len(expr_tree_node.children):
            return False
        return all(match_recursive(rule_tree_node.children[i], expr_tree_node.children[i], vdict) for i in range(len(rule_tree_node.children)))

    if isinstance(rule_tree_node, SymbolNode):
        if not isinstance(expr_tree_node, SymbolNode):
            return False
        if not rule_tree_node.symbol == expr_tree_node.symbol:
            return False
        return True


def load_rules():

    # 文件中的自定义转换规则
    rule_file = './expr_parser/rules.txt'

    input = FileStream(rule_file)
    lexer = exprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.rules()

    rules = list()
    for single_rule in tree.getChildren():
        rule_name = single_rule.getChild(0).getText()
        origin_parse_tree = ParseTree(single_rule.getChild(2))
        transformed_parse_tree = ParseTree(single_rule.getChild(4))
        if single_rule.getChildCount() == 8:
            constrain_parse_tree = ParseTree(single_rule.getChild(6))
        else:
            constrain_parse_tree = None
        rules.append(TransformationRule(rule_name, origin_parse_tree, transformed_parse_tree, constrain_parse_tree))

    return rules


def simplify_expr(expr_str):

    transformations = standard_transformations + (convert_xor, )
    expr = parse_expr(expr_str, transformations=transformations)
    expr = str(simplify(expr))
    expr = expr.replace('**', '^')
    return expr


'''
# 生成等价过程模块
def generate_equal_procedure(path_data, procedure):

    equal_procedures = list()

    for v in path_data.get_all_variables():
        var(v)

    # Horner规则
    ep = copy.deepcopy(procedure)
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
    ep = copy.deepcopy(procedure)

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
                ep = copy.deepcopy(ep)
                ep.set_id(ep.get_id() + '_RULE_' + rule['name'])  # 设置新id
                ep.set_update_expr(updated_var, update_expr)
                equal_procedures.append(ep)
                # 记得将生成的等价procedure加入到path_data中
                path_data.add_procedure(ep)

    return equal_procedures
'''


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
                            el = copy.deepcopy(loop)
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
        exec(x)

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
    path_list = copy.deepcopy(path.get_path_list())
    i = 0
    while i+1 < len(path_list):
        if isinstance(path_list[i], Loop) and isinstance(path_list[i+1], Loop):
            reduce_res = reduce_loop(path_list[i], path_list[i+1])
            if reduce_res:
                del path_list[i:i+2]
                path_list.insert(i, reduce_res)
        i += 1

    ep = copy.deepcopy(path)
    ep.set_path_list(path_list)
    print ('reduce generate path')
    print (ep.to_json())
    equal_paths.append(ep)

    # gamma近似规则
    path_list = copy.deepcopy(path.get_path_list())
    if len(path_list) == 1 and isinstance(path_list[0], Procedure) and len(path_list[0].get_procedure()) == 1:
        update_var = path_list[0].get_procedure()[0][0]
        update_expr = path_list[0].get_procedure()[0][1]
        if update_expr.startswith('gamma(') and update_expr.endswith(')'):
            gamma_input = update_expr[6:-1]
            ep = copy.deepcopy(path)
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
        ep = copy.deepcopy(path)
        ep.set_path_list(t)
        print (ep.to_json())
        equal_paths.append(ep)

    return equal_paths



# 使用给定的规则生成等价表达式集合
def generate_equivalent_expressions(expr, rules):

    expr_set = {expr}
    for i in range(200):
        rule = random.choice(rules)  #随机选取转换规则
        expr = random.sample(expr_set, 1)[0]  #随机选已经生成的等价表达式
        transformed_expr = apply_rule_expr(expr, rule)
        if transformed_expr:
            print('# Apply rule [ %s ] tranform [ %s ] -> [ %s ]' % (rule.rule_name, expr, transformed_expr))
            expr_set.add(transformed_expr.replace(' ', ''))

    return expr_set


'''
# 从规则文件中加载规则
rules = load_rules()
rules_dict = dict()
for rule in rules:
    print('name:' + rule.rule_name)
    print('origin:' + rule.origin_parse_tree.getText())
    print('transformed:' + rule.transformed_parse_tree.getText())
    if rule.constrain_parse_tree:
        print('constrain:' + rule.constrain_parse_tree.getText())
    rules_dict[rule.rule_name] = rule

rules_dict['Simplify'] = SympyRule('Simplify')
rules_dict['Horner'] = SympyRule('Horner')

rules = list()

rules.append(rules_dict['LnDivide'])
rules.append(rules_dict['Simplify'])
rules.append(rules_dict['CommutationPlus'])

rules.append(rules_dict['TaylorLnPlusReverse'])
rules.append(rules_dict['TaylorLnMinusReverse'])

rules.append(rules_dict['Simplify'])

rules.append(rules_dict['FracPartial'])
rules.append(rules_dict['TaylorExp'])

cos2_expr = 'exp(x)/(exp(x)-1)'

expr_set = generate_equivalent_expressions(cos2_expr, rules)
print(len(expr_set))
for e in expr_set:
    print(e)


'''
