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







import copy

'''
用队列重写SI传播过程，propagation会传播并且还会

传播方案2：从源点开始往外面传播，按照队列传播形式。每次所有感染的点都试图感染身边的点。而不是一层一层来
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
        G.node[source]['SI'] = 2
        queue.add(source)

    while 1:
            propagation_layer_list = [] #传播的BFS某一层
            propagation_layer_list.extend(list(queue)) #总是删除第一个。这里不删除
            print('第几层为'+str(len(propagation_layer_list)))
            for source in propagation_layer_list:
                for height in list(G_temp.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.5:
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
            if count / G_temp.number_of_nodes() > 0.4:
                print('超过50%节点了，不用传播啦')
                break
    #数据进去图，看看
    x_list= [i for i in  range(len(y_list))]

    # plot(x_list,y_list,'pro'+str(number))
    # G_temp = G
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

    #特征向量中心性。
    centrality = nx.eigenvector_centrality(subinfectG)
    sort_eigener_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    print('eigenvector_centrality', sort_eigener_centrality)
    # self.center = sort_eigener_centrality[0][0]

    import math
    #Kaza中心性
    # G = nx.path_graph(4)
    maxnumber = max(nx.adjacency_spectrum(subinfectG))
    print(maxnumber)
    phi = (1 + math.sqrt(5)) / 2.0  # largest eigenvalue of adj matrix
    centrality = nx.katz_centrality(subinfectG, 1/ maxnumber -0.01)
    katz_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    print('katz_centrality',katz_centrality)



    center_list = []
    center_list.append(sort_eccentricity_dict[0][0])
    center_list.append(sort_colse_centrality_dict[0][0])
    center_list.append(sort_degree_centrality[0][0])
    center_list.append(sort_eigener_centrality[0][0])
    center_list.append(katz_centrality[0][0])


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







'''
      适用于公式计算公式       为1-  树并集交感染图/树并集并感染图
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
            # count
            Intersection = list(set(circleNodesListnew).intersection(set(singleRegionList)))  # 交集
            Union = list(set(circleNodesList).union(set(singleRegionList)))  # 并集
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
    source_list =product_sourceList(max_sub_graph, 2)
    judge_data(initG)






