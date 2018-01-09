import antlr4
import codecs
import random
from exprLexer import *
from exprParser import *

from parseTree import *

def main(argv):

    # expr_str = 'a*b/(c+d)*e*sin(a,b)+(a+b+c)'
    # print (trans_association(expr_str))

    expr_str = 'sin(a,b,c)+b+c+1.0'

    data = codecs.decode(expr_str, 'ascii', 'strict')
    input = InputStream(data)
    lexer = exprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.expression()

    pt = ParseTree(tree)
    print(pt.getText())


def dfs(node):
    print(type(node))
    if isinstance(node, antlr4.tree.Tree.TerminalNodeImpl):
        return
    for c in node.getChildren():
        dfs(c)


def trans_negative(expr_str):

    data = codecs.decode(expr_str, 'ascii', 'strict')
    input = InputStream(data)
    lexer = exprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.expression()

    candidate_nodes = []

    s = [tree]
    while s:
        n = s.pop()
        if isinstance(n, antlr4.tree.Tree.TerminalNodeImpl):
            continue
        if isinstance(n, exprParser.SignedAtomContext) and n.getChildCount() == 2 and n.getChild(0).getText() == '-':
            candidate_nodes.append(n)
        s.extend(n.getChildren())

    if not candidate_nodes:
        return None

    node = random.choice(candidate_nodes)
    old_str = node.getText()
    new_str = '(-1*' + node.getChild(1).getText() + ')'

    return expr_str.replace(old_str, new_str)


def trans_minus(expr_str):

    data = codecs.decode(expr_str, 'ascii', 'strict')
    input = InputStream(data)
    lexer = exprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.expression()

    candidate_nodes = []

    s = [tree]
    while s:
        n = s.pop()
        if isinstance(n, antlr4.tree.Tree.TerminalNodeImpl):
            continue
        if isinstance(n, exprParser.ExpressionContext) and '-' in [x.getText() for x in n.getChildren()]:
            candidate_nodes.append(n)
        s.extend(n.getChildren())

    if not candidate_nodes:
        return None

    node = random.choice(candidate_nodes)

    candidate_indexes = [i for i, j in enumerate(node.getChildren()) if j.getText() == '-']
    index = random.choice(candidate_indexes)

    old_str = node.getText()
    new_str = '('
    for i in range(node.getChildCount()):
        if i == index:
            new_str += '+('
        new_str += node.getChild(i).getText()

    new_str += '))'

    return expr_str.replace(old_str, new_str)


def trans_divide(expr_str):

    data = codecs.decode(expr_str, 'ascii', 'strict')
    input = InputStream(data)
    lexer = exprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.expression()

    candidate_nodes = []

    s = [tree]
    while s:
        n = s.pop()
        if isinstance(n, antlr4.tree.Tree.TerminalNodeImpl):
            continue
        if isinstance(n, exprParser.MultiplyingExpressionContext) and '/' in [x.getText() for x in n.getChildren()]:
            candidate_nodes.append(n)
        s.extend(n.getChildren())

    if not candidate_nodes:
        return None

    node = random.choice(candidate_nodes)

    index = [i for i, j in enumerate(node.getChildren()) if j.getText() == '/'][-1]

    old_str = node.getText()
    new_str = '('
    for i in range(node.getChildCount()):
        if i == index:
            new_str += '*(1'
        new_str += node.getChild(i).getText()

    new_str += '))'

    return expr_str.replace(old_str, new_str)


def trans_commutation(expr_str):

    data = codecs.decode(expr_str, 'ascii', 'strict')
    input = InputStream(data)
    lexer = exprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.expression()

    candidate_nodes = []

    s = [tree]
    while s:
        n = s.pop()
        if isinstance(n, antlr4.tree.Tree.TerminalNodeImpl):
            continue
        if isinstance(n, exprParser.MultiplyingExpressionContext) and '*' in [x.getText() for x in n.getChildren()]:
            candidate_nodes.append(n)
        if isinstance(n, exprParser.ExpressionContext) and '+' in [x.getText() for x in n.getChildren()]:
            candidate_nodes.append(n)
        s.extend(n.getChildren())

    if not candidate_nodes:
        return None

    node = random.choice(candidate_nodes)

    new_str = ''
    old_str = node.getText()

    index = random.choice([i for i, j in enumerate(node.getChildren()) if j.getText() == get_operator(node)])
    for i in range(index+1, node.getChildCount()):
        new_str += node.getChild(i).getText()
    new_str += get_operator(node)
    for i in range(0, index):
        new_str += node.getChild(i).getText()

    return expr_str.replace(old_str, new_str)


def trans_association(expr_str):

    data = codecs.decode(expr_str, 'ascii', 'strict')
    input = InputStream(data)
    lexer = exprLexer(input)
    stream = CommonTokenStream(lexer)
    parser = exprParser(stream)
    tree = parser.expression()

    candidate_nodes = []

    s = [tree]
    while s:
        n = s.pop()
        if isinstance(n, antlr4.tree.Tree.TerminalNodeImpl):
            continue

        for i in range(n.getChildCount()-2):
            if n.getChild(i).getText() == get_operator(n) and n.getChild(i+2).getText() == get_operator(n):
                candidate_nodes.append(n)
                break

        s.extend(n.getChildren())

    if not candidate_nodes:
        return None

    for n in candidate_nodes:
        print(n.getText())
    node = random.choice(candidate_nodes)

    candidate_indexes = [i for i in range(node.getChildCount()-2) if node.getChild(i).getText() == get_operator(node) and node.getChild(i+2).getText() == get_operator(node)]
    print(candidate_indexes)
    index = random.choice(candidate_indexes)

    old_str = node.getText()
    new_str = ''
    for i in range(node.getChildCount()):

        if i == index+1:
            new_str += '('

        new_str += node.getChild(i).getText()

        if i == index+3:
            new_str += ')'

    return expr_str.replace(old_str, new_str)


def trans_distribution(expr_str):
    return None


def get_operator(n):
        if isinstance(n, exprParser.MultiplyingExpressionContext):
            return '*'
        if isinstance(n, exprParser.ExpressionContext):
            return '+'
        return None


if __name__ == '__main__':
    main(sys.argv)
