# split an expression to a token list
def splitTokenList(expr):

    opList = ['+', '-', '*', '/']

    tokenList = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == '(' or c == ')' or (c in opList):
            tokenList.append(c)
            i += 1
        elif c.isdigit():
            j = i
            while j < len(expr):
                if not expr[j].isdigit():
                    break 
                j += 1
            tokenList.append(expr[i:j])
            i = j 
        elif c.isalpha():
            j = i
            while j < len(expr):
                if not expr[j].isalpha():
                    break 
                j += 1
            tokenList.append(expr[i:j])
            i = j
        else:
            i += 1

    return tokenList


# transform infix expression to postfix expression
def infix2postfix(infixExpr):

    tokenList = splitTokenList(infixExpr)

    s = []
    opList = ['+', '-', '*', '/']
    prec = {}
    prec['/'] = 3
    prec['*'] = 3
    prec['+'] = 2
    prec['-'] = 2
    prec['('] = 1

    

    postfixExpr = []     
    for t in tokenList:
        if t.isalpha():
            postfixExpr.append(t)
        elif t.isdigit():
            postfixExpr.append(t)
        elif t == '(':
            s.append(t)
        elif t == ')':
            topToken = s.pop()
            while topToken != '(':
                postfixExpr.append(topToken)
                topToken = s.pop() 
        else:
            while (s) and (prec[s[-1]] >= prec[t]):
                postfixExpr.append(s.pop())
            s.append(t)

    while s:
        opToken = s.pop()
        postfixExpr.append(opToken)

    return postfixExpr

# transform postfix expression to infix expression
def postfix2infix(tokenList):
    opList = ['+', '-', '*', '/']
    s = []    
    infixExpr = []
    for t in tokenList:
        if t in opList:
            op2 = s.pop()
            op1 = s.pop()
            op = '(' + op1 + t + op2 +')'
            s.append(op)
        else:
            s.append(t)
    return s


# transform an accumulation to stable form
def transform(expr):

    tokens = infix2postfix(expr)
    terms = [] 
    term = []
    for t in tokens:
        if t == '+':
            terms.append(term)
            term = []
        else:
            term.append(t)

    head = terms.pop(0)
    for i in range(len(terms)):
        terms[i] = postfix2infix(terms[i])[0]
    terms.insert(0, postfix2infix(head)[1])
    terms.insert(0, postfix2infix(head)[0])

    terms = reversed(terms)

    return '+'.join(terms)

f = 'a+b*c+(d*e+f)*g'
f = '((((((((((((((x+(x*x))+((x*x)*x))+(((x*x)*x)*x))+((((x*x)*x)*x)*x))+(((((x*x)*x)*x)*x)*x))+((((((x*x)*x)*x)*x)*x)*x))+(((((((x*x)*x)*x)*x)*x)*x)*x))+((((((((x*x)*x)*x)*x)*x)*x)*x)*x))+(((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x))+((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+(((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+((((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+(((((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))+((((((((((((((x*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x)*x))'
f = '(((((((((((((((((((x/2)+((x/2)/3))+(((x/2)/3)/4))+((((x/2)/3)/4)/5))+(((((x/2)/3)/4)/5)/6))+((((((x/2)/3)/4)/5)/6)/7))+(((((((x/2)/3)/4)/5)/6)/7)/8))+((((((((x/2)/3)/4)/5)/6)/7)/8)/9))+(((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10))+((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11))+(((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12))+((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13))+(((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13)/14))+((((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13)/14)/15))+(((((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13)/14)/15)/16))+((((((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13)/14)/15)/16)/17))+(((((((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13)/14)/15)/16)/17)/18))+((((((((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13)/14)/15)/16)/17)/18)/19))+(((((((((((((((((((x/2)/3)/4)/5)/6)/7)/8)/9)/10)/11)/12)/13)/14)/15)/16)/17)/18)/19)/20))'

print transform(f)


