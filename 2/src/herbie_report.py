import os
import re

# 每个herbie实验用例生成输入的范围
case_input_range = {
    '2log': {'begin': '0.0', 'end': 'INF'},
    'exp2': {'begin': '-700', 'end': '700'},
    'expax': {'begin': '-26', 'end': '26'},
    'expm1': {'begin': '-700', 'end': '700'},
    '2nthrt': {'begin': '1.0', 'end': 'INF'},
    '2cbrt': {'begin': '0.0', 'end': 'INF'},
    '2sqrt': {'begin': '0.0', 'end': 'INF'},
    '2isqrt': {'begin': '0.0', 'end': 'INF'},
    'sqrtexp': {'begin': '-1.0', 'end': '1.0'},
    'qlog': {'begin': '-1.0', 'end': '1.0'},
    'logq': {'begin': '-1.0', 'end': '1.0'},
    'logs': {'begin': '0.0', 'end': 'INF'},
    'expq2': {'begin': '-700', 'end': '700'},
    'expq3': {'begin': '-1.0', 'end': '1.0'},
}

# 每个herbie实验用例输入的维度
case_input_dimension = {
    'expax': 2,
    '2cos': 2,
    '2sin': 2,
    '2tan': 2,
    '2nthrt': 2,
    'quad2m': 3,
    'quad2p': 3,
    'quadp': 3,
    'quadm': 3,
    'expq3': 3,
}


# 找到所有的compiled.c文件，也就是包含了Herbie优化后程序代码的文件，将其中优化后程序组成一个C++文件
def summary_compile_c():

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
            start = next(i for i in range(len(lines)) if lines[i].startswith("double f_od"))
            end = next(i for i in range(len(lines)) if lines[i].startswith("}") and i > start) + 1
            lines[start] = lines[start].replace('f_od', funcname)
            for i in range(start, end):
                herbie_file.write(lines[i])
        herbie_file.write('\n')

    herbie_file.close()


def save_herbie_cc(execname, herbie_code, file):

    pattern = re.compile(r'\((.*)\)')
    function_definition = herbie_code.split('\n')[0]
    params = pattern.search(function_definition).group()
    vars = [x.strip().split(' ')[1] for x in params[1:-1].split(',')]


    header = '''#include <cmath>
#include <iostream>
#include <string>
#include <iomanip>
#include "../../src/points.h"
'''

    main = "int main() {\n"
    main += "\tstd::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);\n"
    main += "\tstd::string " + ",".join([x+"_str" for x in vars]) + ";\n"
    main += "\tstd::cin >> " + " >> ".join([x+"_str" for x in vars]) + ";\n"
    for var in vars:
        main += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
    main += "\tdouble r_double = " + execname + "(" + ", ".join([x+"_double" for x in vars]) + ");\n"
    main += "\tstd::cout << double2binary(r_double) << std::endl;\n"
    main += "}\n"

    with open(file, 'w') as f:
        f.write(header)
        f.write("\n")
        f.write(herbie_code)
        f.write("\n")
        f.write(main)


def save_irram_cc(irram_code, file):

    pattern = re.compile(r'\((.*)\)')
    function_definition = irram_code.split('\n')[1]
    params = pattern.search(function_definition).group()
    vars = [x.strip().split(' ')[1] for x in params[1:-1].split(',')]

    funcname = function_definition.split('(')[0].split(' ')[1]

    header = '''#include <string>
#include <iostream>
#include "iRRAM.h"
#include "../../src/points.h"
'''

    main = "void compute() {\n"
    main += "\tstd::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);\n"
    main += "\tiRRAM::cout << iRRAM::setRwidth(30);\n"
    main += "\tstd::string " + ",".join([x+"_str" for x in vars]) + ";\n"
    main += "\tiRRAM::cin >> " + " >> ".join([x+"_str" for x in vars]) + ";\n"
    for var in vars:
        main += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
    for var in vars:
        main += "\tiRRAM::REAL " + var + "_irram(" + var + "_double);\n"
    main += "\tiRRAM::REAL r_irram = " + funcname + "(" + ", ".join([x+"_irram" for x in vars]) + ");\n"
    main += "\tdouble r_double = r_irram.as_double();\n"
    main += '\tiRRAM::cout << double2binary(r_double) << "\\n";\n'
    main += "}\n"

    with open(file, 'w') as f:
        f.write(header)
        f.write("\n")
        f.write(irram_code)
        f.write("\n")
        f.write(main)


