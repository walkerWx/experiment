import os
import re

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

}


# 找到所有的compiled.c文件，也就是包含了Herbie优化后程序代码的文件，将其中优化后程序组成一个C++文件
def generate_herbie_cc():

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


def save_irram_cc(execname, irram_code, file):

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


def save_makefile(herbie_bin, irram_bin, file):

    content = ""
    content += "PROJECTHOME = /Users/walker/Projects\n"
    content += "prefix=$(PROJECTHOME)/iRRAM/installed\n"
    content += "CPPFLAGS = -I$(PROJECTHOME)/iRRAM/installed/include\n"
    content += "CXX = clang++ -std=c++11\n"
    content += "CXXCPP = clang++ -E -std=c++11\n"
    content += "CXXFLAGS = -g -O2\n"
    content += "LDFLAGS = -Xlinker -rpath -Xlinker $(PROJECTHOME)/iRRAM/installed/lib\n"
    content += "LDLIBS =  -L$(PROJECTHOME)/iRRAM/installed/lib -liRRAM -lmpfr -lgmp -lm -lpthread\n"
    content += "all: " + " ".join(herbie_bin) + " " + irram_bin + "\n"
    content += irram_bin + ": " + "irram.cc points.o\n"
    for hb in herbie_bin:
        content += hb + ": " + hb + ".cc points.o\n"
    content += "points.o: ../../src/points.cc ../../src/points.h\n"
    content += "\t$(CXX) -c -o $@ $< $(CXXFLAGS)\n"
    content += "clean:\n"
    content += "\t rm -rf " + irram_bin + " " + " ".join(herbie_bin) + " points.o *.dSYM"

    with open(file, 'w') as f:
        f.write(content)


def prepare(casename):

    print("[INFO] Preparing for case :" + casename)

    os.chdir("/Users/walker/PycharmProjects/experiment/2/src")
    casedir = "../case/" + casename
    os.makedirs(casedir, exist_ok=True)

    generate_herbie_cc()

    herbie_bin = list()  # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    irram_bin = "irram"  # iRRAM可执行文件名称

    herbie_code_file = "herbie.cc"
    irram_code_file = "irram.cc"

    # 获取herbie函数名称以及相应代码
    with open(herbie_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^double (.*?' + casename + r'.*?)\(', re.M)
        herbie_bin = pattern.findall(content)

        pattern = re.compile(r'^double .*?' + casename + r'(?:.|\n)*?\}', re.M)
        herbie_code = pattern.findall(content)

    # 获取irram代码
    with open(irram_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^.*?' + casename + r'(?:.|\n)*?\}', re.M)
        irram_code = pattern.findall(content)

    # 生成herbie的C++实现
    for hb in herbie_bin:
        hb_cc = os.path.join(casedir, hb + '.cc')
        content = [x for x in herbie_code if hb in x][0]
        save_herbie_cc(hb, content, hb_cc)

    # 生成irram的C++实现
    irram_cc = os.path.join(casedir, 'irram.cc')
    content = irram_code[0]
    save_irram_cc(irram_bin, content, irram_cc)

    # 生成Makefile
    make_file = os.path.join(casedir, 'Makefile')
    save_makefile(herbie_bin, irram_bin, make_file)

    # 生成随机浮点数
    print("[INFO] Preparing random floating points..")
    points_file = os.path.join(casedir, 'points.txt')
    params_num = len(herbie_code[0].split('\n')[0].split(','))
    generate_points = './points --dimension=' + str(params_num) + " --file=" + points_file
    if casename in case_input_range:
        generate_points += ' --range=[' + case_input_range[casename]['begin'] + ',' + case_input_range[casename]['end'] + ']'

    print("[INFO] Sample Point Command: " + generate_points)
    os.system('make 2>/dev/null')
    os.system(generate_points)

    print("[INFO] Compiling herbie executables for " + casename)
    os.chdir(casedir)
    os.system('make')


def run(casename):

    print("[INFO] Running case " + casename + " ...")
    os.chdir("/Users/walker/PycharmProjects/experiment/2/src")
    casedir = "../case/" + casename

    herbie_bin = list()  # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    irram_bin = "irram"  # iRRAM可执行文件名称

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

    with open(points_file) as f:
        points = f.readlines()

    for point in points:
        print(point, file=open("point.txt", "w"))
        print("[INFO] Executing herbie program with input :" + point.replace("\n", ""))
        for hb in herbie_bin:
            os.system("./" + hb + " < point.txt >> " + hb + "_result.txt")

    for point in points:
        print(point, file=open("point.txt", "w"))
        print("[INFO] Executing irram program with input :" + point.replace("\n", ""))
        os.system("./" + irram_bin + " < point.txt >> " + irram_bin + "_result.txt")


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

    analysis_command = "../../src/analysis --irram=" + irram_result_file + " --herbie=" + ",".join(herbie_reuslt_files)
    print(analysis_command)
    os.system(analysis_command)


if __name__ == "__main__":

    irram_code_file = "irram.cc"
    with open(irram_code_file, "r") as f:
        content = f.read()

    pattern = re.compile(r'irram_(.*)\(')
    cases = pattern.findall(content)
    print(cases)

    dont = ['expq2', 'expq3']
    done = ['cos2', '2cos', 'invcot', 'sintan', '2atan', 'quadp', 'quadm', '2frac', 'quad2m', 'quad2p', 'tanhf', '3frac', '2tan', '2sin', '2log', 'exp2', 'expax', 'expm1', '2cbrt', '2nthrt', 'sqrtexp', 'qlog', 'logq', '2sqrt', 'logs', '2isqrt']
    #for case in done:
        #prepare(case)
        #run(case)
        #analysis(case)
