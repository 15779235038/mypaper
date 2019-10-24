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
        G.add_node(node, SIDIF=1)
    # 初始化所有边是否感染。Infection
    for edge in list(G.edges):
        G.add_edge(edge[0], edge[1], isDel=0)
        G.add_edge(edge[0], edge[1], isInfect =0)
    print('这个图产生完毕')
    return G

    # pass

'''

产生源点：
方案1：就是下面这种，

'''
def product_sourceList(G,sourceNum):
    # 产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
    sumlist = list(G.nodes)
    print('最大子图个数为',len(sumlist))
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
            # rumorSourceList = random.sample(sumlist, 2)
            # print(nx.shortest_path_length(G,source=rumorSourceList[0],target=rumorSourceList[1]))
            # break
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
    return G







'''
用队列重写SI传播过程，propagation会传播并且还会

传播方案1：从源点开始往外面传播，按照队列传播形式
'''
def   propagation_withT(G,SourceList,T):
    G_temp = nx.Graph()
    G_temp = copy.deepcopy(G)
    '''
    :param G:
    :param SourceList:
    :return:
    '''
    queue = set()
    for source in SourceList:
        G_temp.node[source]['SI'] = 2
        queue.add(source)
    # progation_number = 0
    count1 = 0
    while 1:
        propagation_layer_list = []  # 传播的BFS某一层
        propagation_layer_list.extend(list(queue))  # 总是删除第一个。这里不删除
        print('第几层为' + str(len(propagation_layer_list)))
        for source in propagation_layer_list:
            for height in list(G_temp.neighbors(source)):
                randnum = random.random()
                if randnum < 0.5:
                    G_temp.node[height]['SI'] = 2
                    G_temp.add_edge(source, height, isInfect=1)
                    # 如果被传播，那就将邻接节点放入队列中。
                    queue.add(height)
        propagation_layer_list.clear()
        # queue_set = list(set(queue))
        count = 0
        for nodetemp in list(G.nodes):
            if G_temp.node[nodetemp]['SI'] == 2:
                count = count + 1

        print('被感染点为' + str(count) + '个')
        # progation_number += 1
        count1 += 1
        if count1 == T:
            print('超过50%节点了，不用传播啦')
            break
    # 数据进去图，看看

    return G_temp








import copy

