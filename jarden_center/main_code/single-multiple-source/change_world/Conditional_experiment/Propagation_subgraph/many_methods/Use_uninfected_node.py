
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

    import copy

    '''
    用队列重写SI传播过程，propagation会传播并且还会

    传播方案2：从源点开始往外面传播，按照队列传播形式。每一个时间刻度，每次所有感染的点都试图感染身边的点。而不是一层一层来
    '''

    def propagation1(self,G, SourceList, number=1):


        #正常的感染图是？
        zhengchang_G = nx.Graph()

        progration_node_list =[ ]
        progration_edge_list = [ ]
        G_temp = nx.Graph()
        G_temp = copy.deepcopy(G)
        queue = set() #每个t向外传播的点
        layers = set()    #每层新感染点
        for source in SourceList:
            G.node[source]['SI'] = 2
            queue.add(source)
            # layers.add(source)
            # progation_number = 0
        progration_node_list.append([source])
        propagation_sum_edge_set  = set()
        propagation_layer_edge_set = set()
        while 1:
            layers.clear()
            propagation_layer_list = []  # 传播的BFS某一层
            #传播的边某一层
            propagation_layer_list.extend(list(queue))  # 总是删除第一个。这里不删除
            propagation_sum_edge_set = propagation_sum_edge_set.union(propagation_layer_edge_set)  #并集
            propagation_layer_edge_set.clear()
            queue_temp = copy.deepcopy(queue)
            print('第几层为' + str(len(propagation_layer_list)))
            for source in propagation_layer_list:
                for height in list(G_temp.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.5:
                        G_temp.node[height]['SI'] = 2
                        G_temp.add_edge(source, height, isInfect=1)
                        # 如果被传播，那就将邻接节点放入队列中。
                        propagation_layer_edge_set.add((source, height))
                        queue.add(height)
                        layers.add(height)

                        zhengchang_G.add_edge(source, height)
            # print(queue)
            # print(layers)
            layers.difference_update(queue_temp)  #移除layers中扎起queue_temp中元素
            #对这一层的layers进行只能新加的点和边
            propagation_layer_edge_set.difference_update(propagation_sum_edge_set)
            progration_node_list.append(list(layers))   #这一层所加的节点，要保证每一层节点不一样。只
            #记录第一次被感染的时间t
            progration_edge_list.append(list(propagation_layer_edge_set))
            propagation_layer_list.clear()
            # queue_set = list(set(queue))
            count = 0
            for nodetemp in list(G.nodes):
                if G_temp.node[nodetemp]['SI'] == 2:
                    count = count + 1
            print('被感染点为' + str(count) + '个')
            # progation_number += 1
            if count / G_temp.number_of_nodes() > 0.4:
                print('超过50%节点了，不用传播啦')
                break
        # 数据进去图，看看

        print('progration_node_list',progration_node_list)
        print('progration_dege_lsit',progration_edge_list)
        return G_temp,progration_node_list,progration_edge_list,zhengchang_G












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
            Ten_digits =  node_and_scale[1] *100 // 10
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

        #
        #
        # #每一层的节点也相互连接把。
        # for  single_layer_node_list in sort_list:
        #      for i  in single_layer_node_list[1]:
        #          for j in  [x for  x in single_layer_node_list[1] if x != i]:
        #              # print('i,j',i)
        #              if G_temp.has_edge(i, j):
        #                  subGraph.add_edge(i, j)

        print('node_subGraph', subGraph.number_of_nodes())
        print('edge_subGraph',subGraph.number_of_edges())
        #判断是否是连通图,
        '''
        1 为什么一般图总有一个巨分支？
        2 而在3-regular树却有非常多的分支，多达66.我们的算法也许需要在同层之间也要加上边了。  
        '''

        max_subGraph= self.judge_data(subGraph)

        return max_subGraph







    #抽取子图的第2种方法
    '''
        首先给所有节点按照它邻接节点的被感染率排序。从邻居节点被感染率大的集合开始，
     分层往下走，只让倒数几层节点断，其他不断。
    '''
    def take_subgraph_last(self,infectG):
        # 构建传播子图，
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
        print('这个传播子图的节点个数,也是我们用来做u的备选集合的' + str(len(set(tempGraphNodelist))))
        print('这个感染区域的传播图节点个数')
        # eccentricity_dict = nx.eccentricity(tempGraph)

        # return tempGraph  # 临时图生成
        #划分图区域，进行删除计划。
        G_temp = nx.Graph()
        G_temp = copy.deepcopy(tempGraph)
        # 获取我们所有的图。
        # 拿到所有的感染点,并且统计他们感染率。
        node_scale = []
        infect_listNode = []
        for nodes in list(G_temp.nodes):
             # if infectG.node[nodes]['SI'] == 2:
                neighbor_list = list(infectG.neighbors(nodes))
                count = len([x for x in neighbor_list if infectG.node[x]['SI'] == 2])
                neighbor_list_len = len(neighbor_list)
                node_scale.append([nodes, count / neighbor_list_len])
        # 先做个简单分类。按照从大到小排序.分10档次吧。 #真的可以考虑时间，来分档次。
        sort_dict = defaultdict(list)
        for node_and_scale in node_scale:
            Ten_digits = node_and_scale[1] * 100 // 10 // 2
            sort_dict[Ten_digits].append(node_and_scale[0])
        print(sort_dict)
        sort_list = sorted(sort_dict.items(), key=lambda x: x[0], reverse=True)
        print(sort_list)



        #删除最后一些点。

        for index in range(1 ,len(sort_list)):
            print('sort_list[index][1',sort_list[index][1])
            G_temp.remove_nodes_from(sort_list[index][1])

        subGraph = copy.deepcopy(G_temp)

        print('node_subGraph', subGraph.number_of_nodes())
        print('edge_subGraph',subGraph.number_of_edges())
        #判断是否是连通图,






        #第二种抽取方案。





        max_subGraph= self.judge_data(subGraph)

        return max_subGraph










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
        # print('len(infectG and SI ==2)', len([x for x in list(infectG.nodes) if infectG.node[x]['SI'] ==2]))
        #
        # print('len(inifecG edge)',len([x for x in list(infectG.edges) if infectG.edges[x[0], x[1]]['isInfect'] == 1 ]))
        #
        # print('len(subinfecG)', subinfecG.number_of_nodes())
        # print('edge_subGraph', subinfecG.number_of_edges())

        # 将edge_list中的图画出来，
        # 这是真实的传播情况，我们可能需要将颜色以及传播时间加入。

        G = nx.Graph()
        result = []
        with open('edge_list.txt', 'r') as f:
            for line in f:
                l = line.replace('[', '').replace(']', '').replace(',', '').replace('(', '').replace(')', '')

                ll = l.split()
                n = []
                for i in ll:
                    j = int(i)
                    n.append(j)
                # print(n)
                for i in range(0, len(n), 2):
                    s1 = n[i]
                    s2 = n[i + 1]
                    G.add_edge(s1, s2)
        nx.draw(G, node_size=2, edge_color='r')
        # plt.show()




        '''
        1  抽取子图拿出来。形成传播子图看看
        '''

        #获取传播序列，再把抽取子图拿出来。看看效果。
        nx.draw(subinfecG, node_size=2, edge_color='r')
        # plt.show()


        #验证抽取子图是否好，因为我们是不断抽取边，但是

        #先试试这个传播图的中心性看看。









    '''
    画图
    
    '''
    def draw_picture(self,G,filename):
        nx.draw(G, node_size=2, edge_color='r')
        plt.savefig(filename+".png")
        plt.close()












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
        # sum = 0
        # count = 0
        # for sub_graph in sorted(nx.connected_component_subgraphs(initG), key=len, reverse=True):
        #     # print(type(sub_graph))
        #     # print(sub_graph.number_of_nodes())
        #     sum += sub_graph.number_of_nodes()
        #     count += 1
        # print('count', count)
        # print('sum', sum)
        return Gc




    '''
    1 获得传播子图后，你的评价标准是是什么？
    当然是和真实的数据进行比对
    '''
    def main(self):
        # initG = commons.get_networkByFile('../../../data/3_regular_tree_2000_data.txt')
        # initG = commons.get_networkByFile('../../../data/4_regular_tree_2000_data.txt')
        # initG = commons.get_networkByFile('../../../data/4_regular_graph_3000_data.txt')

        # initG = commons.get_networkByFile('../../../data/treenetwork3000.txt')

        initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')

        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)

        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('查看两源距离')
        # print('distance',nx.shortest_path_length(max_sub_graph,source=source_list[0],target=source_list[1]))
        infectG, node_list, edge_list,zhengchang_G = self.propagation1(max_sub_graph, source_list)

        with open('node_list.txt', 'w') as f:
            for i in node_list:
                f.write(str(i) + '\n')
        with open('edge_list.txt', 'w') as f:
            for i in edge_list:
                f.write(str(i) + '\n')
        #这是我们抽取的子图。
        subinfectG = self.take_subgraph_last(infectG)
        # self.verification(infectG, subinfectG)


        #我们抽取子图
        center_list = commons.revsitionAlgorithm_singlueSource(subinfectG)

        #实验一般的用的图。

        tmep_graph = commons.get_subGraph(infectG)
        center_list2 = commons.revsitionAlgorithm_singlueSource(tmep_graph)

        #真实感染图
        center_list1 = commons.revsitionAlgorithm_singlueSource(zhengchang_G)



        #将3个图都画出来。并保存
        self.draw_picture(subinfectG, 'chouqu')
        self.draw_picture(tmep_graph,'common')
        self.draw_picture(zhengchang_G , 'true')





        print('我们抽取子图边数目', subinfectG.number_of_edges())
        print('一般实验图边数目', tmep_graph.number_of_edges())
        print('一般实验图点数目',tmep_graph.number_of_nodes())
        print('真实感染图边数目',zhengchang_G.number_of_edges())
        print('真实感染图    点数目', zhengchang_G.number_of_nodes())

        for center  in center_list:
            print('distan抽取子图',nx.shortest_path_length(max_sub_graph,source=center,target=source_list[0]))
        for center1  in center_list1:
            print('distance真实感染图',nx.shortest_path_length(max_sub_graph,source=center1,target=source_list[0]))

        for center2 in center_list2:
            print('distance一般实验用图', nx.shortest_path_length(max_sub_graph, source=center2, target=source_list[0]))














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




