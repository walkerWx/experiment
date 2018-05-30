#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import random
import copy

from mergePath import *
from stableAnalysis import *
from path import *

from rule import RULES
from transform import apply_rule_path


# 将一个dict数据结构输出到文件
def output_json(content, file):
    with open(file, 'w') as f:
        json.dump(content, f, indent=2)


# 优化过程的主要逻辑
def optimize(path_file):

    path_data = PathData(path_file)

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

        # 稳定性分析
        res = stable_analysis(path_data, path)
        stable_intervals = res['stable']
        unstable_intervals = res['unstable']

        # 将稳定性分析结果写入JSON文件，以sa结尾，代表stable analysis
        sa_file = os.path.join(casedir, path_data.get_program_name() + '.sa.json')
        output_json(res, sa_file)

        # 直接将稳定部分使用浮点精度实现加入到优化后路径文件中
        if stable_intervals:
            new_path = copy.deepcopy(path)
            new_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], stable_intervals))
            new_path.set_implement(FLOATTYPE)
            opt_path_data.add_path(new_path)

        # 不稳定部分进行等价转化后寻找其稳定形式
        transform_num = 0
        equal_paths = [path]

        while unstable_intervals and transform_num < TRANSFORM_NUM:

            transform_num += 1

            # 随机选取一条等价路径
            p = random.choice(equal_paths)

            # 随机选取一条规则
            r = random.choice(list(RULES))

            # 在路径是运用规则生成新的等价路径
            ep = apply_rule_path(p, r)

            if not ep:
                continue

            if ep.get_implement():
                new_path = copy.deepcopy(ep)
                opt_path_data.add_path(new_path)

            # 筛选出等价路径下稳定的区间
            ep_stable_intervals = [t for t in unstable_intervals if is_stable(path_data, ep, t)]

            # 将该等价路径与稳定区间加入到结果中
            if ep_stable_intervals:
                new_path = copy.deepcopy(ep)
                new_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], ep_stable_intervals))
                new_path.set_implement(FLOATTYPE)
                opt_path_data.add_path(new_path)

            # 去掉已经稳定的区间
            unstable_intervals = [t for t in unstable_intervals if t not in ep_stable_intervals]

            #  变换后得到的等价形式依旧加入到等价计算形式的列表中
            equal_paths.append(ep)

        # 未找到稳定的等价路径的区间，使用高精度实现
        if unstable_intervals:
            new_path = copy.deepcopy(path)
            new_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], unstable_intervals))
            new_path.set_implement(REALTYPE)
            opt_path_data.add_path(new_path)

    # print(opt_path_data.to_json())
    # 结果输出到文件
    output_directory = ''
    if path_file.rfind('/') != -1:
        output_directory = path_file[:path_file.rfind('/')+1]
    output_file = output_directory+path_data.get_program_name()+'_o.pth.json'
    opt_path_data.output_json(output_file)

    merge_path(output_file)


if __name__ == "__main__":
    optimize('../case/herbie/cos2/cos2.pth')

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
