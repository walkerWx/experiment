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
        self.weight = 0


class SympyRule:

    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.weight = 0


class LoopRule:

    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.weight = 0


def initialize_transform_rules():

    # 文件中的自定义转换规则
    rule_file = './rule.txt'

    input = antlr4.FileStream(rule_file)
    lexer = exprLexer(input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.rules()

    rules = set()
    for single_rule in tree.getChildren():
        rule_name = single_rule.getChild(0).getText()
        origin_parse_tree = expr.ParseTree(single_rule.getChild(2))
        transformed_parse_tree = expr.ParseTree(single_rule.getChild(4))
        if single_rule.getChildCount() == 8:
            constrain_parse_tree = expr.ParseTree(single_rule.getChild(6))
        else:
            constrain_parse_tree = None
        rules.add(TransformRule(rule_name, origin_parse_tree, transformed_parse_tree, constrain_parse_tree))

    return rules


def initialize_sympy_rules():
    return {SympyRule('Simplify'), SympyRule('Expand'), SympyRule('Horner'), SympyRule('Taylor')}


def initialize_loop_rules():
    return {LoopRule('LoopReduce'), LoopRule('LoopReverse')}


# 所有转换规则的权重，在应用规则进行等价转换时根据按权重选取规则
rule_weight = {
    'Negative': 1,
    'Minus1': 1,
    'Minus2': 1,
    'Minus3': 1,
    'Divide': 1,
    'LogDivide': 1,
    'LogMinus': 1,
    'LogDivideReverse': 1,
    'CommutationPlus': 1,
    'CommutationPlus1': 1,
    'CommutationMultiply': 1,
    'AssociationPlus': 1,
    'AssociationMultiply': 1,
    'Distribution1': 1,
    'Distribution2': 1,
    'Distribution3': 1,
    'CommDenominator': 1,
    'CommDenominator1': 1,
    'CommDenominator2': 1,
    'FracReduction': 1,
    'FracPartial': 1,
    'NumeratorForm': 1,
    'NumeratorFrom1': 1,
    'NumeratorFrom2': 1,
    'NumeratorFrom3': 3,
    'DenominatorForm': 1,
    'Tan': 1,
    'Sec': 1,
    'Csc': 1,
    'Cot': 1,
    'SinPlus': 1,
    'SinMinus': 1,
    'CosPlus': 1,
    'CosMinus': 1,
    'TanPlus': 1,
    'TanMinus': 1,
    'SinCos': 1,
    'CosSin': 1,
    'CosCos': 1,
    'SinSin': 1,
    'SinCosR': 1,
    'CosSinR': 1,
    'CosCosR': 1,
    'SinSinR': 1,
    'AtanMinus': 1,
    'ExpReduction': 10,
    'TaylorExp': 1,
    'TaylorLog': 1,
    'TaylorLn': 1,
    'TaylorLnPlusReverse': 1,
    'TaylorLnMinusReverse': 1,
    'TaylorLnDivide': 1,
    'TaylorSin': 1,
    'TaylorCos': 1,
    'TaylorTan': 1,
    'PolarRepresentation': 1,
    'ComplexSum1': 1,
    'ComplexSum2': 30,
    'StirlingGamma': 1,
    'GammaTrans': 1,
    'Gamma_0': 1,
    'Gamma_1': 1,
    'Gamma_2': 1,

    'Simplify': 10,
    'Expand': 1,
    'Horner': 1,
    'Taylor': 1,

    'LoopReduce': 1,
    'LoopReverse': 1,

}

RULES = dict()
for r in initialize_transform_rules() | initialize_sympy_rules() | initialize_loop_rules():
    r.weight = rule_weight[r.rule_name]
    RULES[r.rule_name] = r


