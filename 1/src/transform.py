
import random
import codecs
import copy
import antlr4

from rule import TransformRule, SympyRule, RULES

from expr import *
from expr_parser.exprParser import exprParser
from expr_parser.exprLexer import exprLexer

from sympy import *
from sympy.parsing.sympy_parser import *

from expr import *

'''
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
'''


# 根据表达式字符串构建表达式的解析树
def build_parse_tree(expr_str):
    data = codecs.decode(bytes(expr_str, 'utf-8'), 'ascii', 'strict')
    input = antlr4.InputStream(data)
    lexer = exprLexer(input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = exprParser(stream)
    return ParseTree(parser.expression())


# 在表达式的解析树节点上运用规则，返回应用规则后的解析树节点
def apply_rule_node(node, rule):

    if isinstance(rule, SympyRule):

        str_expr = node.getText()
        transformations = standard_transformations + (convert_xor, )
        sympy_expr = parse_expr(str_expr, transformations=transformations)

        if rule.rule_name == 'Simplify':
            str_expr = str(simplify(sympy_expr))
        if rule.rule_name == 'Expand':
            str_expr = str(expand(sympy_expr))
        if rule.rule_name == 'Horner':
            str_expr = str(horner(sympy_expr))
        if rule.rule_name == 'Taylor':
            str_expr = str(series(sympy_expr))
            # sympy泰勒展开式会附带大O标记，这里要做一次字符串处理
            Opos = str_expr.rfind('O')
            if Opos > 0:
                str_expr = str_expr[:Opos-2]
                print(str_expr)

        parse_tree = build_parse_tree(str_expr)
        return parse_tree.root

    if isinstance(rule, TransformRule):

        candidate_nodes = find_matched_nodes(rule.origin_parse_tree.root, node)

        if not candidate_nodes:
            return node

        # 采取随机的策略，在所有匹配的节点中随机选取一个节点，做对应的转换操作
        chosen_node = random.choice(candidate_nodes)

        # 下面首先要找到转换规则中变量在表达式解析树中对应的节点，方法是对两个树结构平行的做DFS
        rule_stack = [rule.origin_parse_tree.root]
        expr_stack = [chosen_node]

        # 节点对应关系的字典
        rule2expr = dict()
        while rule_stack:
            rule_node = rule_stack.pop()
            expr_node = expr_stack.pop()
            if isinstance(rule_node, VariableNode):
                rule2expr[rule_node.getText()] = expr_node
                continue
            rule_stack.extend(rule_node.children)
            expr_stack.extend(expr_node.children)

        # 生成转换后的节点
        transformed_node = copy.deepcopy(rule.transformed_parse_tree.root)
        rule_stack = [transformed_node]
        while rule_stack:
            rule_node = rule_stack.pop()
            for i in range(len(rule_node.children)):
                if isinstance(rule_node.children[i], VariableNode) and rule_node.children[i].getText() in rule2expr:
                    rule_node.children[i] = rule2expr[rule_node.children[i].getText()]
                else:
                    rule_stack.append(rule_node.children[i])

        # 在转换后节点的最顶端做一次simplify操作，去掉一些多余的括号
        for i in range(len(transformed_node.children)):
            transformed_node.children[i] = apply_rule_node(transformed_node.children[i], RULES['Simplify'])


        # 在原计算式中做对应的替换
        if node == chosen_node:
            return transformed_node
        else:
            expr_stack = [node]
            while expr_stack:
                expr_node = expr_stack.pop()
                for i in range(len(expr_node.children)):
                    if expr_node.children[i] == chosen_node:
                        expr_node.children[i] = transformed_node
                    else:
                        expr_stack.append(expr_node.children[i])
        return node


# 在表达式上使用规则进行等价转换，返回一个新的表达式
def apply_rule_expr(expr_str, rule):

    if isinstance(rule, TransformRule):

        expr_parse_tree = build_parse_tree(expr_str)

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
        return expr


def find_matched_nodes(rule_node, expr_node):
    '''

    在expr_node对应的树结构中匹配rule_node的形式，返回所有匹配中的节点，用 DFS + 递归 实现

    :param rule_node:
    :param expr_node:
    :return:

    '''

    matched_nodes = list()

    s = [expr_node]
    while s:
        n = s.pop()
        if match(rule_node, n):
            matched_nodes.append(n)
        s.extend(n.children)

    return matched_nodes


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


# 使用给定的规则生成等价表达式集合
def generate_equivalent_expressions(expr, rules):

    expr_set = {expr}

    # 以 rule@expr 为关键字存储待的规则与表达式，每次随机选取一个进行等价变换，形成新的表达式后与规则列表作笛卡尔乘积然后加入进去

    rule_expr_set = set()
    for rule in rules:
        rule_expr_set.add(rule.rule_name+'@'+expr)

    i = 0
    while rule_expr_set and i <= 200:
        i += 1
        rule_expr = random.sample(rule_expr_set, 1)[0]
        rule_expr_set.remove(rule_expr)
        rule_name, expr = rule_expr.split('@')
        parse_tree = build_parse_tree(expr)
        transformed_expr = apply_rule_node(parse_tree.root, RULES[rule_name]).getText()
        if transformed_expr and transformed_expr not in expr_set:
            print('# Apply rule [ %s ] tranform [ %s ] -> [ %s ]' % (rule_name, expr, transformed_expr))
            for rule in rules:
                rule_expr_set.add(rule.rule_name+'@'+transformed_expr)
            expr_set.add(transformed_expr)

    print("------------------- Remaining Todo ---------------------")
    rule_expr_set= list(rule_expr_set)
    rule_expr_set.sort(key=len)
    for re in rule_expr_set:
        print(re)

    return expr_set

