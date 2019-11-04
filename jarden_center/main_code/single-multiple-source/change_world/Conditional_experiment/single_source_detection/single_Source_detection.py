
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

    def  single_source_bydistance_coverage(self,infectG,subinfectG,true_source):
        sort_dict = commons.partion_layer_dict(infectG, 10)  # 分层
        print('sort_list', sort_dict)
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode,ditance in length_dict.items():
                lens_degree = len(list(nx.neighbors(infectG,othernode)))
                node_import += sort_dict[othernode]*lens_degree / (ditance+1)
            node_cal.append([node,node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1], reverse=True)

        print(sort_list)
        # print('在的',[x[0] for x  in sort_list[:200] if x[0] ==true_source])
        return  sort_list[0]










    #种子节点的看看都在那里
    def single_source_bydistance_coverage_SECOND(self, infectG, subinfectG, true_source):
        sort_dict = commons.partion_layer_dict(infectG, 10)  # 分层
        print('sort_list', sort_dict)
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode, ditance in length_dict.items():
                lens_degree = len(list(nx.neighbors(infectG, othernode)))
                node_import += sort_dict[othernode] * lens_degree / (ditance + 1)
            node_cal.append([node, node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1], reverse=True)
        print(sort_list)
        print('在的', [x[0] for x in sort_list[:200] if x[0] == true_source])
        return sort_list[0]

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
    第5种单源定位方法，
    利用边界点做一个k-core想法。
    '''

    def effectDistance(self, probily):
        return 1 - math.log(probily)

    '''
    
    第6种方法，就是利用2018年的那篇。
    Classifying Quality Centrality for Source
    
    1 找出原始图最大子图，然后找出所有感染点为M+，所有非感染点为M-。
    2 遍历每个点，计算每个点跟它们的距离。再计算平均值。
    '''
    def  single_source_byQuality_centrality(self,infectG,subinfectG):
        #你好，再见
        for edge in infectG.edges:
            # G.add_edge(edge[0], edge[1], weight=1)
            randomnum = random.random()
            infectG.add_edge(edge[0], edge[1], weight=self.effectDistance(randomnum))
        m_list_add = [x for x in list(infectG.nodes()) if infectG.node[x]['SI']== 2]
        m_list_dif = [x for x in list(infectG.nodes()) if infectG.node[x]['SI'] == 1]
        print('len(m_list_dif',len(m_list_add))
        print(subinfectG.number_of_nodes())
        len_add= len(m_list_add)
        len_dif = len(m_list_dif)
        CQ_dict = defaultdict(int)
        for node_temp in m_list_add:
            length_dict = nx.single_source_bellman_ford_path_length(infectG,source=node_temp,weight='weight')
            d_add_all = 0
            d_dif_all = 0
            d_dif_avg = 0
            d_add_avg = 0
            for add in m_list_add:
                d_dif_all += length_dict[add]
            for dif in m_list_dif:
                d_add_all += length_dict[dif]

            d_dif_avg = d_dif_all/len_dif
            d_add_avg = d_add_all/len_add
            CQ_dict[node_temp] = (d_dif_avg -d_add_avg)/d_add_avg

        CQ_dict_sort = sorted(CQ_dict.items(), key=lambda x: x[1],reverse=True)
        print('CQ_dict_sort', CQ_dict_sort)
        return CQ_dict_sort[0]
        # pass








    #几种中心性的性质都试一试吧。hhhh
    def single_source_bybetweenness_centrality(self,subinfectG):
        # 介数中心性
        between_dict = nx.betweenness_centrality(subinfectG)
        sort_eccentricity_dict = sorted(between_dict.items(), key=lambda x: x[1], reverse=True)
        print('sort_eccenritci_dict', sort_eccentricity_dict)



        # #特征向量中心性。
        # centrality = nx.eigenvector_centrality(subinfectG)
        # sort_eigener_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        # print('eigenvector_centrality', sort_eigener_centrality)
        # # self.center = sort_eigener_centrality[0][0]

        import math
        # Kaza中心性
        # G = nx.path_graph(4)
        # maxnumber = max(nx.adjacency_spectrum(subinfectG))
        # print(maxnumber)
        # phi = (1 + math.sqrt(5)) / 2.0  # largest eigenvalue of adj matrix
        # centrality = nx.katz_centrality(subinfectG, 1/ maxnumber -0.01)
        # katz_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        # print('katz_centrality',katz_centrality)

        # center_list = []
        # center_list.append(sort_eccentricity_dict[0][0])
        # center_list.append(sort_colse_centrality_dict[0][0])
        # center_list.append(sort_degree_centrality[0][0])
        # center_list.append(sort_eigener_centrality[0][0])
        # center_list.append(katz_centrality[0][0])

        # return center_list
        return sort_eccentricity_dict[0]

    #接近度中心性
    def  single_source_bycloseness_centrality(self,subinfectG):

        #   接近度中心性
        closeness_centrality = nx.closeness_centrality(subinfectG)
        sort_colse_centrality_dict = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
        print('sort_colse_centrality_dict', sort_colse_centrality_dict)

        return sort_colse_centrality_dict[0]

    #degree_centrali
    def  single_source_bydegree_centrality(self,subinfectG):

        #   度中心性，这个效果最好，简直了。
        degree_centrality = nx.degree_centrality(subinfectG)
        sort_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        print('sort_degree_centrality', sort_degree_centrality)

        return sort_degree_centrality[0]

    #特征向量中心性
    def single_source_byeigenvector_centrality(self, subinfectG):

        #特征向量中心性。
        centrality = nx.eigenvector_centrality(subinfectG,max_iter=1000)
        sort_eigener_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        print('eigenvector_centrality', sort_eigener_centrality)
        # self.center = sort_eigener_centrality[0][0]
        return sort_eigener_centrality[0]



    '''
    1  知道自己的传播时间t，判断jarden center是否可以加上时间t来做。
        
    
    
    
    '''

    def  single_source_get_T_jarden_center(self,t,subinfectG):





        pass
















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
        infectG,T = commons.propagation1(max_sub_graph,source_list)

        subinfectG = commons.get_subGraph_true( infectG)  # 只取感染点，为2表示,真实的感染图。
        #将在这里进行单源测试。
        '''   第一种，就是jarden center '''
        #
        # result_node = self.revsitionAlgorithm_singlueSource(subinfectG)
        # ''' 第二种，就是coverage/distance'''
        # result_node= self.single_source_bydistance_coverage(infectG,subinfectG,source_list[0])
        # '''  第3种，距离中心'''
        # result_node = self.single_source_bydistance( subinfectG)

        #'''  第6种，质量距离中心'''
        # result_node = self.single_source_byQuality_centrality(infectG,subinfectG)


        # #''''第7种，特征向量中心性
        # result_node = self.single_source_bybetweenness_centrality( subinfectG)
        # #''''第8种，反转加t性
        result_node = self.single_source_get_T_jarden_center( T,subinfectG)

        print('真实源是',source_list[0])
        print('预测源是',result_node[0])
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
    # filname = '../../../data/4_regular_graph_3000_data.txt'
    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')
    filname = '../../../data/CA-GrQc.txt'
    # filname = '../../../data/3regular_tree9.txt'
    # method ='distan+ covage'
    # method = 'jardan_center'
    # method ='distance'
    method = '中介中心性'




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




