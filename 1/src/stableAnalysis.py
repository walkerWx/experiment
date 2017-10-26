#!/usr/bin/python
# -*- coding:utf-8 -*-

import json

# 以step为步长对输入区间[start, end]进行划分，并将结果输出 
def divideInputSpace(varNum, start, end, prec, outputFile):

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


    output = {}
    output['varNum'] = varNum 
    output['intervals'] = dn

    with open(outputFile, 'w') as f:
        json.dump(output, f, indent=4)













def stableAnalysis()
