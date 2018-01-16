from .exprParser import *


class ParseTreeNode(object):

    def __init__(self):
        self.children = []
        return

    def getText(self):
        return ''


class OperatorNode(ParseTreeNode):

    def __init__(self, operator, children):
        self.operator = operator
        self.children = children

    def getText(self):

        if len(self.children) < 2:
            return

        return self.children[0].getText() + self.operator + self.children[1].getText()


class VariableNode(ParseTreeNode):

    def __init__(self, variable):
        self.variable = variable
        self.children = []

    def getText(self):
        return self.variable


class FunctionNode(ParseTreeNode):

    def __init__(self, funcname, children):
        self.funcname = funcname
        self.children = children

    def getText(self):
        return self.funcname + '(' + ','.join([x.getText() for x in self.children]) + ')'


class AtomNode(ParseTreeNode):

    def __init__(self, children):
        self.children = children

    def getText(self):
        return ''.join([x.getText() for x in self.children])


class SymbolNode(ParseTreeNode):

    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def getText(self):
        return self.symbol


class ParseTree:

    def __init__(self, tree):

        self.root = self.build(tree)

        '''
        Create a self defined parser tree according to ANTLR parser tree
        :param tree: ANTLR parser tree
        '''

    def build(self, node):

        if isinstance(node, exprParser.VariableContext):
            return VariableNode(node.getChild(0).getText())

        if isinstance(node, exprParser.FuncContext):
            funcname = node.getChild(0).getText()
            children = list()
            for i in range(2, node.getChildCount(), 2):
                children.append(self.build(node.getChild(i)))
            return FunctionNode(funcname, children)

        if isinstance(node, exprParser.ExpressionContext) or isinstance(node, exprParser.MultiplyingExpressionContext) or isinstance(node, exprParser.EquationContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 3:
                operator = node.getChild(1).getText()
                children = list()
                children.append(self.build(node.getChild(0)))
                children.append(self.build(node.getChild(2)))
                return OperatorNode(operator, children)

        if isinstance(node, exprParser.PowExpressionContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 3:
                operator = node.getChild(1).getText()
                children = list()
                children.append(self.build(node.getChild(0)))
                children.append(self.build(node.getChild(2)))
                return OperatorNode(operator, children)

        if isinstance(node, exprParser.SignedAtomContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 2:
                children = list()
                children.append(SymbolNode(node.getChild(0).getText()))
                children.append(self.build(node.getChild(1)))
                return AtomNode(children)

        if isinstance(node, exprParser.AtomContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 3:
                children = list()
                children.append(SymbolNode(node.getChild(0).getText()))
                children.append(self.build(node.getChild(1)))
                children.append(SymbolNode(node.getChild(2).getText()))
                return AtomNode(children)

        if isinstance(node, exprParser.ScientificContext) or isinstance(node, exprParser.ConstantContext):
            if node.getChildCount() == 1:
                return SymbolNode(node.getChild(0).getText())

        return None

    def getText(self):
        return self.root.getText()


