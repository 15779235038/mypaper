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
import math

import Use_uninfected_node
import Partion_graph
import single_Source_detection


class Mutiple_source:
    def __init__(self):
        pass

    '''
    1 对数据集进行判断。从有几个连通子图，每个数目。返回连通子图个数。
    '''

    def judge_data(self, initG):
        '''
        :param initG:
        :return:  #返回最大子图的源点数据集
        '''
        Gc = nx.Graph()
        Gc = max(nx.connected_component_subgraphs(initG), key=len)
        sum = 0
        count = 0
        for sub_graph in sorted(nx.connected_component_subgraphs(initG), key=len, reverse=True):
            # print(type(sub_graph))
            # print(sub_graph.number_of_nodes())
            sum += sub_graph.number_of_nodes()
            count += 1
        print('count', count)
        if count > 1:
            print('图不连通，单还是返回最大子图')
        print('sum', sum)
        return Gc


    #封装函数，传入传播子图以及两个点按照距离分区。传回两个区域。
    def get_partion(self, subinfecG, two_center_list):
        node_twolist = [[], []]
        lengthA_dict = nx.single_source_bellman_ford_path_length(subinfecG, two_center_list[0],
                                                                 weight='weight')
        lengthB_dict = nx.single_source_bellman_ford_path_length(subinfecG, two_center_list[1],
                                                                 weight='weight')
        for node in list(subinfecG.nodes):
            if lengthA_dict[node] > lengthB_dict[node]:  # 这个点离b近一些。
                node_twolist[1].append(node)
            elif lengthA_dict[node] < lengthB_dict[node]:
                node_twolist[0].append(node)
            else:
                node_twolist[0].append(node)
                node_twolist[1].append(node)
        print('len(node_twolist[0]', len(node_twolist[0]))
        print('len(node_twolist[1]', len(node_twolist[1]))
        return node_twolist










    # 产生大量集合，返回被截断的区域。
    def product_many_region(self, p, t, infectG, subinfetG, true_list):
        # 这里的随便，我就用源点了。
        for i in true_list:
            G_temp = commons.propagation1(infectG, i, number=2)

        pass

    def main(self, filename):
        # #拿到图
        # subGraph=self.get_Graph('../Propagation_subgraph/many_methods/result/chouqu.txt')

        # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
        # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
        initG = commons.get_networkByFile(filename)

        # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
        # initG = commons.get_networkByFile('../../../data/4_regular_graph_3000_data.txt')

        # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')

        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 2)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG = commons.propagation1(max_sub_graph, source_list)

        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。

        '''
        思路：
        1  借助概率p= 0，5以及不同的时间t生成大量的集合。假设知道时间吧。
        2 然后用这些集合去覆盖感染区域，尽可能让blue中点多，而红色区域少。
            这种方法还可以用来确定种子节点的。

        '''

        # 1  抽取子图操作，共有3种抽取子图操作。我们选择那3种呢?
        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
        '''''''# 2 分区，分区的太多了，我们看看那种好。'''
        partion_graph_object = Partion_graph.Partion_graph()
        result = partion_graph_object.other_k_center(infectG, subinfectG, source_list, source_number=2)


        single_Source_detection_object = single_Source_detection.Single_source()
        print('result', result)
        # 对每一个感染的点建图，用真实的建成一个传播子图
        result_source_list = []

        '''

            3  针对2传回来的多个区域，开始定位源点。直到单源定位稳定下来。
         '''
        h_T = 0
        result_source=[]
        result_source_list = []
        while 1:
            result_source_list.clear()
            for community in result:
                subsubinfectG = nx.Graph()
                for edge in list(subinfectG.edges()):
                    if edge[0] in community and (edge[1] in community):
                        subsubinfectG.add_edge(edge[0], edge[1])
                        subsubinfectG.add_node(edge[0],SI=1)
                        subsubinfectG.add_node(edge[1], SI=1)
                # 看下图连通吗。
                maxsubsubinfectG = self.judge_data(subsubinfectG)
                # 开始单源定位了。
                source_node = single_Source_detection_object.revsitionAlgorithm_singlueSource(maxsubsubinfectG)
                # source_node = single_Source_detection_object.single_source_bydistance(maxsubsubinfectG)
                # source_node = single_Source_detection_object.single_source_bydistance_coverage(infectG,maxsubsubinfectG,source_list)

                result_source_list.append(source_node[0])
            result_source.append(result_source_list)
            print('上次的是', result_source[-1])
            print('这次是', result_source_list)
            if sorted(result_source[-1]) == sorted(result_source_list):
                break
            result = self.get_partion(subinfectG, result_source_list)



        distance = commons.cal_distance(max_sub_graph, source_list, result_source_list)
        return distance


import time

if __name__ == '__main__':
    test = Mutiple_source()
    sum = 0

    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')

    # initG = commons.get_networkByFile(filename)
    # initG = commons.get_networkByFile('../../../data/4_regular_graph_3000_data.txt')

    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')

    # filname = '../../../data/4_regular_graph_3000_data.txt'
    filname = '../data/CA-GrQc.txt'
    method = '方法，真实子图+ other_center +  单源定位稳定下来。  '
    for i in range(0, 20):
        tempresult = test.main(filname)
        sum += tempresult  # 跑实验
        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果数据集' + str(filname) + str(tempresult) + '\n')
            f.write(method)
    with open('result.txt', "a") as f:
        f.write('数据集' + str(filname) + '总结果' + str(sum / 20) + '\n')
        f.write(method)
        f.write('\n')
    print('result', sum / 20)
    print(sum / 20)




