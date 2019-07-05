import networkx as nx
import random
from networkx.algorithms import community

# from Girvan_Newman import GN #引用模块中的函数

# 读取文件中边关系，然后成为一个成熟的图,是有一个有效距离的。这里需要加


'''
有效距离的定义：度大点的传播距离较远。目前只有一个指标：根据度数的大小。度数越大，与他相连的边的权重越大。
越不容易传播、越可能在距离比较远的时间传播。以此为方法定义权重。
'''


import numpy as np

np.set_printoptions(threshold=np.inf)


def ContractDict(dir, G):
    with open(dir, 'r') as f:
        for line in f:
            line1 = line.split()
            G.add_edge(int(line1[0]), int(line1[1]))

    for edge in G.edges:
        G.add_edge(edge[0], edge[1], weight=1)
        # randomnum = random.random()
        # G.add_edge(edge[0], edge[1], weight=effectDistance(randomnum))

    return G


import math


def effectDistance(probily):
    return 1 - math.log(probily)


def sigmoid(num):
    sig_L = 0
    sig_L = (1 / (1 + np.exp(-num)))
    return sig_L


def disEffectDistance(weight):
    return math.pow(2, (1 - weight))


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

             # infectList.clear()
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

                random_RumorSource = random.choice(sumlist)
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

            flag = 0
            flag1 = 0
            while flag == 0:
                rumorSourceList = []
                random_Rumo = random.sample(sumlist, 1)
                random_RumorSource = random_Rumo[0]
                rumorSourceList.append(random_RumorSource)
                flag1 = 0
                while flag1 == 0:
                    print  ('随机产生的点为' + str(random_RumorSource))
                    resultList = list(nx.dfs_edges(G, source=random_RumorSource, depth_limit=5))
                    # print (resultList)
                    rumorSourceList.append(resultList[3][1])
                    random_RumorSource = resultList[3][1]
                    if len(rumorSourceList) == 4 and len(rumorSourceList) == len(set(rumorSourceList)):  # 重复或者数目达不到要求:
                        print('找到了4个点')
                        flag1 = 1
                        flag = 1
                    elif len(rumorSourceList) == 4 and len(rumorSourceList) != len(set(rumorSourceList)):
                        print ('是四个点，但是却有重复，只能够重新选择新的开始点')
                        flag1 = 1


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


