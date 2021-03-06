
#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/30 12:41 下午

# @Author  : baozhiqiang

# @File    : single_source.py

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

        source_list = commons.product_sourceList(max_sub_graph, 2)

        print('查看两源距离')
        print('distance',nx.shortest_path_length(max_sub_graph,source=source_list[0],target=source_list[1]))
        infectG = commons.propagation1(max_sub_graph, source_list)
        subinfectG = commons.get_subGraph(infectG)
        '''
        思路，单源定位，看看单源定位效果。
        '''

        test_source_list=commons.revsitionAlgorithm_get_goodnode(subinfectG)
        print('test_soucce_list')
        if set(test_source_list) > set(source_list):
            print('是的，是真子集。')

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
        for i in range(30):
            temp = self.main()

        #
        # with open('result_bfs.txt', "a") as f:
        #     # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
        #     f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
        #     f.write('总结果'+str(distance_all/10) + '\n')
        # return distance_all
        # self.plot(x_list, y_list)
        # print(result)

'''


'''
if __name__ == '__main__':
    test = Satisfaction()

    test.practice()   #跑实验
