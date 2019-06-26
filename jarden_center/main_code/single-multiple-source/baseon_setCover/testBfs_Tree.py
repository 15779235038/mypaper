
import networkx as nx
import random
from networkx.algorithms import community



# from Girvan_Newman import GN #引用模块中的函数

# 读取文件中边关系，然后成为一个成熟的图,是有一个有效距离的。这里需要加


'''
有效距离的定义：度大点的传播距离较远。目前只有一个指标：根据度数的大小。度数越大，与他相连的边的权重越大。
越不容易传播、越可能在距离比较远的时间传播。以此为方法定义权重。
'''
from sklearn import preprocessing

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



def  effectDistance(probily):
    return 1- math.log(probily)


def sigmoid(num):
    sig_L = 0
    sig_L = (1 / (1 + np.exp(-num)))
    return sig_L


def Normalization(x):
    return [(float(i) - min(x)) / float(max(x) - min(x)) for i in x]


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
    for j in SourceList:
        infectList = []
        infectList.append(j)
        G.node[j]['SI'] = 2
        for time in range(0,4):
             tempinfectList=[]
             for node in infectList:
                for height in list(G.neighbors(node)):
                        randnum=random.random()
                        if randnum<0.5:
                            G.node[height]['SI'] = 2
                            tempinfectList.append(height)
             for timeInfectnode in tempinfectList:
                 infectList.append(timeInfectnode)


        # nodelist = list(nx.bfs_tree(G, source=SourceList[j], depth_limit=3).nodes)  # 这包含了这个构建的圆的所有节点。
        # edgelist = list(nx.bfs_tree(G, source=SourceList[j], depth_limit=3).edges)
        # print(len(nodelist))
        # nodelist = random.sample(nodelist, int(float(len(nodelist)) * 0.9))  # 从list中随机获取5个元素，作为一个片断返回
        # for i in nodelist:
        #     G.node[i]['SI'] = 2
        # for k in edgelist:
        #     G.adj[k[0]][k[1]]['Infection'] = 2
        print('头两个感染社区点数为' + str(len(infectList)))

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
            random_Rumo = random.sample(sumlist, 1)
            random_RumorSource = random_Rumo[0]
            rumorSourceList.append(random_RumorSource)
            flag = 1
        elif sourceNum == 2:
            random_Rumo = random.sample(sumlist, 1)
            random_RumorSource = random_Rumo[0]
            # 在剩下的节点找到我们的第二个点。
            for node in list(G.nodes):
                if nx.has_path(G, node, random_RumorSource) == True:
                    if nx.shortest_path_length(G, node, random_RumorSource) > 4 and nx.shortest_path_length(G, node,
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
                random_Rumo = random.sample(sumlist, 1)
                random_RumorSource = random_Rumo[0]
                # 找第二、三个点。
                for index in range(len(sumlist) - 2):
                    if nx.has_path(G, sumlist[index], random_RumorSource) == True and nx.has_path(G, sumlist[index + 1],
                                                                                                  random_RumorSource) == True:
                        if nx.shortest_path_length(G, source=sumlist[index],
                                                   target=random_RumorSource) > 4 and nx.shortest_path_length(G, source=
                        sumlist[index], target=random_RumorSource) < 6 and nx.shortest_path_length(G, source=sumlist[
                            index + 1], target=random_RumorSource) > 4 and nx.shortest_path_length(G, source=sumlist[
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

            flag=0
            flag1 = 0
            while flag==0:
                rumorSourceList = []
                random_Rumo = random.sample(sumlist, 1)
                random_RumorSource = random_Rumo[0]
                rumorSourceList.append(random_RumorSource)
                flag1=0
                while flag1==0:
                    print  ('随机产生的点为'+str(random_RumorSource))
                    resultList=list(nx.dfs_edges(G, source=random_RumorSource, depth_limit=5))
                    # print (resultList)
                    rumorSourceList.append(resultList[4][1])
                    random_RumorSource=resultList[4][1]
                    if len(rumorSourceList) == 4 and len(rumorSourceList)==len(set(rumorSourceList)):  # 重复或者数目达不到要求:
                        print('找到了4个点')
                        flag1 =1
                        flag = 1
                    elif len(rumorSourceList) == 4 and len(rumorSourceList)!=len(set(rumorSourceList)):
                        print ('是四个点，但是却有重复，只能够重新选择新的开始点')
                        flag1 = 1



            # flag1=0
            # while flag1==0:
            #
            #     #随机找个点，然后再找一个点。距离跟他有10个距离就可以。
            #     random_RumorSource = random.choice(sumlist)
            #     rumorSourceList=[random.choice(sumlist),random.choice(sumlist),random.choice(sumlist),random.choice(sumlist)]
            #     combinationList = list(combinations(rumorSourceList, 2))
            #
            #     flag2=0
            #     for sample in combinationList:
            #         if  nx.has_path(G, sample[0],sample[1]) == True:
            #
            #                 flag2=1
            #
            #     if flag2==1:
            #         flag1=0
            #     else:
            #         flag1=1
            # if len(rumorSourceList) != len(set(rumorSourceList)) and len(rumorSourceList) != 4:  # 重复或者数目达不到要求
            #     #有重复元素
            #     flag=0
            # else:
            #     flag=1


        elif sourceNum == 5:
            flag = 0
            flag1 = 0
            while flag == 0:
                rumorSourceList = []
                random_Rumo = random.sample(sumlist, 1)
                random_RumorSource = random_Rumo[0]
                rumorSourceList.append(random_RumorSource)
                flag1 = 0
                while flag1 == 0:
                    print('随机产生的点为' + str(random_RumorSource))
                    resultList = list(nx.dfs_edges(G, source=random_RumorSource, depth_limit=5))
                    # print (resultList)
                    rumorSourceList.append(resultList[4][1])
                    random_RumorSource = resultList[4][1]
                    if len(rumorSourceList) == 5 and len(rumorSourceList) == len(set(rumorSourceList)):  # 重复或者数目达不到要求:
                        print('找到了4个点')
                        flag1 = 1
                        flag = 1
                    elif len(rumorSourceList) == 5 and len(rumorSourceList) != len(set(rumorSourceList)):
                        print('是四个点，但是却有重复，只能够重新选择新的开始点')
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
            print('第一个感染社区随机开始的点感染点' + str(randomInfectionNode))
            partion1 = getTuresubinfectionG(infectionG, randomInfectionNode)
            multipleCommuniytlist.append(partion1)  # 第一个社区
            print('把第1个社区加入进去，现在感染社区点个数为' + str(len(multipleCommuniytlist)))
            flag = 1

    print('感染社区个数以及各自人数')
    print(len(multipleCommuniytlist))
    print(len(multipleCommuniytlist[0]))
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


def getkey(pos, value):
    return {value: key for key, value in pos.iteritems()}[value]


import matplotlib.pyplot  as plt


def findmultiplesource(singleRegionList, infectionG, trueSourcelist):
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
    Alternativenodeset = list(set(tempGraphNodelist))  # 备选集合。
    # 求出这个区域最远的路径出来。返回这个区域半径。
    print('这个感染区域的传播半径')
    # maxh=nx.radius(tempGraph)
    '''
      1  选择边界点。（or所有点）
      2  选择中心点，以（u，h）去达到最大的覆盖数目。计算这样形成的u和它所有边界点形成的路径成本。
      3  再以(u1,h1).(u2,h2)去达到这样的覆盖数目，计算这样形成的路径成本之和。（每次增大h，这个子集合的成本都会增大。）
      '''
    # 首先第一步，将这个tempGra圆投影到x，y轴。
    # 让我看看这个图
    ConvertGToCsvSub(tempGraph, 'tempGraph.csv')
    # peripheryList=nx.periphery(tempGraph)  #求解图边界list

    # 随机求一些list，待选集合。偏心率<于某些数值，的元素。
    chooseList = []
    for node in tempGraph.nodes:
        randomnum = random.random()
        if randomnum > 0.95:
            chooseList.append(node)
    # centerlist = list(nx.center(tempGraph))
    # print('感染图的中心为' + str(centerlist))
    # for center in centerlist:
    #     chooseList.append(center)    #
    print('把源点加入进去')
    for j in trueSourcelist:
        chooseList.append(j)
    print('chooseList个元素个数为' + str(len(chooseList)))
    # maxh=nx.radius(tempGraph)
    # print ('感染图半径为'+str(maxh))   #把边都加入话，半径都小了。都不是一个好树了，难受

    chooseList = chooseList[-10:]  # 取最后20个。
    print('chooseList' + '总共有多少元素' + str(len(chooseList)))
    minCoverlist = []
    for sourceNum in range(4, 5):
            print('在源点在' + str(sourceNum) + '个数的情况下')
            # print('在h为' + str(h) + '的情况下')
            if sourceNum == 1:  # 单源点。
                # 单源情况，怎么办。
                # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
                '''
                1 变种jaya算法，首先生成100个种群大小。
                2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
                3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。
                '''
                min = 200
                print('多源情况,先考察同时传播传播')
                print('源点个数为' + str(sourceNum) + '情况')
                # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
                # combinationList = list(combinations(Alternativenodeset, sourceNum))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
                sourceAndH = []
                for htemp in range(2, 5):
                    for sourcetmep in Alternativenodeset:
                        sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
                # 从combinationList中寻找100个样本集。
                Sampleset = random.sample(sourceAndH, 50)
                print('样本集产生完毕，100个，是' + str(Sampleset))
                bestsourceNews = []
                # 迭代五次
                for i in range(1, 4):
                    # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
                    for sourcesi in range(len(Sampleset)):
                        print('当前输入list' + str(Sampleset[sourcesi]))
                        mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                              infectionG)
                        # 往后5个位置找一个比它更好地点。只要找更好就行,找不到就返回不变就可以
                        # 当前的下标
                        currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                        length = len(sourceAndH)
                        for j in range(1, 100, 25):  # 要防止数组越界
                            if currentindex + j < length:  # 只要在范围里面才行。
                                lateelement = sourceAndH[currentindex + j]
                                print('当前输入的后面list' + str(lateelement))
                                latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                                if mincover > latemincover:
                                    mincover = latemincover  # 有更好地就要替换
                                    print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                                    Sampleset[sourcesi] = lateelement  # 替换
                                    print(Sampleset[sourcesi])

                print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
                # 计算样本集的similir，找出最好的。
                for sources in Sampleset:
                    mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
                    if mincover < min:
                        min = mincover  # 这一次最好的覆盖误差率
                        bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

                print('得到多源点情况最小的覆盖率为' + str(min))
                minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])


            elif sourceNum == 2:
                # 两源情况，怎么办。
                # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
                '''

                1 变种jaya算法，首先生成100个种群大小。
                2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
                3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。

                '''
                min = 200
                print('多源情况,先考察同时传播传播')
                print('源点为' + str(sourceNum) + '情况')
                # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
                # combinationList = list(combinations(Alternativenodeset, sourceNum))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
                print('这一步炸了')
                combinationList = []  # 样本集合
                # 随机产生这些可能性，随机生成种群50大小。
                for sampleindex in range(0, 53):
                    combinationList.append([random.choice(Alternativenodeset), random.choice(Alternativenodeset)])

                sourceAndH = []
                hlists = [2, 3]
                for htemp in range(2, 5):
                    for sourcetmep in combinationList:
                        sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
                # 从combinationList中寻找100个样本集。
                Sampleset = random.sample(sourceAndH, 50)
                print('样本集产生完毕，100个，是' + str(Sampleset))
                bestsourceNews = []
                # 迭代五次
                for i in range(1, 4):
                    # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
                    for sourcesi in range(len(Sampleset)):
                        print('当前输入list' + str(Sampleset[sourcesi]))
                        mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                              infectionG)
                        # 随机更换，看如何让变好
                        # currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                        length = len(sourceAndH)
                        for j in range(1, 4, 1):  # 随机变4次，只要能变好
                            lateelement = [[random.choice(Alternativenodeset), random.choice(Alternativenodeset)],random.choice(hlists)]
                            print('当前输入的后面list' + str(lateelement))
                            latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                            if mincover > latemincover:
                                mincover = latemincover  # 有更好地就要替换
                                print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                                Sampleset[sourcesi] = lateelement  # 替换
                                print(Sampleset[sourcesi])

                print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
                # 计算样本集的similir，找出最好的。
                for sources in Sampleset:
                    mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
                    if mincover < min:
                        min = mincover  # 这一次最好的覆盖误差率
                        bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

                print('得到多源点情况最小的覆盖率为' + str(min))
                minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])
                #这时候，我们的minCoverlist有两个min，我们来计算下。当两次的min之差小于某个值，我们认为源点为k。
                Comparisonlist=minCoverlist[-2:]  #取最后两个元素，
                Difference=abs(Comparisonlist[0][2]-Comparisonlist[1][2])
                if Difference ==0:
                    print ('两次覆盖率一样')
                    pass
                elif Difference<0.00001:
                    print('跳出for循环，两次覆盖率几乎相等那么预测源点个数为' + str(sourceNum - 1))
                    break

            elif sourceNum == 3:
                # 两源情况，怎么办。
                # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
                '''
                1 变种jaya算法，首先生成100个种群大小。
                2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
                3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。

                '''
                min = 200
                print('多源情况,先考察同时传播传播')
                print('源点为' + str(sourceNum) + '情况')
                # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
                # combinationList = list(combinations(Alternativenodeset, sourceNum))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
                print('这一步炸了')
                combinationList = []  # 样本集合
                # 随机产生这些可能性，随机生成种群50大小。
                for sampleindex in range(0, 53):
                    combinationList.append([random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                            random.choice(Alternativenodeset)])

                sourceAndH = []
                hlists = [2, 3]
                for htemp in range(2, 5):
                    for sourcetmep in combinationList:
                        sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
                # 从combinationList中寻找100个样本集。
                Sampleset = random.sample(sourceAndH, 50)
                print('样本集产生完毕，100个，是' + str(Sampleset))
                bestsourceNews = []
                # 迭代五次
                for i in range(1, 4):
                    # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
                    for sourcesi in range(len(Sampleset)):
                        print('当前输入list' + str(Sampleset[sourcesi]))
                        mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                              infectionG)
                        # 随机更换，看如何让变好
                        # currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                        length = len(sourceAndH)
                        for j in range(1, 4, 1):  # 随机变4次，只要能变好
                            lateelement = [[random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                            random.choice(Alternativenodeset)],
                                           random.choice(hlists)]
                            print('当前输入的后面list' + str(lateelement))
                            latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                            if mincover > latemincover:
                                mincover = latemincover  # 有更好地就要替换
                                print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                                Sampleset[sourcesi] = lateelement  # 替换
                                print(Sampleset[sourcesi])

                print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
                # 计算样本集的similir，找出最好的。
                for sources in Sampleset:
                    mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
                    if mincover < min:
                        min = mincover  # 这一次最好的覆盖误差率
                        bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

                print('得到多源点情况最小的覆盖率为' + str(min))
                minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])
                Comparisonlist = minCoverlist[-2:]  # 取最后两个元素，
                Difference = abs(Comparisonlist[0][2] - Comparisonlist[1][2])
                if Difference ==0:
                    print('两次覆盖率一样')
                    pass
                elif Difference<0.00001:
                    print('跳出for循环，两次覆盖率几乎相等那么预测源点个数为' + str(sourceNum - 1))
                    break
            elif sourceNum == 4:
                # 两源情况，怎么办。
                # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
                '''

                1 变种jaya算法，首先生成100个种群大小。
                2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
                3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。

                '''
                min = 200
                print('多源情况,先考察同时传播传播')
                print('源点为' + str(sourceNum) + '情况')
                # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
                # combinationList = list(combinations(Alternativenodeset, sourceNum))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
                print ('这一步炸了')
                combinationList=[]   #样本集合
                #随机产生这些可能性，随机生成种群50大小。
                for sampleindex  in range(0,100):
                    combinationList.append([random.choice(Alternativenodeset),random.choice(Alternativenodeset),random.choice(Alternativenodeset),random.choice(Alternativenodeset)])
                sourceAndH = []
                hlists=[2,3]
                for htemp in range(2, 5):
                    for sourcetmep in combinationList:
                        sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
                # 从combinationList中寻找100个样本集。
                Sampleset = random.sample(sourceAndH, 50)
                print('样本集产生完毕，100个，是' + str(Sampleset))
                bestsourceNews = []
                # 迭代五次
                for i in range(1, 7):
                    # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
                    for sourcesi in range(len(Sampleset)):
                        print('当前输入list' + str(Sampleset[sourcesi]))
                        mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                              infectionG)
                        # 随机更换，看如何让变好
                        # currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                        length = len(sourceAndH)
                        for j in range(1, 4, 1):  # 随机变4次，只要能变好
                                lateelement = [[random.choice(Alternativenodeset),random.choice(Alternativenodeset),random.choice(Alternativenodeset),random.choice(Alternativenodeset)],random.choice(hlists)]
                                print('当前输入的后面list' + str(lateelement))
                                latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                                if mincover > latemincover:
                                    mincover = latemincover  # 有更好地就要替换
                                    print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                                    Sampleset[sourcesi] = lateelement  # 替换
                                    print(Sampleset[sourcesi])

                print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
                # 计算样本集的similir，找出最好的。
                for sources in Sampleset:
                    mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
                    if mincover < min:
                        min = mincover  # 这一次最好的覆盖误差率
                        bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

                print('得到多源点情况最小的覆盖率为' + str(min))
                minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])
                # Comparisonlist = minCoverlist[-2:]  # 取最后两个元素，
                # Difference = abs(Comparisonlist[0][2] - Comparisonlist[1][2])
                # if Difference ==0:
                #     print('两次覆盖率一样')
                #     pass
                # elif Difference<0.00001:
                #     print('跳出for循环，两次覆盖率几乎相等那么预测源点个数为' + str(sourceNum - 1))
                #     break
            elif sourceNum == 5:
                # 两源情况，怎么办。
                # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
                '''
                1 变种jaya算法，首先生成100个种群大小。
                2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
                3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。

                '''
                min = 200
                print('多源情况,先考察同时传播传播')
                print('源点为' + str(sourceNum) + '情况')
                # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
                # combinationList = list(combinations(Alternativenodeset, sourceNum))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
                print('这一步炸了')
                combinationList = []  # 样本集合
                # 随机产生这些可能性，随机生成种群50大小。
                for sampleindex in range(0, 53):
                    combinationList.append([random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                            random.choice(Alternativenodeset), random.choice(Alternativenodeset),random.choice(Alternativenodeset)])

                sourceAndH = []
                hlists = [2, 3]
                for htemp in range(2, 5):
                    for sourcetmep in combinationList:
                        sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
                # 从combinationList中寻找100个样本集。
                Sampleset = random.sample(sourceAndH, 50)
                print('样本集产生完毕，100个，是' + str(Sampleset))
                bestsourceNews = []
                # 迭代五次
                for i in range(1, 4):
                    # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
                    for sourcesi in range(len(Sampleset)):
                        print('当前输入list' + str(Sampleset[sourcesi]))
                        mincover = getSimilir(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                              infectionG)
                        # 随机更换，看如何让变好
                        # currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                        length = len(sourceAndH)
                        for j in range(1, 4, 1):  # 随机变4次，只要能变好
                            lateelement = [[random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                            random.choice(Alternativenodeset), random.choice(Alternativenodeset), random.choice(Alternativenodeset)],
                                           random.choice(hlists)]
                            print('当前输入的后面list' + str(lateelement))
                            latemincover = getSimilir(lateelement[0], lateelement[1], singleRegionList, infectionG)
                            if mincover > latemincover:
                                mincover = latemincover  # 有更好地就要替换
                                print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                                Sampleset[sourcesi] = lateelement  # 替换
                                print(Sampleset[sourcesi])

                print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
                # 计算样本集的similir，找出最好的。
                for sources in Sampleset:
                    mincover = getSimilir(sources[0], sources[1], singleRegionList, infectionG)
                    if mincover < min:
                        min = mincover  # 这一次最好的覆盖误差率
                        bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

                print('得到多源点情况最小的覆盖率为' + str(min))
                minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])
                Comparisonlist = minCoverlist[-2:]  # 取最后两个元素，
                Difference = abs(Comparisonlist[0][2] - Comparisonlist[1][2])
                if Difference ==0:
                    print('两次覆盖率一样')
                    pass
                elif Difference<0.00001:
                    print('跳出for循环，两次覆盖率几乎相等那么预测源点个数为' + str(sourceNum - 1))
                    break

    # listToTxt(minCoverlist, 'newresult.txt')
    print(minCoverlist)
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
        print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))
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
        print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))

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