def findmultiplesource(singleRegionList, infectionG, trueSourcelist, sourceNum):
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


    minCoverlist = []
    print('在源点在' + str(sourceNum) + '个数的情况下')
    # print('在h为' + str(h) + '的情况下')
    if sourceNum == 1:  # 单源点。
        #针对tempGraph，计算一个age，就是针对tempGraph。
        DA=0
        L = nx.normalized_laplacian_matrix(tempGraph)
        e = np.linalg.eigvals(L.A)
        print("Largest eigenvalue:", max(e))
        # print("Smallest eigenvalue:", min(e))
        MaxEigenvalue=max(e)
        nodeDaList=[]
        newTempGraph = nx.Graph()
        nodelist=list(tempGraph.nodes)
        for  node  in list(nodelist):
            #计算这个感染图所有的图节点对应的DA值，并统计一定范围的属于某个等级，注意，可能会有多个。
            newTempGraph.clear()
            newTempGraph=tempGraph.copy()
            newTempGraph.remove_node(node)
            L = nx.normalized_laplacian_matrix(newTempGraph)
            e = np.linalg.eigvals(L.A)
            nodeEigenvalue=max(e)
            print (nodeEigenvalue)
            nodeDa=abs(MaxEigenvalue-nodeEigenvalue)/MaxEigenvalue
            print ('--------------------------')
            print(str(node)+'---------'+str(nodeDa))
            nodeDaList.append([node,nodeDa])
        # nodeDaList= sorted(nodeDaList, key=lambda x: (x[1]))
        nodeDaList.sort(key=lambda x: (x[1]))
        print (nodeDaList)
        tempresultlist=nodeDaList[-1:]
        result=[]

        #现在就是一个list，如何聚类？
        for  temp in tempresultlist:
            result.append(temp[0])
        return  result





    elif sourceNum == 2:
        #针对tempGraph，计算一个age，就是针对tempGraph。
        DA=0
        L = nx.normalized_laplacian_matrix(tempGraph)
        e = np.linalg.eigvals(L.A)
        print("Largest eigenvalue:", max(e))
        # print("Smallest eigenvalue:", min(e))

        MaxEigenvalue=max(e)
        nodeDaList=[]
        newTempGraph = nx.Graph()
        nodelist=list(tempGraph.nodes)
        for  node  in list(nodelist):
            #计算这个感染图所有的图节点对应的DA值，并统计一定范围的属于某个等级，注意，可能会有多个。
            newTempGraph.clear()
            newTempGraph=tempGraph.copy()
            newTempGraph.remove_node(node)
            L = nx.normalized_laplacian_matrix(newTempGraph)
            e = np.linalg.eigvals(L.A)
            nodeEigenvalue=max(e)
            print (nodeEigenvalue)
            nodeDa=abs(MaxEigenvalue-nodeEigenvalue)/MaxEigenvalue
            print ('--------------------------')
            print(str(node)+'---------'+str(nodeDa))
            nodeDaList.append([node,nodeDa])
        # nodeDaList= sorted(nodeDaList, key=lambda x: (x[1]))
        nodeDaList.sort(key=lambda x: (x[1]))
        print (nodeDaList)
        tempresultlist=nodeDaList[-2:]
        result=[]
        for  temp in tempresultlist:
            result.append(temp[0])
        return  result








    elif sourceNum == 3:

        # 针对tempGraph，计算一个age，就是针对tempGraph。
        DA = 0
        L = nx.normalized_laplacian_matrix(tempGraph)
        e = np.linalg.eigvals(L.A)
        print("Largest eigenvalue:", max(e))
        # print("Smallest eigenvalue:", min(e))

        MaxEigenvalue = max(e)
        nodeDaList = []
        newTempGraph = nx.Graph()
        nodelist = list(tempGraph.nodes)
        for node in list(nodelist):
            # 计算这个感染图所有的图节点对应的DA值，并统计一定范围的属于某个等级，注意，可能会有多个。
            newTempGraph.clear()
            newTempGraph = tempGraph.copy()
            newTempGraph.remove_node(node)
            L = nx.normalized_laplacian_matrix(newTempGraph)
            e = np.linalg.eigvals(L.A)
            nodeEigenvalue = max(e)
            print(nodeEigenvalue)
            nodeDa = abs(MaxEigenvalue - nodeEigenvalue) / MaxEigenvalue
            print('--------------------------')
            print(str(node) + '---------' + str(nodeDa))
            nodeDaList.append([node, nodeDa])
        # nodeDaList= sorted(nodeDaList, key=lambda x: (x[1]))
        nodeDaList.sort(key=lambda x: (x[1]))
        print(nodeDaList)
        tempresultlist = nodeDaList[-3:]
        result = []
        for temp in tempresultlist:
            result.append(temp[0])
        return result














    elif sourceNum == 4:
        # 针对tempGraph，计算一个age，就是针对tempGraph。
        DA = 0
        L = nx.normalized_laplacian_matrix(tempGraph)
        e = np.linalg.eigvals(L.A)
        print("Largest eigenvalue:", max(e))
        # print("Smallest eigenvalue:", min(e))

        MaxEigenvalue = max(e)
        nodeDaList = []
        newTempGraph = nx.Graph()
        nodelist = list(tempGraph.nodes)
        for node in list(nodelist):
            # 计算这个感染图所有的图节点对应的DA值，并统计一定范围的属于某个等级，注意，可能会有多个。
            newTempGraph.clear()
            newTempGraph = tempGraph.copy()
            newTempGraph.remove_node(node)
            L = nx.normalized_laplacian_matrix(newTempGraph)
            e = np.linalg.eigvals(L.A)
            nodeEigenvalue = max(e)
            print(nodeEigenvalue)
            nodeDa = abs(MaxEigenvalue - nodeEigenvalue) / MaxEigenvalue
            print('--------------------------')
            print(str(node) + '---------' + str(nodeDa))
            nodeDaList.append([node, nodeDa])
        # nodeDaList= sorted(nodeDaList, key=lambda x: (x[1]))
        nodeDaList.sort(key=lambda x: (x[1]))
        print(nodeDaList)
        tempresultlist = nodeDaList[-4:]
        result = []
        for temp in tempresultlist:
            result.append(temp[0])
        return result













    elif sourceNum == 5:
        # 针对tempGraph，计算一个age，就是针对tempGraph。
        DA = 0
        L = nx.normalized_laplacian_matrix(tempGraph)
        e = np.linalg.eigvals(L.A)
        print("Largest eigenvalue:", max(e))
        # print("Smallest eigenvalue:", min(e))

        MaxEigenvalue = max(e)
        nodeDaList = []
        newTempGraph = nx.Graph()
        nodelist = list(tempGraph.nodes)
        for node in list(nodelist):
            # 计算这个感染图所有的图节点对应的DA值，并统计一定范围的属于某个等级，注意，可能会有多个。
            newTempGraph.clear()
            newTempGraph = tempGraph.copy()
            newTempGraph.remove_node(node)
            L = nx.normalized_laplacian_matrix(newTempGraph)
            e = np.linalg.eigvals(L.A)
            nodeEigenvalue = max(e)
            print(nodeEigenvalue)
            nodeDa = abs(MaxEigenvalue - nodeEigenvalue) / MaxEigenvalue
            print('--------------------------')
            print(str(node) + '---------' + str(nodeDa))
            nodeDaList.append([node, nodeDa])
        # nodeDaList= sorted(nodeDaList, key=lambda x: (x[1]))
        nodeDaList.sort(key=lambda x: (x[1]))
        print(nodeDaList)
        tempresultlist = nodeDaList[-5:]
        result = []
        for temp in tempresultlist:
            result.append(temp[0])
        return result

















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
        count = 0
        for i in circleNodesList:
            if i in singleRegionList:
                count = count + 1
        Intersection = list(set(circleNodesList).intersection(set(singleRegionList)))  # 交集
        Union = list(set(circleNodesList).union(set(singleRegionList)))
        ratios = len(Intersection) / len(Union)
        ratio = 1.0 - ratios
        print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))
        return abs(ratio)



    else:
        # 多源点,获得多源点的覆盖率
        circleNodesList = []
        for u in ulist:
            circleNodesList.extend(list(nx.bfs_tree(infectionG, source=u, depth_limit=hlist).nodes))
        circleNodesListnew = list(set(circleNodesList))
        count = 0
        for i in circleNodesList:
            if i in singleRegionList:
                count = count + 1
        # count
        Intersection = list(set(circleNodesList).intersection(set(singleRegionList)))  # 交集
        Union = list(set(circleNodesList).union(set(singleRegionList)))  # 并集
        ratios = len(Intersection) / len(Union)
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