def save_opt_cc(opt_code, file):

    pattern = re.compile(r'\((.*)\)')
    function_definition = opt_code.split('\n')[1]
    params = pattern.search(function_definition).group()
    vars = [x.strip().split(' ')[1] for x in params[1:-1].split(',')]

    funcname = function_definition.split('(')[0].split(' ')[1]

    header = '''#include <string>
#include <iostream>
#include <iomanip>
#include <limits>
#include "../../src/points.h"
'''

    main = "int main() {\n"
    main += "\tstd::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);\n"
    main += "\tstd::string " + ",".join([x+"_str" for x in vars]) + ";\n"
    main += "\tstd::cin >> " + " >> ".join([x+"_str" for x in vars]) + ";\n"
    for var in vars:
        main += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
    main += "\tdouble r_double = " + funcname + "(" + ", ".join([x+"_double" for x in vars]) + ");\n"
    main += '\tstd::cout << double2binary(r_double) << "\\n";\n'
    main += "}\n"

    with open(file, 'w') as f:
        f.write(header)
        f.write("\n")
        f.write(opt_code)
        f.write("\n\n")
        f.write(main)


def save_makefile(bins, file):

    content = ""
    content += "PROJECTHOME = /Users/walker/Projects\n"
    content += "prefix=$(PROJECTHOME)/iRRAM/installed\n"
    content += "CPPFLAGS = -I$(PROJECTHOME)/iRRAM/installed/include\n"
    content += "CXX = clang++ -std=c++11\n"
    content += "CXXCPP = clang++ -E -std=c++11\n"
    content += "CXXFLAGS = -g -O2\n"
    content += "LDFLAGS = -Xlinker -rpath -Xlinker $(PROJECTHOME)/iRRAM/installed/lib\n"
    content += "LDLIBS =  -L$(PROJECTHOME)/iRRAM/installed/lib -liRRAM -lmpfr -lgmp -lm -lpthread\n"
    content += "all: " + " ".join(bins) + "\n"
    for bin in bins:
        content += bin + ": " + bin + ".cc points.o\n"
    content += "points.o: ../../src/points.cc ../../src/points.h\n"
    content += "\t$(CXX) -c -o $@ $< $(CXXFLAGS)\n"
    content += "clean:\n"
    content += "\t rm -rf " + " ".join(bins) + " points.o *.dSYM"

    with open(file, 'w') as f:
        f.write(content)


