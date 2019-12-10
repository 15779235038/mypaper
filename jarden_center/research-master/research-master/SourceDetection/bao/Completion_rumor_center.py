# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

from decimal import *

import math

from experiment import Experiment
from time import clock
import log
import logging
import networkx as nx
import data
import method
from data import *
import  rumor_center as rc
'''
1 补全网络，按照最长的分支。先试试最长的拓扑距离吧，后来试试权重距离
2 然后进行定位，先试试谣言中心。


要看下它的SI是怎么按照概率传播点。

思路：
1 得到每个点关于其它点的距离
2 传播子图，然后计算所有点的rumor center。
3 每个点按照找到传播子图最短距离最远的点，进行BFS树构键
    3.1 得到新的rumor center
    3.2 统计BFS树和传播子图差距，差距越大，越不可能是源点。以差距计算概率，乘以原来的先验
    
4 

'''
class Completion_Center(method.Method):
    """
        detect the source with Rumor Centrality.
        Please refer to the following paper for more details.
        Shah D, Zaman T. Detecting sources of computer viruses in networks: theory and experiment[J].
        ACM SIGMETRICS Performance Evaluation Review, 2010, 38(1): 203-214.
    """

    prior = ''
    prior_detector = None

    def __init__(self, prior_detector):
        method.Method.__init__(self)
        self.method_name = self.__class__, prior_detector.method_name
        self.prior_detector = prior_detector  # 先验检测器

    def detect(self):


        self.reset_centrality()
        self.prior_detector.set_data(self.data)
        self.prior_detector.detect()
        self.prior = nx.get_node_attributes(self.subgraph, 'centrality')


        self.reset_centrality()
        if self.subgraph.number_of_nodes() == 0:
            print 'subgraph.number_of_nodes =0'
            return

        for node in self.subgraph.nodes():
            shortest_path_length_all=nx.shortest_path_length(self.data.graph,source=node,weight=None)
            sorted(shortest_path_length_all.items(), key=lambda x: x[1],reverse=True)
            print('shortnode')
            print(shortnode)



        centrality = {}
        for source in self.subgraph.nodes():
            self.bfs_tree = nx.bfs_tree(self.subgraph, source)

            centrality[source] = Decimal(math.factorial(self.bfs_tree.number_of_nodes())) \
                         / nx.get_node_attributes(self.bfs_tree, 'cumulativeProductOfSubtrees')[source]

        nx.set_node_attributes(self.subgraph, 'centrality',centrality)
        return self.sort_nodes_by_centrality()





if __name__ == "__main__":
    prior_detector1 = rc.RumorCenter()

    # gsba =GSBA(prior_detector1)
    methods = [Completion_Center(prior_detector1)]
    logger = log.Logger(logname='../data/main_test.log', loglevel=logging.INFO,
                        logger="experiment").get_log()


    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'
    start_time = clock()
    print "Starting..."
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
    print(d.graph.number_of_edges())
    print(d)
    d.debug = False
    test_num = 1
    print(d.subgraph)
    # print(infected)
    # d.subgraph= d.graph

    d.subgraph = nx.Graph()
    d.subgraph = nx.subgraph(d.graph, ['1', '2', '4'])
    print('子图节点个数')
    print(d.subgraph.nodes())
    print(d.graph.nodes())

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()

    print('方法是')
    print(experiment.methods)
    for m in experiment.methods:
        m.set_data(d)
        start_time = clock()
        result = m.detect()
        end_time = clock()
        print('result')
        print(result)





