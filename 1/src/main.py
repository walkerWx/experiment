#!/usr/bin/python
# -*- coding:utf-8 -*-

import copy
import os
import subprocess
import logging

from mergePath import *
from stableAnalysis import *
from transform import *

import stableAnalysis



# 优化过程的主要逻辑
def optimize(path_file):

    path_data = PathData(path_file)
    paths = path_data.get_paths()
    constrains = [p.get_constrain() for p in paths]


    # 实验用例所在路径
    casedir = ''
    if path_file.rfind('/') != -1:
        casedir = path_file[:path_file.rfind('/')+1]
    else:
        casedir = '.'

    # 优化后的path，除了路径信息外，其余信息与原path文件相同，路径信息为我们对该path文件中的路径进行优化后添加进去的
    opt_path_data = copy.deepcopy(path_data)

    # 默认的任意精度实现
    for pth in opt_path_data.get_paths():
        pth.set_implement(REALTYPE)

    # generate random points and write them to 'random_points.txt' for later analysis use
    points = list()  # 输入点
    while len(points) < 250:  # 250个随机输入

        values = list()
        types = list()
        for v in path_data.get_input_variables():
            t = path_data.get_variable_type(v)
            types.append(t)
            if t == 'decimal':
                values.append(double2binary(generate_random_double()))
            elif t == 'integer':
                values.append(int2binary(generate_random_int(1, 10000)))

        point = stableAnalysis.Point(values, types)

        # 排除不满足任意一条路径约束的输入
        if not functools.reduce(lambda x, y: x or y, [satisfy(point, path_data.get_input_variables(), c) for c in constrains]):
            continue
        logging.info(point)
        points.append(point)

    # write random points to file
    points_file = os.path.join(casedir, 'points.txt.rd')
    with open(points_file, 'w') as f:
        for point in points:
            f.write(' '.join(point.values))
            f.write('\n')

    #################
    #   稳定性分析  #
    ################

    point_stability = stable_analysis(path_data)
    # remove points not satisfy any constrain
    point_stability = [x for x in point_stability if functools.reduce(lambda m, n: m or n, [satisfy(x[0], path_data.get_input_variables(), c) for c in constrains])]

    # 将输入点根据路径进行划分
    path_point_stability = dict()
    for p in paths:
        path_point_stability[p] = [ps for ps in point_stability if satisfy(ps[0], path_data.get_input_variables(), p.get_constrain())]

    for pth, pnt_stb in path_point_stability.items():

        points = list()  # 该条路径上的输入点
        unstable_points = set()  # 该条路径上不稳定的点
        point_stable_path = dict()  # 每个点所对应的稳定的路径

        for i in range(len(pnt_stb)):
            points.append(pnt_stb[i][0])
            if pnt_stb[i][1]:  # 原来的路径已经稳定
                point_stable_path[pnt_stb[i][0]] = pth
            else:
                point_stable_path[pnt_stb[i][0]] = None
                unstable_points.add(pnt_stb[i][0])

        print("Stable points and corresponding path")
        for pnt, stb_pth in point_stable_path.items():
            if stb_pth:
                print(str(pnt) + " stable on ", end='\t')
                print(stb_pth.to_json())
        print("Still unstable points:")
        for up in unstable_points:
            print(up)

        ####################
        #   随机代数变换    #
        ###################

        # 等价路径集合
        equal_paths = set()

        # 规则集合
        rules = list()
        rules.append(RULES['ComplexSum1'])
        rules.append(RULES['ComplexSum2'])
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
        rules.append(RULES['Distribution3'])
        rules.append(RULES['TaylorLog'])
        rules.append(RULES['LogMinus'])
        rules.append(RULES['AtanMinus'])

        rules.append(RULES['TanPlus'])
        rules.append(RULES['CosPlus'])
        rules.append(RULES['CommDenominator2'])
        rules.append(RULES['SinPlus'])
        rules.append(RULES['CosSinR'])

        rules.append(RULES['Gamma_0'])
        rules.append(RULES['Gamma_1'])
        rules.append(RULES['Gamma_2'])

        rules.append(RULES['NumeratorFrom3'])
        rules.append(RULES['NumeratorFrom2'])

        # 以rule name @ path json形式记录待应用规则与路径组合
        to_transform = set([x.rule_name+'@'+json.dumps(pth.to_json()) for x in rules])

        # 记录已经应用的规则与路径组合，防止重复应用
        done_transform = set()

        start_ticks = time.time()
        run_ticks = 0
        # while len(equal_paths) < 10 and run_ticks < 20:  # 超时时间设置为10s
        while len(equal_paths) < 20:  # 超时时间设置为10s

            # 待应用规则与表达式组合列表为空或输入域均已稳定则结束随机代数变换
            if not to_transform or not unstable_points:
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
                    # print("[INFO] Can't apply rule [" + rule.rule_name + "] on path " + json.dumps(path.to_json()) + "\n")
                    continue

                if json.dumps(ep.to_json()) in equal_paths:
                    # print("[INFO] New generated path already exists!\n")
                    continue

                equal_paths.add(json.dumps(ep.to_json()))

                print("[INFO] Generate equal path:\t" + json.dumps(ep.to_json()) + " by " + chosen_rule_path + "\n")

                # 原不稳定输入点中，在该条路径下计算稳定的输入点
                # 首先根据新的路径生成float.cpp并编译
                generate_cpp(path_data, [ep], implement_type='float')
                subprocess.call(['make > /dev/null'], shell=True)
                ep_stable_points = [up for up in unstable_points if is_point_stable(up)]

                if ep_stable_points:

                    print("stable points on new path :", end='\t')
                    print(ep.to_json())
                    for p in ep_stable_points:
                        point_stable_path[p] = ep
                        print(p)

                # 去掉已经稳定的
                unstable_points = unstable_points - set(ep_stable_points)

                # 将新产生的路径与规则组合加入到to_transform，同时删除done_transform出现的元素
                to_transform = to_transform | set([x.rule_name+'@'+json.dumps(ep.to_json()) for x in rules]) - done_transform

                # long expressions are normally bad, remove them
                to_transform = set([x for x in to_transform if len(x) < 500])

        print("Stable points and corresponding path")
        for p, sp in point_stable_path.items():
            if sp:
                print(str(p) + " stable on ", end='\t')
                print(sp.to_json())
        print("Still unstable points:")
        for up in unstable_points:
            print(up)

        # 将连续的稳定的并且隶属于统一条路径的输入点形成约束，加入到优化后路径文件
        s = 0
        e = s
        while s < len(points):

            while e+1 < len(points) and point_stable_path[points[e]] == point_stable_path[points[e+1]]:
                e += 1

            # points[s] ~ points[e] 均使用 point_stable_path[points[s]] 的计算过程
            sp = copy.deepcopy(point_stable_path[points[s]])  # 优化后路径

            if sp:
                vname = path_data.get_input_variables()[0]
                vtype = path_data.get_variable_type(vname)
                if vtype == 'decimal':
                    vstart = binary2double(points[s].values[0])
                    vend = binary2double(points[e].values[0])
                elif vtype == 'integer':
                    vstart = binary2int(points[s].values[0])
                    vend = binary2int(points[e].values[0])
                sp.add_constrain(str(vstart) + '<=' + vname)
                sp.add_constrain(vname + '<=' + str(vend))
                sp.set_implement(FLOATTYPE)
                opt_path_data.add_path(sp)

            e += 1
            s = e
    '''
    for path in path_data.get_paths():

        res = stable_analysis_new(path_data, path)
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


       
        # 未找到稳定的等价路径的区间，使用高精度实现
        if unstable_intervals:
            real_path = copy.deepcopy(path)
            real_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], unstable_intervals))
            real_path.set_implement(REALTYPE)
            opt_path_data.add_path(real_path)

        print("[INFO] Print all generated equivalent paths:")
        for ep in equal_paths:
            print(ep)
    '''



    # 稳定性分析结果输出到文件
    points_file = os.path.join(casedir, 'points.txt')
    with open(points_file, 'w') as f:
        for (point, stable) in point_stability:
            f.write(' '.join(point.values))
            f.write(' ')
            f.write(str(stable))
            f.write('\n')

    # 优化后路径信息输出到文件
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


