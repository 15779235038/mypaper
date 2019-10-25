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
import  plot_main
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
        self.judge_data(subinfectG)

        # single_source = commons.revsitionAlgorithm_singlueSource(subinfectG)
        distance_iter = nx.shortest_path_length(subinfectG)
        everynode_distance = []
        for node, node_distance in distance_iter:
            # print(node_distance)
            sort_list = sorted(node_distance.items(), key=lambda x: x[1], reverse=True)
            # print('sort_list',sort_list)
            everynode_distance.append([node, sort_list[0][0], sort_list[0][1]])
        # print('everynode_idstance',everynode_distance)
        sort_every_distance = sorted(everynode_distance, key=lambda x: x[2], reverse=True)
        print('sort_every_distance',sort_every_distance)

        #从两个最远的点进行BFS直到找到单源的位置。

        # print(nx.shortest_path_length(infectG,source=single_source[0],target=sort_every_distance[0][0]))
        # print(nx.shortest_path_length(infectG, source=single_source[0], target=sort_every_distance[0][1]))
        #
        # print(nx.shortest_path_length(infectG, source=single_source[0], target=sort_every_distance[1][0]))
        # print(nx.shortest_path_length(infectG, source=single_source[0], target=sort_every_distance[1][1]))
        #
        # print(nx.shortest_path_length(infectG, source=single_source[0], target=sort_every_distance[2][0]))
        # print(nx.shortest_path_length(infectG, source=single_source[0], target=sort_every_distance[2][1]))



        # #根据最远得点，把我们的那个啥，分区，然后利用分区点进行单源定位。。
        node_twolist = [[], []]
        lengthA_dict = nx.single_source_bellman_ford_path_length(subinfectG, sort_every_distance[0][0],
                                                                 weight='weight')
        lengthB_dict = nx.single_source_bellman_ford_path_length(subinfectG, sort_every_distance[0][1],
                                                                 weight='weight')
        for node in list(subinfectG.nodes):
            if lengthA_dict[node] > lengthB_dict[node]:  # 这个点离b近一些。
                node_twolist[1].append(node)
            elif lengthA_dict[node] < lengthB_dict[node]:
                node_twolist[0].append(node)
            # else:
            #     node_twolist[0].append(node)
            #     node_twolist[1].append(node)
        print('len(node_twolist[0]', len(node_twolist[0]))
        print('len(node_twolist[1]', len(node_twolist[1]))
        # 边界点。
        bound_list = []
        for node_temp in list(infectG.nodes()):
            # print(node_temp)
            if infectG.node[node_temp]['SI'] == 2:
                neighbors_list = list(nx.neighbors(infectG, node_temp))
                neighbors_infect_list = [x for x in neighbors_list if infectG.node[x]['SI'] == 2]
                if len(neighbors_list) != 1 and len(neighbors_infect_list) == 1:
                    # if  len(neighbors_infect_list) == 1:
                    bound_list.append(node_temp)



        print('boundelist', len(bound_list))

        print('len(kjlk)',len([x for x in bound_list if x in list(subinfectG.nodes())]))
        left=[x for x in bound_list if x  in node_twolist[0] ]
        right =[x for x in bound_list if x  in node_twolist[1] ]

        print('left',left)
        print('right',right)


        left_source=commons.revsitionAlgorithm_singlueSource_receive(subinfectG,left)
        right_source = commons.revsitionAlgorithm_singlueSource_receive(subinfectG, right)
        if set(left) < set(list(subinfectG.nodes())):
            print('left在感染点里面啊')
        if set(right) < set(list(subinfectG.nodes())):
            print('left在感染点里面啊')
        distance=commons.cal_distance(infectG,[left_source[0],right_source[0]],source_list)


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
    # filname = '../data/3regular_tree9.txt'
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