def multiplePartion(mutiplelist, infectionG, rumorSourceList, sourceNume):
    # 所有单源list
    allsigleSourceList = []
    allSigleSourceListNum = [2, 1]

    # 将第一个传播区域定下来。
    import datetime
    starttime = datetime.datetime.now()
    # long running,这里可以读的文件代替，就比较省时间。反正都是为了allsigleSourcellist填充

    '''   这个是保留项，我觉得反转算法有点问题，反正（u,h是写完了）,下面这个很好时间'''
    for sigleReionlist in mutiplelist:
        allsigleSourceList.append(findmultiplesource(sigleReionlist, infectionG, rumorSourceList, sourceNume))

    resultSource = []

    for sigleRegionSource in allsigleSourceList:
        if len(sigleRegionSource)==1:  # 单源点
            print('算出来的误差率最低单源点情况---------------------------')
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 2:
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 3:
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 4:
            for source in sigleRegionSource:
                resultSource.append(source)
        elif len(sigleRegionSource) == 5:
            for source in sigleRegionSource:
                resultSource.append(source)

    print('总的用反转算法算出来的结果为' + str(resultSource))

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


import numpy as np
import matplotlib.pyplot as plt


def plotform(x, y):
    x = range(1, 4)
    y_train = [1.0, 1.4, 1.1, 1.225, 1.44]
    y_test = [2.53, 2, 31, 2.12, 1]
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
    G = ContractDict('../data/p2p-Gnutella30.txt', Ginti)

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
        sourceList.append(contractSource(G, 1, 2))


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
        infectG = Algorithm1(G, singleSource, 2, 6)
        print('源点传播成功')
        #  找社区，按照代理，只能找到一个社区的。
        multipList = getmultipleCommunity(infectG)
        errordistance = multiplePartion(multipList, infectG, singleSource,1)
        errorSum = errorSum + errordistance
        errordistanceList.append(errordistance)
        print('误差集合为' + str(errordistanceList))
        listToTxt(str(datetime.datetime.now()),'age_result.txt' )
        listToTxt('输出每次结果看看', 'age_result.txt')
        listToTxt(errordistanceList, 'age_result.txt')

    print(errorSum / 10)
    listToTxt(errorSum/10,'result.txt')

    # long running

    endtime = datetime.datetime.now()
    print('执行了这么长时间')
    print((endtime - starttime).seconds)





















