import random
import math
import networkx  as nx
from collections import defaultdict
import commons
from jordan_center import jordan_centrality
import rumor_centrality_graph_main
import numpy as np
import  copy

class Single_source_using_Part:
    def __init__(self):
        pass
    '''
    1 只适用于我们的传播过程。
    需要知道的是每个点的第一次传播时间
    

    '''

    def propagation_time(G, SourceList, number=1):

        y_list = []
        G_temp = nx.Graph()
        G_temp = copy.deepcopy(G)
        '''
        :param G:
        :param SourceList:
        :return:
        '''
        queue = set()
        for source in SourceList:
            G_temp.node[source]['SI'] = 2
            queue.add(source)
        # progation_number = 0

        true_T = 1
        while 1:
            propagation_layer_list = []  # 传播的BFS某一层
            # print('queue',queue)
            propagation_layer_list.extend(list(queue))  # 总是删除第一个。这里不删除
            # print('第几层为'+str(len(propagation_layer_list)))
            for source in propagation_layer_list:
                for height in list(G_temp.neighbors(source)):
                    randnum = random.random()
                    if randnum < 0.3:
                        G_temp.node[height]['SI'] = 2
                        G_temp.add_edge(source, height, isInfect=1)
                        # 如果被传播，那就将邻接节点放入队列中。
                        if G_temp.node[height]['Time']== 1:
                            G_temp.node[height]['Time'] = true_T
                        queue.add(height)
            propagation_layer_list.clear()
            # queue_set = list(set(queue))
            count = 0
            for nodetemp in list(G.nodes):
                if G_temp.node[nodetemp]['SI'] == 2:
                    count = count + 1
            y_list.append(count)
            # print('被感染点为' + str(count) + '个')
            # progation_number += 1
            true_T += 1
            if count / G_temp.number_of_nodes() > 0.6:
                print('超过50%节点了，不用传播啦')
                break
            # if count >200:
            #     break
        # 数据进去图，看看

        return G_temp, true_T


    '''
   复现论文Estimating Infection Sources in Networks Using Partial Timestamps
    思路：   
        从0.1 到1，依次迭代，直到找到最好的参数。
        
        大致过程参考论文吧
        
        
        1  假设有n个感染点，那我们的矩阵
        就是n-1维度，从每个点开始，把其他的感染点构成n-1维度矩阵。构建两个Gromov 矩阵。
        2   
    注意： 只有infectG参数有时间标签。
    
    
    
    
    '''



    def  using_Partial_timestamps(self,infectG,subinfectG,true_soruce):

        randomnode = random.choice(list(subinfectG.nodes()))
        #构建矩阵。给我们的subinfectG中每个点重新绘制点。用一个键值对描述其对应关系，从0开始
        subinfetG_node= dict()
        index =0
        for i  in range(0,subinfectG.num):
            pass





        pass











    '''
      设计本类用来做单源  定位。
    # '''

    def main(self, filename):

        # #拿到图
        initG = commons.get_networkByFile(filename)

        # ecc=nx.eccentricity(initG)
        # sort_ecc=sorted(ecc.items(),key=lambda  x:x[1])
        # product_srouce =sort_ecc[0][0]
        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG, T = self.propagation_time(max_sub_graph, [1000],1)
        # infectG1, T = commons.propagation1(max_sub_graph, [source_list])
        subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。
        # 将在这里进行单源测试。
        print(sorted(list(subinfectG.nodes())))
        #
        # result_node = self.revsitionAlgorithm_singlueSource(subinfectG)
        # ''' 第二种，就是coverage/distance'''
        # result_node= self.single_source_bydistance_coverage(infectG,subinfectG,source_list[0])
        # '''  第3种，距离中心'''
        # result_node = self.single_source_bydistance( subinfectG)

        # '''  第6种，质量距离中心'''
        # result_node = self.single_source_byQuality_centrality(infectG,subinfectG)

        # #''''第7种，特征向量中心性
        # result_node = self.single_source_bybetweenness_centrality( subinfectG)
        # #''''第8种，反转加t性
        # result_node = self.single_source_get_T_jarden_center( T,subinfectG)

        # 第9种，谣言中心性‘’

        result_node = self.rumor_center(infectG, subinfectG, 1000)

        #
        # # #’‘ 乔丹中心性
        #   result_node = self.jarden_cente_networkx(infectG,subinfectG,source_list[0])

        # 覆盖率加我们的操作
        # result_node = self.coverage_BFS_single_source(infectG,subinfectG,source_list[0])

        # #多个观察点
        # result_node = self.coverage_BFS_single_source(infectG,subinfectG,source_list[0])

        # 基于覆盖率的计算方式

        # result_node = self.belief_algorithm(infectG, subinfectG,1000)
        print('真实源是', source_list[0])
        # print('预测源是',result_node[0])
        distance = nx.shortest_path_length(subinfectG, source=1000, target=result_node[0])
        print('结果他们的距离是', distance)
        return distance


import time

if __name__ == '__main__':
    test = Single_source_using_Part()
    sum = 0
    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')
    # initG = commons.get_networkByFile(filename)
    # filname = '../../../data/4_regular_graph_3000_data.txt'
    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')
    filname = '../../../data/CA-GrQc.txt'
    # filname = '../../../data/4regular_tree9.txt'
    # filname = '../../../data/random_tree_10000.txt'
    # filname = '../../../data/5regular_tree_10000.txt'

    # method ='distan+ covage'
    # method = 'jardan_center'
    # method ='distance'
    method = '谣言中心性'
    for i in range(0, 20):
        tempresult = test.main(filname)
        sum += tempresult  # 跑实验
        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果是   ' + str(tempresult) + '      数据集' + '方法' + str(method) + str(filname) + '\n')
    with open('result.txt', "a") as f:
        f.write('数据集' + str(filname) + '方法' + str(method) + '总结果   ' + str(sum / 20) + '\n')
        f.write('\n')
    print('result', sum / 20)
    print(sum / 20)




