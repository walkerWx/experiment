import unittest

from transformRule import *

class TestTransform(unittest.TestCase):

    def setUp(self):

        rules_fromfile = load_rules()

        self.rules = dict()
        for rule in rules_fromfile:
            self.rules[rule.rule_name] = rule

        self.rules['Simplify'] = SympyRule('Simplify')
        self.rules['Expand'] = SympyRule('Expand')
        self.rules['Horner'] = SympyRule('Horner')
        self.rules['Taylor'] = SympyRule('Taylor')

        math_functions = ['sin', 'cos', 'tan', 'exp']
        for f in math_functions:
            rule_name = 'Taylor'+f
            self.rules[rule_name] = SympyRule(rule_name)

    def test_midarc(self):

        expr = '((A1+B1*I)/sqrt(A1^2+B1^2)+(A2+B2*I)/sqrt(A2^2+B2^2))/abs((A1+B1*I)/sqrt(A1^2+B1^2)+(A2+B2*I)/sqrt(A2^2+B2^2))'

        target = 'e^(I*(atan(B1/A1)+atan(B2/A2))/2)'

        rules = list()
        rules.append(self.rules['PolarRepresentation'])
        rules.append(self.rules['CommutationMultiply'])
        rules.append(self.rules['Midarc'])

        rules.append(self.rules['Simplify'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)

        self.assertTrue(target in equivalent_expr)

    def test_logq(self):

        expr = 'log((1-eps)/(1+eps))'

        target = '-2*eps*(3*eps^4+5*eps^2+15)/15'

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['TaylorLnPlusReverse'])
        rules.append(self.rules['TaylorLnMinusReverse'])
        rules.append(self.rules['LnDivide'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)

        self.assertTrue(target in equivalent_expr)

    def test_expq3(self):

        expr = 'eps*(exp((a+b)*eps)-1)/((exp(a*eps)-1)*(exp(b*eps)-1))'
        target = ''

        rules = list()

        equivalent_expr = generate_equivalent_expressions(expr, rules)

        self.assertTrue(target in equivalent_expr)

    def test_2cos(self):

        expr = 'cos(x+e)-cos(x)'

        target = ['(cos(x)*cos(e)-sin(x)*sin(e))-cos(x)', '-2*sin(e/2)*sin(e/2+x)']

        rules = list()
        rules.append(self.rules['SinSinR'])
        rules.append(self.rules['CosPlus'])
        rules.append(self.rules['Simplify'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)

        for te in target:
            self.assertTrue(te in equivalent_expr)


    def test_sqrtexp(self):

        expr = 'sqrt((exp(2*eps)-1)/(exp(eps)-1))'
        target = 'sqrt(exp(eps)+1)'

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['ExpReduction'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)

        self.assertTrue(target in equivalent_expr)

    def test_expq2(self):

        expr = 'exp(x)/(exp(x)-1)'
        target = '1+1/(x+pow(x,2)/2+pow(x,3)/6+pow(x,4)/24)'

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['FracPartial'])
        rules.append(self.rules['TaylorExp'])
        rules.append(self.rules['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        self.assertTrue(target in equivalent_expr)

    def test_2sin(self):

        expr = 'sin(x+e)-sin(x)'
        target = ['sin(x)*cos(e)+cos(x)*sin(e)-sin(x)',
                  'e*(e^4-80*e^2+1920)*cos(e/2+x)/1920']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['SinPlus'])
        rules.append(self.rules['CosSinR'])
        rules.append(self.rules['Taylorsin'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_2tan(self):

        expr = 'tan(x+e) - tan(x)'
        target = ['sin(e)/(cos(x)*(cos(e)*cos(x)-sin(e)*sin(x)))']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['TanPlus'])
        rules.append(self.rules['CosPlus'])
        rules.append(self.rules['CommDenominator2'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_cos2(self):

        expr = '(1-cos(x))/(x*x)'
        target = ['x^4/720-x^2/24+1/2']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['Taylorcos'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_sintan(self):

        expr = '(x-sin(x))/(x-tan(x))'
        target =['x^2*(x^2*(27*x^2/112000-27/2800)+9/40)-1/2']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['Taylor'])
        rules.append(self.rules['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_tanhf(self):

        expr = '(1-cos(x))/sin(x)'
        target = ['sin(x)/(1+cos(x))']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['Taylor'])
        rules.append(self.rules['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)


    def test_logs(self):

        expr = '(n+1)*ln(n+1)-n*ln(n)-1'
        target = ['']



    def test_expax(self):

        expr = 'exp(a*x)-1'
        target = ['a*x*(a*x*(a*x*(a*x*(a*x*(a*x+6)+30)+120)+360)+720)/720']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['Taylorexp'])
        rules.append(self.rules['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_exp2(self):

        expr = 'exp(e)-2+exp(-e)'
        target = ['e^6/360+e^4/12+e^2']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['Taylor'])
        rules.append(self.rules['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_2sqrt(self):

        expr = 'sqrt(x+1)-sqrt(x)'
        target = ['1/(sqrt(x+1)+sqrt(x))']

        rules = list()
        rules.append(self.rules['Simplify'])
        rules.append(self.rules['Taylor'])
        rules.append(self.rules['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)



if __name__ == '__main__':
    unittest.main()