'''
用队列重写SI传播过程，propagation会传播并且还会

传播方案2：从源点开始往外面传播，按照队列传播形式。每一个时间刻度，每次所有感染的点都试图感染身边的点。而不是一层一层来
'''
def   propagation1(G,SourceList,number =1):

    y_list =[]
    G_temp = nx.Graph()
    G_temp = copy.deepcopy(G)
    '''
    :param G:
    :param SourceList:
    :return:
    '''
    queue = set()
    for source in SourceList:
        G_temp.node[source]['SI'] = 2
        queue.add(source)
    # progation_number = 0
    while 1:
            propagation_layer_list = [] #传播的BFS某一层
            propagation_layer_list.extend(list(queue)) #总是删除第一个。这里不删除
            print('第几层为'+str(len(propagation_layer_list)))
            for source in propagation_layer_list:
                for height in list(G_temp.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.5:
                        G_temp.node[height]['SI'] = 2
                        G_temp.add_edge(source, height, isInfect = 1)
                        #如果被传播，那就将邻接节点放入队列中。
                        queue.add(height)
            propagation_layer_list.clear()
            # queue_set = list(set(queue))
            count = 0
            for nodetemp in list(G.nodes):
                if G_temp.node[nodetemp]['SI'] == 2:
                    count = count + 1
            y_list.append(count)
            print('被感染点为' + str(count) + '个')
            # progation_number += 1
            if count / G_temp.number_of_nodes() > 0.5:
                print('超过50%节点了，不用传播啦')
                break
    #数据进去图，看看


    return G_temp




import copy

'''
用队列重写SI传播过程，

传播方案3：不同源点传播有唯一标示性，我们就是看看是否覆盖率真的好。
'''
def   propagation_dif_sigl(G,source,DIF):

    y_list =[]
    G_temp = nx.Graph()
    G_temp = copy.deepcopy(G)
    '''
    '''
    queue = set()
    G.node[source]['SI'] = 2
    queue.add(source)
    G.node[source]['SIDIF']  =DIF
    # progation_number = 0
    while 1:
            propagation_layer_list = [] #传播的BFS某一层
            propagation_layer_list.extend(list(queue)) #总是删除第一个。这里不删除
            print('第几层为'+str(len(propagation_layer_list)))
            for source in propagation_layer_list:
                for height in list(G_temp.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.5:
                        G_temp.node[height]['SI'] = 2
                        G_temp.add_edge(source, height, isInfect=1)
                        if DIF == 4: #这是第二个感染区域了了。加上都要判断一下。
                            if  G_temp.node[height]['SIDIF'] == 3:
                                G_temp.node[height]['SIDIF'] = 5
                            else:
                                G_temp.node[height]['SIDIF'] = DIF
                        else:
                            G_temp.node[height]['SIDIF'] = DIF
                        #如果被传播，那就将邻接节点放入队列中。
                        queue.add(height)
            propagation_layer_list.clear()
            # queue_set = list(set(queue))
            count = 0
            count1 = 0
            for nodetemp in list(G.nodes):
                if G_temp.node[nodetemp]['SIDIF'] == 3 or  G_temp.node[nodetemp]['SIDIF'] == 5:
                    count = count + 1
                elif G_temp.node[nodetemp]['SIDIF'] == 4  or  G_temp.node[nodetemp]['SIDIF'] == 5:
                    count1 += 1
            # y_list.append(count)
            print('第一次被感染点为' + str(count) + '个')
            print('被感染点为' + str(count1) + '个')
            # progation_number += 1

            if DIF == 4:
                if count1 / G_temp.number_of_nodes() > 0.2:
                    print('超过20%节点了，不用传播啦')
                    break
            else:
                if count / G_temp.number_of_nodes() > 0.2:
                    print('超过20%节点了，不用传播啦')
                    break

    #数据进去图，看看


    return G_temp











# import copy

'''
用队列重写SI传播过程，propagation会传播并且还会

传播方案2：从源点开始往外面传播，按照队列传播形式。每一个时间刻度，每次所有感染的点都试图感染身边的点。而不是一层一层来
'''
def   BFS_coverage(G,SourceList,number =1):

    y_list =[]
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
    # progation_number = 0



    while 1:
            propagation_layer_list = [] #传播的BFS某一层
            propagation_layer_list.extend(list(queue)) #总是删除第一个。这里不删除
            print('第几层为'+str(len(propagation_layer_list)))
            for source in propagation_layer_list:
                for height in list(G_temp.neighbors(source)):
                    # randnum = random.random()
                    # if randnum < 0.5:
                        G_temp.node[height]['SI'] = 2
                        #如果被传播，那就将邻接节点放入队列中。
                        queue.add(height)
            propagation_layer_list.clear()
            # queue_set = list(set(queue))
            count = 0
            for nodetemp in list(G.nodes):
                if G_temp.node[nodetemp]['SI'] == 2:
                    count = count + 1
            y_list.append(count)
            print('被感染点为' + str(count) + '个')
            # progation_number += 1
            if count / G_temp.number_of_nodes() > 0.4:
                print('超过50%节点了，不用传播啦')
                break
    #数据进去图，看看



    return G_temp
























import numpy as np
import matplotlib.pyplot as plt
'''
画图
'''
def plot(x_list,y_list,propagation1):

    plt.figure()
    plt.plot(x_list, y_list)
    # plt.savefig('./Conditional_satisfaction/plot/'+str(propagation1) + ".png")
    # plt.show()











'''
这是最一般的拿到传播子图的方式

'''
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
这是拿到真实传播子图的方式,是为了衡量我们的分区方式好不好。
'''
def  get_subGraph_true(infectG):
        #构建传播子图，
        singleRegionList = []
        for node_index in list(infectG.nodes()):
            if infectG.node[node_index]['SI'] == 2:
                singleRegionList.append(node_index)
        tempGraph = nx.Graph()
        tempGraphNodelist = []
        for edge in infectG.edges:
            # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
            if infectG.edges[edge[0], edge[1]]['isInfect'] ==1:
                if edge[0] in singleRegionList and edge[1] in singleRegionList:
                    tempGraph.add_edges_from([edge], weight=1)
                    tempGraphNodelist.append(edge[0])
                    tempGraphNodelist.append(edge[1])
        print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
        print('这个感染区域的传播图节点个数')
        # eccentricity_dict = nx.eccentricity(tempGraph)
        return tempGraph   # 临时图生成





'''

1 分层算法，输入原感染图。注意要包含感染和未感染点，还有分层的层数参数

'''

def partion_layer(G,number_layer= 10):
    G_temp = nx.Graph()
    subGraph = nx.Graph()
    G_temp = copy.deepcopy(G)
    # 获取我们所有的图。
    # 拿到所有的感染点,并且统计他们感染率。
    node_scale = []
    infect_listNode = []
    for nodes in list(G_temp.nodes):
        if G_temp.node[nodes]['SI'] == 2:
            neighbor_list = list(G_temp.neighbors(nodes))
            count = len([x for x in neighbor_list if G_temp.node[x]['SI'] == 2])
            neighbor_list_len = len(neighbor_list)
            node_scale.append([nodes, count / neighbor_list_len])
    # 先做个简单分类。按照从大到小排序.分10档次吧。 #真的可以考虑时间，来分档次。
    sort_dict = defaultdict(list)

    for node_and_scale in node_scale:
        Ten_digits = node_and_scale[1] * 100 // 10
        sort_dict[Ten_digits].append(node_and_scale[0])
    print(sort_dict)
    sort_list = sorted(sort_dict.items(), key=lambda x: x[0], reverse=True)
    print(sort_list)
    return sort_list






'''

1 分层算法，输入原感染图。注意要包含感染和未感染点，还有分层的层数参数
返回键值对
'''

def partion_layer_dict(G,number_layer= 10):
    G_temp = nx.Graph()
    subGraph = nx.Graph()
    G_temp = copy.deepcopy(G)
    # 获取我们所有的图。
    # 拿到所有的感染点,并且统计他们感染率。
    node_dict=dict()
    infect_listNode = []

    for nodes in list(G_temp.nodes):
        if G_temp.node[nodes]['SI'] == 2:
            neighbor_list = list(G_temp.neighbors(nodes))
            count = len([x for x in neighbor_list if G_temp.node[x]['SI'] == 2])
            neighbor_list_len = len(neighbor_list)
            node_dict[nodes]=count / neighbor_list_len
    return node_dict


'''

1 分层算法，输入原感染图。注意要包含感染和未感染点，还有分层的层数参数,这个分层比较严格。
返回键值对
'''

def partion_layer_dict_bfs(G,subinfectG,bfs_layer,number_layer,sourcelist):
    G_temp = nx.Graph()
    subGraph = nx.Graph()
    G_temp = copy.deepcopy(G)
    # 获取我们所有的图。
    # 拿到所有的感染点,并且统计他们感染率。
    node_dict = defaultdict(int)
    infect_listNode = []

    for nodes in list(G_temp.nodes):
        if G_temp.node[nodes]['SI'] == 2:
            neighbor_list = list(G_temp.neighbors(nodes))
            count = len([x for x in neighbor_list if G_temp.node[x]['SI'] == 2])
            neighbor_list_len = len(neighbor_list)
            node_dict[nodes]=count / neighbor_list_len
            # node_dict[nodes] = count

    count1 =0
    for k ,v in node_dict.items():
        if v ==1:
            count1 += 1
    print('count1',count1)
    print('感染总图节点个数',len(list(G_temp.nodes())))
    print('感染点个数',len(node_dict.items()))
    #计算每个点附近两层的
    node_dict_bfs = defaultdict(int)
    #这是每个点的覆盖率，现在某些点肯定要更精细点。
    for node,coverage  in node_dict.items():
        node_dict_temp = copy.deepcopy(node_dict)
        # BFS_node_list = list(nx.bfs_tree(subinfectG, source=node, depth_limit=3).nodes)
        edges =nx.bfs_edges(G_temp,node, depth_limit=5)
        BFS_node_list = [node] + [v for u, v in edges]
        neighbor_list_temp = list(G_temp.neighbors(node))
        lens= len(neighbor_list_temp)
        # print('BFS_node_list',BFS_node_list)
        temp_coverage = 0
        for bfs_node in BFS_node_list:
            temp_coverage += (node_dict_temp[bfs_node])/((nx.shortest_path_length(G_temp,source=node,target=bfs_node))+1)
        node_dict_bfs[node] = temp_coverage
    print(node_dict_bfs)
    sort_list = sorted(node_dict_bfs.items(), key=lambda x: x[1], reverse=True)
    print(sort_list)
    print(nx.shortest_path_length(G_temp,source=sourcelist[0],target=sort_list[0][0]))
    print(nx.shortest_path_length(G_temp, source=sourcelist[1], target=sort_list[0][0]))
    print(nx.shortest_path_length(G_temp, source=sourcelist[0], target=sort_list[1][0]))
    print(nx.shortest_path_length(G_temp, source=sourcelist[1], target=sort_list[1][0]))

    print(node_dict_bfs[sourcelist[0]])
    print(node_dict_bfs[sourcelist[1]])
    return sort_list[:400]





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
def test_BFS_node( G, source_node, depth = 5):
        print('source_node', source_node)
        dfs_successor = nx.bfs_successors(G, source=source_node,depth_limit=depth)
        dfs_successor =dict(dfs_successor)
        # print('dfs_successor', dfs_successor)
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
        # print(dfs_result)
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

    # #特征向量中心性。
    # centrality = nx.eigenvector_centrality(subinfectG)
    # sort_eigener_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    # print('eigenvector_centrality', sort_eigener_centrality)
    # # self.center = sort_eigener_centrality[0][0]

    import math
    #Kaza中心性
    # G = nx.path_graph(4)
    # maxnumber = max(nx.adjacency_spectrum(subinfectG))
    # print(maxnumber)
    # phi = (1 + math.sqrt(5)) / 2.0  # largest eigenvalue of adj matrix
    # centrality = nx.katz_centrality(subinfectG, 1/ maxnumber -0.01)
    # katz_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    # print('katz_centrality',katz_centrality)



    center_list = []
    center_list.append(sort_eccentricity_dict[0][0])
    center_list.append(sort_colse_centrality_dict[0][0])
    center_list.append(sort_degree_centrality[0][0])
    # center_list.append(sort_eigener_centrality[0][0])
    # center_list.append(katz_centrality[0][0])


    return center_list




'''
1 对数据集进行判断。从有几个连通子图，每个数目。我们最关心在最大的连通子图产生源点。

'''

def  judge_data(initG):
    '''
    :param initG:
    :return:  #返回最大子图的源点数据集
    '''
    Gc = nx.Graph()
    Gc = max(nx.connected_component_subgraphs(initG), key=len)
    # for sub_graph in sorted(nx.connected_component_subgraphs(initG), key=len, reverse=True):
    #     print(type(sub_graph))

    return  Gc




def judge_connect(subinfecG):
    count = 0
    for sub_graph in sorted(nx.connected_component_subgraphs(subinfecG), key=len, reverse=True):
        print(sub_graph)
        count +=1
    if count ==1:
        print('传播子图是连通')
        return subinfecG
    else:
        print('传播子图不连通,返回最大子图')
        return  max(nx.connected_component_subgraphs(subinfecG), key=len)








'''
      适用于公式计算公式       为1-  树交集交感染图/树并集并感染图
'''

def getSimilir1( ulist, hlist, singleRegionList, infectionG):
        '''
        S树-S感染。
        :param ulist:
        :param hlist:
        :param singleRegionList:
        :param infectionG:
        :return:
        '''
        if isinstance(ulist, int):
            circleNodesList = list(nx.bfs_tree(infectionG, source=ulist, depth_limit=hlist).nodes)  # 这包含了这个构建的圆的所有节点。
            # 计算列表相似度试试看
            # print ('感染源的h节点集合为'+str(circleNodesList))

            Intersection = list(set(circleNodesList).intersection(set(singleRegionList)))  # 交集
            Union = list(set(circleNodesList).union(set(singleRegionList)))
            count = 0
            for i in Intersection:
                if i in Union:
                    count = count + 1
            ratios = count / len(Union)
            ratio = 1.0 - ratios
            # print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))
            return abs(ratio)

        else:
            # 多源点,获得多源点的覆盖率

            # print('ulist看下啦啦啦啦',ulist)
            circleNodesList = []
            for u in ulist:
                circleNodesList.extend(list(nx.bfs_tree(infectionG, source=u, depth_limit=hlist).nodes))
            circleNodesListnew = list(set(circleNodesList))
            # print('len(circleNodesListnew',len(circleNodesListnew))
            # print('circleNodesListnew',len(circleNodesListnew) )
            # print('len(singleRegionList)',len(singleRegionList))
            # count
            Intersection = list(set(circleNodesListnew).intersection(set(singleRegionList)))  # 交集
            # print('Intersection',len(Intersection))
            Union = list(set(circleNodesList).union(set(singleRegionList)))  # 并集
            # print('Union', len(Union))
            count = 0
            for i in Intersection:
                if i in Union:
                    count = count + 1
            ratios = count / len(Union)
            ratio = 1.0 - ratios
            # print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))
            return abs(ratio)




















# 设计反向传播算法，接收参数。u，h，infectG。
def revsitionAlgorithm(u, h, infectG, subinfectG):
            print('反转算法参数,u和h' + str(u) + '----------' + str(h))
            nodelist = list(nx.bfs_tree(subinfectG, source=u, depth_limit=h).nodes)
            source1G = nx.Graph()  # 构建新的单源传播圆出来
            for edge in subinfectG.edges:
                if edge[0] in nodelist and edge[1] in nodelist:
                    source1G.add_edge(edge[0], edge[1])

            print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
                source1G.number_of_edges()))
            # 在nodelist找出源点来。
            times = 50  # 时间刻多点
            IDdict = {}
            IDdict_dup = {}
            # 先赋予初始值。
            for node in list(source1G.nodes):
                # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
                IDdict[node] = [node]
                IDdict_dup[node] = [node]
            allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
            for t in range(times):
                print(
                    't为' + str(t) + '的时候-----------------------------------------------------------------------------')
                for node in nodelist:  # 对每一个节点来说
                    for heighbour in list(source1G.neighbors(node)):  # 对每一个节点的邻居来说
                        retD = list(
                            set(IDdict[heighbour]).difference(set(IDdict[node])))  # 如果邻居中有这个node没有的，那就加到这个node中去。
                        if len(retD) != 0:  # 表示在B中，但不在A.是有的，那就求并集
                            # 求并集,把并集放进我们的retC中。
                            # print ('并集就是可使用'+str(retD))
                            retC = list(set(IDdict[heighbour]).union(set(IDdict[node])))
                            IDdict_dup[node] = list(set(IDdict_dup[node] + retC))  # 先用一个dict把结果装入,然后这个时间过去再加回去。

                for key, value in IDdict_dup.items():
                    IDdict[key] = IDdict_dup[key]
                # for key, value in IDdict.items():
                #     print(key, value)
                # 在每一个时间刻检查是否有节点满足获得所有的id了。

                flag = 0
                for key, value in IDdict.items():
                    # d.iteritems: an iterator over the (key, value) items
                    if sorted(IDdict[key]) == sorted(nodelist):
                        print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                        print('它的key为' + str(key))
                        allnodelist_keylist.append(key)
                        print('有了接受所有的节点了这样的节点了')
                        flag = 1

                if flag == 1:
                    break
            # print (IDdict)
            print(allnodelist_keylist)

            result = 0
            resultlist = []
            # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
            if len(allnodelist_keylist) == 1:
                print('那就是这个源点了')
                result = allnodelist_keylist[0]
            else:
                # 构建样本路径
                print('构建样本路径看看')
                jarcenlist = []
                for i in allnodelist_keylist:
                    jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                    resultlist = sorted(jarcenlist, key=lambda x: x[1])
                result = resultlist[0][0]
                print('构建样本路径之后结果为' + str(resultlist[0][0]))

            return result








# 设计反向传播算法第二版本，就是根据传播图，接收参数infectG。就可以了
def revsitionAlgorithm_singlueSource(subinfectG):
            # print('反转算法参数,u和h' + str(u) + '----------' + str(h))
            nodelist = list(subinfectG.nodes)

            source1G = nx.Graph()  # 构建新的单源传播圆出来
            source1G = subinfectG
            print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
                source1G.number_of_edges()))
            # 在nodelist找出源点来。
            times = 80  # 时间刻多点
            IDdict = {}

            IDdict_dup = {}
            # 先赋予初始值。
            for node in list(source1G.nodes):
                # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
                IDdict[node] = [node]
                IDdict_dup[node] = [node]
            allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
            for t in range(times):
                print(
                    't为' + str(t) + '的时候-----------------------------------------------------------------------------')
                for node in nodelist:  # 对每一个节点来说
                    for heighbour in list(source1G.neighbors(node)):  # 对每一个节点的邻居来说
                        retD = list(
                            set(IDdict[heighbour]).difference(set(IDdict[node])))  # 如果邻居中有这个node没有的，那就加到这个node中去。
                        if len(retD) != 0:  # 表示在B中，但不在A.是有的，那就求并集
                            # 求并集,把并集放进我们的retC中。
                            # print ('并集就是可使用'+str(retD))
                            retC = list(set(IDdict[heighbour]).union(set(IDdict[node])))
                            IDdict_dup[node] = list(set(IDdict_dup[node] + retC))  # 先用一个dict把结果装入,然后这个时间过去再加回去。

                for key, value in IDdict_dup.items():
                    IDdict[key] = IDdict_dup[key]
                # for key, value in IDdict.items():
                #     print(key, value)
                # 在每一个时间刻检查是否有节点满足获得所有的id了。

                flag = 0
                for key, value in IDdict.items():
                    # d.iteritems: an iterator over the (key, value) items
                    if sorted(IDdict[key]) == sorted(nodelist):
                        print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                        print('它的key为' + str(key))
                        allnodelist_keylist.append(key)
                        print('有了接受所有的节点了这样的节点了')
                        flag = 1
                    #如果有收集到了50%的节点，那么就到了。

                if flag == 1:
                    break
            # print (IDdict)
            print(allnodelist_keylist)

            result = 0
            resultlist = []
            # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
            if len(allnodelist_keylist) == 1:
                print('那就是这个源点了')
                result = allnodelist_keylist
            else:
                '''
                之前只返回某一个节点的
                '''
                # 构建样本路径
                print('构建样本路径看看')
                jarcenlist = []
                for i in allnodelist_keylist:
                    jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                    resultlist = sorted(jarcenlist, key=lambda x: x[1])
                result = [resultlist[0][0]]
                print('构建样本路径之后结果为' + str(resultlist[0][0]))


                '''
                现在返回所有能接收到所有源点的。
                '''
                # result = allnodelist_keylist

            return result   #只返回最好的node












# 设计反向传播算法第三版本，就是根据传播图，接收参数infectG。就可以了
def revsitionAlgorithm_get_goodnode(subinfectG):
            # print('反转算法参数,u和h' + str(u) + '----------' + str(h))
            nodelist = list(subinfectG.nodes)
            nodelist_half_len = len(nodelist) / 2
            print('nodelist_half_len',nodelist_half_len)
            source1G = nx.Graph()  # 构建新的单源传播圆出来
            source1G = subinfectG
            print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
                source1G.number_of_edges()))
            # 在nodelist找出源点来。
            times = 50  # 时间刻多点
            IDdict = {}
            best_node_list = []
            IDdict_dup = {}
            # 先赋予初始值。
            for node in list(source1G.nodes):
                # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
                IDdict[node] = [node]
                IDdict_dup[node] = [node]
            allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key

            t_scope = 0
            for t in range(times):
                print(
                    't为' + str(t) + '的时候-----------------------------------------------------------------------------')
                for node in nodelist:  # 对每一个节点来说
                    for heighbour in list(source1G.neighbors(node)):  # 对每一个节点的邻居来说
                        retD = list(
                            set(IDdict[heighbour]).difference(set(IDdict[node])))  # 如果邻居中有这个node没有的，那就加到这个node中去。
                        if len(retD) != 0:  # 表示在B中，但不在A.是有的，那就求并集
                            # 求并集,把并集放进我们的retC中。
                            # print ('并集就是可使用'+str(retD))
                            retC = list(set(IDdict[heighbour]).union(set(IDdict[node])))
                            IDdict_dup[node] = list(set(IDdict_dup[node] + retC))  # 先用一个dict把结果装入,然后这个时间过去再加回去。

                for key, value in IDdict_dup.items():
                    IDdict[key] = IDdict_dup[key]
                # for key, value in IDdict.items():
                #     print(key, value)
                # 在每一个时间刻检查是否有节点满足获得所有的id了。

                flag = 0
                for key, value in IDdict.items():
                    # d.iteritems: an iterator over the (key, value) items
                    if sorted(IDdict[key]) == sorted(nodelist):
                        print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                        print('它的key为' + str(key))
                        allnodelist_keylist.append(key)
                        print('有了接受所有的节点了这样的节点了')
                        flag = 1
                    else:
                            if len(set(IDdict[key])) > nodelist_half_len:
                                best_node_list.append(key)


                print('计算增长曲线',len(set(best_node_list)))
                if len(set(best_node_list))> 0  :
                    t_scope += 1

                if t_scope == 1:
                 break  #相邻两个t内的得到节点

                if flag == 1:
                    break
                # 现在返回所有能接收到所有源点的。
                # '''
                # result = allnodelist_keylist
            print('len(best_node_list', len(set(best_node_list)))
            return list(set(best_node_list))









'''
抽象jaya算法出来，需要的参数是感染子图，所有个体数据集，固定源点个数。固定h或者listh
返回最好的样本就行了
'''
def  jaya(tempGraph, best_h_node,fix_number_source,best_h,singleRegionList):
    '''
        默认种群大小50，迭代4次，每次都随机更新种群大小。
    :param infectG:
    :param best_h_node:
    :param fix_number_source:
    :param best_h:
    :return:
    '''
    fix_number_sourcetemp = fix_number_source
    Sampleset = []
    for i in range(50):
        Sampleset.append(random.sample(best_h_node, fix_number_source))
    # infectG =infectG
    min_cover = 1
    min = 1
    mincover = None
    bestsourceNews = None
    minCoverlist = []
    for iter_number in range(4):
        for sample_index in range(len(Sampleset)):
            mincover = getSimilir1(Sampleset[sample_index], best_h, singleRegionList,
                                           tempGraph)
            # 随机更换，看如何让变好
            for j in range(1, 4, 1):  # 随机变4次，只要能变好
                # lateelement = [random.choice(best_h_node), random.choice(best_h_node),
                #                 random.choice(best_h_node),random.choice(best_h_node)]

                lateelement = [random.choice(best_h_node) for i in range(fix_number_source)]
                # print('当前输入的后面list' + str(lateelement))
                latemincover = getSimilir1(lateelement, best_h, singleRegionList, tempGraph)
                if mincover > latemincover:
                    mincover = latemincover  # 有更好地就要替换
                    # print("要进行替换了" + str(Sampleset[sample_index]) + '被替换成lateelement')
                    Sampleset[sample_index] = lateelement  # 替换
                    # print(Sampleset[sample_index])
        # print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
        # 计算样本集的similir，找出最好的。
        for sources in Sampleset:
            mincover = getSimilir1(sources, best_h, singleRegionList, tempGraph)
            if mincover < min:
                min = mincover  # 这一次最好的覆盖误差率
                bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。
        print('得到多源点情况最小的覆盖率为' + str(bestsourceNews) + str(min))
        minCoverlist.append([bestsourceNews, best_h, min])
    print(minCoverlist)
    result = sorted(minCoverlist, key=lambda x: (x[2]))
    return result[0]






'''
抽象jaya算法动态h出来出来，需要的参数是感染子图，所有个体数据集，固定源点个数。固定h或者listh
返回最好的样本就行了
'''
def  jayawith_dynami_H(tempGraph, best_h_node,fix_number_source,best_h_list,singleRegionList):
    '''
        默认种群大小50，迭代4次，每次都随机更新种群大小。
    :param infectG:
    :param best_h_node:
    :param fix_number_source:
    :param best_h:
    :return:
    '''
    fix_number_sourcetemp = fix_number_source
    Sampleset = []
    for i in range(50):
        Sampleset.append(random.sample(best_h_node, fix_number_source))
    # infectG =infectG
    min_cover = 1
    min = 1
    mincover = None
    bestsourceNews = None
    minCoverlist = []

    for best_h  in best_h_list:
        for iter_number in range(4):
            for sample_index in range(len(Sampleset)):
                mincover = getSimilir1(Sampleset[sample_index], best_h, singleRegionList,
                                               tempGraph)
                # 随机更换，看如何让变好
                for j in range(1, 4, 1):  # 随机变4次，只要能变好
                    # lateelement = [random.choice(best_h_node), random.choice(best_h_node),
                    #                 random.choice(best_h_node),random.choice(best_h_node)]

                    lateelement = [random.choice(best_h_node) for i in range(fix_number_source)]
                    # print('当前输入的后面list' + str(lateelement))
                    latemincover = getSimilir1(lateelement, best_h, singleRegionList, tempGraph)
                    if mincover > latemincover:
                        mincover = latemincover  # 有更好地就要替换
                        # print("要进行替换了" + str(Sampleset[sample_index]) + '被替换成lateelement')
                        Sampleset[sample_index] = lateelement  # 替换
                        # print(Sampleset[sample_index])
            # print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
            # 计算样本集的similir，找出最好的。
            for sources in Sampleset:
                mincover = getSimilir1(sources, best_h, singleRegionList, tempGraph)
                if mincover < min:
                    min = mincover  # 这一次最好的覆盖误差率
                    bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。
            print('得到多源点情况最小的覆盖率为' + str(bestsourceNews) + str(min))
            minCoverlist.append([bestsourceNews, best_h, min])
        print(minCoverlist)
    result = sorted(minCoverlist, key=lambda x: (x[2]))
    return result[0]






'''
真实源点(一个或者多个），动态h，仅仅找到最好的h，以及覆盖率就可以了
'''
def  jayawith_dynami_H_TrueSource(tempGraph, best_h_node,fix_number_source,best_h_list,singleRegionList):
    '''
        默认种群大小50，迭代4次，每次都随机更新种群大小。
    :param infectG:
    :param best_h_node:
    :param fix_number_source:
    :param best_h:
    :return:
    '''
    fix_number_sourcetemp = fix_number_source
    Sampleset = []
    for i in range(50):
        Sampleset.append(random.sample(best_h_node, fix_number_source))
    # infectG =infectG
    min_cover = 1
    min = 1
    mincover = None
    bestsourceNews = None
    minCoverlist = []

    for best_h  in best_h_list:
        for iter_number in range(4):
            for sample_index in range(len(Sampleset)):
                mincover = getSimilir1(Sampleset[sample_index], best_h, singleRegionList,
                                               tempGraph)
                # 随机更换，看如何让变好
                for j in range(1, 4, 1):  # 随机变4次，只要能变好
                    # lateelement = [random.choice(best_h_node), random.choice(best_h_node),
                    #                 random.choice(best_h_node),random.choice(best_h_node)]

                    lateelement = [random.choice(best_h_node) for i in range(fix_number_source)]
                    # print('当前输入的后面list' + str(lateelement))
                    latemincover = getSimilir1(lateelement, best_h, singleRegionList, tempGraph)
                    if mincover > latemincover:
                        mincover = latemincover  # 有更好地就要替换
                        # print("要进行替换了" + str(Sampleset[sample_index]) + '被替换成lateelement')
                        Sampleset[sample_index] = lateelement  # 替换
                        # print(Sampleset[sample_index])
            # print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
            # 计算样本集的similir，找出最好的。
            for sources in Sampleset:
                mincover = getSimilir1(sources, best_h, singleRegionList, tempGraph)
                if mincover < min:
                    min = mincover  # 这一次最好的覆盖误差率
                    bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。
            print('得到多源点情况最小的覆盖率为' + str(bestsourceNews) + str(min))
            minCoverlist.append([bestsourceNews, best_h, min])
        print(minCoverlist)
    result = sorted(minCoverlist, key=lambda x: (x[2]))
    return result[0]







'''
1  生成真实传播图，真实的点，真实的边。
2 用来测试单源的方法，


'''
def  product_progration_file(sourceNumber =1):
    # #拿到图
    # subGraph=self.get_Graph('../Propagation_subgraph/many_methods/result/chouqu.txt')

    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    initG =get_networkByFile('../../../data/treenetwork3000.txt')
    # initG = commons.get_networkByFile('../../../data/4_regular_graph_3000_data.txt')

    max_sub_graph = judge_data(initG)
    # source_list = product_sourceList(max_sub_graph, 2)
    source_list = product_sourceList(max_sub_graph, 1)
    # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
    infectG = propagation1(max_sub_graph, source_list)

    subinfectG = get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
    # 将在这里进行单源测试。


    #生成一个单源传播图。到文件中
    with open('subinfectG.txt', "a") as f:
        for edge in list(subinfectG.edges()):
            f.write(str(edge[0])+'  ' +str(edge[1])+ '\n')
    pass




'''
抽取函数分层，有两个函数，一个是知道h，一个是不知道h,但是有hlist
参数：分层的dict，以及h。
返回最好的候选集合，以及H。
'''




'''


在一个图中计算两个K点之间距离点匈牙利算法。
'''

def cal_distance(infectG,true_Source_list,findSource_list):
        lenA= len(true_Source_list)
        lenB = len(findSource_list)
        print('真实结果为'+str(true_Source_list))
        print('找到的为'+str(findSource_list))
        matrix_temp = []
        for i in range(0, len(true_Source_list)):
            temp = []
            for j in range(0, len(findSource_list)):
                temp.append(nx.shortest_path_length(infectG, source=true_Source_list[i],
                                                      target=findSource_list[j]))

            matrix_temp.append(temp)
        print('看下这个结果是如何'+str(matrix_temp))
        import numpy as np
        cost = np.array(matrix_temp)
        from scipy.optimize import linear_sum_assignment
        row_ind, col_ind = linear_sum_assignment(cost)
        allcost = cost[row_ind, col_ind].sum()
        print('总的代价为'+str(allcost))
        first_result_cost_list = [true_Source_list,findSource_list,allcost / lenA]
        distance_error = allcost/lenA
        return allcost / lenA



if __name__ == '__main__':

    initG = get_networkByFile('.././data/CA-GrQc.txt')
    max_sub_graph = judge_data(initG)
    # source_list =product_sourceList_circle(max_sub_graph, 2)
    # judge_data(initG)






