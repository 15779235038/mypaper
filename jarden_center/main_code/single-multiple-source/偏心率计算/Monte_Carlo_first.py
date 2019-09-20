#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/17 10:00 上午

# @Author  : baozhiqiang

# @File    : Monte_Carlo.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************


# !/usr/bin/python3

# -*-coding:utf-8 -*-

# Reference:**********************************************

# @Time    : 2019/9/11 2:05 上午

# @Author  : baozhiqiang

# @File    : Different_time.py

# @User    : bao

# @Software: PyCharm

# Reference:**********************************************


import random
import math

import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict

from random import sample
'''





'''

'''
思路：
   1  构建传播网络
   2  计算传播子图的所有点偏心率，
   3  按照偏心率大小分级
   4  不断从每一级中抽取节点进行蒙特卡洛模拟，直到某一级别。模拟就是随机抽取多少点进行m距离覆盖率计算。
   4   直到确定某一级别的覆盖率普遍低，可以通过求和方式求。在根据这一层进行jaya算法。样本为【k个点】，h就是m。
   5  找出最合适的k个点，进行单源定位。
   6  模式图能帮助我们什么？

'''


class FindSource:
    def __init__(self):
        self.initG = None  # 原始图
        self.findSource_list = None  # 当前找到的源的list
        self.findSource_set = None  # 当前找到的源的set
        self.infectG = None  # 感染图
        self.fix_number_source = 3  # 确定的源数目
        self.source_list = None  # 确定下来的源数目。
        self.true_Source_list = None  # 真实源点
        self.netwrok_filename = None  # 文件名字
        self.infectG_list = None  # 感染的多个图列表。
        self.single_best_result = None
        self.tempGraph = None  # 临时生成传播子图
        self.first_result_cost_list = None  # 你求得第一个图的比较好距离。
        self.all_result_cost_list = []
        self.findSource_list = []
        self.distance_error = None

    def ContractDict(self, dir, G):
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

    def get_networkByFile(self, fileName='../data/facebook_combined.txt'):
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

    def product_sourceList(self):
        # 产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
        sumlist = list(self.initG.nodes)

        G = self.initG
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
        self.true_Source_list = rumorSourceList
        # return rumorSourceList

    def constract_Infection_netWork(self):
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
        G = self.initG
        SourceList = self.true_Source_list
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
        self.infectG = G
        # return G


    '''
     2  计算图的所有点偏心率，The eccentricity of a node v is the maximum distance from v to
    all other nodes in G.
   3  按照偏心率大小分级
   4  不断从每一级中抽取节点固定次数进行蒙特卡洛模拟，这一层的计算覆盖率。如果计算所有采样结果的覆盖率总和，如果总和很低，就是这一层。并且h也确定下来。
   直到某一级别。模拟就是随机抽取多少点进行m距离覆盖率计算。
   4   直到确定某一级别的覆盖率普遍低，可以通过求和方式求。在根据这一层进行jaya算法。样本为【k个点】，h就是m。
   5  找出最合适的k个点，进行单源定位。
    '''
    def  cal_ecctity(self):
        #构建传播子图，
        singleRegionList = []
        for node_index in list(self.infectG.nodes()):
            if self.infectG.node[node_index]['SI'] == 2:
                singleRegionList.append(node_index)
        tempGraph = nx.Graph()
        tempGraphNodelist = []
        for edge in self.infectG.edges:
            # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
            if edge[0] in singleRegionList and edge[1] in singleRegionList:
                tempGraph.add_edges_from([edge], weight=1)
                tempGraphNodelist.append(edge[0])
                tempGraphNodelist.append(edge[1])
        self.tempGraph = tempGraph  # 临时图生成

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
        #从偏心率大的考虑，先保存最大偏心度。
        sort_eccentricity_dict = sorted(eccentri_dict.items(),key= lambda x:x[0],reverse=True)
        max_eccentric = sort_eccentricity_dict[0][0]
        print('输出最大的就是那个偏心率'+str(max_eccentric))
        from random import sample
        best_h = 0
        M_dis = 0
        best_h_node = []
        min_cover = 100  # 某一层的覆盖率，肯定会比这个小。
        tempGraph =self.infectG         #采用不同的感染图

        for eccentric, node_list in sort_eccentricity_dict:
            print('how to that')
            print(eccentric,node_list)
            M_dis =  max_eccentric - eccentric  #最好的bFS树半径。
            #随机挑选k个点固定次数。
            temp_all_cover = 0
            temp_cover = 0
            temp_ave_cover = 0
            if len(node_list) > self.fix_number_source*2: #这一层只有大于3个点才可以。
                itemNumber =  int(len(node_list)/10)   #层数越大，节点越多，应该采样越多才能逼近近似值。
                for frequency  in range(itemNumber): #抽取10次,这里有问题，有些层数目多，怎么抽取会好点？按照层数抽取相应的次数会比较好点，公平。
                    slice = random.sample(node_list, self.fix_number_source)
                    temp_cover = self.getSimilir1(slice, M_dis, singleRegionList, tempGraph)
                    temp_all_cover += temp_cover
                if temp_all_cover != 0:
                    temp_ave_cover = temp_all_cover/itemNumber  #求出平均覆盖率。
                    print('temp_ave_cover',temp_ave_cover)
                else:
                    temp_ave_cover = 0.1
                if temp_ave_cover <= min_cover:
                    #这一层表现优异，记下h，以及这一层的所有节点。
                    print('每次平均的覆盖率是'+str(min_cover))
                    print('temp_ave_cover',temp_ave_cover)
                    min_cover = temp_ave_cover
                    best_h_node = node_list
                    best_h = M_dis
        print('输出表现优异同学,看看'+str(best_h_node),str(best_h))
        #得到最优层数解，再大量进行选择，使用jaya算法。构建大量样本。在固定h下的寻找最合适的节点。

        '''
        1 构建种群样本下
        2 在固定h下更新
        '''
        fix_number_sourcetemp = self.fix_number_source
        Sampleset =  [ ]
        for i  in range(50):
            Sampleset.append(random.sample(best_h_node, self.fix_number_source))
        infectG= self.infectG
        min_cover = 1
        min = 1
        mincover = None
        bestsourceNews = None
        minCoverlist = []
        for  iter_number in range(4):
            for sample_index in range(len(Sampleset)):
                mincover = self.getSimilir1(Sampleset[sample_index], best_h, singleRegionList,
                                        tempGraph)
                # 随机更换，看如何让变好
                for j in range(1, 4, 1):  # 随机变4次，只要能变好
                    # lateelement = [random.choice(best_h_node), random.choice(best_h_node),
                    #                 random.choice(best_h_node),random.choice(best_h_node)]

                    lateelement = [random.choice(best_h_node) for i in range(self.fix_number_source)]
                    # print('当前输入的后面list' + str(lateelement))
                    latemincover = self.getSimilir1(lateelement, best_h, singleRegionList, tempGraph)
                    if mincover > latemincover:
                        mincover = latemincover  # 有更好地就要替换
                        # print("要进行替换了" + str(Sampleset[sample_index]) + '被替换成lateelement')
                        Sampleset[sample_index] = lateelement  # 替换
                        # print(Sampleset[sample_index])
            # print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
            # 计算样本集的similir，找出最好的。
            for sources in Sampleset:
                mincover = self.getSimilir1(sources, best_h, singleRegionList, tempGraph)
                if mincover < min:
                    min = mincover  # 这一次最好的覆盖误差率
                    bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。
            print('得到多源点情况最小的覆盖率为' +str(bestsourceNews)+ str(min))
            minCoverlist.append([bestsourceNews, best_h, min])
        print(minCoverlist)
        result = sorted(minCoverlist, key=lambda x: (x[2]))
        self.single_best_result = result[0]



    '''
      适用于公式计算公式       为1-  树并集交感染图/树并集并感染图
      '''

    def getSimilir1(self, ulist, hlist, singleRegionList, infectionG):
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


    def  cal_reverse_algorithm(self,infectG):
        resultSource = []
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
        self.distance_error = allcost/lenA
        return allcost / lenA
    def main(self,dir):
        '''
        走来不要那么难，先搞定树吧。才能继续搞定图。
        :return:
        '''
        pre = '../data/'
        last = '.txt'
        # filename = ''
        self.get_networkByFile(fileName=pre+dir+last)  # 获取图，
        self.product_sourceList()  # 生成源点
        self.constract_Infection_netWork()  # 开始传染
        self.cal_ecctity()      #找到最好的覆盖率结果。
        self.cal_reverse_algorithm(self.infectG)  # 找到反转算法后的生成答案点
        self.cal_distance(self.infectG)


    '''
    计算误差100次。
    
    '''
    def cal_distanceError(self,dir):
        self.fix_number_source = 2
        distance = 0
        for i in range(10):
            self.main(dir)
            distance += self.distance_error
        result =distance/10
        # 导入time模块
        import time
        # 打印时间戳
        # print(time.time())
        pre = './result/'
        last = '.txt'
        with open(pre+dir+'first'+last, 'w') as f:
            f.write(str(time.time())+'\n')
            f.write(str(10)+'    '+str(result))
        print(distance/10)







test  = FindSource()
filename = 'CA-GrQc'
test.cal_distanceError(filename)





