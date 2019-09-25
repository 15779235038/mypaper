#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/23 8:42 下午

# @Author  : baozhiqiang

# @File    : likeBFS_mult_souce.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************

import commons
import  copy
'''

思路：

1  怎么验证你的想法是正确的呢？

    让1源点传播，然后再根据这个源点进行BFS，查看传播次数以及BFS层数。判断两者重合度。
'''
from  collections import defaultdict
import  networkx as nx


import random
import math

import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import  commons
class  LikeBFS:
    def __init__(self):
        pass




    '''
    
    
    设计两个函数，相同源点，一个是BFS，一个是传播源点。
    
    '''
    def  get_BFS(self, infectG,source,level ):
        dict=commons.test_BFS_node(infectG,source,depth= level)
        print(dict)
        sort_BFS_dict = sorted(dict.items(),key= lambda x: x[0])
        y_list = []
        for everyLevel, node_list in sort_BFS_dict:
            print('len(node_list)',len(node_list))
            y_list.append(len(node_list))
        return y_list[1:]
        # pass

    '''
    这是是传播，只有知道传播几次才能知道BFS应该几层，SI传播的定义是
    
    每个时间刻，每个节点都试图向附近节点以一定的概率传播谣言信息。
    
    '''
    def  get_paogration(self,G,SourceList):
        y_list = []
        G_temp = nx.Graph()
        G_temp = copy.deepcopy(G)
        '''
        :param G:
        :param SourceList:
        :return:
        '''
        queue = set()
        for source in SourceList:
            G.node[source]['SI'] = 2
            queue.add(source)
        progation_number = 0
        while 1:
            propagation_layer_list = []  # 传播的BFS某一层
            propagation_layer_list.extend(list(set(queue)))  # 总是删除第一个。这里不删除
            print('第几个时间刻节点传播为' + str(len(propagation_layer_list)))
            # y_list.append(len(propagation_layer_list))      #每个时间刻被感染的节点
            count_nuber = 0
            for source in propagation_layer_list:
                for height in list(G_temp.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.5:
                        G_temp.node[height]['SI'] = 2
                        # 如果被传播，那就将邻接节点放入队列中。
                        if  height not in queue: #不在以前传播中，是传播到新的节点的数目，他会不断的充实这个BFS树
                            count_nuber += 1
                        queue.add(height)
            y_list.append(count_nuber)
            propagation_layer_list.clear()
            # queue_set = list(set(queue))
            count = 0
            for nodetemp in list(G.nodes):
                if G_temp.node[nodetemp]['SI'] == 2:
                    count = count + 1

            print('被感染点为' + str(count) + '个')
            progation_number += 1
            if count / G_temp.number_of_nodes() > 0.9:
                print('超过50%节点了，不用传播啦')
                break
        # 数据进去图，看看
        return G_temp, progation_number, y_list


    '''
    画图
    '''

    def plot(self,x_list, y_list, propagation1,Probability):
        plt.figure()
        plt.plot(x_list, y_list)
        plt.title('increase number of people for evert t  at'+str(Probability))

        plt.savefig('result/result_oneSource/'+str(propagation1) + ".png")
        # plt.show()
        plt.close()


    def plot_plus(self,x_list,y_list1,y_list2,propagation1,Probability):

        # label = 'y2'
        plt.plot(x_list, y_list1, 'g', label = 'progation')
        plt.plot(x_list, y_list2, 'r--', label='BFS')
        plt.legend()
        plt.title('increase number of people for evert t  at'+str(Probability))

        plt.ylabel('Increased number of infected people for every t')
        plt.savefig('result/result_oneSource/'+str(propagation1) + ".png")
        plt.close()

        # pass

    def  plot_sum_increase(self,x_list,y_list1,y_list2,filename,Probability):
        temp1 = 0
        temp2 = 0
        new_list1 =[]
        new_list2 = []
        for  y1, y2  in zip(y_list1, y_list2):
            temp1  +=y1
            new_list1.append(temp1)
            temp2 += y2
            new_list2.append(temp2)

        plt.plot(x_list, new_list1, 'g', label='progation')
        plt.plot(x_list, new_list2, 'r--', label='BFS')
        plt.legend()
        plt.title('sum number of people for evert t at'+str(Probability))
        plt.xlabel('t')
        plt.ylabel('sum of infected people for every t')
        plt.savefig('result/result_oneSource/' + str(filename) + ".png")
        plt.close()
    # pass
    def  get_best_BFScenter(self,subinfectG,fix_number_souce,progation_number,source_list):
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
        '''
        #根据传播源点进行BFS，查看传播图的节点跟BFS的相似度。
        '''
        similar =0
        print('progration_number',progation_number)
        for source_temp in source_list:
            lists = list(nx.bfs_tree(subinfectG,source= source_temp,depth_limit=progation_number))  #源点BFS传播次数的
            #判断两个list的相似程度，判断有多少一样的元素
            print('len(lists)',len(lists))
            count = 0
            for  node in lists:
                if node in singleRegionList:
                    count +=1
            print('count',count)
            print('len(singleRegionLis', len(singleRegionList))
            similar = count/len(singleRegionList)
            print(similar)






    def main(self):
        initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')

        # initG = commons.get_networkByFile('../../../data/treenetwork3000.txt')

        max_sub_graph = commons.judge_data(initG)
        source_list = commons.product_sourceList(max_sub_graph, 1)
        infectG, progration_number, y_list1 = self.get_paogration(max_sub_graph, source_list)
        # print('progration_number',progration_number)
        # print('len(y_list1)',len(y_list1))
        y_list2 = self.get_BFS(max_sub_graph,source_list[0],progration_number)
        print(len(y_list2))
        print(len(y_list1))
        Probability = 0.5
        self.plot(range(len(y_list1)),y_list1,'progration',Probability)
        self.plot(range(len(y_list1)),y_list2,'bfs',Probability)
        self.plot_plus(range(len(y_list2)),y_list1,y_list2,'every_t',Probability)
        self.plot_sum_increase(range(len(y_list2)),y_list1,y_list2,'sum',Probability)
        #重新画一个图，记录增长总数变化。



test = LikeBFS()
test.main()
