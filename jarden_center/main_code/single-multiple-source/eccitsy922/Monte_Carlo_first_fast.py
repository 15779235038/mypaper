#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/26 10:52 上午

# @Author  : baozhiqiang

# @File    : Monte_Carlo_first_fast.py

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
        self.radius_graph =6




    '''
     2  计算图的所有点偏心率，The eccentricity of a node v is the maximum distance from v to
    all other nodes in G.
   3  按照偏心率大小分级
   4  不断从每一级中抽取节点固定次数进行蒙特卡洛模拟，这一层的计算覆盖率。如果计算所有采样结果的覆盖率总和，如果总和很低，就是这一层。并且h也确定下来。
   直到某一级别。模拟就是随机抽取多少点进行m距离覆盖率计算。
   4   直到确定某一级别的覆盖率普遍低，可以通过求和方式求。在根据这一层进行jaya算法。样本为【k个点】，h就是m。
   5  找出最合适的k个点，进行单源定位。
    '''
    def  cal_ecctity(self,source_list):
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
        min_eccentric = sort_eccentricity_dict[-1][0]
        print('输出最大的就是那个偏心率'+str(max_eccentric))
        from random import sample
        best_h = 0
        M_dis = 0
        best_h_node = []
        min_cover = 100  # 某一层的覆盖率，肯定会比这个小。
        tempGraph = self.infectG

        self.test_coverage(source_list,6,tempGraph,singleRegionList)

        for  node_list_index in range(len(sort_eccentricity_dict)-1):
            for h in range(self.radius_graph // 2, self.radius_graph, 1):
                # print('how to that')
                # print(sort_eccentricity_dict[node_list_index][1])
                # print(sort_eccentricity_dict[node_list_index][0])
                sort_eccentricity_dict[node_list_index][1].extend(sort_eccentricity_dict[node_list_index + 1][1])
                # print(sort_eccentricity_dict[node_list_index][1])
                M_dis = max_eccentric - sort_eccentricity_dict[node_list_index][0]  # 最好的bFS树半径。
                # 随机挑选k个点固定次数。
                temp_all_cover = 0
                temp_cover = 0
                temp_ave_cover = 0
                if len(sort_eccentricity_dict[node_list_index][1]) > self.fix_number_source * 2:  # 这一层只有大于3个点才可以。
                    itemNumber = int(len(sort_eccentricity_dict[node_list_index][1]) / 20)  # 层数越大，节点越多，应该采样越多才能逼近近似值。
                    for frequency in range(itemNumber):  # 抽取10次,这里有问题，有些层数目多，怎么抽取会好点？按照层数抽取相应的次数会比较好点，公平。
                        slice = random.sample(sort_eccentricity_dict[node_list_index][1], self.fix_number_source)
                        temp_cover = commons.getSimilir1(slice, h, singleRegionList, tempGraph)
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
                        best_h_node = sort_eccentricity_dict[node_list_index][1]
                        best_h = h
        print('输出表现优异同学,看看' + str(best_h_node), str(best_h))
        #得到最优层数解，再大量进行选择，使用jaya算法。构建大量样本。在固定h下的寻找最合适的节点。
        '''
        1 构建种群样本下
        2 在固定h下更新
        '''
        self.single_best_result = commons.jaya(tempGraph, best_h_node, self.fix_number_source, best_h, singleRegionList)
        return best_h,singleRegionList,tempGraph


    '''
    1 实验覆盖率是不是真的有那么好，以找到最好的h和真实的的源点。和感染图
    
    
    '''
    def  test_coverage(self,sourcelist,h,infectG,singleregionList):
        print('查看真实源点的覆盖率以及真实h，看看我们的算法是不是那么智能。找到好的覆盖率')
        mins= 10
        h = 0
        for   h_temp  in range(2,11,1):
            sim=commons.getSimilir1(sourcelist,h_temp,singleregionList,infectG)
            if sim< mins:
                mins =sim
                h =h_temp
        print('最好的覆盖率以及h',str(sim)+'   '+str(h))


    def  cal_reverse_algorithm(self,infectG):
        resultSource = []
        source = None
        for  index in range(len(self.single_best_result[0])):
             source =  commons.revsitionAlgorithm(self.single_best_result[0][index], self.single_best_result[1],infectG , self.tempGraph)
             resultSource.append(source)
        print(resultSource)
        self.findSource_list = resultSource

    def main(self,dir):
        '''
        走来不要那么难，先搞定树吧。才能继续搞定图。
        :return:
        '''
        pre = '../data/'
        last = '.txt'
        # filename = ''
        self.initG = commons.get_networkByFile(fileName=pre+dir+last)  # 获取图，
        max_sub_graph = commons.judge_data( self.initG)
        source_list = commons.product_sourceList(max_sub_graph, self.fix_number_source)
        self.true_Source_list = source_list
        self.infectG = commons.propagation1(max_sub_graph,self.true_Source_list)  # 开始传染
        best_h,singleRegionList,tempGraph =self.cal_ecctity(source_list)      #找到最好的覆盖率结果。
        # self.test_coverage(source_list,best_h,tempGraph,singleRegionList)
        self.cal_reverse_algorithm(self.infectG)  # 找到反转算法后的生成答案点
        self.distance_error = commons.cal_distance(self.infectG, self.true_Source_list, self.findSource_list)

        # return commons.cal_distance(self.infectG, self.true_Source_list,self.findSource_list)


    '''
    计算误差100次。
    '''
    def cal_distanceError(self,dir):
        self.fix_number_source = 4
        distance = 0
        count = 0
        for i in range(10):
            self.main(dir)
            distance += self.distance_error
            count += 1
            print('distance/次数',distance/count)
        result =distance/10
        # 导入time模块
        import time
        # 打印时间戳
        # print(time.time())
        pre = './result/'
        last = '.txt'
        with open(pre+dir+'first'+last, 'a') as f:
            f.write(str(time.asctime(time.localtime(time.time()) ))+'\n')
            f.write(str(10)+'     '+str(dir)+'    '+str(result))
        print(distance/10)

test  = FindSource()
filename = 'facebook_combined'
test.cal_distanceError(filename)





