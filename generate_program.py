#!/usr/bin/python 

import sys

path_file = sys.argv[1]

with open(path_file, 'r') as pf:
    output_file_name = pf.readline().rstrip() + "_opt.cc"
    open(output_file_name, 'w').close()
    function_num = int(pf.readline())
    for _ in range(0, function_num):
        function_name = pf.readline().rstrip()
        param_num = int(pf.readline())
        param_list = pf.readline().split()
        path_num = int(pf.readline())
        constrains = []
        paths = []
        stability = []
        for i in range(0, path_num):
            constrains.append(pf.readline().rstrip())
            paths.append(pf.readline().rstrip())
            stability.append(pf.readline().rstrip())

        of = open(output_file_name, 'a')
        of.write("double " + function_name + "(")
        for i in range(0, param_num):
            if (i != param_num-1):
                of.write("double " + param_list[i] + ",")
            else:
                of.write("double " + param_list[i])
        of.write(") { \n")
        if (path_num == 1):
            of.write("\treturn "+ paths[0] + ";\n")
        of.write("}\n\n")
    of.close()

