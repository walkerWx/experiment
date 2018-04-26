#!/usr/bin/env sage
# -*- coding: utf-8 -*-

import antlr4

import expr

from expr_parser.exprParser import exprParser
from expr_parser.exprLexer import exprLexer


class TransformRule:

    def __init__(self, rule_name, origin_parse_tree, transformed_parse_tree, constrain_parse_tree=None):
        self.rule_name = rule_name
        self.origin_parse_tree = origin_parse_tree
        self.transformed_parse_tree = transformed_parse_tree
        self.constrain_parse_tree = constrain_parse_tree


class SympyRule:

    def __init__(self, rule_name):
        self.rule_name = rule_name


def initialize_transform_rules():

    # 文件中的自定义转换规则
    rule_file = './rule.txt'

    input = antlr4.FileStream(rule_file)
    lexer = exprLexer(input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.rules()

    rules = list()
    for single_rule in tree.getChildren():
        rule_name = single_rule.getChild(0).getText()
        origin_parse_tree = expr.ParseTree(single_rule.getChild(2))
        transformed_parse_tree = expr.ParseTree(single_rule.getChild(4))
        if single_rule.getChildCount() == 8:
            constrain_parse_tree = expr.ParseTree(single_rule.getChild(6))
        else:
            constrain_parse_tree = None
        rules.append(TransformRule(rule_name, origin_parse_tree, transformed_parse_tree, constrain_parse_tree))

    return rules


def initialize_sympy_rules():
    return {SympyRule('Simplify'), SympyRule('Expand'), SympyRule('Horner'), SympyRule('Taylor')}


TRANSFORM_RULES = initialize_transform_rules()
SYMPY_RULES = initialize_sympy_rules()

RULES = dict()
for r in TRANSFORM_RULES:
    RULES[r.rule_name] = r
for r in SYMPY_RULES:
    RULES[r.rule_name] = r