def multiplePartion(mutiplelist, infectionG, rumorSourceList):
    # 所有单源list
    allsigleSourceList = []
    allSigleSourceListNum = [2, 1]

    # 将第一个传播区域定下来。
    import datetime
    starttime = datetime.datetime.now()
    # long running,这里可以读的文件代替，就比较省时间。反正都是为了allsigleSourcellist填充

    '''   这个是保留项，我觉得反转算法有点问题，反正（u,h是写完了）,下面这个很好时间'''
    for sigleReionlist in mutiplelist:
        allsigleSourceList.append(findmultiplesource(sigleReionlist, infectionG, rumorSourceList))

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
    print('最后我们找到的误差率最低的的每个分区的圆点和他的h是' + str(allsigleSourceList))

    for sigleRegionSource in allsigleSourceList:
        if isinstance(sigleRegionSource[0], int):  # 单源点
            print('算出来的误差率最低单源点情况---------------------------')
            source3 = revsitionAlgorithm(sigleRegionSource[0], sigleRegionSource[1], infectionG, infectionG)
            print('用反转算法计算出来的单源点为' + str(source3))
            resultSource.append(source3)
            resultSource.clear()

        elif len(sigleRegionSource[0]) == 2:
            print('算出来的误差率最低2源点情况---------------------------')
            source1 = revsitionAlgorithm(sigleRegionSource[0][0], sigleRegionSource[1], infectionG, infectionG)
            source2 = revsitionAlgorithm(sigleRegionSource[0][1], sigleRegionSource[1], infectionG, infectionG)
            print('用反转算法计算出来的源点为' + str(source2) + str(source1))
            resultSource.append(source1)
            resultSource.append(source2)
            resultSource.clear()

        elif len(sigleRegionSource[0]) == 3:
            print('算出来的误差率最低3源点情况---------------------------')
            source1 = revsitionAlgorithm(sigleRegionSource[0][0], sigleRegionSource[1], infectionG, infectionG)
            source2 = revsitionAlgorithm(sigleRegionSource[0][1], sigleRegionSource[1], infectionG, infectionG)
            source3 = revsitionAlgorithm(sigleRegionSource[0][2], sigleRegionSource[1], infectionG, infectionG)
            print('用反转算法计算出来的源点为' + str(source2) + str(source1))
            resultSource.append(source1)
            resultSource.append(source2)
            resultSource.append(source3)
        elif len(sigleRegionSource[0]) == 4:
            print('算出来的误差率最低3源点情况---------------------------')
            source1 = revsitionAlgorithm(sigleRegionSource[0][0], sigleRegionSource[1], infectionG, tempGraph1)
            source2 = revsitionAlgorithm(sigleRegionSource[0][1], sigleRegionSource[1], infectionG, tempGraph1)
            source3 = revsitionAlgorithm(sigleRegionSource[0][2], sigleRegionSource[1], infectionG, tempGraph1)
            source4 = revsitionAlgorithm(sigleRegionSource[0][3], sigleRegionSource[1], infectionG, tempGraph1)
            print('用反转算法计算出来的源点为' + str(source2) + str(source1))
            resultSource.append(source1)
            resultSource.append(source2)
            resultSource.append(source3)
            resultSource.append(source4)
            resultSource.clear()
            for j in sigleRegionSource[0]:
                resultSource.append(j)
        elif len(sigleRegionSource[0]) == 5:
             print('算出来的误差率最低3源点情况---------------------------')
             source1 = revsitionAlgorithm(sigleRegionSource[0][0], sigleRegionSource[1], infectionG, infectionG)
             source2 = revsitionAlgorithm(sigleRegionSource[0][1], sigleRegionSource[1], infectionG, infectionG)
             source3 = revsitionAlgorithm(sigleRegionSource[0][2], sigleRegionSource[1], infectionG, infectionG)
             source4 = revsitionAlgorithm(sigleRegionSource[0][3], sigleRegionSource[1], infectionG, infectionG)
             source5 = revsitionAlgorithm(sigleRegionSource[0][4], sigleRegionSource[1], infectionG, infectionG)
             print('用反转算法计算出来的源点为' + str(source2) + str(source1))
             resultSource.append(source1)
             resultSource.append(source2)
             resultSource.append(source3)
             resultSource.append(source4)
             resultSource.append(source5)

    print('总的用反转算法算出来的结果为' + str(resultSource))
    listToTxt(resultSource, 'newresult.txt')


    errordistanceFor = []
    # 上面这两个，可以干一架了。
    for turesourcelist in rumorSourceList:  # 真实源
        everydistion = []
        for resultsourceindex in resultSource:  # 自己算法找出的源。
            everydistion.append([resultsourceindex,
                                 nx.shortest_path_length(infectionG, source=turesourcelist, target=resultsourceindex)])
        everydistion = sorted(everydistion, key=lambda x: (x[1]))
        # 结果集匹配到了，最好的结果就要移除这个了。
        resultSource.remove(everydistion[0][0])  # 移除最小距离的那个
        print('输出4个源的时候，每次每个源跟他们计算时候距离的从低到高排序序列。')
        print(everydistion)
        errordistanceFor.append(everydistion[0][1])
    multipdistance = 0
    for error in errordistanceFor:
        multipdistance = multipdistance + error
    # errordistance=nx.shortest_path_length(infectionG,source=resultSource[0],target=rumorSourceList[0])
    print('误差距离为' + str(multipdistance))
    return multipdistance / len(errordistanceFor)

    # do something other


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
    times = 6  # 时间刻多点
    IDdict = {}
    IDdict_dup = {}
    # 先赋予初始值。
    for node in list(source1G.nodes):
        # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
        IDdict[node] = [node]
        IDdict_dup[node] = [node]
    allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
    for t in range(times):
        print('t为' + str(t) + '的时候-----------------------------------------------------------------------------')
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
    # print (nx.shortest_path_length(subinfectG,result,u))  #0
    # print (nx.shortest_path_length(subinfectG,125,result) )#  2
    # print(nx.shortest_path_length(subinfectG, 4022, result))  #  8
    #


