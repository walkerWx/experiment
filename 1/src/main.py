#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
from copy import deepcopy

from mergePath import *
from transform import *
from stableAnalysis import *
from path import *

# 优化后程序两种不同的实现类型：浮点数实现、高精度实现
FLOATTYPE = 'float'
REALTYPE = 'real'


# 判断一个表达式在给定约束下是否稳定
def is_stable(path):
    return False


# 判断一条路径在给定约束下是否在数学意义上不稳定
def is_unstable(path):
    return False


# 优化过程的主要逻辑
def optimize(path_file):

    path_data = PathData(path_file)

    # 优化后的path
    opt_path_data = deepcopy(path_data)
    opt_path_data.clear_paths()

    # horner形式总优于其原来的形式
    horner_transform(path_data)

    for path in path_data.get_paths():

        # 路径在数学意义上计算不稳定，无法进行优化，依然使用高精度实现
        if is_unstable(path):
            new_path = deepcopy(path)
            new_path.set_implement(REALTYPE)
            opt_path_data.add_path(new_path)
            continue

        # 不稳定分析
        res = stable_analysis(path_data, path)

        if res['stable'] != '':
            new_path = deepcopy(path)
            new_path.add_constrain(res['stable'])
            new_path.set_implement(FLOATTYPE)
            opt_path_data.add_path(new_path)

        if res['unstable'] != '':

            unstable_path = deepcopy(path)
            unstable_path.add_constrain(res['unstable'])

            # transform the path into an equivalent paths list
            equal_paths = generate_equal_path(path_data, unstable_path)

            find_stable = False
            for ep in equal_paths:
                # find a stable path in the equivalent paths set
                if is_stable(ep):
                    find_stable = True
                    ep.set_implement(FLOATTYPE)
                    opt_path_data.add_path(ep)
                    break
            
            # if we can not find a stable path, we just keep the original multi-precision version
            if not find_stable:
                unstable_path.set_implement(REALTYPE)
                opt_path_data.add_path(unstable_path)

    # write optimized paths to file
    output_directory = ''
    if path_file.rfind('/') != -1:
        output_directory = path_file[:path_file.rfind('/')+1]
    output_file = output_directory+path_data.get_program_name()+'.opt.pth'
    opt_path_data.output_json(output_file)

'''
optimize('../case/midarc/midarc.pth')
mergePath('../case/midarc/midarc.opt.pth')
optimize('../case/analytic/analytic.pth')
mergePath('../case/analytic/analytic.opt.pth')
'''

optimize('../case/analytic/analytic.pth')
# mergePath('../case/analytic/analytic.opt.pth')


