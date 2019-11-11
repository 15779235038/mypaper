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
import rumor_centrality
import jordan_centrality


class Single_source:
    def __init__(self):
        pass



    '''
    多个独立观察图，然后进行联合单源定位。
    '''

    def mutiple_Observation(self, infectG, siG, siG2, source_ture):
        # 将图构造成两个list，一个是感染点list，一个是感染和它的邻居点构造成的list
        infect_node = []
        infect_neighbour_list = []
        print(infectG.number_of_nodes())
        # random_node = random.choice(list(siG.nodes()))
        # subinfectG = nx.bfs_tree(siG, source=random_node)
        subinfectG = siG
        # who_infected =  [[] for i in range(infectG.number_of_nodes())]
        # 找出最大的id数目。
        maxs = 0
        for node_index in list(infectG.nodes):
            if node_index > maxs:
                maxs = node_index
        print('maxs', maxs)
        for node in list(subinfectG.nodes()):
            infect_node.append(node)
        who_infected = [[] for i in range(maxs + 1)]

        i = 0
        for node_temp in infect_node:
            neighbour_list = list(nx.neighbors(subinfectG, node_temp))
            neighbour_list_index = []
            for neighbour in neighbour_list:
                neighbour_list_index.append(infect_node.index(neighbour))
            who_infected[i] = neighbour_list_index
            i += 1

        print('infect_node', infect_node)
        print('who_infected', who_infected)
        rumor_center_object = rumor_centrality.rumor_center()

        rumor_center, center = rumor_center_object.rumor_centrality(who_infected)

        print('rumor_center', rumor_center)
        print('center', center)
        return [infect_node[rumor_center]]

    '''
      设计本类用来做单源  定位。
    # '''

    def main(self, filename):

        # #拿到图
        initG = commons.get_networkByFile(filename)
        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG, T = commons.propagation1(max_sub_graph, source_list)
        infectG1, T = commons.propagation1(max_sub_graph, source_list)
        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
        # 将在这里进行单源测试。

        subinfectG1 = commons.get_subGraph_true(infectG1)

        # 多个观察点
        result_node = self.mutiple_Observation(infectG, subinfectG,subinfectG1, source_list[0])







        print('真实源是', source_list[0])
        print('预测源是', result_node[0])
        distance = nx.shortest_path_length(subinfectG, source=source_list[0], target=result_node[0])
        print('结果是', distance)
        return distance


'''


'''
import time

if __name__ == '__main__':
    test = Single_source()
    sum = 0
    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')
    # initG = commons.get_networkByFile(filename)
    # filname = '../../../data/4_regular_graph_3000_data.txt'
    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')
    # filname = '../../../data/CA-GrQc.txt'
    filname = '../../../data/3regular_tree9.txt'
    # method ='distan+ covage'
    # method = 'jardan_center'
    # method ='distance'
    method = '乔丹中心性'

    for i in range(0, 20):
        tempresult = test.main(filname)
        sum += tempresult  # 跑实验
        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果是   ' + str(tempresult) + '      数据集' + '方法' + str(method) + str(filname) + '\n')
    with open('result.txt', "a") as f:
        f.write('数据集' + str(filname) + '方法' + str(method) + '总结果   ' + str(sum / 20) + '\n')
        f.write('\n')
    print('result', sum / 20)
    print(sum / 20)




