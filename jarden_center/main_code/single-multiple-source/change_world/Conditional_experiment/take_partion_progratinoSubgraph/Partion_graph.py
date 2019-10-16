



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
   第一种方案，利用K-center,k距离支配集合。
   
    随机选择两点，使得
    '''
    def Partion_graph_K_center(self, G, source_number_=2):
        #开始分区，输出每个区域的点和边。当前是两源的。






















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

        subinfectG = commons.get_subGraph(infectG_other) #只取感染点，为2表示
        #然后将感染点之间所有边都相连接起来。


        #首先进行


        '''
        
        
        应该在这个地方进行传播分区的各种实验，先做好2源的分区。
        '''

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




