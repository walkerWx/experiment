#!/usr/bin/python
# -*- coding:utf-8 -*-

import copy
import os

from mergePath import *
from stableAnalysis import *
from transform import *


# 将一个dict数据结构输出到文件
def output_json(content, file):
    with open(file, 'w') as f:
        json.dump(content, f, indent=2)


# 优化过程的主要逻辑
def optimize(path_file):

    path_data = PathData(path_file)
    print(path_data.to_json())

    # 实验用例所在路径
    casedir = ''
    if path_file.rfind('/') != -1:
        casedir = path_file[:path_file.rfind('/')+1]
    else:
        casedir = '.'

    # 优化后的path，除了路径信息外，其余信息与原path文件相同，路径信息为我们对该path文件中的路径进行优化后添加进去的
    opt_path_data = copy.deepcopy(path_data)
    opt_path_data.clear_paths()

    for path in path_data.get_paths():

        # TODO 稳定性分析应该放在此循环外，首先将输入域根据路径划分，再进行优化

        # 稳定性分析
        res = stable_analysis(path_data, path)
        stable_intervals = res['stable']
        unstable_intervals = res['unstable']

        # 将稳定性分析结果写入文件
        sa_file = os.path.join(casedir, path_data.get_program_name() + '.sa.json')
        output_json(res, sa_file)

        # 直接将稳定部分使用浮点精度实现加入到优化后路径文件中
        if stable_intervals:
            float_path = copy.deepcopy(path)
            float_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], stable_intervals))
            float_path.set_implement(FLOATTYPE)
            opt_path_data.add_path(float_path)

        # 所有不稳定输入域均已经优化
        if not unstable_intervals:
            break

        # 不稳定部分进行等价转化形成等价计算路径集合
        equal_paths = generate_equal_paths(path, num=2)

        for ep in equal_paths:

            print(ep.to_json())

            # 所有不稳定输入域均已经优化
            if not unstable_intervals:
                break

            # 在该等价计算路径下计算稳定的不稳定输入域
            ep_stable_intervals = shieve_stable_interval(path_data, path, ep, unstable_intervals)

            # 将该等价路径与稳定区间加入到结果中
            if ep_stable_intervals:

                print("stable intervals on path")
                print(ep_stable_intervals)
                print(ep.to_json())

                opt_path = copy.deepcopy(ep)
                opt_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], ep_stable_intervals))
                opt_path.set_implement(FLOATTYPE)
                opt_path_data.add_path(opt_path)

            # 去掉已经稳定的区间
            unstable_intervals = [t for t in unstable_intervals if t not in ep_stable_intervals]

        # 未找到稳定的等价路径的区间，使用高精度实现
        if unstable_intervals:
            real_path = copy.deepcopy(path)
            real_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], unstable_intervals))
            real_path.set_implement(REALTYPE)
            opt_path_data.add_path(real_path)

    # 结果输出到文件
    opt_path_file = os.path.join(casedir, opt_path_data.get_program_name()+'_o.pth.json')
    output_json(opt_path_data.to_json(), opt_path_file)

    # 路径合并
    merge_path(opt_path_file)


if __name__ == "__main__":
    optimize('../case/iRRAM/jmmuller/jmmuller.pth')

'''
mergePath('../case/midarc/midarc.opt.pth')
optimize('../case/analytic/analytic.pth')
mergePath('../case/analytic/analytic.opt.pth')

#path_file = sys.argv[1]
#optimize(path_file)
# optimize('../case/e_example/e_example.pth')
# optimize('../case/analytic/analytic.pth')
# optimize('../case/midarc/midarc.pth')
optimize('../case/float_extension/float_extension.pth')
# optimize('../case/jmmuller/jmmuller.pth')
# optimize('../case/gamma/gamma.pth')
'''
