#!/usr/bin/python
# -*- coding:utf-8 -*-

import json

# 以step为步长对输入区间[start, end]进行划分，并将结果输出 
def divideInputSpace(varNum, start, end, prec):

    d1 = []
    dn = []

    i = 0
    step = 10**(-prec) 
    while (start+i*step < end):
        d1.append([[round(start+i*step, prec), round(start+(i+1)*step, prec)]])
        i = i + 1
        
    dn = list(d1)
    for _ in range(varNum-1):
        dt = []
        for i in dn:
            for j in d1:
                dt.append(list(i) + j)
        dn = list(dt)


    '''
    output = {}
    output['varNum'] = varNum 
    output['intervals'] = dn

    with open(outputFile, 'w') as f:
        json.dump(output, f, indent=4)
    '''

    return dn


# 计算每个变量的范围表示的N维空间的所有顶点，例如 x = [1, 2], y = [2, 4] 对应二维空间中的4个顶点 (1, 2) (1, 4) (2, 2) (2, 4)
def interval2Points(interval):

    varNum = len(interval)
    points = [[interval[0][0]], [interval[0][1]]]
    i = 1
    while (i < len(interval)):
        t = []
        for point in points:
            t.append(point + [interval[i][0]])
            t.append(point + [interval[i][1]])
        points = list(t)
        i += 1
        
    return points


def stableAnalysis(varNum, path, constrain):
    
    start = 0
    end = 1
    prec = 2 # step = 1e-2 

     
    intervals = divideInputSpace(varNum, start, end, prec)
    points = [interval2Points(interval) for interval in intervals]
     

    for i in range(len(intervals)):
        print (intervals[i])
        print (points[i])
    
    

stableAnalysis(2,2,2)

