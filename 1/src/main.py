#!/usr/bin/python
# -*- coding:utf-8 -*-

import copy
import os
import subprocess

from mergePath import *
from stableAnalysis import *
from transform import *


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

        # TODO 稳定性分析应该放在此循环外，首先将输入域根据路径划分，再进行优化

        #################
        #   稳定性分析   #
        ################

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

        ####################
        #   随机代数变换    #
        ###################

        # 等价路径集合
        equal_paths = set()

        # 规则集合
        rules = list()
        rules.append(RULES['LoopReduce'])
        rules.append(RULES['LoopReverse'])
        rules.append(RULES['TaylorCos'])
        rules.append(RULES['Taylor'])
        rules.append(RULES['Simplify'])
        rules.append(RULES['Horner'])
        rules.append(RULES['SinSinR'])
        rules.append(RULES['CosPlus'])
        rules.append(RULES['ExpReduction'])
        rules.append(RULES['FracPartial'])
        rules.append(RULES['TaylorExp'])

        # 以rule name @ path json形式记录待应用规则与路径组合
        to_transform = set([x.rule_name+'@'+json.dumps(path.to_json()) for x in rules])

        # 记录已经应用的规则与路径组合，防止重复应用
        done_transform = set()

        start_ticks = time.time()
        run_ticks = 0
        while len(equal_paths) < 10 and run_ticks < 20:  # 超时时间设置为10s

            # 待应用规则与表达式组合列表为空或输入域均已稳定则结束随机代数变换
            if not to_transform or not unstable_intervals:
                break

            run_ticks = time.time() - start_ticks

            # 根据每条规则的权重随机选取一条规则
            rule = choose_rule_by_weight(rules)

            # 在待应用规则与路径组合中按规则随机选一条
            candidates = [x for x in to_transform if x.startswith(rule.rule_name+'@')]
            if not candidates:
                continue
            chosen_rule_path = random.choice(candidates)
            to_transform.remove(chosen_rule_path)
            done_transform.add(chosen_rule_path)

            path = Path(json.loads(chosen_rule_path.split('@')[1]))

            print(chosen_rule_path)

            # 在路径上应用规则所得到的等价路径集合，注意路径应用规则所得到的等价路径可能不止一条，所以这里是个集合，包含了所有可能结果
            eps = [apply_rule_path(path, rule)]

            for ep in eps:

                if not ep:
                    print("[INFO] Can't apply rule [" + rule.rule_name + "] on path " + json.dumps(path.to_json()) + "\n")
                    continue

                if json.dumps(ep.to_json()) in equal_paths:
                    print("[INFO] New generated path already exists!\n")
                    continue

                equal_paths.add(json.dumps(ep.to_json()))

                print("[INFO] Generate equal path:\t" + json.dumps(ep.to_json()) + " by " + chosen_rule_path + "\n")

                # 在该等价计算路径下计算稳定的不稳定输入域
                ep_stable_intervals = filter_stable_interval(path_data, path, ep, unstable_intervals)

                # 将该等价路径与稳定区间加入到结果中
                if ep_stable_intervals:

                    print("stable intervals on path")
                    print(ep_stable_intervals)
                    print(ep.to_json())
                    print("")

                    opt_path = copy.deepcopy(ep)
                    opt_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], ep_stable_intervals))
                    opt_path.set_implement(FLOATTYPE)
                    opt_path_data.add_path(opt_path)

                # 去掉已经稳定的区间
                unstable_intervals = [t for t in unstable_intervals if t not in ep_stable_intervals]

                # 将新产生的路径与规则组合加入到to_transform，同时删除done_transform出现的元素
                to_transform = to_transform | set([x.rule_name+'@'+json.dumps(ep.to_json()) for x in rules]) - done_transform

        # 未找到稳定的等价路径的区间，使用高精度实现
        if unstable_intervals:
            real_path = copy.deepcopy(path)
            real_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], unstable_intervals))
            real_path.set_implement(REALTYPE)
            opt_path_data.add_path(real_path)

        print("[INFO] Print all generated equivalent paths:")
        for ep in equal_paths:
            print(ep)

    # 结果输出到文件
    opt_path_file = os.path.join(casedir, opt_path_data.get_program_name()+'_o.pth.json')
    output_json(opt_path_data.to_json(), opt_path_file)

    ##############
    #   路径合并  #
    ##############
    merge_path(opt_path_file)


# 将一个dict数据结构输出到文件
def output_json(content, file):
    with open(file, 'w') as f:
        json.dump(content, f, indent=2)


# 根据规则权重按权随机去规则
def choose_rule_by_weight(rules):
    weights = [x.weight for x in rules]
    return random.choices(rules, weights)[0]


if __name__ == "__main__":


    # todo
    #optimize('../case/herbie/2cos/2cos.pth')

    # done
    #optimize('../case/iRRAM/jmmuller/jmmuller.pth')
    #optimize('../case/herbie/logq/logq.pth')
    #optimize('../case/herbie/sqrtexp/sqrtexp.pth')
    #optimize('../case/herbie/expq2/expq2.pth')
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
