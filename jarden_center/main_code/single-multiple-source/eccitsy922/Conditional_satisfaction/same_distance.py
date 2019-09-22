#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/21 12:15 下午

# @Author  : baozhiqiang

# @File    : same_distance.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************

import numpy as np
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
import  commons
print(commons)

'''
思路：
  1 生成传播子图，
  2 使用多种传播子图中心点，进行BFS。
  3 判断真实源点是否集中于BFS的某一层。

'''


class Satisfaction:
    def __init__(self):
       pass

    def  main(self):
        initG = commons.get_networkByFile('../../data/CA-GrQc.txt')
        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)

        source_list = commons.product_sourceList(max_sub_graph, commons.fix_number_source)
        infectG = commons.propagation1(initG, source_list)
        subinfectG = commons.get_subGraph(infectG)
        #求解中心性
        pre = '../data_center/'
        last = '.txt'
        filname = 'CA-GrQc'
        center_list = commons.get_center_list(subinfectG)
        print('center_list', center_list)
        dfs_result_dict = defaultdict(list)
        #对每个节点都做BFS，从而判断真实源点在BFS那一层。
        result = []
        for center in center_list:
            temp = []
            # commons.test_BFS_node(subinfectG, source = center,)
            dfs_result_dict = commons.test_BFS_node(subinfectG, source_node=center, depth = 4)
            print('dfs_result_dict', dfs_result_dict)
            for source in source_list:
                for depth, depth_list in dfs_result_dict.items():
                    if source in depth_list:
                        temp.append([center, source, depth])
            result.append(temp)
        print(result)
        variance_list = []
        #使用方差计算。
        for every_ecc in result:
             distemp =[i[2] for i in every_ecc]  #收集每种中心性的方差，方差越小越好。
             # 求标准差
             arr_std = np.std(distemp, ddof=1)
             variance_list.append(arr_std)
        print('variancelist，每次的结果',variance_list)
        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(variance_list).replace('[','').replace(']','') + '\n')
        return variance_list

    '''
    
    跑50次，看下方差平均差。评判那种中心性好
    '''
    def   practice(self):
        distance =[ ]
        for i in range(50):
            temp = self.main()

    def getdata(self):
        import sys
        result = []
        with open('result.txt', 'r') as f:
            for line in f:
                temp = []
                line = line.replace('[','').replace(']','').replace(' ','')
                for i in list(line.strip('\n').split(',')):
                    temp.append(float(i))
                result.append(temp)

        distance1 = [i[0] for i in result]
        distance2 = [i[1] for i in result]
        distance3 = [i[2] for i in result]
        distance4 = [i[3] for i in result]
        distance5 = [i[4] for i in result]
        print('distance1', distance1)
        print('distance2', distance2)
        print('distance3', distance3)

        print('first', np.mean(distance1))
        print('second', np.mean(distance2))
        print('third', np.mean(distance3))
        print('four', np.mean(distance4))
        print('five', np.mean(distance5))

        # print(result)




if __name__ == '__main__':

    test = Satisfaction()
    test.getdata() #判断是否公平
    # test.practice()   #跑实验