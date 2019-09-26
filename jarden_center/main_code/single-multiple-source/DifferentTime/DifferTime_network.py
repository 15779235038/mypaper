
import networkx as nx
import random
from networkx.algorithms import community
from munkres import Munkres, print_matrix



import commons
print(commons)

# from Girvan_Newman import GN #引用模块中的函数

# 读取文件中边关系，然后成为一个成熟的图,是有一个有效距离的。这里需要加


'''
有效距离的定义：度大点的传播距离较远。目前只有一个指标：根据度数的大小。度数越大，与他相连的边的权重越大。
越不容易传播、越可能在距离比较远的时间传播。以此为方法定义权重。
'''


import  numpy as np
np.set_printoptions(threshold=np.inf)
def ContractDict(dir, G):
    with open(dir, 'r') as f:
        for line in f:
            line1 = line.split()
            G.add_edge(int(line1[0]), int(line1[1]))

    for edge in  G.edges:
        G.add_edge(edge[0], edge[1], weight=1)
        # G.add_edge(edge[0],edge[1],weight=effectDistance(randomnum))
    print(len(list(G.nodes)))
    # G.remove_node(0)
    print (len(list(G.nodes)))
    return G

import math








import  commons

def  effectDistance(probily):
    return 1- math.log(probily)


def sigmoid(num):
    sig_L = 0
    sig_L = (1 / (1 + np.exp(-num)))
    return sig_L


def Normalization(x):
    return [(float(i) - min(x)) / float(max(x) - min(x)) for i in x]


def Algorithm(G, SourceList, time_sum, hlist):
    '''
    我们认为时间片是有问题的，这个时间片应该就是按照，不能是每隔一个时间片就传染一波。只能说每隔一个时间片就记录
    一线。传播也有有概率的。
    '''
    # this  are  two point to  传播
    # 每个传播节点都需要传播，让我们看看那些节点都需要传播
    nodelist = []
    edgelist = []
    infectionNodelist = []

    print('开始传染的点是' + str(SourceList))
    for j in SourceList:
        infectList = []
        infectList.append(j)
        G.node[j]['SI'] = 2
        for time in range(0,5):
             tempinfectList=[]
             for node in list(set(infectList)):
                for height in list(G.neighbors(node)):
                        randnum=random.random()
                        if randnum<0.5:
                            G.node[height]['SI'] = 2
                            tempinfectList.append(height)
             infectList.clear()
             for timeInfectnode in tempinfectList:
                 infectList.append(timeInfectnode)

        print('头两个感染社区点数为' + str(len(infectList)))

    return G






'''

本种传播方式适用于只传播50%节点就可以了

'''




def Algorithm1(G, SourceList, time_sum, hlist):
    '''
    我们认为时间片是有问题的，这个时间片应该就是按照，不能是每隔一个时间片就传染一波。只能说每隔一个时间片就记录
    一线。传播也有有概率的。
    '''
    # this  are  two point to  传播
    # 每个传播节点都需要传播，让我们看看那些节点都需要传播
    nodelist = []
    edgelist = []
    infectionNodelist = []

    print('开始传染的点是' + str(SourceList))
    infectList=[]
    stack = []
    for j in SourceList:
        # infectList.append(j)
        stack.append(j)
        G.node[j]['SI'] = 2

    #   没有具体的时间概念，传播大概到了50%，就停止传播。开始做实验

    count_number  =0
    fix_probli = 0.5
    while  1:
        tempinfectList = []
        print('stack',stack)
        for node_index in range(len(set(stack))):      #infectList表示的是每一个时刻传播到的点
            for height in list(G.neighbors(stack[node_index])):
                randnum = random.random()
                if randnum < 0.8:
                    G.node[height]['SI'] = 2
                    tempinfectList.append(height)
                    # print('G.neghbors(nodes)', list(G.neighbors(stack[node_index])))
        print('tempinfecLis',tempinfectList)
        # infectList=list(infectList)

        stack.extend(tempinfectList)
        stack = list(set(stack))
        #每一个时间点过去，判断有没有感染图的50%的点，感染了就可以，否则不行
        count=0
        for nodetemp  in  list(G.nodes):
            if G.node[ nodetemp]['SI'] ==2:
                    infectList.append(nodetemp)
                    count=count+1
        print ('被感染点为'+str(count)+'个')

        count_number  += 1
        if count_number  ==10:
            fix_probli = 1
        if  count/G.number_of_nodes() > 0.5:
            print ('超过50%节点了，不用传播啦')
            break






    return G