def read_points_file(points_file):
    points = list()
    initial_points_file = open(points_file, 'r')
    for line in initial_points_file:
        if line == '\n':
            continue
        values = line.split(' ')
        types = ['decimal' for i in range(len(values))]
        point = stableAnalysis.Point(values, types)
        logging.info(str(point))
        points.append(point)
    initial_points_file.close()
    return points


def optimize_for_multi_input(path_file, points_file):
    path_data = PathData(path_file)
    paths = path_data.get_paths()
    constrains = [p.get_constrain() for p in paths]

    # 实验用例所在路径
    casedir = ''
    if path_file.rfind('/') != -1:
        casedir = path_file[:path_file.rfind('/') + 1]
    else:
        casedir = '.'

    # 优化后的path，除了路径信息外，其余信息与原path文件相同，路径信息为我们对该path文件中的路径进行优化后添加进去的
    opt_path_data = copy.deepcopy(path_data)

    # 默认的任意精度实现
    for pth in opt_path_data.get_paths():
        pth.set_implement(REALTYPE)

    # generate random points and write them to 'random_points.txt' for later analysis use
    points = read_points_file(points_file) # input points


    # write inout points to file
    points_file = os.path.join(casedir, 'points.txt.rd')
    with open(points_file, 'w') as f:
        for point in points:
            f.write(' '.join(point.values))
            f.write('\n')

    #################
    #   稳定性分析  #
    ################

    unstable_lower_bounds, unstable_upper_bounds, point_stability = stable_analysis2(path_data, points_file)
    # remove points not satisfy any constrain
    point_stability = [x for x in point_stability if functools.reduce(lambda m, n: m or n,
                                                                      [satisfy(x[0], path_data.get_input_variables(), c)
                                                                       for c in constrains])]

    # 将输入点根据路径进行划分
    path_point_stability = dict()
    for p in paths:
        path_point_stability[p] = [ps for ps in point_stability if
                                   satisfy(ps[0], path_data.get_input_variables(), p.get_constrain())]

    for pth, pnt_stb in path_point_stability.items():

        points = list()  # 该条路径上的输入点
        unstable_points = set()  # 该条路径上不稳定的点
        point_stable_path = dict()  # 每个点所对应的稳定的路径

        for i in range(len(pnt_stb)):
            points.append(pnt_stb[i][0])
            if pnt_stb[i][1]:  # 原来的路径已经稳定
                point_stable_path[pnt_stb[i][0]] = pth
            else:
                point_stable_path[pnt_stb[i][0]] = None
                unstable_points.add(pnt_stb[i][0])

        print("Stable points and corresponding path")
        for pnt, stb_pth in point_stable_path.items():
            if stb_pth:
                print(str(pnt) + " stable on ", end='\t')
                print(stb_pth.to_json())
        print("Still unstable points:")
        for up in unstable_points:
            print(up)

        ####################
        #   随机代数变换    #
        ###################

        # 等价路径集合
        equal_paths = set()

        # 规则集合
        rules = list()
        # rules.append(RULES['Midarc'])
        # rules.append(RULES['ComplexSum1'])
        rules.append(RULES['ComplexSum2'])
        # rules.append(RULES['LoopReduce'])
        # rules.append(RULES['LoopReverse'])
        # rules.append(RULES['TaylorCos'])
        # rules.append(RULES['Taylor'])
        # rules.append(RULES['Simplify'])
        # rules.append(RULES['Horner'])
        # rules.append(RULES['SinSinR'])
        # rules.append(RULES['CosPlus'])
        # rules.append(RULES['ExpReduction'])
        # rules.append(RULES['FracPartial'])
        # rules.append(RULES['TaylorExp'])
        # rules.append(RULES['Distribution3'])
        # rules.append(RULES['TaylorLog'])
        # rules.append(RULES['LogMinus'])
        # rules.append(RULES['AtanMinus'])
        #
        # rules.append(RULES['TanPlus'])
        # rules.append(RULES['CosPlus'])
        # rules.append(RULES['CommDenominator2'])
        # rules.append(RULES['SinPlus'])
        # rules.append(RULES['CosSinR'])
        #
        # rules.append(RULES['Gamma_0'])
        # rules.append(RULES['Gamma_1'])
        # rules.append(RULES['Gamma_2'])
        #
        # rules.append(RULES['NumeratorFrom3'])
        # rules.append(RULES['NumeratorFrom2'])

        # 以rule name @ path json形式记录待应用规则与路径组合
        to_transform = set([x.rule_name + '@' + json.dumps(pth.to_json()) for x in rules])

        # 记录已经应用的规则与路径组合，防止重复应用
        done_transform = set()

        start_ticks = time.time()
        run_ticks = 0
        # while len(equal_paths) < 10 and run_ticks < 20:  # 超时时间设置为10s
        while len(equal_paths) < 20:  # 超时时间设置为10s

            # 待应用规则与表达式组合列表为空或输入域均已稳定则结束随机代数变换
            if not to_transform or not unstable_points:
                break

            run_ticks = time.time() - start_ticks

            # 根据每条规则的权重随机选取一条规则
            rule = choose_rule_by_weight(rules)

            # 在待应用规则与路径组合中按规则随机选一条
            candidates = [x for x in to_transform if x.startswith(rule.rule_name + '@')]
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
                    # print("[INFO] Can't apply rule [" + rule.rule_name + "] on path " + json.dumps(path.to_json()) + "\n")
                    continue

                if json.dumps(ep.to_json()) in equal_paths:
                    # print("[INFO] New generated path already exists!\n")
                    continue

                equal_paths.add(json.dumps(ep.to_json()))

                print("[INFO] Generate equal path:\t" + json.dumps(ep.to_json()) + " by " + chosen_rule_path + "\n")

                # get stable area in new path
                # 首先根据新的路径生成float.cpp并编译
                generate_cpp(path_data, [ep], implement_type='float')
                subprocess.call(['make > /dev/null'], shell=True)
                areas_num = len(unstable_lower_bounds)

                generate_cpp(path_data, [ep], implement_type='float')
                subprocess.call(['make > /dev/null'], shell=True)
                ep_stable_points = [up for up in unstable_points if is_point_stable(up)]
                types = ['decimal' for i in range(len(unstable_lower_bounds[0]))]

                for i in range(areas_num):
                    lower_bound_point = stableAnalysis.Point(unstable_lower_bounds[i], types)
                    upper_bound_point = stableAnalysis.Point(unstable_upper_bounds[i], types)
                    if is_point_stable(lower_bound_point) and is_point_stable(upper_bound_point):
                        sp = copy.deepcopy(ep)
                        if sp:
                            parameters_num = len(unstable_lower_bounds[i])
                            vname = path_data.get_input_variables()[0]
                            vtype = path_data.get_variable_type(vname)
                            constraint = ""
                            for k in range(parameters_num):
                                vname = path_data.get_input_variables()[k]
                                vtype = path_data.get_variable_type(vname)
                                if vtype == 'decimal':
                                    vstart = binary2double(lower_bound_point.values[k])
                                    vend = binary2double(upper_bound_point.values[k])
                                elif vtype == 'integer':
                                    vstart = binary2int(lower_bound_point.values[k])
                                    vend = binary2int(upper_bound_point.values[k])
                                sp.add_constrain(str(vstart) + '<=' + vname)
                                sp.add_constrain(vname + '<=' + str(vend))
                            sp.set_implement(FLOATTYPE)
                            opt_path_data.add_path(sp)

    '''
    for path in path_data.get_paths():

        res = stable_analysis_new(path_data, path)
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



        # 未找到稳定的等价路径的区间，使用高精度实现
        if unstable_intervals:
            real_path = copy.deepcopy(path)
            real_path.add_constrain(intervals2constrain(path_data.get_input_variables(), [path_data.get_variable_type(x) for x in path_data.get_input_variables()], unstable_intervals))
            real_path.set_implement(REALTYPE)
            opt_path_data.add_path(real_path)

        print("[INFO] Print all generated equivalent paths:")
        for ep in equal_paths:
            print(ep)
    '''

    # 稳定性分析结果输出到文件
    points_file = os.path.join(casedir, 'points.txt')
    with open(points_file, 'w') as f:
        for (point, stable) in point_stability:
            f.write(' '.join(point.values))
            f.write(' ')
            f.write(str(stable))
            f.write('\n')

    # 优化后路径信息输出到文件
    opt_path_file = os.path.join(casedir, opt_path_data.get_program_name() + '_o.pth.json')
    output_json(opt_path_data.to_json(), opt_path_file)

    ##############
    #   路径合并  #
    ##############
    merge_path(opt_path_file)

