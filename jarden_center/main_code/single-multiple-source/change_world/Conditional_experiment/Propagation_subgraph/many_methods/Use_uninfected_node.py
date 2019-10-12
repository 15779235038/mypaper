
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

# sys.path.append('mypaper/mypaper/jarden_center/main_code/single-multiple-source/eccitsy922/commons.py')
# print(sys.path)
import commons

import copy

import time

from  collections import  defaultdict
class Satisfaction:
    def __init__(self):
        pass

    #抽取子图的第一种方法
    '''
        首先给所有节点按照它邻接节点的被感染率排序。从邻居节点被感染率大的集合开始，
     分层往下走，如果第一层的节点直接跟第二层的节点都有边相连。就连接起来。一层一层来。
    '''



    def take_subgraph(self,infectG):
        G_temp = nx.Graph()
        subGraph = nx.Graph()
        G_temp = copy.deepcopy(infectG)
        # 获取我们所有的图。
        #拿到所有的感染点,并且统计他们感染率。
        node_scale =[]
        infect_listNode = []
        for  nodes in list(G_temp.nodes):
            if G_temp.node[nodes]['SI'] == 2:
                    neighbor_list =list(G_temp.neighbors(nodes))
                    count = len([x for x in neighbor_list if G_temp.node[x]['SI']==2])
                    neighbor_list_len = len(neighbor_list)
                    node_scale.append([nodes, count / neighbor_list_len])
        #先做个简单分类。按照从大到小排序.分10档次吧。 #真的可以考虑时间，来分档次。
        sort_dict = defaultdict(list)
        for  node_and_scale in node_scale:
            Ten_digits =  node_and_scale[1] *100 //10
            sort_dict[Ten_digits].append(node_and_scale[0])
        print(sort_dict)
        sort_list = sorted(sort_dict.items(), key= lambda x:x[0], reverse=True )
        print(sort_list)
        #将每两层之间节点进行连接就好。
        for index in range(len(sort_list)-1 ):
            for first_node in sort_list[index][1]:
                for second_node in sort_list[index+1][1]:
                    if  G_temp.has_edge(first_node,second_node)  :
                        subGraph.add_edge(first_node,second_node)


        print('node_subGraph', subGraph.number_of_nodes())
        print('edge_subGraph',subGraph.number_of_edges())
        #判断是否是连通图,
        '''
        1 为什么一般图总有一个巨分支？
        2 而在3-regular树却有非常多的分支，多达66.我们的算法也许需要在同层之间也要加上边了。  
        '''

        judge_data= self.judge_data(subGraph)

        return subGraph










    #本函数用来衡量，是否能够将传播结构很好的反应出来。如何验证呢?
    '''
    分别从下面几个方面验证。
     1 节点数目和边的数目对照
     2 结构显示。
    '''

    def verification(self,infectG,subinfecG):

        '''
        1 第一个节点数目的比较。
        2  第二个就是画图进行比较。
        '''
        print('len(infectG and SI ==2)', len([x for x in list(infectG.nodes) if infectG.node[x]['SI'] ==2]))

        print('len(inifecG edge)',len([x for x in list(infectG.edges) if infectG.edges[x[0], x[1]]['isInfect'] == 1 ]))

        print('len(subinfecG)', subinfecG.number_of_nodes())
        print('edge_subGraph', subinfecG.number_of_edges())





        '''
        1  先将原有的传播形式画出来，后将我们的图画出来。
        '''


        












        # pass


    '''
    1 对数据集进行判断。从有几个连通子图，每个数目。返回连通子图个数。
    '''
    def judge_data(self,initG):
        '''
        :param initG:
        :return:  #返回最大子图的源点数据集
        '''
        Gc = nx.Graph()
        Gc = max(nx.connected_component_subgraphs(initG), key=len)
        sum = 0
        count = 0
        for sub_graph in sorted(nx.connected_component_subgraphs(initG), key=len, reverse=True):
            # print(type(sub_graph))
            # print(sub_graph.number_of_nodes())
            sum += sub_graph.number_of_nodes()
            count += 1
        print('count', count)
        print('sum', sum)


        # return Gc




    '''
    1 获得传播子图后，你的评价标准是是什么？
    当然是和真实的数据进行比对
    
    '''
    def main(self):
        initG = commons.get_networkByFile('../../../data/3_regular_tree_2000_data.txt')
        # initG = commons.get_networkByFile('../../../data/treenetwork3000.txt')

        # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')

        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)

        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('查看两源距离')
        # print('distance',nx.shortest_path_length(max_sub_graph,source=source_list[0],target=source_list[1]))
        infectG = commons.propagation1(max_sub_graph, source_list)
        subinfectG = self.take_subgraph(infectG)
        self.verification(infectG,subinfectG)












    def plot(self, x_list, y_list, ):
        plt.figure()
        plt.plot(x_list, y_list)
        plt.title('Multiple central measures')
        plt.savefig('first' + ".png")
        # plt.show()
        plt.close()

    '''

    跑50次，看下方差平均差。评判那种中心性好
    '''

    def practice(self):
        distance_all = 0
        for i in range(30):
            temp = self.main()
            distance_all += temp
        with open('result_samplePath.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('总结果'+str(distance_all/30) + '\n')
        return distance_all
        # self.plot(x_list, y_list)
        # print(result)

'''


'''
if __name__ == '__main__':
    test = Satisfaction()

    test.practice()   #跑实验




