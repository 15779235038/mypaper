#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/23 8:42 下午

# @Author  : baozhiqiang

# @File    : likeBFS.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************

import commons
'''

思路：

1  怎么验证你的想法是正确的呢？

    让1或者多个源点传播，然后寻找最好的覆盖率的BFS树，查看BFS树的源点跟传播源点距离。

'''
from  collections import defaultdict
import  networkx as nx


import random
import math

import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict
import  commons
class  LikeBFS:
    def __init__(self):
        pass


    def  get_best_BFScenter(self,subinfectG,fix_number_souce):
        '''

        根据传播子图，找到最好的覆盖率的BFS点。
        :return:
        '''
        # 构建传播子图，
        singleRegionList = []
        for node_index in list(subinfectG.nodes()):
            if subinfectG.node[node_index]['SI'] == 2:
                singleRegionList.append(node_index)
        print('singleReginList',singleRegionList)
        tempGraph = nx.Graph()
        tempGraphNodelist = []
        for edge in subinfectG.edges:
            # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
            if edge[0] in singleRegionList and edge[1] in singleRegionList:
                tempGraph.add_edges_from([edge], weight=1)
                tempGraphNodelist.append(edge[0])
                tempGraphNodelist.append(edge[1])
        # self.tempGraph = tempGraph  # 临时图生成
        print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
        print('这个感染区域的传播图节点个数')


        eccentricity_dict = nx.eccentricity(tempGraph)
        # print(list(eccentricity_dict.items()))
        # eccentricity_list= sorted(list(eccentricity_dict.items()), key= lambda  x:x[1])
        # print(eccentricity_list)
        eccentri_dict = defaultdict(list)
        for node_id, eccentric in eccentricity_dict.items():
            eccentri_dict[eccentric].append(node_id)
        print(eccentri_dict)
        # 从偏心率大的考虑，先保存最大偏心度。
        sort_eccentricity_dict = sorted(eccentri_dict.items(), key=lambda x: x[0], reverse=True)
        max_eccentric = sort_eccentricity_dict[0][0]
        min_eccentric = sort_eccentricity_dict[-1][0]
        print('输出最大的就是那个偏心率' + str(max_eccentric))
        from random import sample
        best_h = 0
        M_dis = 0
        best_h_node = []
        min_cover = 100  # 某一层的覆盖率，肯定会比这个小。
        for node_list_index in range(len(sort_eccentricity_dict) - 1):
            print('how to that')
            print(sort_eccentricity_dict[node_list_index][1])
            print(sort_eccentricity_dict[node_list_index][0])
            sort_eccentricity_dict[node_list_index][1].extend(sort_eccentricity_dict[node_list_index + 1][1])
            print(sort_eccentricity_dict[node_list_index][1])

            M_dis = max_eccentric - sort_eccentricity_dict[node_list_index][0] + 1  # 最好的bFS树半径。
            # 随机挑选k个点固定次数。
            temp_all_cover = 0
            temp_cover = 0
            temp_ave_cover = 0
            if len(sort_eccentricity_dict[node_list_index][1]) > fix_number_souce * 2:  # 这一层只有大于3个点才可以。
                itemNumber = int(len(sort_eccentricity_dict[node_list_index][1]) / 10)  # 层数越大，节点越多，应该采样越多才能逼近近似值。
                for frequency in range(itemNumber):  # 抽取10次,这里有问题，有些层数目多，怎么抽取会好点？按照层数抽取相应的次数会比较好点，公平。
                    slice = random.sample(sort_eccentricity_dict[node_list_index][1], fix_number_souce)
                    temp_cover = commons.getSimilir1(slice, M_dis, singleRegionList, tempGraph)
                    temp_all_cover += temp_cover
                if temp_all_cover != 0:
                    temp_ave_cover = temp_all_cover / itemNumber  # 求出平均覆盖率。
                    print('temp_ave_cover', temp_ave_cover)
                else:
                    temp_ave_cover = 0.1
                if temp_ave_cover <= min_cover:
                    # 这一层表现优异，记下h，以及这一层的所有节点。
                    print('每次平均的覆盖率是' + str(min_cover))
                    print('temp_ave_cover', temp_ave_cover)
                    min_cover = temp_ave_cover
                    best_h_node = sort_eccentricity_dict[node_list_index][1]
                    best_h = M_dis
        print('输出表现优异同学,看看' + str(best_h_node), str(best_h))
        # 得到最优层数解，再大量进行选择，使用jaya算法。构建大量样本。在固定h下的寻找最合适的节点。
        '''
        1 构建种群样本下
        2 在固定h下更新
        '''
        return commons.jaya(tempGraph, best_h_node, fix_number_souce, best_h, singleRegionList)



    def main(self):
        initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
        max_sub_graph = commons.judge_data(initG)
        source_list = commons.product_sourceList(max_sub_graph, commons.fix_number_source)
        infectG,number = commons.propagation1(initG, source_list)
        # subinfectG = commons.get_subGraph(infectG)
        result =self.get_best_BFScenter(infectG, commons.fix_number_source)
        commons.cal_distance(infectG,source_list, result[0])





test = LikeBFS()
test.main()
