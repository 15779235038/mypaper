#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/21 12:11 下午

# @Author  : baozhiqiang

# @File    : common.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************

import random
import math
import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict
from random import sample


fix_number_source = 4


'''
共有的工具类，参数，所有固定跑实验的东西都在这个里面了。






'''

def ContractDict(dir, G):
    '''
    :param dir:
    :param G:    从文件中拿点
    :return:
    '''
    with open(dir, 'r') as f:
        for line in f:
            line1 = line.split()
            G.add_edge(int(line1[0]), int(line1[1]))
    for edge in G.edges:
        G.add_edge(edge[0], edge[1], weight=1)
        # G.add_edge(edge[0],edge[1],weight=effectDistance(randomnum))
    print(len(list(G.nodes)))
    # G.remove_node(0)
    print(len(list(G.nodes)))
    return G


def get_networkByFile( fileName='../data/facebook_combined.txt'):
    #  制造这个图
    Ginti = nx.Graph()
    # 构建图，这个图是有有效距离的。
    G = ContractDict(fileName, Ginti)
    # 因为邮件是一个有向图，我们这里构建的是无向图。
    print('一开始图的顶点个数', G.number_of_nodes())
    print('一开始图的边个数', G.number_of_edges())
    #  先给全体的Cn、Scn,time的0的赋值。
    for node in list(G.nodes):
        G.add_node(node, SI=1)
    # 初始化所有边是否感染。Infection
    for edge in list(G.edges):
        G.add_edge(edge[0], edge[1], isDel=0)
    print('这个图产生完毕')
    return G

    # pass


def product_sourceList(G,sourceNum):
    # 产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
    sumlist = list(G.nodes)
    flag = 0
    flag1 = 0
    rumorSourceList = []
    # 先随机找个点，然后找到距离它为>6,小于10的吧。
    while (flag == 0):
        if sourceNum == 1:
            # random_RumorSource = random.randint(0, 7000)
            random_Rumo = random.sample(sumlist, 1)
            random_RumorSource = random_Rumo[0]
            rumorSourceList.append(random_RumorSource)
            flag = 1
        elif sourceNum == 2:
            # random_Rumo = random.sample(sumlist, 1)
            # random_RumorSource = random_Rumo[0]

            random_RumorSource = random.choice(sumlist)
            # 在剩下的节点找到我们的第二个点。
            for node in list(G.nodes):
                if nx.has_path(G, node, random_RumorSource) == True:
                    if nx.shortest_path_length(G, node, random_RumorSource) > 4 and nx.shortest_path_length(G,
                                                                                                            node,
                                                                                                            random_RumorSource) < 6:
                        rumorSourceList.append(node)
                        rumorSourceList.append(random_RumorSource)
                        flag = 1
                        break
        elif sourceNum == 3:
            print('3源点情况。')
            threeNumberFLAG = 0
            while threeNumberFLAG == 0:
                # 先随机找一个点。
                # random_Rumo = random.sample(sumlist, 1)
                # random_RumorSource = random_Rumo[0]

                random_RumorSource = random.choice(sumlist)
                # 找第二、三个点。
                for index in range(len(sumlist) - 2):
                    if nx.has_path(G, sumlist[index], random_RumorSource) == True and nx.has_path(G, sumlist[
                        index + 1], random_RumorSource) == True:
                        if nx.shortest_path_length(G, source=sumlist[index],
                                                   target=random_RumorSource) > 4 and nx.shortest_path_length(G,
                                                                                                              source=
                                                                                                              sumlist[
                                                                                                                  index],
                                                                                                              target=random_RumorSource) < 6 and nx.shortest_path_length(
                            G, source=sumlist[index + 1],
                            target=random_RumorSource) > 4 and nx.shortest_path_length(G, source=sumlist[
                            index + 1], target=random_RumorSource) < 6:
                            rumorSourceList.append(random_RumorSource)
                            rumorSourceList.append(sumlist[index])
                            rumorSourceList.append(sumlist[index + 1])
                            print('找到了3源点了。')
                            break
                if len(rumorSourceList) == 3:
                    print('找到了3个点')
                    threeNumberFLAG = 1
                    flag = 1
                else:
                    pass


        elif sourceNum == 4:

            flag = 0

            flag1 = 0

            while flag == 0:

                random_RumorSource = random.choice(sumlist)

                flag1 = 0

                while flag1 == 0:

                    print('随机产生的点为' + str(random_RumorSource))

                    rumorSourceList = []

                    rumorSourceList.append(random_RumorSource)

                    nehibor = []

                    for j in range(0, 3):

                        for i in range(0, 4):
                            nehibor = list(G.neighbors(random_RumorSource))

                            randomnumber = random.randint(0, len(nehibor) - 1)

                            random_RumorSource = nehibor[randomnumber]

                        rumorSourceList.append(random_RumorSource)

                    if len(rumorSourceList) == 4 and len(rumorSourceList) == len(

                            set(rumorSourceList)):  # 重复或者数目达不到要求:

                        print('找到了4个点')

                        flag1 = 1

                        flag = 1


                    elif len(rumorSourceList) == 4 and len(rumorSourceList) != len(set(rumorSourceList)):

                        print('是四个点，但是却有重复，只能够重新选择新的开始点')

                        flag1 = 1

        elif sourceNum == 5:

            flag = 0

            flag1 = 0

            while flag == 0:

                random_RumorSource = random.choice(sumlist)

                flag1 = 0

                while flag1 == 0:

                    print('随机产生的点为' + str(random_RumorSource))

                    rumorSourceList = []

                    rumorSourceList.append(random_RumorSource)

                    nehibor = []

                    for j in range(0, 4):

                        for i in range(0, 4):
                            nehibor = list(G.neighbors(random_RumorSource))

                            randomnumber = random.randint(0, len(nehibor) - 1)

                            random_RumorSource = nehibor[randomnumber]

                        rumorSourceList.append(random_RumorSource)

                    if len(rumorSourceList) == 5 and len(rumorSourceList) == len(

                            set(rumorSourceList)):  # 重复或者数目达不到要求:

                        print('找到了5个点')

                        flag1 = 1

                        flag = 1


                    elif len(rumorSourceList) == 5 and len(rumorSourceList) != len(set(rumorSourceList)):

                        print('是5个点，但是却有重复，只能够重新选择新的开始点')

                        flag1 = 1

    # 查看产生随机源点的个数2，并且他们距离为3.
    print('源点个数' + str(len(rumorSourceList)) + '以及产生的两源点是' + str(rumorSourceList))
    # rumorSourceList=[125,4022]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 95
    print('真实两源感染是' + str(rumorSourceList))

    return rumorSourceList


