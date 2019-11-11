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

import single_Source_detection

import  jordan_centrality
class Graph_tree:
    def __init__(self):
        pass



    '''
    1 随机选择一个点构建BFS树，这个树传入我们的函数中，
    计算所有的Dt（u）和Ut=d（u，v）
    2 
    '''

    def  graph_tree(self,infectG,subiG):
        # 将图构造成两个list，一个是感染点list，一个是感染和它的邻居点构造成的list
        infect_node = []
        infect_neighbour_list = []
        print(subiG.nodes())
        random_node = random.choice(list(subiG.nodes()))
        print('random_node',random_node)
        subinfectG = nx.bfs_tree(subiG, source=random_node)
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
            neighbour_list = list(nx.all_neighbors(subinfectG, node_temp))
            neighbour_list_index = []
            for neighbour in neighbour_list:
                neighbour_list_index.append(infect_node.index(neighbour))
            who_infected[i] = neighbour_list_index
            i += 1

        print('infect_node', infect_node)
        print('who_infected', who_infected)

        up_messages = []
        root_node = infect_node.index(random_node)

        print('以root——node为根节点',root_node)
        len_node =infectG.number_of_nodes()
        for i in range(len_node):
            up_messages.append([0, 0])
        jordan_center_object = jordan_centrality.jordan()
        up_message = jordan_center_object.jorden_centrality_upmessage(root_node,who_infected)


        print('up_message',up_message)
        #up_message 中每一个对应我们的infect_node的下标。








    def main(self, filename):

        # #拿到图
        initG = commons.get_networkByFile(filename)
        max_sub_graph = commons.judge_data(initG)
        print('是否是一棵树？', nx.is_tree(max_sub_graph))
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG, T = commons.propagation1(max_sub_graph, source_list)

        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
        # 将在这里进行单源测试。
        '''   第一种，就是jarden center '''
        #
        object_single = single_Source_detection.Single_source()

        self.graph_tree(infectG,subinfectG)

        reverse_node = object_single.revsitionAlgorithm_singlueSource(subinfectG)
        result_node = self.single_source_bound_ture(subinfectG, reverse_node[0], source_list[0])
        print('真实源是', source_list[0])
        print('预测源是', result_node[0])
        distance = nx.shortest_path_length(subinfectG, source=source_list[0], target=result_node[0])
        print('结果是', distance)
        return distance


'''
'''
import time

if __name__ == '__main__':
    test = Graph_tree()
    sum = 0
    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')
    # initG = commons.get_networkByFile(filename)
    # filname = '../../../data/4_regular_graph_3000_data.txt'
    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')
    filname = '../../../../data/CA-GrQc.txt'
    # filname = '../../../../data/3regular_tree9.txt'
    # method ='distan+ covage'
    # method = 'jardan_center'
    # method ='distance'
    method = '图转树'

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




