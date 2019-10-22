



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
    目标函数为两个点距离对方区域不同点的平均距离，两个平均距离越大越好。
   
    随机选择两点，使得
    '''
    def Partion_graph_K_center(self, G, true_source_list ,source_number_=2):
        #开始分区，输出每个区域的点和边。当前是两源的。

        sort_list = commons.partion_layer(G, 10)  #分层
        first_layer = [x for x in sort_list[0][1]]  #用第一层的节点。
        #先验证源点在不在第一层。
        b = set(true_source_list)
        print('源点在不在第一层呢？',b.issubset(first_layer))
        print('第一层节点个数',len(first_layer))
        subinfectG = commons.get_subGraph_true(G)  # 获取真实的传播图

        #判断是否连通看看。
        self.judge_connect(subinfectG)
        print('如果不连通，这个方法就会出问题，一定要是连连通的。')
        two_source = random.sample(first_layer, 2)  # 从list中随机获取2个元素，作为一个片断返回

        flag = 1
        lengthA_B = 10000
        good_two_result = []
        best_node_two_result = None

        averageA = 1
        averageB = 1
        for iter  in range(0,100):
            #对这两个点进行Djstra，计算所有点到他们的距离。
            print('two_source',two_source)
            lengthA_dict = nx.single_source_bellman_ford_path_length(subinfectG,two_source[0],weight='weight')
            lengthB_dict = nx.single_source_bellman_ford_path_length(subinfectG,two_source[1],weight='weight')
            #统计两者距离相等的点个数
            count =0
            for node,distance in lengthB_dict.items():
                if lengthA_dict[node] == lengthB_dict[node]:
                    count += 1
            print('两者距离相等的点个数为',count)
            #初始化两个集合，用来保存两个类别节点集合。
            node_twolist = [[], []]   #保存两个类别节点集合
            node_diff_twolist = [[],[]] #保存不同点
            count  =0
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
                    count += 1
            print('node_twolist1 ',len(node_twolist[1]))
            print('node_twolist2 ', len(node_twolist[0]))
            print('count是公共节点数目',count)
            #在两个list中找到中心位置，有几种中心性可以度量的。或者进行快速算法。
            #判断这次找的两个中心好不好。

            lengthA_sum = 0  #a这个不同点，
            lengthB_sum = 0
            for i in node_diff_twolist[0]:  #距离a近，第一个源点近的点。统计它跟第二个区域点的距离之和
                lengthA_sum += lengthB_dict[i]
            for j in node_diff_twolist[1]:  # 距离b近，第二个源点近的点。统计它跟第二个区域点的距离之和
                lengthB_sum += lengthA_dict[j]

            print('平均距离计算')
            average_lengthA = lengthB_sum/len(node_diff_twolist[0])
            average_lengthB = lengthA_sum /len(node_diff_twolist[1])

            sums = lengthA_sum + lengthB_sum
            print(lengthA_B)
            print('平均距离有增大就可以了。')
            if average_lengthA >averageA and average_lengthB >averageB:

               averageA = average_lengthA
               averageB =average_lengthB
               print('sums',sums)
                #是比原来好的的两个源。
               print('node_diff_twolist', len(node_diff_twolist[0]))
               print('node_diff_twolist', len(node_diff_twolist[1]))
               print('更行sums',sums)
               lengthA_B = sums
               good_two_result=two_source
               best_node_two_result = node_twolist

            else:
                #重新长生两个源吧。这里还是可以做优化的，选择的方向问题。
                two_source = random.sample(first_layer, 2)
                print('新生成两个源是',two_source)
        print('传播子图所有节点个数', len(list(subinfectG.nodes())))
        print('len(good_two_result[0]',len(best_node_two_result[0]))
        print('len(good_two_result[0]', len(best_node_two_result[1]))

        print('分开的两个区域的点的交集大小。')
        print('LEN',len([x for x in best_node_two_result[0] if x in best_node_two_result[1]]))
        print('good_two_result', good_two_result)
        print('short_length',nx.shortest_path_length(subinfectG,source=good_two_result[0],target=good_two_result[1]))
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
    3 找出高中介性节点，然后随机找两点，让这两点距离自己所属于的
区域距离之和最小。
    '''
    def delete_high_betweenness_centrality(self,infectG):
        subinfectG = commons.get_subGraph_true(infectG)
        sort_list= Partion_common.get_layer_node_between(subinfectG)
        #根据中介性分层然后删除。
        print('sort_list',sort_list)  #先验证高中介性节点是否在中间。
        # for every_node in sort_list:
        first_layer_between = [x[0] for x in sort_list[0]]  #取第一层节点
        two_source = random.sample(first_layer_between, 2)  # 从list中随机获取2个元素，作为一个片断返回

        lengthA_B = 100000
        good_two_result = []
        best_node_two_result = None
        for iter in range(0, 100):
            # 对这两个点进行Djstra，计算所有点到他们的距离。
            print('two_source', two_source)
            lengthA_dict = nx.single_source_bellman_ford_path_length(subinfectG, two_source[0], weight='weight')
            lengthB_dict = nx.single_source_bellman_ford_path_length(subinfectG, two_source[1], weight='weight')
            # 初始化两个集合，用来保存两个类别节点集合。
            node_twolist = [[], []]  # 保存两个类别节点集合
            node_diff_twolist = [[], []]  # 保存不同点
            for node in list(subinfectG.nodes):
                if lengthA_dict[node] > lengthB_dict[node]:  # 这个点离b近一些。
                    node_twolist[1].append(node)
                    node_diff_twolist[1].append(node)
                elif lengthA_dict[node] < lengthB_dict[node]:
                    node_twolist[0].append(node)
                    node_diff_twolist[0].append(node)
                else:
                    node_twolist[0].append(node)
                    node_twolist[1].append(node)
            print('node_twolist', len(node_twolist[1]))
            # 在两个list中找到中心位置，有几种中心性可以度量的。或者进行快速算法。
            # 判断这次找的两个中心好不好。

            lengthA_sum = 0  # a这个不同点，
            lengthB_sum = 0
            for i in node_diff_twolist[0]:  # 距离a近，第一个源点近的点。统计它跟自己区域点的距离之和
                lengthA_sum += lengthA_dict[i]
            for j in node_diff_twolist[1]:  # 距离b近，第二个源点近的点。统计它跟自己区域点的距离之和
                lengthB_sum += lengthB_dict[j]

            sums = lengthA_sum + lengthB_sum
            if sums < lengthA_B:
                print('sums', sums)
                # 是比原来好的的两个源。
                lengthA_B = sums
                good_two_result = two_source
                best_node_two_result = node_twolist
            else:
                # 重新长生两个源吧。这里还是可以做优化的，选择的方向问题。
                two_source = random.sample(first_layer_between, 2)

        print('good_two_result', good_two_result)
        print('good_node_two_result', best_node_two_result)

        return [[good_two_result[0],best_node_two_result[0]],[good_two_result[1],best_node_two_result[1]]]

    '''
       4  删除高中介性边，分批次删除。直到图不连通
       传入的还是原图，有感染和未感染点的。
       
       只有树上才有用。
       '''

    def delete_high_betweenness_edge_centrality(self, infectG):
        subinfectG = commons.get_subGraph_true(infectG)
        # 根据中介性分层然后删除。
        sort_list = Partion_common.get_layer_edge_between(subinfectG)
        print('sort_list',sort_list)

        commons_node_list = []
        one_subgraph = None
        two_subgraph = None
        for  edge,between  in sort_list:  #
                    print(edge,between)
                    subinfectG.remove_edge(edge[0],edge[1])
                    commons_node_list.append(edge[0])
                    commons_node_list.append(edge[1])
                    #重新计算一下那个中介
                    one_subgraph_nodelist,two_subgraph_nodelist = self.judge_two_subgraph(subinfectG)
                    print('one_subgraph',one_subgraph_nodelist)
                    if len(one_subgraph_nodelist) > 1:
                        print('true')
                        one_subgraph_nodelist,two_subgraph_nodelist = one_subgraph_nodelist,two_subgraph_nodelist
                        break
        commons_node_list_copy =copy.deepcopy(commons_node_list)
        print('commons_node_liost',commons_node_list.extend(one_subgraph_nodelist))
        commons_node_list.extend(one_subgraph_nodelist)
        commons_node_list_copy.extend(two_subgraph_nodelist)
        return [commons_node_list,commons_node_list_copy]

    '''
          5  每次选择剩下节点最高的中介数的边进行删除。
          直到出现两个子图。

          只有树上才有用。
          '''
    def delete_high_betweenness_edge_centrality_second(self, infectG):
        subinfectG = commons.get_subGraph_true(infectG)
        # 根据中介性分层然后删除。

        commons_node_list = []
        one_subgraph = None
        two_subgraph = None
        commons_node_list_copy =[ ]
        flag = 1
        while flag:
                sort_list = Partion_common.get_layer_edge_between(subinfectG)
                print('sort_list', sort_list)
                print('sort_list[0][0][0]',sort_list[0][0][0])
                subinfectG.remove_edge(sort_list[0][0][0], sort_list[0][0][1])
                commons_node_list.append(sort_list[0][0][0])
                commons_node_list.append(sort_list[0][0][1])
                # 重新计算一下那个中介
                one_subgraph_nodelist, two_subgraph_nodelist = self.judge_two_subgraph2(subinfectG)
                print('one_subgraph', one_subgraph_nodelist)
                if one_subgraph_nodelist and two_subgraph_nodelist:
                    one_subgraph_nodelist, two_subgraph_nodelist = one_subgraph_nodelist, two_subgraph_nodelist
                    commons_node_list_copy = copy.deepcopy(commons_node_list)
                    # print('commons_node_liost', commons_node_list.extend(one_subgraph_nodelist))
                    commons_node_list.extend(one_subgraph_nodelist)
                    commons_node_list_copy.extend(two_subgraph_nodelist)
                    break

        return [commons_node_list, commons_node_list_copy]

    def  judge_two_subgraph(self,subinfecG):
        mutiple_graph = sorted(nx.connected_component_subgraphs(subinfecG), key=len, reverse=True)
        # print('mutiple_graph',mutiple_graph[0])
        print(len(mutiple_graph))
        if len(mutiple_graph) >= 2:
            print('mutiple1', mutiple_graph[0].number_of_nodes())
            print('mutiple2', mutiple_graph[1].number_of_nodes())
            print('list', list(mutiple_graph[0].nodes()))
            if mutiple_graph[0].number_of_nodes() - mutiple_graph[1].number_of_nodes() <200:
                print('---------------')
                print(list(mutiple_graph[0].nodes()), list(mutiple_graph[1].nodes()))
                return list(mutiple_graph[0].nodes()), list(mutiple_graph[1].nodes())

            else:
                return  [1],[2]
        else:
            return [1],[2]


    '''
          6  层次聚类，
          两个点具有较高相似性体现在两个点的覆盖率很高，还很近。就把他们归为一类，
 对于高中介性点，直接当成中间点，剩下的就按照这种方法分开。可以做的
           6.1 选择一个相似度测度计算所有定点对的相似性
           6.2 每个顶点自成一组，
           6.3 找到相似性最大的两个群组，合并
           6.4 用单一连接，完全连接，平均连接聚类之一，计算合并后的群组和其他群组
           之间相似性
           6.5 重复3，4.直到只有两个群组。
          '''

















    '''
              7标签传播的方法
              7.1 每个节点初始化两个标签，因为是2源
              7.2 不断迭代，直到两个节点的标签属于度比较大。
              
            #注意传入的就是一个感染图，只有感染节点。
              '''

    def  label_progration_community(self, G,label_number =2):
        #初始化给每个结点加一个就好了啊。
        #每个节点的标签就是一个list把。[[1,1/2],[2,2/3]]
        for node in list(G.nodes):
            G.add_node(node, labels=[[node, 1], [node,1]])
        for iter in range(0,10):
            for node in list(G.nodes):
                #用两个字典。一个字典是某元素出现次数，一个是该标签
                #隶属度
                temp_dict_number  = defaultdict(int )
                temp_dict = defaultdict(int )
                # print('G.neighbors(node',list(G.neighbors(node)))
                for neight in list(G.neighbors(node)):
                    for label,belong_value  in G.node[neight]['labels']:
                        temp_dict_number[label] +=1
                        temp_dict[label] += belong_value
                #取平均值。
                # for label,number in temp_dict_number.items():
                #     temp_dict[label] = temp_dict[label]
                # print('temp_dict',temp_dict)

                #排序，
                temp_list = sorted(temp_dict.items(), key=lambda  x:x[1], reverse=True)
                # print('temp_list', temp_list)
                lens= len( G.node[node]['labels'])
                #将前两项给给这个节点标签。
                if lens >1 and len(temp_list) >1:
                    G.node[node]['labels']=[temp_list[0],temp_list[1]]
                else:
                    G.node[node]['labels'][1] = temp_list[0]

            #终止条件是？两个社区数量变化不大。


        for node in list(G.nodes):
            print(G.node[node]['labels'])
        pass

    '''
                 8马尔科夫链过程。
                  '''

    def Markov_Chain(self, G, label_number=2):


       pass









    '''
    只判断是否有两个子图的函数。有就返回
    
    '''
    def  judge_two_subgraph2(self,subinfecG):
        mutiple_graph = sorted(nx.connected_component_subgraphs(subinfecG), key=len, reverse=True)
        # print('mutiple_graph',mutiple_graph[0])
        print(len(mutiple_graph))

        if len(mutiple_graph) == 2:
            print('出现两个子图了')
            print('mutiple1', mutiple_graph[0].number_of_nodes())
            print('mutiple2', mutiple_graph[1].number_of_nodes())
            print('list', list(mutiple_graph[0].nodes()))
            return list(mutiple_graph[0].nodes()), list(mutiple_graph[1].nodes())
        else:
            return False,False








    '''
    1
    
    
    '''



    '''
    用来验证两个node_list之间的对不对。取比较大的那个。
    
    '''
    def verification(self,node_list,true_list):
        #用真实的例子中的每个分区的list和边的list。进行比较就好了啊。


        a1=len([x for x in node_list[0] if x in true_list[0]])/len(true_list[0])
        b1 = len([x for x in node_list[1] if x in true_list[1]]) / len(true_list[1])
        a2 = len([x for x in node_list[0] if x in true_list[1]]) / len(true_list[1])
        b2 = len([x for x in node_list[1] if x in true_list[0]]) / len(true_list[0])
        if a1+b1 > a2+b2:
            print('输出看看',(a1+b1)/2)
            return (a1+b1)/2
        else:
            print('输出看看', (a2 + b2) / 2)
            return (a2 + b2) / 2


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
        # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
        # initG = commons.get_networkByFile('../../data/4_regular_tree_3000_data.txt')
        # initG = commons.get_networkByFile('../../../data/4_regular_graph_3000_data.txt')

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
        print('common_node_list',len(node_list5))



        subinfectG = commons.get_subGraph_true(infectG_other) #只取感染点，为2表示,真实的感染图。
        #然后将感染点之间所有边都相连接起来。
        #第一种方法。

        '''
        应该在这个地方进行传播分区的各种实验，先做好2源的分区。
        '''
        twosource_node_list =self.Partion_graph_K_center(infectG_other,source_list,2)
        #进行覆盖率走，并进行jaya算法。
        # twosource_node_list=self.jaya_add_coverage(infectG_other)
        #进行删除边操作。
        # twosource_node_list = self.delete_high_betweenness_edge_centrality_second(infectG_other)
        # print(twosource_node_list)
        # return self.verification(twosource_node_list, [node_list3, node_list4])


        #
        # # 第7种方法。
        #
        # twosource_node_list = self.label_progration_community(subinfectG)
        # print(twosource_node_list)
        # return self.verification(twosource_node_list,[node_list3,node_list4])
        #
        # # #第四种，进行判断高中介性点为中间点。判断比例
        # # twosource_node_list= self.delete_high_betweenness_centrality(infectG_other)
        # #
        #

        print('真实的情况第一个社区first——node_list3', len(node_list3))
        print('真实的情况第一个社区second——node_list4', len(node_list4))
        print('common_node_list', len(node_list5))
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
import  time
if __name__ == '__main__':
    test = Partion_graph()
    sum =0
    for i  in range(0,2):
        tempresult =test.main()
        sum += tempresult #跑实验
        with open('result_samplePath.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果'+str(tempresult) + '\n')
    print('result',sum/20)
    print(sum/20)




