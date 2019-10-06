#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/24 3:58 下午

# @Author  : baozhiqiang

# @File    : coverage_mulSource.py

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
        print('两个节点的距离',nx.shortest_path_length(max_sub_graph,source= source_list[0],target=source_list[1]))
        #看下分区效果行不行，传播两次，就好了，
        # 一个是SI为2，一个是SI为3。交叉区域为4。
        infectG = commons.propagation_dif_sigl(max_sub_graph, source_list[0], 3)    #3表示一个源点。
        infectG_other = commons.propagation_dif_sigl(infectG, source_list[1], 4)  # 4标示表示一个源点。 如果两个标示重合，
        #那就取5

        #提起其中某些节点的东西，提取3，4，5
        node_list3 = []
        node_list4 = []
        node_list5 = []
        for nodes in  list(infectG_other.nodes):
            if infectG_other.node[nodes]['SIDIF']==3:
                node_list3.append(nodes)
            elif  infectG_other.node[nodes]['SIDIF']==4:
                node_list4.append(nodes)
            elif infectG_other.node[nodes]['SIDIF']==5:
                node_list5.append(nodes)
        node_list3.extend(node_list5)
        node_list4.extend(node_list5)

        print('first——node_list3',len(node_list3))
        print('second——node_list4',len(node_list4))

        subinfectG = commons.get_subGraph(infectG_other) #只取感染点，为2表示
        '''
        思路，单源定位，覆盖率效果较好的是不是真的拟合了传播子图。
        '''
        singleRegionList = list(subinfectG.nodes)
        #进行覆盖率走，并进行jaya算法。
        results = commons.jayawith_dynami_H(infectG, singleRegionList, 2, [4, 5, 6], singleRegionList)
        print(results)

        node_coverage1 = []
        node_coverage2 = []

        # #计算两个传播区域的重合区域。

        node_coverage1.extend(list(nx.bfs_tree(infectG, source=results[0][0], depth_limit=results[1])))
        node_coverage2.extend(list(nx.bfs_tree(infectG, source=results[0][1], depth_limit=results[1])))

        #判断那个跟那个拟合。就看BFS树源点跟那个近就可以了。就认为是那个。
        lengtha =nx.shortest_path_length(infectG, source=results[0][0], target=source_list[0])
        lengthb = nx.shortest_path_length(infectG, source=results[0][1], target=source_list[0])
        print('length1',lengtha)
        print('lengthb',lengthb)
        if  lengtha >  lengthb:
            a= [x for x in node_list3 if x in node_coverage2]
            print('len(a)', len(a))
            print(len(a)/len(node_list3))

            b = [x for x in node_list4 if x in node_coverage1]
            print('len(b)',len(b))
            print(len(b)/len(node_list4))

            print('失败匹配')
            c = [x for x in node_list3 if x in node_coverage1]
            print('len(c)', len(c))
            print(len(c) / len(node_list3))
            d = [x for x in node_list4 if x in node_coverage2]
            print('len(c)', len(d))
            print(len(d) / len(node_list4))

        else:
            a = [x for x in node_list3 if x in node_coverage1]
            print('len(a)', a)
            print(len(a) / len(node_list3))
            b = [x for x in node_list4 if x in node_coverage2]
            print('len(b)', b)
            print(len(b) / len(node_list4))

            print('失败匹配')
            c = [x for x in node_list3 if x in node_coverage2]
            print('len(c)', len(c))
            print(len(c) / len(node_list3))
            d = [x for x in node_list4 if x in node_coverage1]
            print('len(c)', len(d))
            print(len(d) / len(node_list4))




        #测试下覆盖率是否真实。
        # print('souce       target',[source_list[0],results[0][0]])
        # print('result',nx.shortest_path_length(infectG,source=source_list[0],target=results[0][0]))
        # return nx.shortest_path_length(infectG,source=source_list[0],target=results[0][0])






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
            distance_all += temp
        with open('result_coverage.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('总结果'+str(distance_all/30) + '\n')
        return distance_all
        # self.plot(x_list, y_list)
        # print(result)

'''

这个文件是用来看你的分区到底行不行。
'''
if __name__ == '__main__':
    test = Satisfaction()

    test.practice()   #跑实验