# 产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
def contractSource(G, sourceNum, sourceMaxDistance):
    sumlist = list(G.nodes)
    flag = 0
    flag1 = 0
    rumorSourceList = []
    # 先随机找个点，然后找到距离它为>6,小于10的吧。
    while (flag == 0):

        if sourceNum == 1:
            # random_RumorSource = random.randint(0, 7000)

            random_RumorSource = random.choice(sumlist)
            rumorSourceList.append(random_RumorSource)
            flag = 1
        elif sourceNum == 2:
            random_Rumo = random.sample(sumlist, 1)
            random_RumorSource = random_Rumo[0]
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
                    for j in range(0, 2):
                        for i in range(0, 4):
                            nehibor = list(G.neighbors(random_RumorSource))
                            randomnumber = random.randint(0, len(nehibor) - 1)
                            random_RumorSource = nehibor[randomnumber]
                        rumorSourceList.append(random_RumorSource)
                    if len(rumorSourceList) == 3 and len(rumorSourceList) == len(set(rumorSourceList)):  # 重复或者数目达不到要求:
                        print('找到了4个点')
                        flag1 = 1
                        flag = 1
                    elif len(rumorSourceList) == 3 and len(rumorSourceList) != len(set(rumorSourceList)):
                        print('是四个点，但是却有重复，只能够重新选择新的开始点')
                        flag1 = 1

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
                            randomnumber=random.randint(0, len(nehibor)-1)
                            random_RumorSource = nehibor[randomnumber]
                        rumorSourceList.append(random_RumorSource)
                    if len(rumorSourceList) == 4 and len(rumorSourceList) == len(set(rumorSourceList)):  # 重复或者数目达不到要求:
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
                    nehibor=[]
                    for  j  in range(0,4):
                        for i in range(0, 4):
                            nehibor = list(G.neighbors(random_RumorSource))
                            randomnumber = random.randint(0, len(nehibor)-1)
                            random_RumorSource = nehibor[randomnumber]
                        rumorSourceList.append(random_RumorSource)
                    if len(rumorSourceList) == 5 and len(rumorSourceList) == len(set(rumorSourceList)):  # 重复或者数目达不到要求:
                        print('找到了5个点')
                        flag1 = 1
                        flag = 1
                    elif len(rumorSourceList) == 5 and len(rumorSourceList) != len(set(rumorSourceList)):
                        print('是5个点，但是却有重复，只能够重新选择新的开始点')
                        flag1 = 1

    # 查看产生随机源点的个数2，并且他们距离为3.
    print('源点个数' + str(len(rumorSourceList)) + '以及产生的真实源点是' + str(rumorSourceList))
    # rumorSourceList=[125,4022]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 95
    print('真实两源感染是' + str(rumorSourceList))
    return rumorSourceList


import csv


