



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
import  Partion_common
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
   1  然后从第一层随机选择两点，，
   外层的节点根据距离加入他们。每个点只需要算一次迪杰斯特拉就可以了。
   
   2 选择新的结果。
   不断更新就是为了缩小某一个目标函数，让选中的点距离自己不同类别
   的点距离之和最小。   分别将多个相加起来。
   
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
        lengthA_B = 100000
        good_two_result = []
        best_node_two_result = None
        for iter  in range(0,100):
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

            lengthA_sum = 0  #a这个不同点，
            lengthB_sum = 0
            for i in node_diff_twolist[0]:  #距离a近，第一个源点近的点。统计它跟第二个区域点的距离之和
                lengthA_sum += lengthB_dict[i]
            for j in node_diff_twolist[1]:  # 距离b近，第二个源点近的点。统计它跟第二个区域点的距离之和
                lengthB_sum += lengthA_dict[j]

            sums = lengthA_sum + lengthB_sum
            if sums <lengthA_B:
               print('sums',sums)
                #是比原来好的的两个源。
               lengthA_B = sums
               good_two_result=two_source
               best_node_two_result = node_twolist

            else:
                #重新长生两个源吧。这里还是可以做优化的，选择的方向问题。
                two_source = random.sample(first_layer, 2)

        print('good_two_result', good_two_result)
        print('good_node_two_result', best_node_two_result)

        return [[good_two_result[0],best_node_two_result[0]],[good_two_result[1],best_node_two_result[1]]]




    '''
    
    使用jaya有参数的操作。
    
    
    '''

    def   jaya_add_coverage(self,infectG):
            subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。

            print('传播图的点个数为', subinfectG.number_of_nodes())
            print('传播图的边个数为', subinfectG.number_of_edges())

            print('传播子图是否连通？', )
            sub_connect_infect = self.judge_connect(subinfectG)
            singleRegionList = list(sub_connect_infect.nodes)
            results = commons.jayawith_dynami_H(infectG, singleRegionList, 2, [4, 5, 6, 7], singleRegionList)
            print(results)
            node_coverage1 = []
            node_coverage2 = []
            # #计算两个传播区域的重合区域。
            node_coverage1.extend(list(nx.bfs_tree(infectG, source=results[0][0], depth_limit=results[1])))
            node_coverage2.extend(list(nx.bfs_tree(infectG, source=results[0][1], depth_limit=results[1])))
            return [[results[0][0],node_coverage1],[results[0][1],node_coverage2]]






    '''
    3 删除高中介性节点，分批次删除。直到图不连通
    传入的还是原图，有感染和未感染点的。
    '''
    def delete_high_betweenness_centrality(self,infectG):
        subinfectG = commons.get_subGraph_true(infectG)
        #根据中介性分层然后删除。




    '''
       4  删除高中介性边，分批次删除。直到图不连通
       传入的还是原图，有感染和未感染点的。
       '''

    def delete_high_betweenness_edge_centrality(self, infectG):
        subinfectG = commons.get_subGraph_true(infectG)
        # 根据中介性分层然后删除。
        sort_list = Partion_common.get_layer_edge_between(subinfectG)

        for  i  in range(0,10):  #



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

        '''
        应该在这个地方进行传播分区的各种实验，先做好2源的分区。
        '''
        #第一种方法。
        # twosource_node_list =self.Partion_graph_K_center(infectG_other,source_list,2)
        #进行覆盖率走，并进行jaya算法。
        # twosource_node_list=self.jaya_add_coverage(infectG_other)
        #进行删除边操作。
        twosource_node_list = self.delete_high_betweenness_edge_centrality(infectG_other)
        node_coverage1 = twosource_node_list[0][1]
        node_coverage2 = twosource_node_list[1][1]
        #判断那个跟那个拟合。就看BFS树源点跟那个近就可以了。就认为是那个。
        lengtha =nx.shortest_path_length(infectG, source=twosource_node_list[0][0], target=source_list[0])
        lengthb = nx.shortest_path_length(infectG, source=twosource_node_list[1][0], target=source_list[0])
        print('length1',lengtha)
        print('lengthb',lengthb)
        if  lengtha >  lengthb:
            print('成功匹配。')
            a= [x for x in node_list3 if x in node_coverage2]
            print('len(a)', len(a))
            print(len(a)/len(node_list3))

            A_ratio = len(a) / len(node_list3)

            b = [x for x in node_list4 if x in node_coverage1]
            print('len(b)',len(b))
            print(len(b)/len(node_list4))
            B_ratio =  len(b)/len(node_list4)
            print('失败匹配')
            c = [x for x in node_list3 if x in node_coverage1]
            print('len(c)', len(c))
            print(len(c) / len(node_list3))
            d = [x for x in node_list4 if x in node_coverage2]
            print('len(c)', len(d))
            print(len(d) / len(node_list4))


            return   (A_ratio+B_ratio)/2

        else:
            print('成功匹配。')
            a = [x for x in node_list3 if x in node_coverage1]
            print('len(a)', a)
            print(len(a) / len(node_list3))
            b = [x for x in node_list4 if x in node_coverage2]
            print('len(b)', b)
            print(len(b) / len(node_list4))
            A_ratio = len(a) / len(node_list3)
            B_ratio = len(b) / len(node_list4)
            print('失败匹配')
            c = [x for x in node_list3 if x in node_coverage2]
            print('len(c)', len(c))
            print(len(c) / len(node_list3))
            d = [x for x in node_list4 if x in node_coverage1]
            print('len(c)', len(d))
            print(len(d) / len(node_list4))
            return (A_ratio + B_ratio) / 2
'''


'''
if __name__ == '__main__':
    test = Partion_graph()
    sum =0
    for i  in range(0,20):
        sum +=test.main()   #跑实验

    print('result',sum/20)
    print(sum/20)




