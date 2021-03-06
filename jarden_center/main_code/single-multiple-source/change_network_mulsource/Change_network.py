#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/11 2:05 上午

# @Author  : baozhiqiang

# @File    : Different_time.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************


import random
import math

import  networkx  as nx
import  numpy
from munkres import  print_matrix,Munkres
'''

1  生成一系列静态网络，代表传播过程。可直接利用一个小数据构建。设定一个5%的增加边，在动态之中寻找源点。
    这样可以构建t0，t1，。。。。。tn的矩阵，每一个都是m维的向量。t0，t1为固定时间间隔。
        （m是网络节点个数）

2  矩阵构建完毕，我们知道整个传播过程这是一个m*n矩阵。但是我们只知道我们只能获取谣言已经发生的某些
    比如t5，t6，t7的连续一段传播情况。我们也不知道5的存在。

3  那么这个好像高中学过的，给一列有规律的数，取其中一段，请写出第一个数字是多少。每个数字之间靠的
动态传播。不过我们这里是其中一段的传播情况，包含第一个到第几个元素数字在里面。




'''



'''
思路2：
    构建多个网络，每个时间段都会动态增删一定数量的边。进行传播。
    对第一个网络进行BFS构建，找到k个源点。
    第二个网络帮助对k的M远的点进行BFS构建。
            首先对形成的k个图第一个进行BFS算法，确定源点。然后第二个图只进行那几个源点的
   M远的点进行BFS构建即可。
考虑：这样的话，那多个网络只是让结果跟精确一点？没体现价值啊？

'''
class  FindSource:
    def __init__(self):
        self.initG = None  #原始图
        self.k = 3   #k个图
        self.change_ratio = 0.05  #动态图改动比例
        self.infect_ratio = 0.5  #感染比例
        self.findSource_list = None  #当前找到的源的list
        self.findSource_set = None    #当前找到的源的set
        self.infectG = None # 感染图
        self.fix_number_source = 3  #确定的源数目
        self.source_list = None #确定下来的源数目。
        self.true_Source_list = None #真实源点
        self.netwrok_filename = None #文件名字
        self.infectG_list = None  #感染的多个图列表。
        self.single_best_result= None
        self.tempGraph = None  #临时生成传播子图
        self.first_result_cost_list = None   #你求得第一个图的比较好距离。
        self.last_result_cost_list = None   #后面所求的图的集合
        self.k_distance = 2                 #后面的图寻求的距离
        self.all_result_cost_list = []

    def ContractDict(self,dir, G):
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

    def  get_networkByFile(self,fileName='../data/facebook_combined.txt'):
        #  制造这个图
        Ginti = nx.Graph()
        # 构建图，这个图是有有效距离的。
        G = self.ContractDict(fileName, Ginti)
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
        self.initG = G

        # pass


    def  product_sourceList(self):
        # 产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
            sumlist = list(self.initG.nodes)

            G =self.initG
            sourceNum = self.fix_number_source
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
                        random_Rumo = random.sample(sumlist, 1)
                        random_RumorSource = random_Rumo[0]
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
                    templist = list(nx.all_simple_paths(G, source=174, target=2419))
                    print(templist)
                    max = 0
                    result = []
                    for temp in templist:
                        if len(temp) > max:
                            max = len(temp)
                            result = temp
                    print(result)

            # 查看产生随机源点的个数2，并且他们距离为3.
            print('源点个数' + str(len(rumorSourceList)) + '以及产生的两源点是' + str(rumorSourceList))
            # rumorSourceList=[125,4022]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 95
            print('真实两源感染是' + str(rumorSourceList))
            self.true_Source_list = rumorSourceList
            # return rumorSourceList

    def   constract_Infection_netWork(self):
        '''
        :param G:
        :param infect_ratio:
        :return:  按照感染比例感染的图
        '''
        '''
            我们认为时间片是有问题的，这个时间片应该就是按照，不能是每隔一个时间片就传染一波。只能说每隔一个时间片就记录
            一线。传播也有有概率的。
        '''
        print('开始传染的点是' + str(self.true_Source_list))
        G= self.initG
        SourceList =self.true_Source_list
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
            if count / G.number_of_nodes() > 0.5:
                print('超过50%节点了，不用传播啦')
                break
        self.infectG = G
        # return G


    def  Constract_ManynetWrok(self):
        '''
        :param infectG:   #感染图
        :param K:           #再次改动K次
        :param ratio:       #每次改动比例
        :return:            #返回每次改动的传染图
        '''
        '''
        思路，先增删ratio的边，再进行一次传播。先增加5%的，再删除5%。
        '''
        number_edge = self.infectG.number_of_edges()
        edge_list = list(self.infectG.edges())
        change_list = [] #
        change_list.append(self.infectG)
        for index in range(self.k):
            #确定需要增删的边数目。
            change_edge_number  = (number_edge) * self.change_ratio
            for  random_edge in range(int(change_edge_number-1)):
                #随机生成某一个数,然后进行删除。
                random_edge_index= random.randint(0, number_edge-1)
                if self.infectG.has_edge(edge_list[random_edge_index][0], edge_list[random_edge_index][1]):  #该边存在
                    # print('该边存在的')
                    # self.infecG.remove_edge(edge_list[random_edge_index][0], edge_list[random_edge_index][1])
                    #不能真的删除，得设置一个标志。
                    # self.infecG.edge[edge_list[random_edge_index][0]]['SI'] == 2:
                    self.infectG.edges[edge_list[random_edge_index][0], edge_list[random_edge_index][1]]['isDel'] = 1  #标志删除了。
            #对这里的infecG进行一次传播。那些边的标志为1的，就不要传播了
            self.infectG = self.infect_infectG(self.infectG) #再次感染一次
            change_list.append(self.infectG) #chage_list只保存传染后的图。
        print('添加后的对象列表')
        print(len(change_list))
        self.infectG_list = change_list

    def  infect_infectG(self,infecG):
        '''
        用传染好的图再传染一次
        :return:
        '''

        # print('开始传染的点是' + str(self.true_Source_list))
        G = infecG
        infectList = []
        for j in G.nodes():
            if  G.node[j]['SI'] == 2:
                infectList.append(j)
        for node in list(set(infectList)):  # infectList表示的是每一个时刻传播到的点
            for height in list([j for j in list(G.neighbors(node)) if  G.edges[node,j]['isDel']!=1]): #只有没删才能够查够传染
                randnum = random.random()
                if randnum < 0.5:
                    G.node[height]['SI'] = 2
        return G




    def Constract_BFS(self,infectG, fix_Number_source,Candidate_node = None):
        '''

        :param infectG:    #感染图
        :param fix_Number_source:  #确定的源数目
        :return:                #返回源的id
        '''

        '''
        获取被感染的传播子图，然后进行BFS构建。
        
        '''
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
        self.tempGraph = tempGraph  #临时图生成
        print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
        print('这个感染区域的传播图节点个数')
        Alternativenodeset = []
        if Candidate_node:
            Alternativenodeset = list(set(Candidate_node))
        else:
            Alternativenodeset = list(set(tempGraphNodelist))  # 备选集合。
        minCoverlist = []
        if fix_Number_source == 3:
            # 两源情况，怎么办。
            # 用jaya算法，总的list我们知道了的，但是我们也要知道jaya需要的x1和x2空间，注意我这里是离散型数据，就是x1，x2 是离散型的。非连续，怎么办？
            '''
            1 变种jaya算法，首先生成100个种群大小。
            2  然后，算出每个similir，然后有最坏的那个，还有最好的那个。把最坏的那个拿出来，最好的那个拿出来。
            3 开始计算，让其他98个节点，靠近最好（计算最短距离，然后靠近那个店），远离最坏（计算最短距离，不靠近那个店，随便选个点走。）。
    
            '''
            min = 200
            print('多源情况,先考察同时传播传播')
            # print('源点为' + str(sourceNumber) + '情况')
            # 先判断源点个数，从chooseList中随机挑选两点，进行h构建。
            # combinationList = list(combinations(Alternativenodeset, sourceNumber))  # 这是排列组合，再次针对这个排列组合,这是所有的两个
            print('这一步炸了')
            combinationList = []  # 样本集合
            # 随机产生这些可能性，随机生成种群50大小。
            for sampleindex in range(0, 53):
                combinationList.append([random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                        random.choice(Alternativenodeset)])
            sourceAndH = []
            hlists = [i for i  in range(10,40)]
            for htemp in range(10, 40):
                for sourcetmep in combinationList:
                    sourceAndH.append([sourcetmep, htemp])  # sourceAndH 是所有的东西，就是[source,h]格式。
            # 从combinationList中寻找100个样本集。
            Sampleset = random.sample(sourceAndH, 50)
            print('样本集产生完毕，100个，是' + str(Sampleset))
            bestsourceNews = []
            # 迭代五次
            for i in range(1, 9):
                # 我这里根本不是靠近最优的那个嘛。就是随机，那就随机变好吧。每个都更新一遍。每个都更新，只要变好就行。
                for sourcesi in range(len(Sampleset)):
                    # print('当前输入list' + str(Sampleset[sourcesi]))
                    mincover = self.getSimilir1(Sampleset[sourcesi][0], Sampleset[sourcesi][1], singleRegionList,
                                           infectG)
                    # 随机更换，看如何让变好
                    # currentindex = sourceAndH.index([Sampleset[sourcesi][0], Sampleset[sourcesi][1]])
                    length = len(sourceAndH)
                    for j in range(1, 4, 1):  # 随机变4次，只要能变好
                        lateelement = [[random.choice(Alternativenodeset), random.choice(Alternativenodeset),
                                        random.choice(Alternativenodeset)],
                                       random.choice(hlists)]
                        # print('当前输入的后面list' + str(lateelement))
                        latemincover = self.getSimilir1(lateelement[0], lateelement[1], singleRegionList, infectG)
                        if mincover > latemincover:
                            mincover = latemincover  # 有更好地就要替换
                            print("要进行替换了" + str(sourceAndH[sourcesi]) + '被替换成lateelement')
                            Sampleset[sourcesi] = lateelement  # 替换
                            print(Sampleset[sourcesi])

            print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
            # 计算样本集的similir，找出最好的。
            for sources in Sampleset:
                mincover = self.getSimilir1(sources[0], sources[1], singleRegionList, infectG)
                if mincover < min:
                    min = mincover  # 这一次最好的覆盖误差率
                    bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。

            print('得到多源点情况最小的覆盖率为' + str(min))
            minCoverlist.append([bestsourceNews[0], bestsourceNews[1], min])

        print(minCoverlist)
        # 返回的应该是最可能的结果。获取mincover最小的返回。第三个元素才是需要考虑东西。
        # listToTxt(minCover, 'result.txt')
        result = sorted(minCoverlist, key=lambda x: (x[2]))
        # listToTxt(result[0], 'coverError.txt')  # 覆盖率结果
        self.single_best_result = result[0]
        # return result[0]

    '''
    适用于公式计算公式       为1-  树并集交感染图/树并集并感染图
    '''

    def getSimilir1(self,ulist, hlist, singleRegionList, infectionG):
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
    def revsitionAlgorithm(self,u, h, infectG, subinfectG):
            print('反转算法参数,u和h' + str(u) + '----------' + str(h))
            nodelist = list(nx.bfs_tree(subinfectG, source=u, depth_limit=h).nodes)
            source1G = nx.Graph()  # 构建新的单源传播圆出来
            for edge in subinfectG.edges:
                if edge[0] in nodelist and edge[1] in nodelist:
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


    def  cal_reverse_algorithm(self,infectG):
        resultSource = [ ]
        source = None
        for  index in range(len(self.single_best_result[0])):
             source =  self.revsitionAlgorithm(self.single_best_result[0][index], self.single_best_result[1],infectG , self.tempGraph)
             resultSource.append(source)
        print(resultSource)
        self.findSource_list = resultSource

    def cal_distance(self,infectG):
        lenA= len(self.true_Source_list)
        lenB = len(self.findSource_list)
        print('真实结果为'+str(self.true_Source_list))
        print('找到的为'+str(self.findSource_list))
        matrix_temp = []
        for i in range(0, len(self.true_Source_list)):
            temp = []
            for j in range(0, len(self.findSource_list)):
                temp.append(nx.shortest_path_length(infectG, source=self.true_Source_list[i],
                                                      target=self.findSource_list[j]))

            matrix_temp.append(temp)
        print('看下这个结果是如何'+str(matrix_temp))
        import numpy as np
        cost = np.array(matrix_temp)
        from scipy.optimize import linear_sum_assignment
        row_ind, col_ind = linear_sum_assignment(cost)
        allcost = cost[row_ind, col_ind].sum()
        print('总的代价为'+str(allcost))
        self.first_result_cost_list = [self.true_Source_list,self.findSource_list,allcost / lenA]


        return allcost / lenA


    def  get_Candidate_node(self):
         '''

         根据第一个结果获得候选集合子节点，用临时的图就行
         :return:
         '''
         Candidate_node = []
         print(self.first_result_cost_list[1])  #找到的源点
         for node in self.first_result_cost_list[1]:
            nodelist = list(nx.bfs_tree(self.tempGraph, source=node, depth_limit=self.k_distance).nodes)
            Candidate_node.extend(nodelist)
         print('输出候选集合为-------------------------------------')
         print('候选集合'+str(len(set(Candidate_node))))
         self.last_result_cost_list = list(set(Candidate_node))
         # return  list(set(Candidate_node))

    def  main(self):
        self.get_networkByFile(fileName='../data/treenetwork3000.txt') #获取图，
        self.product_sourceList()        #生成源点
        self.constract_Infection_netWork()     #开始传染
        self.Constract_ManynetWrok()   #生成传染网络
        self.Constract_BFS(self.infectG_list[0], self.fix_number_source) #先针对第一个做个BFS源点检测
        self.cal_reverse_algorithm(self.infectG_list[0]) # 找到反转算法后的生成答案点
        self.cal_distance(self.infectG_list[0])


        #
        #
        # #后来就是动态图的变化，后面的图就根据第一个的结果附近k距离进行BFS即可。
        # self.get_Candidate_node() #获取第一个的被选源点，作为第二次的候选集合
        # self.Constract_BFS(self.infectG_list[1],self.fix_number_source,Candidate_node= self.last_result_cost_list)
        # self.cal_reverse_algorithm(self.infectG_list[1])
        # self.cal_distance(self.infectG_list[1])
        #
        #
        # #
        # self.get_Candidate_node()  # 获取第一个的被选源点，作为第二次的候选集合
        # self.Constract_BFS(self.infectG_list[2], self.fix_number_source, Candidate_node=self.last_result_cost_list)
        # self.cal_reverse_algorithm(self.infectG_list[2])
        # self.cal_distance(self.infectG_list[2])












test  = FindSource()
test.main()



