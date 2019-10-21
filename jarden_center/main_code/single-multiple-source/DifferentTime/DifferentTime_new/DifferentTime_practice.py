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

    from itertools import combinations

    def listFlatten(self,src):
        tmp = []
        for i in src:
            if type(i) is not list:
                tmp.append(i)
            else:
                tmp.extend(self.listFlatten(i))
        return tmp

    def Parttion_Different_Time(self, subinfectG, sourceNumber=2 ):

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

        resultListAll = []
        sourceBFS = []
        for h in range(2,11):
            # 随机找两个源，开始
            sourcePartition = []
            randomSource = []
            for number in range(0, sourceNumber):
                randomSource.append(random.choice(Alternativenodeset))
                sourcePartition.append([])
            for index in range(len(sourcePartition)):
                sourcePartition[index].append(randomSource[index])

            # print(sourcePartition)  # 3个区域划分完毕

            # sourceBFS = []
            # 那么现在根据增大h吧，让我看看结果。增大h，然后构建BFS树。
            for source in randomSource:
                sourceBFS.append(list(nx.bfs_tree(tempGraph, source=source, depth_limit=h).nodes))

            # 然后这sourceBFS包括所有的这两个点构成h的list了。求个合集，跟总的求差集。把差的重新分配好。
            unionList = list(set(self.listFlatten(sourceBFS)))
            # print('两个BFS的合集的个数为' + str(len(unionList)))
            difSet = list(set(Alternativenodeset).difference(set(unionList)))
            print ('两个bfs和整个图差集的个数为'+str(len(difSet)))

            for node in difSet:  # 针对差集重新分配
                # 分别计算到两个源的距离。
                lengthlist = []
                for index1 in range(0, sourceNumber):
                    lengthlist.append([index1, randomSource[index1], node,
                                       nx.shortest_path_length(tempGraph, source=node, target=randomSource[index1])])
                resulttemp = sorted(lengthlist, key=lambda x: (x[3]))
                # print('输出关于这个东西的距离集合看看')
                # print(resulttemp)
                # 加入第一个队列中。

                # print ('-------------------')
                # print ('查看社区数目'+str(len(sourceBFS)))
                sourceBFS[resulttemp[0][0]].append(node)


            for singlePartition in sourceBFS:  # 对每个分区求jarden  center
                source1G = nx.Graph()  # 构建新的单源传播圆出来
                for edge in tempGraph.edges:
                    if edge[0] in singlePartition and edge[1] in singlePartition:
                        source1G.add_edge(edge[0], edge[1])

        return sourceBFS






    def main(self):
        # #拿到图
        # subGraph=self.get_Graph('../Propagation_subgraph/many_methods/result/chouqu.txt')

        # initG = commons.get_networkByFile('../data/CA-GrQc.txt')
        # initG = commons.get_networkByFile('../data/3regular_tree1000.txt')
        initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')

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
        底下将是所有的步骤组合操作。目前是2源的。
        1  抽取子图操作
        2  分区
        3 分别多源定位
        '''

        # 1  抽取子图操作，共有3种抽取子图操作。我们选择那3种呢?
        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。

        '''''''# 2 分区，分区的太多了，我们看看那种好。'''

        '''2.1  Different'''

        result =self.Parttion_Different_Time(infectG, sourceNumber=2)
        print('result',len(result))
        single_Source_detection_object = single_Source_detection.Single_source()
        print('result', result)
        # 对每一个感染的点建图，用真实的建成一个传播子图
        result_source_list = []







        '''

            3  针对2传回来的多个区域，开始定位源点。
         '''
        for community_node, community in result:
            subsubinfectG = nx.Graph()
            for edge in list(subinfectG.edges()):
                if edge[0] in community and (edge[1] in community):
                    subsubinfectG.add_edge(edge[0], edge[1])
            # 看下图连通吗。
            maxsubsubinfectG = self.judge_data(subsubinfectG)
            # 开始单源定位了。

            source_node = single_Source_detection_object.revsitionAlgorithm_singlueSource(maxsubsubinfectG)
            result_source_list.append(source_node[0])

        distance = commons.cal_distance(max_sub_graph, source_list, result_source_list)

        return distance


import time

if __name__ == '__main__':
    test = Mutiple_source()
    sum = 0
    for i in range(0, 20):
        tempresult = test.main()
        sum += tempresult  # 跑实验
        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果' + str(tempresult) + '\n')
    print('result', sum / 20)
    print(sum / 20)