def constract_Infection_netWork(G,SourceList):
    '''
    :param G:
    :param infect_ratio:
    :return:  按照感染比例感染的图
    '''
    print('开始传染的点是' + str(SourceList))
    infectList = []
    for j in SourceList:
        infectList.append(j)
        G.node[j]['SI'] = 2
    #   没有具体的时间概念，传播大概到了50%，就停止传播。开始做实验
    while 1:
        tempinfectList = []
        for node in list(set(infectList)):  # infectList表示的是每一个时刻传播到的点
            for height in list(G.neighbors(node)):
                randnum = random.random()
                if randnum < 0.5:
                    G.node[height]['SI'] = 2
                    tempinfectList.append(height)
        infectList = list(set(infectList))
        # infectList.clear()
        for timeInfectnode in tempinfectList:
            infectList.append(timeInfectnode)
        # 每一个时间点过去，判断有没有感染图的50%的点，感染了就可以，否则不行
        count = 0
        for nodetemp in list(G.nodes):
            if G.node[nodetemp]['SI'] == 2:
                count = count + 1
        print('被感染点为' + str(count) + '个')
        if count / G.number_of_nodes() > 0.3:
            print('超过50%节点了，不用传播啦')
            break
    # .infectG = G
    return G







'''
用队列重写SI传播过程，propagation会传播并且还会

传播方案1：从源点开始往外面传播，按照队列传播形式
'''
def   propagation(G,SourceList):
    '''
    :param G:
    :param SourceList:
    :return:
    '''
    y_list =[]
    queue = []
    for source in SourceList:
        G.node[source]['SI'] = 2
        queue.append(source)
    while 1:
            propagation_layer_list = [] #传播的BFS某一层
            while len(queue) > 0:
                propagation_layer_list.append(queue.pop(0))  #总是删除第一个
            print('第几层为'+str(propagation_layer_list))
            for source in propagation_layer_list:
                for height in list(G.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.5:
                        G.node[height]['SI'] = 2
                        #如果被传播，那就将邻接节点放入队列中。
                        queue.append(height)
            propagation_layer_list.clear()
            count = 0
            for nodetemp in list(G.nodes):
                if G.node[nodetemp]['SI'] == 2:
                    count = count + 1
            y_list.append(count)
            print('被感染点为' + str(count) + '个')
            if count / G.number_of_nodes() > 0.5:
                print('超过50%节点了，不用传播啦')
                break

            # 数据进去图，看看
    # x_list = [i for i in range(len(y_list))]
    # plot(x_list, y_list, 'pro')
    return G








'''
用队列重写SI传播过程，propagation会传播并且还会

传播方案2：从源点开始往外面传播，按照队列传播形式。每次所有感染的点都试图感染身边的点。而不是一层一层来
'''
def   propagation1(G,SourceList):

    y_list =[]
    '''
    :param G:
    :param SourceList:
    :return:
    '''
    queue = set()
    for source in SourceList:
        G.node[source]['SI'] = 2
        queue.add(source)

    while 1:
            propagation_layer_list = [] #传播的BFS某一层
            propagation_layer_list.extend(list(queue)) #总是删除第一个。这里不删除
            print('第几层为'+str(len(propagation_layer_list)))
            for source in propagation_layer_list:
                for height in list(G.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.5:
                        G.node[height]['SI'] = 2
                        #如果被传播，那就将邻接节点放入队列中。
                        queue.add(height)
            propagation_layer_list.clear()
            # queue_set = list(set(queue))
            count = 0
            for nodetemp in list(G.nodes):
                if G.node[nodetemp]['SI'] == 2:
                    count = count + 1
            y_list.append(count)
            print('被感染点为' + str(count) + '个')
            if count / G.number_of_nodes() > 0.4:
                print('超过50%节点了，不用传播啦')
                break
    #数据进去图，看看
    x_list= [i for i in  range(len(y_list))]

    # plot(x_list,y_list,'pro1')
    return G


import numpy as np
import matplotlib.pyplot as plt
'''
画图
'''
def plot(x_list,y_list,propagation1):
    # x = [0, 1]
    # y = [0, 1]
    plt.figure()
    plt.plot(x_list, y_list)
    plt.savefig(str(propagation1) + ".png")
    plt.show()












def  get_subGraph(infectG):
   #构建传播子图，
        singleRegionList = []
        for node_index in list(infectG.nodes()):
            if infectG.node[node_index]['SI'] == 2:
                singleRegionList.append(node_index)
        tempGraph = nx.Graph()
        tempGraphNodelist = []
        for edge in infectG.edges:
            # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
            if edge[0] in singleRegionList and edge[1] in singleRegionList:
                tempGraph.add_edges_from([edge], weight=1)
                tempGraphNodelist.append(edge[0])
                tempGraphNodelist.append(edge[1])
        print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
        print('这个感染区域的传播图节点个数')
        # eccentricity_dict = nx.eccentricity(tempGraph)

        return tempGraph   # 临时图生成




'''
    从txt中获取每个数据集的中心点依次做实验
    '''

def get_data(dir):
        a = open(dir)
        lines = a.readlines()
        lists = []  # 直接用一个数组存起来就好了
        for line in lines:
            lists.append(int(line))
        print(lists)
        center_list = lists
        return  center_list




'''
    返回一个源点进行BFS每一层的节点，以键值对形式返回。层数：节点。
    目前固定5层。
    '''
def test_BFS_node( G, source_node, depth=5):
        print('source_node', source_node)
        dfs_successor = nx.bfs_successors(G, source=source_node)
        dfs_successor =dict(dfs_successor)
        print('dfs_successor', dfs_successor)
        stack = []
        dfs_result = defaultdict(list)
        depth = 1
        dfs_result[0].append(source_node)
        stack.append(source_node)
        while len(stack) > 0:
            node_list = stack
            temp = []
            for i in list(node_list):
                if i in dfs_successor.keys():
                    for neighbour in dfs_successor[i]:
                        temp.append(neighbour)
                        dfs_result[depth].append(neighbour)
            depth += 1
            stack = temp
        print(dfs_result)
        return dfs_result






'''
根据传播子图生成相应的中心点list
'''
def  get_center_list(subinfectG):
    # 介数中心性
    between_dict = nx.betweenness_centrality(subinfectG)
    sort_eccentricity_dict = sorted(between_dict.items(), key=lambda x: x[1], reverse=True)
    print('sort_eccenritci_dict', sort_eccentricity_dict)

    #   接近度中心性
    closeness_centrality = nx.closeness_centrality(subinfectG)
    sort_colse_centrality_dict = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
    print('sort_colse_centrality_dict', sort_colse_centrality_dict)

    #   度中心性，这个效果最好，简直了。
    degree_centrality = nx.degree_centrality(subinfectG)
    sort_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
    print('sort_degree_centrality', sort_degree_centrality)
    center_list = []
    center_list.append(sort_eccentricity_dict[0][0])
    center_list.append(sort_colse_centrality_dict[0][0])
    center_list.append(sort_degree_centrality[0][0])
    return center_list




'''
1 对数据集进行判断。从有几个连通子图，每个数目。我们最关心在最大的连通子图产生源点。

'''

def  judge_data(initG):
    '''

    :param initG:
    :return:  #返回最大子图的源点数据集
    '''





if __name__ == '__main__':
    initG = get_networkByFile('.././data/CA-GrQc.txt')
    source_list =product_sourceList(initG, 2)
    # infectG =propagation(initG, source_list)
    infectG =propagation1(initG, source_list)
    #画图