# 生成Herbie优化后代码，其实现从当前目录的herbie.cc中获取
def generate_herbie_cc(casename):

    # 新建case文件夹
    os.chdir("/Users/walker/PycharmProjects/experiment/2/src")
    casedir = "../case/" + casename
    os.makedirs(casedir, exist_ok=True)

    # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    herbie_bin = list()

    # Herbie实现文件，可调用summary_compile_c函数生成
    herbie_code_file = "herbie.cc"

    # 获取herbie函数名称以及相应代码
    with open(herbie_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^double (.*?' + casename + r'.*?)\(', re.M)
        herbie_bin = pattern.findall(content)

        pattern = re.compile(r'^double .*?' + casename + r'(?:.|\n)*?\}', re.M)
        herbie_code = pattern.findall(content)

    # 生成herbie的C++实现
    for hb in herbie_bin:
        hb_cc = os.path.join(casedir, hb + '.cc')
        content = [x for x in herbie_code if hb in x][0]
        save_herbie_cc(hb, content, hb_cc)


# 生成irram任意精度代码，其实现从当前目录的irram.cc中获取
def generate_irram_cc(casename):

    casedir = "/Users/walker/PycharmProjects/experiment/2/case/" + casename
    srcdir = "/Users/walker/PycharmProjects/experiment/2/src/"
    os.chdir(srcdir)

    # iRRAM可执行文件名称
    irram_bin = "irram"

    # irram实现文件，直接按照数学公式纯手工编写
    irram_code_file = "irram.cc"

    # 获取irram实现文件中的代码实现
    with open(irram_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^.*?' + casename + r'(?:.|\n)*?\}', re.M)
        irram_code = pattern.findall(content)

    # 生成irram的C++实现
    irram_cc = os.path.join(casedir, 'irram.cc')
    content = irram_code[0]
    save_irram_cc(content, irram_cc)


# 生成opt代码，其实现从当前目录的opt.cc中获取
def generate_opt_cc(casename):

    casedir = "/Users/walker/PycharmProjects/experiment/2/case/" + casename
    srcdir = "/Users/walker/PycharmProjects/experiment/2/src/"
    os.chdir(srcdir)

    # 经我们工具优化后可执行文件名称
    opt_bin = "opt"

    # 优化后实现文件，暂时通过手工编写，后续需要自动化实现
    opt_code_file = "opt.cc"

    # 获取优化后文件中代码实现
    with open(opt_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^.*?' + casename + r'(?:.|\n)*?\}', re.M)
        opt_code = pattern.findall(content)

    # 生成优化后文件的C++实现
    opt_cc = os.path.join(casedir, 'opt.cc')
    content = opt_code[0]
    save_opt_cc(content, opt_cc)


# 生成Makefile
def generate_makefile(casename):

    casedir = "/Users/walker/PycharmProjects/experiment/2/case/" + casename
    srcdir = "/Users/walker/PycharmProjects/experiment/2/src/"
    os.chdir(casedir)

    # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    herbie_bin = list()

    # Herbie实现文件，可调用summary_compile_c函数生成
    herbie_code_file = os.path.join(srcdir, "herbie.cc")

    # 获取herbie可执行文件名称
    with open(herbie_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^double (.*?' + casename + r'.*?)\(', re.M)
        herbie_bin = pattern.findall(content)

    # 生成Makefile
    make_file = os.path.join(casedir, 'Makefile')
    irram_bin = "irram"
    opt_bin = "opt"
    save_makefile(herbie_bin + [irram_bin] + [opt_bin], make_file)


# 生成随机输入，也就是随机采点，默认256个，结果存储在case目录的points.txt中，以二进制表示
def generate_points(casename):

    print("[INFO] Preparing random floating points..")

    casedir = "/Users/walker/PycharmProjects/experiment/2/case/" + casename
    srcdir = "/Users/walker/PycharmProjects/experiment/2/src/"
    os.chdir(srcdir)

    points_file = os.path.join(casedir, 'points.txt')

    if casename in case_input_dimension:
        params_num = case_input_dimension[casename]
    else:
        params_num = 1

    generate_points = './points --dimension=' + str(params_num) + " --file=" + points_file
    if casename in case_input_range:
        generate_points += ' --range=[' + case_input_range[casename]['begin'] + ',' + case_input_range[casename]['end'] + ']'

    print("[INFO] Sample Point Command: " + generate_points)
    os.system('make 2>/dev/null')
    os.system(generate_points)


# 将之前生成的herbie，irram，opt文件编译成可执行文件
def compile_executables(casename):

    print("[INFO] Compiling herbie executables for " + casename)

    casedir = "/Users/walker/PycharmProjects/experiment/2/case/" + casename
    os.chdir(casedir)

    os.system('make')


# 每个herbie用例的准备工作
def prepare(casename):

    print("[INFO] Preparing for case :" + casename)

    # 生成Herbie优化后代码，其实现从当前目录的herbie.cc中获取
    generate_herbie_cc(casename)

    # 生成irram任意精度代码，其实现从当前目录的irram.cc中获取
    generate_irram_cc(casename)

    # 生成opt代码，其实现从当前目录的opt.cc中获取
    generate_opt_cc(casename)

    # 生成Makefile
    generate_makefile(casename)

    '''
    # 生成随机输入，也就是随机采点，默认256个，结果存储在case目录的points.txt中，以二进制表示
    # generate_points(casename)
    '''

    # 将之前生成的herbie，irram，opt文件编译成可执行文件
    compile_executables(casename)


# 跑irrram,opt,herbie程序，输入为随机采点得到的points.txt文件，输出结果以二进制形式写入到 XXX_result.txt
def run(casename):

    print("[INFO] Running case " + casename + " ...")
    os.chdir("/Users/walker/PycharmProjects/experiment/2/src")
    casedir = "../case/" + casename

    herbie_bin = list()  # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    irram_bin = "irram"  # iRRAM可执行文件名称
    opt_bin = "opt"  # 优化有程序的可执行文件名称

    herbie_code_file = "herbie.cc"

    # 获取herbie可执行文件
    with open(herbie_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^double (.*?' + casename + r'.*?)\(', re.M)
        herbie_bin = pattern.findall(content)

    points_file = "points.txt"

    os.chdir(casedir)

    # 删除旧文件
    for hb in herbie_bin:
        try:
            os.remove(hb+"_result.txt")
        except OSError:
            pass

    try:
        os.remove(irram_bin+"_result.txt")
    except OSError:
        pass

    try:
        os.remove(opt_bin+"_result.txt")
    except OSError:
        pass

    with open(points_file) as f:
        points = f.readlines()

    for point in points:
        print(point, file=open("point.txt", "w"))
        print("[INFO] Executing herbie program with input :" + point.replace("\n", ""))
        for hb in herbie_bin:
            os.system("./" + hb + " < point.txt >> " + hb + "_result.txt")

    for point in points:
        print(point, file=open("point.txt", "w"))
        print("[INFO] Executing optimized program with input :" + point.replace("\n", ""))
        os.system("./" + opt_bin + " < point.txt >> " + opt_bin + "_result.txt")

    for point in points:
        print(point, file=open("point.txt", "w"))
        print("[INFO] Executing irram program with input :" + point.replace("\n", ""))
        os.system("./" + irram_bin + " < point.txt >> " + irram_bin + "_result.txt")


# 分析跑程序得到的result.txt文件，得到每个用例的两种误差，包括herbie所定义的误差以及相对误差，结果输出到result.csv，主要是对analysis的调用
def analysis(case):

    print(case)
    casedir = os.path.join("/Users/walker/PycharmProjects/experiment/2/case", case)
    os.chdir(os.path.join(casedir))

    result_files = [f for f in os.listdir(casedir) if os.path.isfile(os.path.join(casedir, f)) and f.endswith("result.txt")]

    herbie_reuslt_files = list()
    for f in result_files:
        if f.startswith("irram"):
            irram_result_file = f
        if f.startswith("herbie"):
            herbie_reuslt_files.append(f)
        if f.startswith("opt"):
            opt_result_file = f

    analysis_command = "../../src/analysis --irram=" + irram_result_file + " --herbie=" + ",".join(herbie_reuslt_files) + " --opt=" + opt_result_file
    os.system(analysis_command)
    print("")


if __name__ == "__main__":

    irram_code_file = "irram.cc"
    with open(irram_code_file, "r") as f:
        content = f.read()

    pattern = re.compile(r'irram_(.*)\(')
    cases = pattern.findall(content)
    print(cases)

    analysis('2cos')
