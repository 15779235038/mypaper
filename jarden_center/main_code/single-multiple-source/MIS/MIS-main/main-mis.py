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

    def ContractDict(self,dir, G):
        with open(dir, 'r') as f:
            for line in f:
                line1 = line.split()
                G.add_edge(int(line1[0]), int(line1[1]))

        for edge in G.edges:
            # G.add_edge(edge[0], edge[1], weight=1)
            randomnum = random.random()
            G.add_edge(edge[0], edge[1], weight=self.effectDistance(randomnum))

        return G

    import math

    def effectDistance(self,probily):
        return 1 - math.log(probily)

    def sigmoid(self,num):
        sig_L = 0
        sig_L = (1 / (1 + np.exp(-num)))
        return sig_L

    def disEffectDistance(self,weight):
        return math.pow(2, (1 - weight))

    def Normalization(self,x):
        return [(float(i) - min(x)) / float(max(x) - min(x)) for i in x]




    def findmultiplesource(self,infectionG, subinfectG, sourceNumber=2 ):
        # 首先需要判断是否多源。不断找源点去对这个区域。
        tempGraph = nx.Graph()
        tempGraph = subinfectG
        tempGraphNodelist = []
        for node in list(tempGraph.nodes):
            tempGraphNodelist.append(node)
        print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
        print('这个感染区域的传播图节点个数')
        print(tempGraph.number_of_nodes())
        Alternativenodeset = list(tempGraph.nodes())  # 备选集合。
        print('tempgraph的所有点数' + str(len(Alternativenodeset)))
        minCoverlist = []
        print('在源点在' + str(sourceNumber) + '个数的情况下')
        # print('在h为' + str(h) + '的情况下')
        # 计算图的拉普拉斯
        k = 1
        sourceNum = 2
        # while 1:
        minCoverlist = []
        print('在源点在' + str(sourceNum) + '个数的情况下')
        # print('在h为' + str(h) + '的情况下')

        #基于k-means的方法。
        if sourceNum == 2:
            partion_region =[]
            #选择距离最远的点。
            distance_iter=nx.shortest_path_length(subinfectG)
            everynode_distance = []
            for node,node_distance  in distance_iter:
                # print(node_distance)
                sort_list = sorted(node_distance.items(), key=lambda x: x[1], reverse=True)
                # print('sort_list',sort_list)
                everynode_distance.append([node,sort_list[0][0],sort_list[0][1]])
            # print('everynode_idstance',everynode_distance)
            sort_every_distance =sorted(everynode_distance,key = lambda  x:x[2],reverse=True)
            # print(sort_every_distance)
            node_twolist = [[],[]]
            lengthA_dict = nx.single_source_bellman_ford_path_length(subinfectG, sort_every_distance[0][0], weight='weight')
            lengthB_dict = nx.single_source_bellman_ford_path_length(subinfectG, sort_every_distance[0][1], weight='weight')
            for node in list(subinfectG.nodes):
                if lengthA_dict[node] > lengthB_dict[node]:  # 这个点离b近一些。
                    node_twolist[1].append(node)
                elif lengthA_dict[node] < lengthB_dict[node]:
                    node_twolist[0].append(node)
                else:
                    node_twolist[0].append(node)
                    node_twolist[1].append(node)
            print('len(node_twolist[0]',len(node_twolist[0]))
            print('len(node_twolist[1]',len(node_twolist[1]))
            return node_twolist












    def main(self,filename):
        # #拿到图
        # subGraph=self.get_Graph('../Propagation_subgraph/many_methods/result/chouqu.txt')

        # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
        # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
        # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')

        initG = commons.get_networkByFile(filename)
        # initG = commons.get_networkByFile('../../../data/4_regular_graph_3000_data.txt')

        # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')

        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 2)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG = commons.propagation1(max_sub_graph, source_list)

        # subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
        single_Source_detection_object = single_Source_detection.Single_source()

        '''
        底下将是所有的步骤组合操作。目前是2源的。
        1  抽取子图操作
        2  分区
        3 分别多源定位
        '''

        # 1  抽取子图操作，共有3种抽取子图操作。我们选择那3种呢?
        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。

        '''''''# 2 分区，分区的太多了，我们看看那种好。'''

        result=self.findmultiplesource(infectG,subinfectG,sourceNumber=2)

        result_source_list =[]
        for  community in result:
            subsubinfectG = nx.Graph()
            for edge in list(subinfectG.edges()):
                if edge[0] in community and (edge[1] in community):
                    subsubinfectG.add_edge(edge[0], edge[1])
            # 看下图连通吗。
            maxsubsubinfectG = self.judge_data(subsubinfectG)
            # 开始单源定位了。
            '''jar center'''
            source_node = single_Source_detection_object.revsitionAlgorithm_singlueSource(maxsubsubinfectG)
            # source_node = single_Source_detection_object.single_source_bydistance_coverage(infectG, maxsubsubinfectG)
            result_source_list.append(source_node[0])

        distance = commons.cal_distance(max_sub_graph, source_list, result_source_list)


        return distance


import time

if __name__ == '__main__':
    test = Mutiple_source()
    sum = 0

    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')

    # initG = commons.get_networkByFile(filename)
    # initG = commons.get_networkByFile('../../../data/4_regular_graph_3000_data.txt')

    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')

    # filname = '../../data/4_regular_graph_3000_data.txt'
    filname = '../../data/CA-GrQc.txt'
    # filname = '../../data/facebook_combined.txt'

    method = 'mis+反转算法'
    # method = 'mis+dis+coverage'
    for i in range(0, 20):
        tempresult = test.main(filname)
        sum += tempresult  # 跑实验
        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('数据集'+str(filname)+'方法'+method+'每一步的结果' + str(tempresult) + '\n')
    with open('result.txt', "a") as f:
        f.write('数据集'+str(filname) + '总结果' + str(sum / 20) + '\n')
        f.write('\n')
    print(sum / 20)




