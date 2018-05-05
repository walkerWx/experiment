import os
import re


class HerbieReport:

    '''
        Herbie报告，包含了所有的Herbie用例
    '''

    def __init__(self, dir):
        for root, dirs, files in os.walk(dir):
            for name in files:
                if name == 'graph.html':
                    case_file = os.path.join(root, name)
                    hc = HerbieCase(case_file)

        return


class HerbieCase:

    '''
        Herbie用例，包含了用例名称，原始计算式，转换后计算式等信息
    '''

    def __init__(self, file):

        self.case_name = ''  # 用例名称
        self.origin_expr = ''  # 原始计算式
        self.transformed_expr = list()  # 转换后计算式
        self.constrain_expr = list()  # 转换后计算式对应约束，len(transformed_expr) = len(constrain_expr) + 1，最后有else情况

        try:
            report_file = open(file, 'r', encoding='utf-8')
        except IOError:
            print("[Error] Can't Open file " + file + '. Exit.')
            exit()

        report_content = report_file.read()

        case_name_pattern = re.compile(r'results for ([a-z0-9]+)', re.I)

        try:
            m = case_name_pattern.search(report_content)
            self.case_name = m.group(1)
        except AttributeError:
            print("[Error] Can't find case name. Exit.")
            exit()

        origin_expr_pattern = re.compile(r'<div class=\'program\'>(.*?)</div>', re.S)
        try:
            m = origin_expr_pattern.findall(report_content)
            self.origin_expr = m[0]
            self.transformed_expr = m[1]
        except AttributeError:
            print("[Error] Cant't find origin expression. Exit.")

        # 对提取的字符串做些预处理
        self.origin_expr = self.origin_expr.replace('\[', '')
        self.origin_expr = self.origin_expr.replace('\]', '')

        self.transformed_expr = self.transformed_expr.replace('\[', '')
        self.transformed_expr = self.transformed_expr.replace('\]', '')
        self.transformed_expr = self.transformed_expr.replace('\\begin{array}{l}', '')
        self.transformed_expr = self.transformed_expr.replace('\\end{array}', '')
        self.transformed_expr = self.transformed_expr.replace('\\;', '')
        self.transformed_expr = self.transformed_expr.replace('\\\\', '')
        self.transformed_expr = self.transformed_expr.replace('\\cdot', '*')
        self.transformed_expr = self.transformed_expr.replace('\\left', '')
        self.transformed_expr = self.transformed_expr.replace('\\right', '')

        transformed = [x for x in self.transformed_expr.splitlines() if not re.match(r'^\s*$', x)]  # 去掉空行

        self.transformed_expr = list()
        self.constrain_expr = list()

        if len(transformed) == 1:
            self.transformed_expr.extend(transformed)
            return
        else:
            for line in transformed:
                if line.startswith('\\mathbf{if}') and line.endswith(':'):
                    self.constrain_expr.append(line[11:-1])
                elif line.startswith('\\mathbf{else}:'):
                    continue
                else:
                    self.transformed_expr.append(line)

        print('Case name:' + '\t'*5 + self.case_name)
        print('Origin expression:' + '\t'*3 + self.origin_expr)
        print('Transformed expression:')
        print('\n'.join(self.transformed_expr))
        print('Constrain expression:')
        print('\n'.join(self.constrain_expr))


if __name__ == "__main__":

    # 找到所有的compiled.c文件，也就是包含了Herbie优化后程序代码的文件，将其中优化后程序组成一个C文件
    compiled_files = list()
    report_dir = '/Users/walker/Desktop/HerbieCases'
    for root, dirs, files in os.walk(report_dir):
        for file in files:
            if file == "compiled.c":
                compiled_files.append(os.path.join(root, file))

    compiled_files.sort()

    herbie_file = open("herbie.cc", "w")

    for compiled_file in compiled_files:

        [report_num, case_name] = compiled_file.split('/')[-3:-1]
        funcname = '_'.join(["herbie", report_num, case_name.replace('-', '_')])
        with open(compiled_file) as file:
            lines = file.readlines()
            start = next(i for i in range(len(lines)) if lines[i].startswith("double f_of"))
            end = next(i for i in range(len(lines)) if lines[i].startswith("}") and i > start) + 1
            lines[start] = lines[start].replace('f_of', funcname)
            for i in range(start, end):
                herbie_file.write(lines[i])
        herbie_file.write('\n')

    herbie_file.close()