def ConvertGToCsv(G, dir):
    # python2可以用file替代open
    with open(dir, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source", "target", "weight"])
        for u, v in G.edges():
            # print (G.adj[u][v]['Infection'])
            writer.writerow([u, v, G.adj[u][v]['Infection']])


# 传播子图代入

def ConvertGToCsvSub(G, dir):
    # python2可以用file替代open
    with open(dir, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source", "target", "weight"])
        for u, v in G.edges():
            # print (G.adj[u][v]['Infection'])
            writer.writerow([u, v, G.adj[u][v]['weight']])


from queues1 import *


def getTuresubinfectionG(infectG, randomInfectionsource):
    infectionNodeList = []
    for nodes in list(infectG.nodes):
        if infectG.node[nodes]['SI'] == 2:
            infectionNodeList.append(nodes)


    return infectionNodeList


def multiplelistTo_ormialy(mutiolist):
    alllist = []
    for i in range(len(mutiolist)):
        for j in range(len(mutiolist[i])):
            alllist.append(mutiolist[i][j])
    return alllist


import random


def getmultipleCommunity(infectionG):
    # return  multipleCommuniytlist
    multipleCommuniytlist = []

    # start  by  a  random  SInode
    randomInfectionNode = 0
    # sum  nodes  in  infect G:
    sumlist = list(infectionG.nodes)
    flag1 = 0
    flag2 = 0
    flag = 0
    while flag == 0:
        infectionList = []
        allList = []
        diff_list = []
        # 刚开始啥社区都没有
        if len(multipleCommuniytlist) == 0:
            print('在没有社区的操作')
            # 刚开始随机产生一个点。
            while flag1 == 0:
                randomnumber = random.sample(sumlist, 1)
                if infectionG.node[randomnumber[0]]['SI'] == 2:
                    randomInfectionNode = randomnumber[0]
                    flag1 = 1
            # print('第一个感染社区随机开始的点感染点' + str(randomInfectionNode))
            partion1 = getTuresubinfectionG(infectionG, randomInfectionNode)
            multipleCommuniytlist.append(partion1)  # 第一个社区
            print('把第1个社区加入进去，现在感染社区点个数为' + str(len(multipleCommuniytlist)))
            flag = 1

    # print('感染社区个数以及各自人数')
    # print(len(multipleCommuniytlist))
    # print(len(multipleCommuniytlist[0]))
    return multipleCommuniytlist


# 随机产生一个源点。
def randomSourcelist(subinfectG):
    nodelist = []
    for node in subinfectG:
        nodelist.append(node)
    slice = random.sample(nodelist, 1)
    print('随机产生的源点是' + str(slice))
    sllietemp = slice[0]
    return sllietemp


from itertools import combinations

def listFlatten(src):
    tmp = []
    for i in src:
        if type(i) is not list:
            tmp.append(i)
        else:
            tmp.extend(listFlatten(i))
    return tmp






def getkey(pos, value):
    return {value: key for key, value in pos.iteritems()}[value]


import matplotlib.pyplot  as plt


def findmultiplesource(singleRegionList, infectionG, trueSourcelist,sourceNumber):
    # 首先需要判断是否多源。不断找源点去对这个区域。
    tempGraph = nx.Graph()
    tempGraphNodelist = []
    for edge in infectionG.edges:
        # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
        if edge[0] in singleRegionList and edge[1] in singleRegionList:
            tempGraph.add_edges_from([edge], weight=1)
            tempGraphNodelist.append(edge[0])
            tempGraphNodelist.append(edge[1])

    print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
    print('这个感染区域的传播图节点个数')
    print(tempGraph.number_of_nodes())
    Alternativenodeset = list(tempGraph.nodes())  # 备选集合。
    print ('tempgraph的所有点数'+str(len(Alternativenodeset)))

    minCoverlist = []

    print('在源点在' + str(sourceNumber) + '个数的情况下')
    # print('在h为' + str(h) + '的情况下')
    if sourceNumber == 1:  # 单源点。
        # 单源情况，怎么办。
        # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
        '''
        1 变种jaya算法，首先生成100个种群大小。
        2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
        3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。
        '''
        min = 200
        print('多源情况,先考察同时传播传播')
        print('源点个数为' + str(sourceNumber) + '情况')
        # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
        # combinationList = list(combinations(Alternativenodeset, sourceNumber))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
        sourceAndH = []
        for htemp in range(2, 5):
            for sourcetmep in Alternativenodeset:
                sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
        # 从combinationList中寻找100个样本集。
        Sampleset = random.sample(sourceAndH, 50)
        # print('样本集产生完毕，100个，是' + str(Sampleset))
        bestsourceNews = []
        # 迭代五次
        for i in range(1, 4):
            # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
            for sourcesi in range(len(Sampleset)):
                # print('当前输入list' + str(Sampleset[sourcesi]))
                mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                      infectionG)
                # 往后5个位置找一个比它更好地点。只要找更好就行,找不到就返回不变就可以
                # 当前的下标
                currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                length = len(sourceAndH)
                for j in range(1, 100, 25):  # 要防止数组越界
                    if currentindex + j < length:  # 只要在范围里面才行。
                        lateelement = sourceAndH[currentindex + j]
                        # print('当前输入的后面list' + str(lateelement))
                        latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                        if mincover > latemincover:
                            mincover = latemincover  # 有更好地就要替换
                            # print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                            Sampleset[sourcesi] = lateelement  # 替换
                            # print(Sampleset[sourcesi])

        # print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
        # 计算样本集的similir，找出最好的。
        for sources in Sampleset:
            mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
            if mincover < min:
                min = mincover  # 这一次最好的覆盖误差率
                bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

        print('得到多源点情况最小的覆盖率为' + str(min))
        minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])


    elif sourceNumber == 2:


        resultListAll = []
        for h in range(2, 4):
            # 随机找两个源，开始
            sourcePartition = []
            randomSource = []
            for number in range(0, sourceNumber):
                randomSource.append(random.choice(Alternativenodeset))
                sourcePartition.append([])
            for index in range(len(sourcePartition)):
                sourcePartition[index].append(randomSource[index])

            # print(sourcePartition)  # 3个区域划分完毕



            sourceBFS=[]
            #那么现在根据增大h吧，让我看看结果。增大h，然后构建BFS树。
            for  source in randomSource:
                sourceBFS.append(list(nx.bfs_tree(tempGraph, source=source, depth_limit=h).nodes))

            #然后这sourceBFS包括所有的这两个点构成h的list了。求个合集，跟总的求差集。把差的重新分配好。
            unionList=list(set(listFlatten(sourceBFS)))
            # print('两个BFS的合集的个数为' + str(len(unionList)))
            difSet=list(set(Alternativenodeset).difference(set( unionList)))
            # print ('两个bfs和整个图差集的个数为'+str(len(difSet)))



            for node in difSet:   #针对差集重新分配
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

            result = []
            for singlePartition in sourceBFS:  #对每个分区求jarden  center
                source1G = nx.Graph()  # 构建新的单源传播圆出来
                for edge in tempGraph.edges:
                    if edge[0] in singlePartition and edge[1] in singlePartition:
                        source1G.add_edge(edge[0], edge[1])

                # egitinum=nx.laplacian_spectrum(source1G)
                # print('特征值是'+str(egitinum))
                # for eg in egitinum:
                #     if eg==0:
                #      print (eg)

                # print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
                #     source1G.number_of_edges()))
                #将某些无邻居的点删除。因为根本不是一个连接子图。
                for  removenode  in  list(source1G.nodes):
                    if   len(list(source1G.neighbors(removenode)))==0:
                        source1G.remove_node(removenode)

                # print ('移除后顶点个数为'+str(source1G.number_of_nodes()))






                # 在nodelist找出源点来。
                times = 40  # 时间刻多点
                IDdict = {}
                IDdict_dup = {}
                # 先赋予初始值。
                for node in list(source1G.nodes):
                    # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
                    IDdict[node] = [node]
                    IDdict_dup[node] = [node]
                allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
                for t in range(times):
                    print('t为' + str(
                        t) + '的时候-----------------------------------------------------------------------------')
                    for node in list(source1G.nodes):  # 对每一个节点来说
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
                        if sorted(IDdict[key]) == sorted(singlePartition):
                            print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                            print('它的key为' + str(key))
                            allnodelist_keylist.append(key)
                            print('有了接受所有的节点了这样的节点了')
                            flag = 1

                    if flag == 1:
                        break
                # print (IDdict)
                print(allnodelist_keylist)

                result_jarden = 0
                resultlist=[]
                # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
                if len(allnodelist_keylist) == 1:
                    print('那就是这个源点了')
                    result_jarden = allnodelist_keylist[0]
                else:
                    # 构建样本路径
                    print('构建样本路径看看')
                    jarcenlist = []
                    for i in allnodelist_keylist:
                        jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                        resultlist = sorted(jarcenlist, key=lambda x: x[1])
                    result_jarden = resultlist[0][0]
                    print('构建样本路径之后结果为' + str(resultlist[0][0]))
                result.append( result_jarden )
            resultListAll.append(result)
            print ('输出resultListAll为多少'+str(resultListAll))
            distance=[]
            if len(resultListAll)>=2:
                    temp_result=resultListAll[-2:]
                    distance.append(nx.shortest_path_length(infectionG,source=temp_result[0][0],target=temp_result[1][0]))
                    distance.append(nx.shortest_path_length(infectionG,source=temp_result[0][1],target=temp_result[1][1]))

                    print ('两者距离之和让我们看看怎么显示'+str(distance))
                    if  max(distance)<=2:
                        break



        return resultListAll[-1:]







    elif sourceNumber == 3:

        resultListAll = []
        for h in range(2, 4):
            # 随机找两个源，开始
            sourcePartition = []
            randomSource = []
            for number in range(0, sourceNumber):
                randomSource.append(random.choice(Alternativenodeset))
                sourcePartition.append([])
            for index in range(len(sourcePartition)):
                sourcePartition[index].append(randomSource[index])

            print(sourcePartition)  # 3个区域划分完毕

            sourceBFS = []
            # 那么现在根据增大h吧，让我看看结果。增大h，然后构建BFS树。
            for source in randomSource:
                sourceBFS.append(list(nx.bfs_tree(tempGraph, source=source, depth_limit=h).nodes))

            # 然后这sourceBFS包括所有的这两个点构成h的list了。求个合集，跟总的求差集。把差的重新分配好。
            unionList = list(set(listFlatten(sourceBFS)))
            print('两个BFS的合集的个数为' + str(len(unionList)))
            difSet = list(set(Alternativenodeset).difference(set(unionList)))
            print('两个bfs和整个图差集的个数为' + str(len(difSet)))

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
                #
                # print('-------------------')
                # print('查看社区数目' + str(len(sourceBFS)))
                sourceBFS[resulttemp[0][0]].append(node)

            result = []
            for singlePartition in sourceBFS:  # 对每个分区求jarden  center
                source1G = nx.Graph()  # 构建新的单源传播圆出来
                for edge in tempGraph.edges:
                    if edge[0] in singlePartition and edge[1] in singlePartition:
                        source1G.add_edge(edge[0], edge[1])

                # egitinum = nx.laplacian_spectrum(source1G)
                # print('特征值是' + str(egitinum))
                # for eg in egitinum:
                #     if eg == 0:
                #         print(eg)

                # print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
                #     source1G.number_of_edges()))
                # 将某些无邻居的点删除。因为根本不是一个连接子图。
                for removenode in list(source1G.nodes):
                    if len(list(source1G.neighbors(removenode))) == 0:
                        source1G.remove_node(removenode)

                # print('移除后顶点个数为' + str(source1G.number_of_nodes()))

                # 在nodelist找出源点来。
                times = 40  # 时间刻多点
                IDdict = {}
                IDdict_dup = {}
                # 先赋予初始值。
                for node in list(source1G.nodes):
                    # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
                    IDdict[node] = [node]
                    IDdict_dup[node] = [node]
                allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
                for t in range(times):
                    # print('t为' + str(
                    #     t) + '的时候-----------------------------------------------------------------------------')
                    for node in list(source1G.nodes):  # 对每一个节点来说
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
                        if sorted(IDdict[key]) == sorted(singlePartition):
                            print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                            print('它的key为' + str(key))
                            allnodelist_keylist.append(key)
                            print('有了接受所有的节点了这样的节点了')
                            flag = 1

                    if flag == 1:
                        break
                # print (IDdict)
                print(allnodelist_keylist)

                result_jarden = 0
                resultlist = []
                # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
                if len(allnodelist_keylist) == 1:
                    print('那就是这个源点了')
                    result_jarden = allnodelist_keylist[0]
                else:
                    # 构建样本路径
                    print('构建样本路径看看')
                    jarcenlist = []
                    for i in allnodelist_keylist:
                        jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                        resultlist = sorted(jarcenlist, key=lambda x: x[1])
                    result_jarden = resultlist[0][0]
                    print('构建样本路径之后结果为' + str(resultlist[0][0]))
                result.append(result_jarden)
            resultListAll.append(result)
            print('输出resultListAll为多少' + str(resultListAll))
            distance = []
            if len(resultListAll) >= 2:
                temp_result = resultListAll[-2:]
                distance.append(nx.shortest_path_length(infectionG, source=temp_result[0][0], target=temp_result[1][0]))
                distance.append(nx.shortest_path_length(infectionG, source=temp_result[0][1], target=temp_result[1][1]))

                print('两者距离之和让我们看看怎么显示' + str(distance))
                if max(distance) <= 2:
                    break

        return resultListAll[-1:]

    elif sourceNumber == 4:

        resultListAll = []
        for h in range(2, 5):
            # 随机找两个源，开始
            sourcePartition = []
            randomSource = []
            for number in range(0, sourceNumber):
                randomSource.append(random.choice(Alternativenodeset))
                sourcePartition.append([])
            for index in range(len(sourcePartition)):
                sourcePartition[index].append(randomSource[index])
            print(sourcePartition)  # 3个区域划分完毕



            sourceBFS=[]
            #那么现在根据增大h吧，让我看看结果。增大h，然后构建BFS树。
            for  source in randomSource:
                sourceBFS.append(list(nx.bfs_tree(tempGraph, source=source, depth_limit=h).nodes))

            #然后这sourceBFS包括所有的这两个点构成h的list了。求个合集，跟总的求差集。把差的重新分配好。
            unionList=list(set(listFlatten(sourceBFS)))
            print('两个BFS的合集的个数为' + str(len(unionList)))
            difSet=list(set(Alternativenodeset).difference(set( unionList)))
            print ('两个bfs和整个图差集的个数为'+str(len(difSet)))




            for node in difSet:   #针对差集重新分配
                # 分别计算到两个源的距离。
                lengthlist = []
                for index1 in range(0, sourceNumber):
                    lengthlist.append([index1, randomSource[index1], node,
                                       nx.shortest_path_length(tempGraph, source=node, target=randomSource[index1])])
                resulttemp = sorted(lengthlist, key=lambda x: (x[3]))
                print('输出关于这个东西的距离集合看看')
                print(resulttemp)
                # 加入第一个队列中。
                sourceBFS[resulttemp[0][0]].append(node)

            result = []
            for singlePartition in sourceBFS:  #对每个分区求jarden  center
                source1G = nx.Graph()  # 构建新的单源传播圆出来
                for edge in tempGraph.edges:
                    if edge[0] in singlePartition and edge[1] in singlePartition:
                        source1G.add_edge(edge[0], edge[1])

                print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
                    source1G.number_of_edges()))
                # 在nodelist找出源点来。
                times = 40  # 时间刻多点
                IDdict = {}
                IDdict_dup = {}
                # 先赋予初始值。
                for node in list(source1G.nodes):
                    # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
                    IDdict[node] = [node]
                    IDdict_dup[node] = [node]
                allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
                for t in range(times):
                    print('t为' + str(
                        t) + '的时候-----------------------------------------------------------------------------')
                    for node in list(source1G.nodes):  # 对每一个节点来说
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
                        if sorted(IDdict[key]) == sorted(singlePartition):
                            print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                            print('它的key为' + str(key))
                            allnodelist_keylist.append(key)
                            print('有了接受所有的节点了这样的节点了')
                            flag = 1

                    if flag == 1:
                        break
                # print (IDdict)
                print(allnodelist_keylist)

                result_jarden = 0
                resultlist=[]
                # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
                if len(allnodelist_keylist) == 1:
                    print('那就是这个源点了')
                    result_jarden = allnodelist_keylist[0]
                else:
                    # 构建样本路径
                    print('构建样本路径看看')
                    jarcenlist = []
                    for i in allnodelist_keylist:
                        jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                        resultlist = sorted(jarcenlist, key=lambda x: x[1])
                    result_jarden = resultlist[0][0]
                    print('构建样本路径之后结果为' + str(resultlist[0][0]))
                result.append( result_jarden )
            resultListAll.append(result)
            print ('输出resultListAll为多少'+str(resultListAll))
            distance=[]
            if len(resultListAll)>=2:
                    temp_result=resultListAll[-2:]
                    distance.append(nx.shortest_path_length(infectionG,source=temp_result[0][0],target=temp_result[1][0]))
                    distance.append(nx.shortest_path_length(infectionG,source=temp_result[0][1],target=temp_result[1][1]))
                    distance.append(nx.shortest_path_length(infectionG, source=temp_result[0][2], target=temp_result[1][2]))
                    distance.append(
                        nx.shortest_path_length(infectionG, source=temp_result[0][3], target=temp_result[1][3]))
                    print ('两者距离之和让我们看看怎么显示'+str(distance))
                    if  max(distance)<=2:
                        break



        return resultListAll[-1:]



    elif sourceNumber == 5:
        resultListAll = []
        for h in range(3, 6):
            # 随机找两个源，开始
            sourcePartition = []
            randomSource = []
            for number in range(0, sourceNumber):
                randomSource.append(random.choice(Alternativenodeset))
                sourcePartition.append([])
            # for index in range(len(sourcePartition)):
            #     sourcePartition[index].append(randomSource[index])
            #     Alternativenodeset.remove(randomSource[index])
            # print(sourcePartition)  # 3个区域划分完毕

            sourceBFS = []
            # 那么现在根据增大h吧，让我看看结果。增大h，然后构建BFS树。
            for source in randomSource:
                sourceBFS.append(list(nx.bfs_tree(tempGraph, source=source, depth_limit=h).nodes))

            # 然后这sourceBFS包括所有的这两个点构成h的list了。求个合集，跟总的求差集。把差的重新分配好。
            unionList = list(set(listFlatten(sourceBFS)))
            print('两个BFS的合集的个数为' + str(len(unionList)))
            difSet = list(set(Alternativenodeset).difference(set(unionList)))
            print('两个bfs和整个图差集的个数为' + str(len(difSet)))

            for node in difSet:  # 针对差集重新分配
                # 分别计算到两个源的距离。
                lengthlist = []
                for index1 in range(0, sourceNumber):
                    lengthlist.append([index1, randomSource[index1], node,
                                       nx.shortest_path_length(tempGraph, source=node, target=randomSource[index1])])
                resulttemp = sorted(lengthlist, key=lambda x: (x[3]))
                print('输出关于这个东西的距离集合看看')
                print(resulttemp)
                # 加入第一个队列中。
                sourceBFS[resulttemp[0][0]].append(node)

            result = []
            for singlePartition in sourceBFS:  # 对每个分区求jarden  center
                source1G = nx.Graph()  # 构建新的单源传播圆出来
                for edge in tempGraph.edges:
                    if edge[0] in singlePartition and edge[1] in singlePartition:
                        source1G.add_edge(edge[0], edge[1])

                print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
                    source1G.number_of_edges()))
                # 在nodelist找出源点来。
                times = 40  # 时间刻多点
                IDdict = {}
                IDdict_dup = {}
                # 先赋予初始值。
                for node in list(source1G.nodes):
                    # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
                    IDdict[node] = [node]
                    IDdict_dup[node] = [node]
                allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
                for t in range(times):
                    print('t为' + str(
                        t) + '的时候-----------------------------------------------------------------------------')
                    for node in list(source1G.nodes):  # 对每一个节点来说
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
                        if sorted(IDdict[key]) == sorted(singlePartition):
                            # print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                            # print('它的key为' + str(key))
                            allnodelist_keylist.append(key)
                            # print('有了接受所有的节点了这样的节点了')
                            flag = 1

                    if flag == 1:
                        break
                # print (IDdict)
                print(allnodelist_keylist)

                result_jarden = 0
                resultlist = []
                # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
                if len(allnodelist_keylist) == 1:
                    print('那就是这个源点了')
                    result_jarden = allnodelist_keylist[0]
                else:
                    # 构建样本路径
                    print('构建样本路径看看')
                    jarcenlist = []
                    for i in allnodelist_keylist:
                        jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                        resultlist = sorted(jarcenlist, key=lambda x: x[1])
                    result_jarden = resultlist[0][0]
                    # print('构建样本路径之后结果为' + str(resultlist[0][0]))
                result.append(result_jarden)
            resultListAll.append(result)
            # print('输出resultListAll为多少' + str(resultListAll))
            distance = []
            if len(resultListAll) >= 2:
                temp_result = resultListAll[-2:]
                distance.append(nx.shortest_path_length(infectionG, source=temp_result[0][0], target=temp_result[1][0]))
                distance.append(nx.shortest_path_length(infectionG, source=temp_result[0][1], target=temp_result[1][1]))
                distance.append(nx.shortest_path_length(infectionG, source=temp_result[0][2], target=temp_result[1][2]))
                distance.append(
                    nx.shortest_path_length(infectionG, source=temp_result[0][3], target=temp_result[1][3]))
                distance.append(
                    nx.shortest_path_length(infectionG, source=temp_result[0][4], target=temp_result[1][4]))
                # print('两者距离之和让我们看看怎么显示' + str(distance))
                if max(distance) <= 2:
                    break

        return resultListAll[-1:]

    # listToTxt(minCoverlist, 'newresult.txt')
    # print(minCoverlist)
    # 返回的应该是最可能的结果。获取mincover最小的返回。第三个元素才是需要考虑东西。
    # listToTxt(minCover, 'result.txt')
    result = sorted(minCoverlist, key=lambda x: (x[2]))
    # listToTxt(result[0], 'newresult.txt')
    return result[0]


