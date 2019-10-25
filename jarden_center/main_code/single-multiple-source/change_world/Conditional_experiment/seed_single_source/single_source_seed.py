import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community
import random
import math
import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict
from random import sample
import sys
import copy
import Partion_common
import commons


class Seed_single_source:
    def __init__(self):
        pass



    '''
    第一种覆盖率计算，
    公式为： a点=  a周围所有的点周围被感染的点数目 / 离这个a点距离  
    我们提出一种新的单源定位方法，基于覆盖率计算的。
    统计每个点对于整个感染图的每个点计算公式，包括距离中心和覆盖率中心的综合计算方式。
    公式等于覆盖率/距离,越大越好。

    思路：从每个点计算一次djstra方法，统计距离。
    传入的是原始图
    
    效果：在树上效果好。

    '''

    def single_source_bydistance_coverage(self, infectG, subinfectG, true_source):
        sort_dict = commons.partion_layer_dict(infectG, 10)  # 分层
        print('sort_list', sort_dict)
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, source=node, weight='weight')
            for othernode, ditance in length_dict.items():
                lens_degree = len(list(nx.neighbors(infectG, othernode)))
                node_import += sort_dict[othernode] * lens_degree / (ditance + 1)
            node_cal.append([node, node_import ])
        sort_list = sorted(node_cal, key=lambda x: x[1], reverse=True)
        print(sort_list)
        # print('在的', [x[0] for x in sort_list[:100] if x[0] == true_source])
        #只需要返回在你排序的集合中，源点在第几位就可以了。
        for index in range(0,len(sort_list)):
            if true_source == sort_list[index][0]:
                return index



    '''
       第2种覆盖率计算，
       公式为： a点=  a周围所有的点覆盖率 / 离这个a点距离  
       我们提出一种新的单源定位方法，基于覆盖率计算的。
       统计每个点对于整个感染图的每个点计算公式，包括距离中心和覆盖率中心的综合计算方式。
       公式等于覆盖率/距离,越大越好。

       思路：从每个点计算一次djstra方法，统计距离。
       传入的是原始图
       效果：在树上效果好。
       '''
    # 种子节点的看看都在那里
    def single_source_bydistance_coverage_SECOND(self, infectG, subinfectG, true_source):
        sort_dict = commons.partion_layer_dict(infectG, 10)  # 分层
        print('sort_list', sort_dict)
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode, ditance in length_dict.items():
                lens_degree = len(list(nx.neighbors(infectG, othernode)))
                node_import += sort_dict[othernode]  / (ditance + 1)
            node_cal.append([node, node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1], reverse=True)
        print(sort_list)
        # print('在的', [x[0] for x in sort_list[:100] if x[0] == true_source])
        # 只需要返回在你排序的集合中，源点在第几位就可以了。
        for index in range(0, len(sort_list)):
            if true_source == sort_list[index][0]:
                return index




    #单源种子节点，利用消息传播算法。当有接受到全部节点的1/n的节点出现时。是effect
    #节点。某些点可以最早接受到所有源点的点。














    #种子节点还有呢？




    '''
      #设计本类用来做单源定位。
    '''

    def main(self, filename,method):

        # #拿到图
        initG = commons.get_networkByFile(filename)
        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG = commons.propagation1(max_sub_graph, source_list)
        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
        # 将在这里进行种子节点覆盖。
        ''' 第1种，就是coverage/distance'''
        func = getattr(self,method)
        sort_partion = func(infectG, subinfectG, source_list[0])
        return sort_partion


'''


'''
import time

if __name__ == '__main__':
    test = Seed_single_source()
    sum = 0
    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')

    # initG = commons.get_networkByFile(filename)
    filname = '../../../data/3regular_tree9.txt'

    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')

    # filname = '../../../data/CA-GrQc.txt'

    # method = 'distan+ covage'
    # method = 'jardan_center'
    # method ='distance'
    # method= 'single_source_bydistance_coverage_SECOND'
    method='single_source_bydistance_coverage'


    for i in range(0, 20):
        tempresult = test.main(filname,method)


        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果是   ' + str(tempresult) + '      数据集' + '方法' + str(method) + str(filname) + '\n')

    print(sum)




