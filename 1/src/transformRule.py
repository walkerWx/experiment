#!/usr/bin/env sage
# -*- coding: utf-8 -*-

import codecs
import random
import copy

from sympy import *
from sympy.parsing.sympy_parser import *

from expr_parser.parseTree import *
from expr_parser.exprParser import exprParser
from expr_parser.exprLexer import exprLexer


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
def apply_rule(expr_str, rule):

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


rules = load_rules()
rules_dict = dict()
for rule in rules:
    '''
    print ('name:' + rule.rule_name)
    print ('origin:' + rule.origin_parse_tree.getText())
    print ('transformed:' + rule.transformed_parse_tree.getText())
    if rule.constrain_parse_tree:
        print ('constrain:' + rule.constrain_parse_tree.getText())
    '''
    rules_dict[rule.rule_name] = rule

rules = list()
rules.append(rules_dict['PolarRepresentation'])
#rules.append(rules_dict['FracReduction'])
rules.append(rules_dict['CommutationMultiply'])
rules.append(rules_dict['Midarc'])
#rules.append(rules_dict['Distribution3'])

rules.append(SympyRule('Simplify'))
#rules.append(SympyRule('Expand'))

expr_str = '((A1+B1*I)/sqrt(A1^2+B1^2)+(A2+B2*I)/sqrt(A2^2+B2^2))/abs((A1+B1*I)/sqrt(A1^2+B1^2)+(A2+B2*I)/sqrt(A2^2+B2^2)))'

expr_set = {expr_str}


for i in range(500):
    rule = random.choice(rules)
    expr = random.sample(expr_set, 1)[0]
    transformed_expr = apply_rule(expr_str, rule)
    if transformed_expr:
        expr_str = transformed_expr
        print(rule.rule_name)
        print(transformed_expr)
        expr_set.add(transformed_expr.replace(' ', ''))
        print('')

for e in expr_set:
    print(e)