def listToTxt(listTo, dir):
    fileObject = open(dir, 'a')
    fileObject.write(str(listTo))
    fileObject.write('\n')
    fileObject.close()


def getSimilir(ulist, hlist, singleRegionList, infectionG):
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
            #计算交集在并集中的出现次数。
        ratios = count / len(Union)
        ratio = 1.0 - ratios
        # print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))
        return abs(ratio)



    else:
        # 多源点,获得多源点的覆盖率
        circleNodesList = []
        for u in ulist:
            circleNodesList.extend(list(nx.bfs_tree(infectionG, source=u, depth_limit=hlist).nodes))
        circleNodesListnew = list(set(circleNodesList))

        # count
        Intersection = list(set(circleNodesList).intersection(set(singleRegionList)))  # 交集
        Union = list(set(circleNodesList).union(set(singleRegionList)))  # 并集
        count = 0
        for i in Intersection:
            if i in Union:
                count = count + 1
        ratios = count / len(Union)
        ratio = 1.0 - ratios
        # print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))

        return abs(ratio)


import sys


def getListfortxt(rootdir):
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)

    lists = [x for x in lines if x != []]
    return lists


'''
this   function  :   to  get  sourcelist fo  everyRegionList  and   caluce  every  distance of  source and result


'''

import math
import numpy

