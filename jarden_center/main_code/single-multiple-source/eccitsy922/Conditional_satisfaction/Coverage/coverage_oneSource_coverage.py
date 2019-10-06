#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/24 3:57 下午

# @Author  : baozhiqiang

# @File    : coverage_oneSource_coverage.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************



import numpy as np
import matplotlib.pyplot as plt

import random
import math
import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict
from random import sample
import sys

sys.path.append('mypaper/mypaper/jarden_center/main_code/single-multiple-source/eccitsy922/commons.py')
print(sys.path)
import commons

# print(commons)

'''
思路：
  1 生成传播子图，
  2 使用多种传播子图中心点，进行BFS。
  3 判断真实源点是否集中于BFS的某一层。

'''
import time


class Satisfaction:
    def __init__(self):
        pass

    def main(self):
        initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
        # initG = commons.get_networkByFile('../../../data/treenetwork3000.txt')

        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)

        source_list = commons.product_sourceList(max_sub_graph, 1)

        # print('查看两源距离')
        # print('distance',nx.shortest_path_length(max_sub_graph,source=source_list[0],target=source_list[1]))
        infectG = commons.propagation1(max_sub_graph, source_list)
        subinfectG = commons.get_subGraph(infectG)

        singleRegionList = list(subinfectG.nodes)
        '''
        思路，单源定位，看看单源定位和覆盖率效果。
        '''
        # 再从真实源点看，真实源点的覆盖率是多少？
        TrueCoverage = commons.jayawith_dynami_H_TrueSource(infectG, source_list, 1, [4,5, 6,7,8,9,10], singleRegionList)
        print('True_Source_Coverage', TrueCoverage)
        #进行覆盖率走，并进行jaya算法。
        results = commons.jayawith_dynami_H(infectG, singleRegionList, 1, [4, 5, 6], singleRegionList)
        print('good_coverage_soucre',results)

        with open('result_coverage_compare.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('覆盖率比较结果，真实源点'+str(TrueCoverage[2]) + '\n')
            f.write('覆盖率比较结果，找到的覆盖率比较好的点'+str(results[2]) + '\n')
            f.write('两者距离   ' + str(nx.shortest_path_length(infectG, source=source_list[0], target=results[0][0])) + '\n')

        # print('souce       target',[source_list[0], results[0][0]])
        # print('result',nx.shortest_path_length(infectG,source=source_list[0],target=results[0][0]))
        # return nx.shortest_path_length(infectG, source=source_list[0], target=results[0][0])








    def plot(self, x_list, y_list, ):
        plt.figure()
        plt.plot(x_list, y_list)
        plt.title('Multiple central measures')
        plt.savefig('first' + ".png")
        # plt.show()
        plt.close()

    '''

    跑50次，看下方差平均差。评判那种中心性好
    '''

    def practice(self):
        distance_all = 0
        for i in range(10):
            temp = self.main()
            # distance_all += temp
        # with open('result_coverage.txt', "a") as f:
        #     # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
        #     f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
        #     f.write('总结果'+str(distance_all/30) + '\n')
        # return distance_all
        # self.plot(x_list, y_list)
        # print(result)

'''


'''
if __name__ == '__main__':
    test = Satisfaction()

    test.practice()   #跑实验




