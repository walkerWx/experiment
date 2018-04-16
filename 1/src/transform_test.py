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

    def test_midarc(self):

        midacr_expr = '((A1+B1*I)/sqrt(A1^2+B1^2)+(A2+B2*I)/sqrt(A2^2+B2^2))/abs((A1+B1*I)/sqrt(A1^2+B1^2)+(A2+B2*I)/sqrt(A2^2+B2^2))'

        target_expr = 'e^(I*(atan(B1/A1)+atan(B2/A2))/2)'

        midarc_rules = list()
        midarc_rules.append(self.rules['PolarRepresentation'])
        midarc_rules.append(self.rules['CommutationMultiply'])
        midarc_rules.append(self.rules['Midarc'])

        midarc_rules.append(self.rules['Simplify'])

        equvalent_expr = generate_equvalent_expressions(midacr_expr, midarc_rules)

        self.assertTrue(target_expr in equvalent_expr)

    def test_logq(self):

        logq_expr = 'log((1-eps)/(1+eps))'

        target_expr = '-2*eps*(3*eps^4+5*eps^2+15)/15'

        logq_rules = list()
        logq_rules.append(self.rules['Simplify'])
        logq_rules.append(self.rules['TaylorLnPlusReverse'])
        logq_rules.append(self.rules['TaylorLnMinusReverse'])
        logq_rules.append(self.rules['LnDivide'])

        equvalent_expr = generate_equvalent_expressions(logq_expr, logq_rules)

        self.assertTrue(target_expr in equvalent_expr)

if __name__ == '__main__':
    unittest.main()