def multiplePartion(mutiplelist, infectionG, rumorSourceList,sourceNumber):
    # 所有单源list
    allsigleSourceList = []

    # 将第一个传播区域定下来。
    import datetime
    starttime = datetime.datetime.now()
    # long running,这里可以读的文件代替，就比较省时间。反正都是为了allsigleSourcellist填充

    '''   这个是保留项，我觉得反转算法有点问题，反正（u,h是写完了）,下面这个很好时间'''
    for sigleReionlist in mutiplelist:
        allsigleSourceList.append(findmultiplesource(sigleReionlist, infectionG, rumorSourceList,sourceNumber))

    # 构建关于这个社区的传播子图
    tempGraph1 = nx.Graph()
    for edge in infectionG.edges:
        # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
        if edge[0] in mutiplelist[0] and edge[1] in mutiplelist[0]:
            tempGraph1.add_edges_from([edge], weight=1)
    print('这个感染区域的传播子图边个数')
    print(tempGraph1.number_of_edges())
    print(tempGraph1.number_of_nodes())

    resultSource = []
    # allsigleSourceList=[[(472, 5397), 3, 0.08817960508520417]]
    # 现在已经返回关于每个社区的源点及其社区了，开始画图吧。
    # print('最后我们找到的误差率最低的的每个分区的圆点和他的h是' + str(allsigleSourceList))

    for sigleRegionSource in allsigleSourceList:
        if isinstance(sigleRegionSource[0], int):  # 单源点
            print ('算出来的结果为')
            resultSource.clear()
            resultSource.append(sigleRegionSource[0])

        elif len(sigleRegionSource[0]) == 2:
            resultSource.clear()
            for  source in sigleRegionSource[0]:
                resultSource.append(source)
        elif len(sigleRegionSource[0]) == 3:
            resultSource.clear()
            for source in sigleRegionSource[0]:
                resultSource.append(source)

        elif len(sigleRegionSource[0]) == 4:
            resultSource.clear()
            for source in sigleRegionSource[0]:
                resultSource.append(source)

        elif len(sigleRegionSource[0]) == 5:
            resultSource.clear()
            for source in sigleRegionSource[0]:
                resultSource.append(source)


    # print('总的用反转算法算出来的结果为' + str(resultSource))
    # listToTxt(resultSource, 'newresult.txt')




    listToTxt(rumorSourceList, 'compare.txt')
    listToTxt(resultSource, 'compare.txt')


    lenA = len(rumorSourceList)
    lenB = len(resultSource)
    print('真实结果为' + str(rumorSourceList))
    print('找到的为' + str(resultSource))
    matrix_temp = []
    for i in range(0, len(rumorSourceList)):
        temp = []
        for j in range(0, len(resultSource)):
            temp.append(nx.shortest_path_length(infectionG, source=rumorSourceList[i],
                                                target=resultSource[j]))

        matrix_temp.append(temp)
    print('看下这个结果是如何' + str(matrix_temp))
    import numpy as np
    cost = np.array(matrix_temp)
    from scipy.optimize import linear_sum_assignment
    row_ind, col_ind = linear_sum_assignment(cost)
    allcost = cost[row_ind, col_ind].sum()
    print('总的代价为' + str(allcost))
    return allcost/len(rumorSourceList)




