if __name__ == "__main__":

    # Herbie case
    # optimize('../case/herbie/sqrtexp/sqrtexp.pth')
    # optimize('../case/herbie/sintan/sintan.pth')
    # optimize('../case/herbie/cos2/cos2.pth')
    # optimize('../case/herbie/2nthrt/2nthrt.pth')
    # optimize('../case/herbie/2log/2log.pth')
    # optimize('../case/herbie/2frac/2frac.pth')
    # optimize('../case/herbie/2cos/2cos.pth')
    # optimize('../case/herbie/2cbrt/2cbrt.pth')
    # optimize('../case/herbie/tanhf/tanhf.pth')
    # optimize('../case/herbie/qlog/qlog.pth')
    # optimize('../case/herbie/logs/logs.pth')
    # optimize('../case/herbie/logq/logq.pth')
    # optimize('../case/herbie/invcot/invcot.pth')
    # optimize('../case/herbie/expq3/expq3.pth')
    # optimize('../case/herbie/expq2/expq2.pth')
    # optimize('../case/herbie/expm1/expm1.pth')
    # optimize('../case/herbie/expax/expax.pth')
    # optimize('../case/herbie/exp2/exp2.pth')
    # optimize('../case/herbie/3frac/3frac.pth')
    # optimize('../case/herbie/2tan/2tan.pth')
    # optimize('../case/herbie/2sin/2sin.pth')
    # optimize('../case/herbie/2atan/2atan.pth')

    # NumeratorFrom2
    # optimize('../case/herbie/quadp/quadp.pth')
    # optimize('../case/herbie/quadm/quadm.pth')
    # optimize('../case/herbie/quad2p/quad2p.pth')
    # optimize('../case/herbie/quad2m/quad2m.pth')

    # NumeratorFrom3
    # optimize('../case/herbie/2sqrt/2sqrt.pth')
    # optimize('../case/herbie/2isqrt/2isqrt.pth')

    # midarc
    # optimize('../case/herbie/midarc/midarc.pth')
    # optimize('../case/iRRAM/midarc/midarc_real.pth')
    # optimize_for_multi_input('../case/iRRAM/midarc/midarc_real.pth', '../case/iRRAM/midarc/midarc_points.txt')
    # optimize_for_multi_input('../case/herbie/midarc/midarc_real.pth', '../case/herbie/midarc/midarc_points.txt')
    # iRRMA case
    # optimize('../case/iRRAM/analytic/analytic.pth')
    # optimize('../case/iRRAM/e_example/e_example.pth')
    optimize('../case/iRRAM/float_extension/float_extension.pth')
    # optimize('../case/iRRAM/jmmuller/jmmuller.pth')
    # optimize('../case/iRRAM/harmonic/harmonic.pth')
    # optimize('../case/iRRAM/gamma/gamma.pth')






'''
mergePath('../case/midarc/midarc.opt.pth')
optimize('../case/analytic/analytic.pth')
mergePath('../case/analytic/analytic.opt.pth')

#path_file = sys.argv[1]
#optimize(path_file)
# optimize('../case/e_example/e_example.pth')
# optimize('../case/analytic/analytic.pth')
# optimize('../case/midarc/midarc.pth')
optimize('../case/float_extension/float_extension.pth.bak')
# optimize('../case/jmmuller/jmmuller.pth')
# optimize('../case/gamma/gamma.pth')
'''
