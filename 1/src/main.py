#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
from copy import deepcopy

from mergePath import *
from transform import *
from stableAnalysis import *
from path import *



# 判断一条路径在给定约束下是否在数学意义上不稳定
def is_unstable(path):
    return False


# 优化过程的主要逻辑
def optimize(path_file):

    path_data = PathData(path_file)

    # 优化后的path
    opt_path_data = deepcopy(path_data)
    opt_path_data.clear_paths()

    for path in path_data.get_paths():

        # 路径在数学意义上计算不稳定，无法进行优化，依然使用高精度实现
        if is_unstable(path):
            new_path = deepcopy(path)
            new_path.set_implement(REALTYPE)
            opt_path_data.add_path(new_path)
            continue

        # 不稳定分析
        res = stable_analysis(path_data, path)
        stable_intervals = res['stable']
        unstable_intervals = res['unstable']

        # 直接将稳定部分加入到结果中去
        if stable_intervals:
            print("STABLE INTERVALS")
            print(stable_intervals)
            new_path = deepcopy(path)
            new_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], stable_intervals))
            new_path.set_implement(FLOATTYPE)
            opt_path_data.add_path(new_path)

        # 不稳定部分进行等价转化后寻找其稳定形式
        if unstable_intervals:
            print("UNSTABLE INTERVALS")
            print(unstable_intervals)

            # 生成等价路径
            equal_paths = generate_equal_path(opt_path_data, path)

            for ep in equal_paths:

                print(ep.to_json())

                if ep.get_implement:
                    new_path = deepcopy(ep)
                    opt_path_data.add_path(new_path)

                # 根据path生成对应可执行cpp文件并编译，后续分析路径稳定性时需要使用
                generate_cpp(opt_path_data, ep)
                call(['make'], shell=True)

                # 筛选出等价路径下稳定的区间
                ep_stable_intervals = [t for t in unstable_intervals if is_stable(path_data, ep, t)]
                print(len(ep_stable_intervals))

                # 将该等价路径与稳定区间加入到结果中
                if ep_stable_intervals:
                    new_path = deepcopy(ep)
                    new_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], ep_stable_intervals))
                    new_path.set_implement(FLOATTYPE)
                    opt_path_data.add_path(new_path)

                # 去掉已经稳定的区间
                unstable_intervals = [t for t in unstable_intervals if t not in ep_stable_intervals]

                if not unstable_intervals:
                    break

            # 未找到稳定的等价路径的区间，使用高精度实现
            if unstable_intervals:
                new_path = deepcopy(path)
                new_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], unstable_intervals))
                new_path.set_implement(REALTYPE)
                opt_path_data.add_path(new_path)

    # print(opt_path_data.to_json())
    # 结果输出到文件
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

# optimize('../case/harmonic/harmonic.pth')
# optimize('../case/e_example/e_example.pth')
optimize('../case/analytic/analytic.pth')
# optimize('../case/midarc/midarc.pth')
# optimize('../case/float_extension/float_extension.pth')
# optimize('../case/jmmuller/jmmuller.pth')
# optimize('../case/gamma/gamma.pth')