# 设计反向传播算法，接收参数。u，h，infectG。
def revsitionAlgorithm(u, h, infectG, subinfectG):
    print('反转算法参数,u和h' + str(u) + '----------' + str(h))
    nodelist = list(nx.bfs_tree(subinfectG, source=u, depth_limit=h).nodes)
    source1G = nx.Graph()  # 构建新的单源传播圆出来
    for edge in subinfectG.edges:
        if edge[0] in nodelist and edge[1] in nodelist:
            source1G.add_edge(edge[0], edge[1])

    print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(source1G.number_of_edges()))
    # 在nodelist找出源点来。
    times =15  # 时间刻多点
    IDdict = {}
    IDdict_dup = {}
    # 先赋予初始值。
    for node in list(source1G.nodes):
        # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
        IDdict[node] = [node]
        IDdict_dup[node] = [node]
    allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
    for t in range(times):
        # print('t为' + str(t) + '的时候-----------------------------------------------------------------------------')
        for node in nodelist:  # 对每一个节点来说
            for heighbour in list(source1G.neighbors(node)):  # 对每一个节点的邻居来说
                retD = list(set(IDdict[heighbour]).difference(set(IDdict[node])))  # 如果邻居中有这个node没有的，那就加到这个node中去。
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
                # print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                # print('它的key为' + str(key))
                allnodelist_keylist.append(key)
                # print('有了接受所有的节点了这样的节点了')
                flag = 1

        if flag == 1:
            break
    # print (IDdict)
    print(allnodelist_keylist)

    result = 0
    resultlist = []
    # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
    if len(allnodelist_keylist) == 1:
        # print('那就是这个源点了')
        result = allnodelist_keylist[0]
    else:
        # 构建样本路径
        # print('构建样本路径看看')
        jarcenlist = []
        for i in allnodelist_keylist:
            jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
            resultlist = sorted(jarcenlist, key=lambda x: x[1])
        result = resultlist[0][0]
        # print('构建样本路径之后结果为' + str(resultlist[0][0]))

    return result

