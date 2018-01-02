#!/usr/bin/env sage
# -*- coding: utf-8 -*-

from __future__ import print_function

# from transform import convert_expr
from path import *
from config import *


# TODO
# different type implemention && loop implemention
# merge paths in pth file to a C program
def merge_path(path_file):

    path_data = PathData(path_file)

    code_header = \
'''
#include <iostream>
#include <iomanip>
#include <limits>
#include <cmath>

#include "iRRAM.h"
#include "../../src/gamma.h"

#define euler_gamma (0.57721566490)

using namespace std;
using namespace iRRAM;

'''

    code_body = ''

    # 函数声明
    param_list = ', '.join([FLOAT[path_data.get_variable_type(x)] + ' ' + x for x in path_data.get_input_variables()])
    code_body += FLOAT['decimal'] + ' ' + path_data.get_function_name() + '(' + param_list + ')\n'
    code_body += '{\n'

    # 变量声明
    for v in path_data.get_variables():
        if v not in path_data.get_input_variables():
            code_body += '\t' + FLOAT[path_data.get_variable_type(v)] + ' ' + v + ';\n'

    code_body += '\n'

    for p in path_data.get_paths():

        print(p.to_json())

        if p.get_implement() == FLOATTYPE:
            code_body += p.to_cpp_code(FLOATTYPE, indent=1)
        elif p.get_implement() == REALTYPE:
            code_body += p.to_mixed_code(path_data, indent=1)

        code_body += '\n'

    # return语句
    code_body += '\treturn ' + path_data.get_return_expr() + ';\n'
    code_body += '}\n\n'

    # main函数
    code_body += 'void compute(){\n'

    for v in path_data.get_input_variables():
        code_body += '\t' + FLOAT[path_data.get_variable_type(v)] + ' ' + v + ';\n'

    code_body += '\t' + FLOAT['cin'] + ' >> ' + ' >> '.join(path_data.get_input_variables()) + ';\n'

    code_body += '\t' + FLOAT['cout'] + ' << scientific << setprecision(numeric_limits<double>::digits10);\n'

    code_body += '\t' + FLOAT['cout'] + ' << ' + path_data.get_function_name() + '(' + ', '.join(path_data.get_input_variables()) +') << endl;\n'

    code_body += '}\n'


    # output to file
    output_directory = ''
    if path_file.rfind('/') != -1:
        output_directory = path_file[:path_file.rfind('/')+1]

    output_file = open(output_directory+path_data.get_program_name()+'_o.cc', 'w')

    print (code_header, file=output_file)
    print (code_body, file=output_file)




