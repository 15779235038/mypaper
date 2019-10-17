



import numpy as np
import matplotlib.pyplot as plt

import random
import math
import networkx  as nx
import numpy
from munkres import print_matrix, Munkres
from collections import defaultdict
from random import sample
import sys

import commons
class Partion_graph:
    def __init__(self):
        pass
    '''
    本类用来划分传播区域,先做好两源的。
    '''
    def get_Graph(self,filename):
        #通过文件生成图。
        subGraph = commons.get_networkByFile(filename)
        #该图必定连通。
        #开始分区，输出每个区域的点和边。当前是两源的。
        return subGraph

    '''
   第一种方案，k-center，先分层。注意传入的得是原始图。
   然后从内层随机选择两点，这两点将内层的全部加入他们，
   外层的节点根据距离加入他们。每个点只需要算一次迪杰斯特拉就可以了。
   
   怎么重新调整呢？不断更新就是为了缩小某一个目标函数，让选中的点距离不同类别
   的点距离之和最小。。
   
    随机选择两点，使得
    '''
    def Partion_graph_K_center(self, G,true_source_list ,source_number_=2):
        #开始分区，输出每个区域的点和边。当前是两源的。

        sort_list = commons.partion_layer(G, 10)  #分层
        first_layer = [x for x in sort_list[0][1]]  #用第一层的节点。
        #先验证源点在不在第一层。
        b = set(true_source_list)
        print('源点在不在第一层呢？',b.issubset(first_layer))
        subinfectG = commons.get_subGraph_true(G)  # 获取真实的传播图
        two_source = random.sample(first_layer, 2)  # 从list中随机获取2个元素，作为一个片断返回
        flag = 1
        while flag:
            #对这两个点进行Djstra，计算所有点到他们的距离。
            print('two_source',two_source)
            lengthA_dict = nx.single_source_bellman_ford_path_length(subinfectG,two_source[0],weight='weight')
            lengthB_dict = nx.single_source_bellman_ford_path_length(subinfectG,two_source[1],weight='weight')
            #初始化两个集合，用来保存两个类别节点集合。
            node_twolist = [[], []]   #保存两个类别节点集合
            node_diff_twolist = [[],[]] #保存不同点
            for node in list(subinfectG.nodes):
                if lengthA_dict[node] >lengthB_dict[node]: #这个点离b近一些。
                    node_twolist[1].append(node)
                    node_diff_twolist[1].append(node)
                elif lengthA_dict[node] < lengthB_dict[node]:
                    node_twolist[0].append(node)
                    node_diff_twolist[0].append(node)
                else:
                    node_twolist[0].append(node)
                    node_twolist[1].append(node)
            print('node_twolist',len(node_twolist[1]))
            #在两个list中找到中心位置，有几种中心性可以度量的。或者进行快速算法。
            #判断这次找的两个中心好不好。
            


            flag =0


























        pass











    def verification(self,node_list,edge_list):
        #用真实的例子中的每个分区的list和边的list。进行比较就好了啊。
        pass


    def judge_connect(self,subinfecG):
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
      #设计本类用来划分区域。
      1会有的方法有根据原图划分。
      2 划分结果比较。
      3 多个数据集测试。

    '''
    def  main(self):

         # #拿到图
         # subGraph=self.get_Graph('../Propagation_subgraph/many_methods/result/chouqu.txt')


        initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 2)
        print('两个节点的距离',nx.shortest_path_length(max_sub_graph,source= source_list[0],target=source_list[1]))
        #看下分区效果行不行，传播两次，就好了，
        # 一个是SI为2，一个是SI为3。交叉区域为4。
        infectG = commons.propagation_dif_sigl(max_sub_graph, source_list[0], 3)    #3表示一个源点。
        infectG_other = commons.propagation_dif_sigl(infectG, source_list[1], 4)  # 4标示表示一个源点。 如果两个标示重合，
        #那就取5

        #提起其中某些节点的东西，提取3，4，5
        node_list3 = []
        node_list4 = []
        node_list5 = []
        for nodes in  list(infectG_other.nodes):
            if infectG_other.node[nodes]['SIDIF']==3:
                node_list3.append(nodes)
            elif  infectG_other.node[nodes]['SIDIF']==4:
                node_list4.append(nodes)
            elif infectG_other.node[nodes]['SIDIF']==5:
                node_list5.append(nodes)
        node_list3.extend(node_list5)
        node_list4.extend(node_list5)

        print('first——node_list3',len(node_list3))
        print('second——node_list4',len(node_list4))

        subinfectG = commons.get_subGraph_true(infectG_other) #只取感染点，为2表示,真实的感染图。


        #然后将感染点之间所有边都相连接起来。


        #首先进行


        '''
        应该在这个地方进行传播分区的各种实验，先做好2源的分区。
        '''

        self.Partion_graph_K_center(infectG_other,source_list,2)

        #进行覆盖率走，并进行jaya算法。

        print('传播图的点个数为',subinfectG.number_of_nodes())
        print('传播图的边个数为', subinfectG.number_of_edges())

        print('传播子图是否连通？',)
        sub_connect_infect =self.judge_connect(subinfectG)
        singleRegionList = list(sub_connect_infect.nodes)
        results = commons.jayawith_dynami_H(infectG_other, singleRegionList, 2, [4, 5, 6,7], singleRegionList)
        print(results)

        node_coverage1 = []
        node_coverage2 = []


        # #计算两个传播区域的重合区域。
        node_coverage1.extend(list(nx.bfs_tree(infectG, source=results[0][0], depth_limit=results[1])))
        node_coverage2.extend(list(nx.bfs_tree(infectG, source=results[0][1], depth_limit=results[1])))




        #判断那个跟那个拟合。就看BFS树源点跟那个近就可以了。就认为是那个。
        lengtha =nx.shortest_path_length(infectG, source=results[0][0], target=source_list[0])
        lengthb = nx.shortest_path_length(infectG, source=results[0][1], target=source_list[0])
        print('length1',lengtha)
        print('lengthb',lengthb)
        if  lengtha >  lengthb:
            print('成功匹配。')
            a= [x for x in node_list3 if x in node_coverage2]
            print('len(a)', len(a))
            print(len(a)/len(node_list3))

            b = [x for x in node_list4 if x in node_coverage1]
            print('len(b)',len(b))
            print(len(b)/len(node_list4))

            print('失败匹配')
            c = [x for x in node_list3 if x in node_coverage1]
            print('len(c)', len(c))
            print(len(c) / len(node_list3))
            d = [x for x in node_list4 if x in node_coverage2]
            print('len(c)', len(d))
            print(len(d) / len(node_list4))

        else:
            print('成功匹配。')
            a = [x for x in node_list3 if x in node_coverage1]
            print('len(a)', a)
            print(len(a) / len(node_list3))
            b = [x for x in node_list4 if x in node_coverage2]
            print('len(b)', b)
            print(len(b) / len(node_list4))

            print('失败匹配')
            c = [x for x in node_list3 if x in node_coverage2]
            print('len(c)', len(c))
            print(len(c) / len(node_list3))
            d = [x for x in node_list4 if x in node_coverage1]
            print('len(c)', len(d))
            print(len(d) / len(node_list4))









'''


'''
if __name__ == '__main__':
    test = Partion_graph()

    test.main()   #跑实验




