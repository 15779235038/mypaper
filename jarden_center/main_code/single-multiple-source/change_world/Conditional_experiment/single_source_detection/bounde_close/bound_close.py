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

import  single_Source_detection
class Single_source_bound:
    def __init__(self):
        pass

    # 在树上做实验，产生源点必须离边界近。大概就是倒数几层的位置
    def  produce_source(self,initG,source_number):
        #从某个树图中产生某个离边界点近的节点。
        #从0出发，找出最长的路径，然后取一半路径长度的为源点。

        length_dict = nx.single_source_bellman_ford_path_length(initG, 0, weight='weight')

        sort_list = sorted(length_dict.items(), key=lambda x: x[1], reverse=True)
        print('最长的为', sort_list[0][1])
        true_source =None
        for node, distance in sort_list:
            if distance == sort_list[0][1]//2:
                true_source = node
        print('实验结果',length_dict[true_source])
        return [true_source]




    #开始定位

    '''
    
    
    
    写着变成反转算法加距离中心了。有问题啊，怎么处理啊。
    '''
    def single_source_bound(self, subinfectG,source_node):
        source_find = None
        temp_node = source_node[0]
        #收集所有边界点，看看结果。
        bounde_list =[]
        for node in list(subinfectG.nodes()):
            if nx.degree(subinfectG,node) ==1:
                bounde_list.append(node)
        while 1:
            neihbour_distanc = []
            for neihbour in list(nx.neighbors(subinfectG,temp_node)):
                distance_all = 0
                length_dict = nx.shortest_path_length(subinfectG, source=neihbour, weight='weight')
                for  bounde_node, distance in length_dict.items():
                     if bounde_node in bounde_list:  #将这个点距离所有边界点最短距离计算进来
                        distance_all += distance
                neihbour_distanc.append([neihbour, distance_all])
            neihbour_sort_list= sorted(neihbour_distanc,key=lambda x:x[1])
            if neihbour_sort_list[0][0] == temp_node:
                source_find = temp_node
                break
            else:
                print('两者为', temp_node)
                print('两者为', neihbour_sort_list[0][0] )
                temp_node = neihbour_sort_list[0][0]
        return [source_find]




    ''' 1
    从这个源点开始，构建定向树，从所有边界点出发，往上回溯。贡献给父节点自己。每个节点存
    着源点的自己子树的边界点个数。
    2
    分层来吧。
    统计所有边界点的位置，然后从别的算法找出来
    '''
    def single_source_bound_ture(self, subinfectG,source_node,true_source):
        Digraph_tree = nx.bfs_tree(subinfectG, source=source_node)
        node_boundlist =[]
        for nodes in list(Digraph_tree.nodes()):
            Digraph_tree.node[nodes]['number_end_bound'] = 0 #初始化，
            if nx.degree(Digraph_tree,nodes) == 1:
                node_boundlist.append(nodes)
        print('node_boundlist',node_boundlist)
        node_boundlist_len = []
        for node_temp in list(Digraph_tree.nodes()):
            edges = nx.bfs_edges(Digraph_tree, node_temp)
            nodes = [node_temp] + [v for u, v in edges]
            comon_list=[x for x in nodes if x in node_boundlist]
            node_boundlist_len.append([node_temp,len(comon_list)])
            # print(len(comon_list))
            Digraph_tree.node[node_temp]['number_end_bound'] = len(comon_list) # 初始化，

        print('好像不对啊。')
        #现在每个点都有自己的边界点数目统计了。从源点出发，从邻居节点找最多的那条。直到找到一个边界点为止。
        max_node_path = []
        node_index = source_node
        while 1:
            max = 0
            max_node_path.append(node_index)
            if node_index in node_boundlist:
                break
            for neighbour in list(nx.neighbors(Digraph_tree,node_index)):
                print('neighbour',neighbour)
                print('number_end', Digraph_tree.node[neighbour]['number_end_bound'])
                if Digraph_tree.node[neighbour]['number_end_bound'] >max:
                    max = Digraph_tree.node[neighbour]['number_end_bound']
                    node_index = neighbour
            print('max_node_path',max_node_path)

        print('真实源离这些点距离')
        for path_node in max_node_path:

            print(nx.shortest_path_length(subinfectG,source=true_source,target=path_node))

        print('走过的路径是多少？',max_node_path)







    '''
      1 设计本类做单源定位
      过程： 在树上做实验，产生源点必须离边界近。大概就是倒数几层的位置。
      1 然后先做一个rumor centrality，然后就根据所有边界点的位置，让源点
      走向边界点最多的那个分支。直到走到最近的的一个边界点，记录沿途走过的
      点。或者可以加上密度的说法。
      
    '''

    def main(self, filename):

        # #拿到图
        initG = commons.get_networkByFile(filename)
        max_sub_graph = commons.judge_data(initG)
        print('是否是一棵树？',nx.is_tree(max_sub_graph))
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = self.produce_source(max_sub_graph, 1)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG, T = commons.propagation1(max_sub_graph, source_list)

        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
        # 将在这里进行单源测试。
        '''   第一种，就是jarden center '''
        #
        object_single = single_Source_detection.Single_source()
        reverse_node = object_single.revsitionAlgorithm_singlueSource(subinfectG)
        result_node=self.single_source_bound_ture(subinfectG,reverse_node[0],source_list[0])
        print('真实源是', source_list[0])
        print('预测源是', result_node[0])
        distance = nx.shortest_path_length(subinfectG, source=source_list[0], target=result_node[0])
        print('结果是', distance)
        return distance


'''
'''
import time

if __name__ == '__main__':
    test = Single_source_bound()
    sum = 0
    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')
    # initG = commons.get_networkByFile(filename)
    # filname = '../../../data/4_regular_graph_3000_data.txt'
    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')
    # filname = '../../../data/CA-GrQc.txt'
    filname = '../../../../data/3regular_tree9.txt'
    # method ='distan+ covage'
    # method = 'jardan_center'
    # method ='distance'
    method = '中介中心性'

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




