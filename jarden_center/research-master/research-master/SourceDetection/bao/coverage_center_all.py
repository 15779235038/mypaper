# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import math
from decimal import *


import method


from time import clock
import log
import logging
import networkx as nx
import data

from experiment import Experiment


class CoverageCenter(method.Method):
    """
        detect the source with Rumor Centrality.
        Please refer to the following paper for more details.
        Shah D, Zaman T. Detecting sources of computer viruses in networks: theory and experiment[J].
        ACM SIGMETRICS Performance Evaluation Review, 2010, 38(1): 203-214.
    """

    visited = set()  # node set
    bfs_tree = nx.Graph()


    '''   
    1 加二阶邻域覆盖率，给每个点加一个覆盖率就是覆盖率参数。
    2 

    '''
    def detect(self):
        """detect the source with Rumor Centrality.
        Returns:
            @rtype:int
            the detected source
        """
        if self.subgraph.number_of_nodes() == 0:
            print 'subgraph.number_of_nodes =0'
            return

        self.reset_centrality()
        centrality = {}

        # 进行所有点有向树构建，再进行层次遍历。针对每一层都进行传播点/全部的比例计算。
        node_every_ratio = []
        temp_nodes = self.subgraph.nodes()
        # print('temp_nodes')
        # print(temp_nodes)
        for source in self.subgraph.nodes():
            # print('从什么开始')
            # print(source)
            # 进行BFS树构造，
            tree = nx.bfs_tree(self.data.graph, source=source)
            # 进行层次遍历。返回每一层顶点。
            BFS_nodes = self.BFS_nodes(tree, source, self.data.graph,self.subgraph)
            # print(BFS_nodes)
            ratio_all = 0
            for layer_node in BFS_nodes:
                # print('layter_ndes')
                # print(layer_node)
                infect_node_len = len([x for x in layer_node if x in temp_nodes])
                # print('infect_node_len')
                # print(infect_node_len)
                infect_ratio = infect_node_len*1.0 / len(layer_node)  # 感染点的比例
                # print('iinfect_ratio')
                # print(infect_ratio)
                ratio_all += infect_ratio
            ratio_average = ratio_all*1.0 / len(BFS_nodes)
            centrality[source] = Decimal(ratio_average)

        print('让我看下这个ratio _average的centiality')
        print(centrality)
        nx.set_node_attributes(self.subgraph, 'centrality',centrality)
        return self.sort_nodes_by_centrality()



    def BFS_nodes(self,tree, source, infectG,subgraph):
        queue = []
        queue.append(source)
        layer_node = []
        layer_node.append([source])
        while queue:
            temp_layer_node = []
            for i in queue:
                for neighbour in list(nx.neighbors(tree, i)):
                    if neighbour != i:
                        temp_layer_node.append(neighbour)
            # 如果某一层的被感染点为0，就退出。不用再加了。
            if len([x for x in temp_layer_node if x in subgraph.nodes() ])== 0:
                break
            layer_node.append(temp_layer_node)
            queue = temp_layer_node
        return layer_node


if __name__ == "__main__":
    prior_detector1 = CoverageCenter()
    # gsba =GSBA(prior_detector1)
    methods = [prior_detector1]
    logger = log.Logger(logname='../data/main_test.log', loglevel=logging.INFO,
                        logger="experiment").get_log()

    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'
    start_time = clock()
    # print "Starting..."
    # data就是我们的图，我们可以做一些操作。      创建一个简单的图。试试看结果。
    ''' 
    1 创建例子的图
    2 给定传播点子图

    '''

    infected = set()
    infected.add(1)
    infected.add(2)
    infected.add(4)
    d = data.Graph("../data/test.txt", weighted=1)
    # print(d.graph.number_of_edges())
    # print(d)
    d.debug = False
    test_num = 3
    # print(d.subgraph)
    # #print(infected)
    # d.subgraph= d.graph

    d.subgraph = nx.Graph()
    d.subgraph = nx.subgraph(d.graph, ['1', '2', '4'])
    # print('子图节点个数')
    # print(d.subgraph.nodes())
    # print(d.graph.nodes())

    # print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()

    for m in experiment.methods:
        m.set_data(d)
        start_time = clock()
        result = m.detect()
        end_time = clock()
        # print('result')
        # print(result)




