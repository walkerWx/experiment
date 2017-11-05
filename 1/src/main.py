#!/usr/bin/python
# -*- coding:utf-8 -*-

import json

from mergePath import *
from transform import *
from stableAnalysis import *


def isEqualPathStable(path, constrain):
    return True

# 判断一个表达式在给定约束下是否稳定
def isStable(path, constrain):
    return False 

# 判断一条路径在给定约束下是否在数学意义上不稳定
def isMathUnstable(path, constrain):
    return False

# 优化过程的主要逻辑
def optimize(pthFile):
    # 解析path文件，得到路径抽取所得到的路径与约束 
    with open(pthFile) as f:

        data = json.load(f)
        variableNum = data['variableNum']
        variables = data['variables']
        pathNum = data['pathNum']
        paths = data['paths']
        constrains = data['constrains']


    # 优化后的路劲以及其对应的约束以及实现类型
    optPaths = []
    optConstrains = []
    optType = []

    # 优化后程序两种不同的实现类型：浮点数实现、高精度实现
    FLOATTYPE = 'float'
    REALTYPE = 'real'

    for i in range(pathNum):

        # 路径计算稳定，无需进行优化 
        if (isStable(paths[i], constrains[i])):
            optPaths.append(paths[i])
            optConstrains.append(constrains[i])
            optType.append(FLOATTYPE)
            continue
     
        # 路径在数学意义上计算不稳定，无法进行优化，依然使用高精度实现
        if (isMathUnstable(paths[i], constrains[i])):
            optPaths.append(paths[i])
            optConstrains.append(constrains[i])
            optType.append(REALTYPE)
            continue

         
        # 对于单变量的多项式计算，horner形式总优于其原来的形式 
        if (len(variables) == 1):
            paths[i] = hornerTransform(variables[0], paths[i])

        # analysis the stability of the path, divide the constrain into 3 parts: stable, unstable, unknown
        res = stableAnalysis(variables, paths[i], constrains[i])  

        if (res['stable'] != ''):
            optPaths.append(paths[i])
            optConstrains.append(res['stable'])
            optType.append(FLOATTYPE)

        if (res['unstable'] != ''):

            # transform the path into an equvalent paths set
            equalPaths = generateEqualPath(variables, paths[i])
            print (equalPaths)

            findStable = False
            for j in range(len(equalPaths)):
                # find a stable path in the equvalent paths set
                if (isEqualPathStable(equalPaths[j], res['unstable'])):
                    findStable = True
                    optPaths.append(equalPaths[j])
                    optConstrains.append(constrains[i])
                    optType.append(FLOATTYPE)
                    break
            
            # if we can not find a stable path, we just keep the original multi-precision version
            if (not findStable):
                optPaths.append(paths[i])
                optConstrains.append(constrains[i])
                optType.append(REALTYPE)

    # write optimized paths to file
    outputData = {} 
    outputData['programName'] = data['programName']
    outputData['functionName'] = data['functionName']
    outputData['variables'] = data['variables']
    outputData['pathNum'] = len(optPaths)
    outputData['constrains'] = optConstrains
    outputData['paths'] = optPaths
    outputData['types'] = optType 
    
    outputDirectory = ''
    if (pthFile.rfind('/') != -1):
        outputDirectory = pthFile[:pthFile.rfind('/')+1]
    outputFile = outputDirectory+data['programName']+'.opt.pth'
    print (outputFile)
    print (outputData)

    with open(outputFile, 'w') as f:
        json.dump(outputData, f, indent=4)


'''
optimize('../case/midarc/midarc.pth')
mergePath('../case/midarc/midarc.opt.pth')
'''
optimize('../case/analytic/analytic.pth')
mergePath('../case/analytic/analytic.opt.pth')
