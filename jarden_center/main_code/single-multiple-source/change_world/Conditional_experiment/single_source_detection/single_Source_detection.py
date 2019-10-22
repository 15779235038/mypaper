
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community
import random
import math
import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict
from random import sample
import sys
import  copy
import  Partion_common
import commons
class Single_source:
    def __init__(self):
        pass

    # 这是sample-path，也就是commons挖过来的
    def revsitionAlgorithm_singlueSource(self,subinfectG):
        # print('反转算法参数,u和h' + str(u) + '----------' + str(h))
        nodelist = list(subinfectG.nodes)
        source1G = nx.Graph()  # 构建新的单源传播圆出来
        source1G = subinfectG
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
                # 如果有收集到了50%的节点，那么就到了。

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

        return result  #只返回最好的node



    '''
    
    第二种单源定位方法。
    我们提出一种新的单源定位方法，基于覆盖率计算的。
    统计每个点对于整个感染图的每个点计算公式，包括距离中心和覆盖率中心的综合计算方式。
    公式等于覆盖率/距离,越大越好。
    
    思路：从每个点计算一次djstra方法，统计距离。
    传入的是原始图
    
  
    
    '''

    def  single_source_bydistance_coverage(self,infectG,subinfectG):
        sort_dict = commons.partion_layer_dict(infectG, 10)  # 分层
        print('sort_list', sort_dict)
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode,ditance in length_dict.items():
                node_import += sort_dict[othernode] / (ditance+1)
            node_cal.append([node,node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1], reverse=True)
        print(sort_list)
        return  sort_list[0]





    '''
    第3种单源定位方法。距离中心
    就是每个点距离其他点最近的距离中心。就是了的。

    '''
    def  single_source_bydistance(self,subinfectG):
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode,ditance in length_dict.items():
                node_import += ditance
            node_cal.append([node,node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1])
        print(sort_list)
        return  sort_list[0]









    '''
      #设计本类用来做单源定位。
    '''

    def main(self,filename):

        # #拿到图
        initG = commons.get_networkByFile(filename)
        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG = commons.propagation1(max_sub_graph,source_list)

        subinfectG = commons.get_subGraph_true( infectG)  # 只取感染点，为2表示,真实的感染图。
        #将在这里进行单源测试。
        '''   第一种，就是jarden center '''
        #
        # result_node = self.revsitionAlgorithm_singlueSource(subinfectG)
        # ''' 第二种，就是coverage/distance'''
        # result_node= self.single_source_bydistance_coverage(infectG,subinfectG)

        '''  第3种，距离中心'''
        result_node = self.single_source_bydistance( subinfectG)

        distance= nx.shortest_path_length(subinfectG,source=source_list[0],target=result_node[0])
        print('结果是', distance)
        return distance



'''


'''
import time

if __name__ == '__main__':
    test = Single_source()
    sum = 0
    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')

    # initG = commons.get_networkByFile(filename)
    filname = '../../../data/4_regular_graph_3000_data.txt'

    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')

    # filname = '../../data/CA-GrQc.txt'



    # method ='distan+ covage'
    # method = 'jardan_center'
    method ='distance'



    
    for i in range(0, 20):
        tempresult = test.main(filname)
        sum += tempresult  # 跑实验

        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果是   '+str(tempresult)+'      数据集'+'方法'+str(method) + str(filname) +   '\n')
    with open('result.txt', "a") as f:
        f.write('数据集' + str(filname)+'方法' +str(method)+ '总结果   ' + str(sum / 20) + '\n')
        f.write('\n')
    print('result', sum / 20)
    print(sum / 20)