import numpy as np
import matplotlib.pyplot as plt


def plotform(x, y):
    x = range(1, 4)
    y_train = [1.0, 1.4, 1.1 , 1.225,1.44]
    y_test = [2.53, 2, 31, 2.12,1]
    # plt.plot(x, y, 'ro-')
    # plt.plot(x, y1, 'bo-')
    # pl.xlim(-1, 11)  # 限定横轴的范围
    # pl.ylim(-1, 110)  # 限定纵轴的范围

    plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='our method')
    plt.plot(x, y_test, marker='*', ms=10, label='other method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of sources')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    plt.title("Wiki-Vote  data")  # 标题
    plt.savefig('f1.png')
    plt.show()


import datetime

if __name__ == '__main__':

    starttime = datetime.datetime.now()
    '''

    1  产生一个社区，无非就是源点从1到5.然后用我们这种方式
    判断准确率。
    '''

    # 1 产生这个图。

    #  制造这个图
    Ginti = nx.Graph()
    # 初始化图,加很多节点
    # for index in range(1,1005):
    #     print (index)
    #     Ginti.add_node(index)

    # 构建图，这个图是有有效距离的。
    # G = ContractDict('../data/CA-GrQc.txt', Ginti)

    G = ContractDict('../data/Wiki-Vote.txt', Ginti)

    # 因为邮件是一个有向图，我们这里构建的是无向图。
    print('一开始图的顶点个数', G.number_of_nodes())
    print('一开始图的边个数', G.number_of_edges())

    #  先给全体的Cn、Scn,time的0的赋值。
    for node in list(G.nodes):
        G.add_node(node, SI=1)

    # 初始化所有边是否感染。Infection
    for edge in list(G.edges):
        G.add_edge(edge[0], edge[1], Infection=1)

    print('这个图产生完毕')

    sourceList = []
    #  从1个源点产生到5个源点。但都是有交集的。按照交叉领域来比较？
    #
    # for  sourceNumber  in  range(1,4):
    #     sourceList.append(contractSource(G,sourceNumber,2))
    # print (sourceList)
    #
    # print ('产生3源点成功------------------------------------------')

    # 产生10次，每次都有误差，计算出来。并统计。
    max_sub_graph = commons.judge_data(G)
    for i in range(1, 21):
        source_list = commons.product_sourceList(max_sub_graph, 3)
        sourceList.append(source_list)


    errordistanceList = []  # 误差集合。
    errorSum = 0
    errorCount=0
    infectGs = nx.Graph()
    # 对每一个单源点都有这个操作。
    for singleSource in sourceList:
        #  先给全体的Cn、Scn,time的0的赋值。
        for node in list(G.nodes):
            G.add_node(node, SI=1)
        # 初始化所有边是否感染。Infection
        for edge in list(G.edges):
            G.add_edge(edge[0], edge[1], Infection=1)
        # 开始之前都要刷新这个图，
        # infectG = commons.propagation1(G, singleSource, 5)
        print('源点传播成功')
        # max_sub_graph = commons.judge_data(G)
        # source_list = commons.product_sourceList(max_sub_graph, 3)
        # true_Source_list = source_list
        infectGs = commons.propagation1(max_sub_graph, singleSource)  # 开始传染
        #  找社区，按照代理，只能找到一个社区的。
        multipList = getmultipleCommunity(infectGs)
        errordistance = multiplePartion(multipList, infectGs, singleSource, 3)
        errorSum = errorSum + errordistance
        errordistanceList.append(errordistance)
        listToTxt(str(datetime.datetime.now()), 'DiffTime.txt')
        errorCount=errorCount+1
        listToTxt('输出第'+str(errorCount)+'次结果看看', 'DiffTime.txt')
        listToTxt(errordistanceList, 'DiffTime.txt')
        listToTxt('输出平均值' + str(errorSum / len(errordistanceList)), 'DiffTime.txt')
        print('误差集合为' + str(errordistanceList))
        print(str(errorSum / len(errordistanceList)))
    print(errorSum / 20)
    # long running
    endtime = datetime.datetime.now()
    print('执行了这么长时间')
    print((endtime - starttime).seconds)























