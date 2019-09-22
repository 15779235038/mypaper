#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/18 11:33 上午

# @Author  : baozhiqiang

# @File    : Monte_Carlo_second.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************




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
import  commons
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
        self.fix_number_source = 4  # 确定的源数目
        self.source_list = None  # 确定下来的源数目。
        self.true_Source_list = None  # 真实源点
        self.netwrok_filename = None  # 文件名字
        self.infectG_list = None  # 感染的多个图列表。
        self.single_best_result = None
        self.tempGraph = None  # 临时生成传播子图
        self.first_result_cost_list = None  # 你求得第一个图的比较好距离。
        self.all_result_cost_list = []
        self.findSource_list = []
        self.singe_source_result = None     #传播子图进行单源定位的结果
        self.singleRegionList  = None  #传播子图的节点数目
        self.radius = 0
        self.distance_error = None






        # 设计反向传播算法，接收参数。u，h，infectG。
    def revsitionAlgorithm_pre(self, infectG):

            # 构建传播子图，
            singleRegionList = []
            for node_index in list(infectG.nodes()):
                if infectG.node[node_index]['SI'] == 2:
                    singleRegionList.append(node_index)
            self.singleRegionList = singleRegionList
            tempGraph = nx.Graph()
            tempGraphNodelist = []
            for edge in infectG.edges:
                # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
                if edge[0] in singleRegionList and edge[1] in singleRegionList:
                    tempGraph.add_edges_from([edge], weight=1)
                    tempGraphNodelist.append(edge[0])
                    tempGraphNodelist.append(edge[1])
            self.tempGraph = tempGraph  # 临时图生成
            source1G =nx.Graph()
            nodelist = list(tempGraph.nodes)
            source1G = tempGraph
            print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
            print('这个感染区域的传播图节点个数')
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
            print('result单源传播结果',result)
            self.singe_source_result = result


    def  cal_reverse_algorithm(self,infectG):
        resultSource = []
        source = None
        for  index in range(len(self.single_best_result[0])):
             source =  commons.revsitionAlgorithm(self.single_best_result[0][index], self.single_best_result[1],infectG , self.tempGraph)
             resultSource.append(source)
        print(resultSource)
        self.findSource_list = resultSource


    from collections import defaultdict


    from random import sample
    '''
    
    1   针对单源点，进行BFS
    2   获取每层节点，然后进行抽样就可以了。
    '''

    def cal_BFS_monte_Carlo(self):

        tempGraph = nx.Graph()
        tempGraph = self.tempGraph
        print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraph.nodes))))
        print('这个感染区域的传播图节点个数')
        dfs_result_dict =commons.test_BFS_node(tempGraph, source_node=self.singe_source_result)
        sort_dfs_result_dict = sorted(dfs_result_dict.items(), key=lambda x: x[0])
        print('sort_dfs_result_dict',sort_dfs_result_dict)
        '''
        这里我们只知道中心点的BFS点，还不能确定H。我们可以以传播子图的半径为最大h。进行
        '''

        singleRegionList = self.singleRegionList
        #计算半径。
        # radius_graph= nx.radius(tempGraph)
        # radius_graph = 40

        tempGraph =self.infectG         #采用不同的感染图

        radius_graph =self.radius
        print('图半径为', radius_graph)
        best_h = 0
        best_h_node = []
        min_cover = 100  # 某一层的覆盖率，肯定会比这个小。
        for h  in range(radius_graph// 2, radius_graph, 1):
            for  k ,node_list in sort_dfs_result_dict:
                print('how to that')
                # print(eccentric, node_list)
                # M_dis = max_eccentric - eccentric  # 最好的bFS树半径。
                # 随机挑选k个点固定次数。
                temp_all_cover = 0
                temp_cover = 0
                temp_ave_cover = 0
                if len(node_list) > self.fix_number_source * 2:  # 这一层只有大于3个点才可以。
                    if len(node_list) > 20:
                        itemNumber = int(len(node_list) / 2)  # 层数越大，节点越多，应该采样越多才能逼近近似值。
                    else:
                        itemNumber = 2      #这是树的情况，每一层节点太少了
                    for frequency in range(itemNumber):  # 抽取10次,这里有问题，有些层数目多，怎么抽取会好点？按照层数抽取相应的次数会比较好点，公平。
                        slice = random.sample(node_list, self.fix_number_source)
                        temp_cover = commons.getSimilir1(slice, h,singleRegionList, tempGraph)
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
                        best_h_node = node_list
                        best_h = h

        print('输出表现优异同学,看看' + str(best_h_node), str(best_h))
        # 得到最优层数解，再大量进行选择，使用jaya算法。构建大量样本。在固定h下的寻找最合适的节点。
        '''
        1 构建种群样本下
        2 在固定h下更新
        '''
        fix_number_sourcetemp = self.fix_number_source
        Sampleset = []
        for i in range(50):
            Sampleset.append(random.sample(best_h_node, self.fix_number_source))
        infectG = self.infectG
        min_cover = 1
        min = 1
        mincover = None
        bestsourceNews = None
        minCoverlist = []
        for iter_number in range(5):
            for sample_index in range(len(Sampleset)):
                mincover = commons.getSimilir1(Sampleset[sample_index], best_h, singleRegionList,
                                            tempGraph)
                # 随机更换，看如何让变好
                for j in range(1, 4, 1):  # 随机变4次，只要能变好
                    # lateelement = [random.choice(best_h_node), random.choice(best_h_node),
                    #                random.choice(best_h_node)]
                    #
                    lateelement = [random.choice(best_h_node) for i in range(self.fix_number_source)]

                    # print('当前输入的后面list' + str(lateelement))
                    latemincover = commons.getSimilir1(lateelement, best_h, singleRegionList, tempGraph)
                    if mincover > latemincover:
                        mincover = latemincover  # 有更好地就要替换
                        # print("要进行替换了" + str(Sampleset[sample_index]) + '被替换成lateelement')
                        Sampleset[sample_index] = lateelement  # 替换
                        # print(Sampleset[sample_index])
            # print('经过5次迭代之后的sample的list为多少呢？' + str(Sampleset))
            # 计算样本集的similir，找出最好的。
            for sources in Sampleset:
                mincover = commons.getSimilir1(sources, best_h, singleRegionList, tempGraph)
                if mincover < min:
                    min = mincover  # 这一次最好的覆盖误差率
                    bestsourceNews = sources  # 最好的覆盖误差率对应的最好的那个解。
            print('得到多源点情况最小的覆盖率为' + str(min))
            minCoverlist.append([bestsourceNews, best_h, min])
        print(minCoverlist)
        result = sorted(minCoverlist, key=lambda x: (x[2]))
        self.single_best_result = result[0]








    '''
    1  先对整个传播子图图进行单源定位(样本路径），找出一个源点。这步可以替换成其他中心度。
    2然后进行BFS，扩大层数
    3在每一层上蒙特卡洛模拟，求出最优秀的那一层。
    4按照前面方法的套路来。
    '''
    def main(self,dir):
        '''
        :return:
        '''
        # filename= 'treenetwork3000.txt' #半径为40
        #对于树图，以及普通图。参数可能设置不一样，h变换不一样。需要手动调整。
        # filename = 'CA-GrQc.txt'
        self.radius = 6

        pre = '../data/'
        last = '.txt'
        # filename = ''
        self.initG = commons.get_networkByFile(fileName=pre + dir + last)  # 获取图，
        max_sub_graph = commons.judge_data(self.initG)
        source_list = commons.product_sourceList(max_sub_graph, self.fix_number_source)
        self.true_Source_list = source_list
        self.infectG = commons.propagation1(self.initG, self.true_Source_list)  # 开始传染
        self.revsitionAlgorithm_pre(self.infectG)  # 找到反转算法后的生成答案点
        self.cal_BFS_monte_Carlo()  # 找到最好的覆盖率结果。
        self.cal_reverse_algorithm(self.infectG)  # 找到反转算法后的生成答案点
        self.distance_error = commons.cal_distance(self.infectG, self.true_Source_list, self.findSource_list)

        # return commons.cal_distance(self.infectG, self.true_Source_list, self.findSource_list)

    '''
    计算误差100次。

    '''

    def cal_distanceError(self, dir):
        self.fix_number_source = 2
        distance = 0
        for i in range(10):
            self.main(dir)
            distance += self.distance_error
        result = distance / 10
        # 导入time模块
        import time
        # 打印时间戳
        # print(time.time())
        pre = './result/'
        last = '.txt'
        with open(pre + dir +'second'+ last, 'a') as f:
            f.write(str(time.time()) + '\n')
            f.write(str(10) + '    ' + str(result))
        print(distance / 10)


test = FindSource()
filename = 'CA-GrQc'
test.cal_distanceError(filename)