#
#
#
# rumorSourceList=contractSource(G,3,5)  #产生源点。图，源点个数，源点差距距离。
# hlist=[3,2]   #不同传播区域传播深度，
# infectG=Algorithm1(G,rumorSourceList,5,hlist )  #产生感染图，深度是3
#
# #gephi 查看infectG转成csv情况。
# ConvertGToCsv(infectG,'G.csv')
# subinfectG=nx.Graph()
# count=1
# count1=1
# for  edge in  infectG.edges:
#     # print (edge)\
#     if  infectG.adj[edge[0]][edge[1]]['Infection']==1:
#        count1 =count1+1
#     if  infectG.adj[edge[0]][edge[1]]['Infection']==2:
#         count = count + 1
#         subinfectG.add_edges_from([(edge[0],edge[1])],weight= 1)
#
# print (count)
# print (count1)
# # 因为邮件是一个有向图，我们这里构建的是无向图。
# print('传染子图的顶点个数',  subinfectG.number_of_nodes())
# print('传染子图的边个数',  subinfectG.number_of_edges())
#
#
# ConvertGToCsvSub(subinfectG,'SubInfectionG.csv')
# #
# #检测是否是有相互感染到。
#
# print (nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))
# print (nx.shortest_path(subinfectG, rumorSourceList[0], rumorSourceList[1], weight='weight'))  #在子图中有路径，就是感染到了。
#
# if nx.has_path(subinfectG,rumorSourceList[1],rumorSourceList[2])==False:
#     if nx.has_path(subinfectG,rumorSourceList[0],rumorSourceList[2])==False:
#         print('========================================================================')
#         print ('这里的第3个点，跟他们都没有路径相连。可以的')
# else:
#     print ('========================================================================')
#     print ('这里的第3个点，不行的，很烦')
# # print (nx.shortest_path(subinfectG, rumorSourceList[1], rumorSourceList[2], weight='weight'))    #这个报错就是第三个point并没有被感染到的意思。
#
# #now  to  practice single-multiple  source Partition.Get  ture  parition
#
#
#
# # if  769  in list(infectG.nodes):
# #     print ('明明就在')
# multipList=getmultipleCommunity(infectG)
# multiplePartion(multipList, infectG,rumorSourceList)
#
#
#
# #产生一组模拟两源数据的，然后计算平均值。
#
#
#
#
#
#


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
    G = ContractDict('../data/facebook_combined.txt', Ginti)

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

    for i in range(1, 11):
        sourceList.append(contractSource(G, 4, 2))

    errordistanceList = []  # 误差集合。
    errorSum = 0

    # 对每一个单源点都有这个操作。
    for singleSource in sourceList:
        #  先给全体的Cn、Scn,time的0的赋值。
        for node in list(G.nodes):
            G.add_node(node, SI=1)
        # 初始化所有边是否感染。Infection
        for edge in list(G.edges):
            G.add_edge(edge[0], edge[1], Infection=1)
        # 开始之前都要刷新这个图，
        infectG = Algorithm1(G, singleSource, 5, 6)
        print('源点传播成功')
        #  找社区，按照代理，只能找到一个社区的。
        multipList = getmultipleCommunity(infectG)
        errordistance = multiplePartion(multipList, infectG, singleSource)
        errorSum = errorSum + errordistance
        errordistanceList.append(errordistance)
        print('误差集合为' + str(errordistanceList))
    print(errorSum / 10)

    # long running

    endtime = datetime.datetime.now()
    print('执行了这么长时间')
    print((endtime - starttime).seconds)





















