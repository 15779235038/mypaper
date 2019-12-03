# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import decimal
import networkx as nx
import method
import rumor_center
import math
from blist import blist

from time import clock
import log
import logging
import networkx as nx
import data
import rumor_center as rc
from experiment import Experiment


class GSBA(method.Method):
    """detect the source with Greedy Search Bound Approximation.
        Please refer to the my paper for more details.
    """
    prior = ''
    prior_detector = None

    def __init__(self, prior_detector):
        method.Method.__init__(self)
        self.method_name = self.__class__, prior_detector.method_name
        self.prior_detector = prior_detector  # 先验检测器

    ''' 
    那么是如何检测的呢？我觉得先有先验给每个点构建分数，然后再有后验加上。两者乘积

    '''

    def detect(self):
        """detect the source with GSBA.
        Returns:
            @rtype:int
            the detected source
        """

        ''' 
        '''
        self.reset_centrality()
        self.prior_detector.set_data(self.data)
        self.prior_detector.detect()
        self.prior = nx.get_node_attributes(self.subgraph, 'centrality')

        self.reset_centrality()
        rc = rumor_center.RumorCenter()
        rc.set_data(self.data)
        rc.detect()
        rumor_centralities = nx.get_node_attributes(self.subgraph, 'centrality')
        # print('先验加进去，试试看')
        self.reset_centrality()
        infected_nodes = set(self.subgraph.nodes())
        n = len(infected_nodes)
        print(infected_nodes)
        print('infected_nodes')

        posterior = {}
        included = set()
        neighbours = set()
        weights = self.data.weights
        for v in infected_nodes:
            print('------从v点开始----------')
            print(v)
            """find the approximate upper bound by greedy searching"""
            included.clear()
            neighbours.clear()
            included.add(v)
            neighbours.add(v)
            likelihood = 1
            w = {}  # effective propagation probabilities: node->w
            w_key_sorted = blist()
            w[v] = 1
            w_key_sorted.append(v)
            while len(included) < n:
                print('邻居用来计算所谓的neighbours')
                print(neighbours)
                w_sum = sum([w[j] for j in neighbours])
                u = w_key_sorted.pop()  # pop out the last element from w_key_sorted with the largest w
                likelihood *= w[u] / w_sum
                print('分母是？')
                print(w_sum)
                print('likelihood')
                print(likelihood)
                included.add(u)
                neighbours.remove(u)
                new = nx.neighbors(self.data.graph, u)
                print('new也就是在总图中的邻居')
                print(new)
                for h in new:
                    print('遍历到某个邻居')
                    print(h)
                    if h in included:
                        continue
                    neighbours.add(h)
                    # compute w for h
                    w_h2u = weights[self.data.node2index[u], self.data.node2index[h]]
                    # w_h2u = weights[self.data.node2index[u]][self.data.node2index[h]]
                    if h in w.keys():
                        print('------')
                        print(w[h])
                        print(w_h2u)
                        w[h] = 1 - (1 - w[h]) * (1 - w_h2u)
                        print('w[h]，，，，h在keys')
                        print(w[h])
                    else:
                        print('h不在keys')
                        w[h] = w_h2u
                        print(w[h])

                    print('w是什么')
                    print(w)
                    # h_neighbor = nx.neighbors(self.data.graph, h)
                    # w_h = 1
                    # for be in included.intersection(h_neighbor):
                    #     w_h *= 1 - self.data.get_weight(h, be)
                    # w[h] = 1 - w_h
                    """insert h into w_key_sorted, ranking by w from small to large"""
                    if h in infected_nodes:
                        print('开始排序了')
                        if h in w_key_sorted:
                            w_key_sorted.remove(h)  # remove the old w[h]
                        k = 0

                        while k < len(w_key_sorted):
                            if w[w_key_sorted[k]] > w[h]:
                                break
                            k += 1
                        print(w_key_sorted)
                        w_key_sorted.insert(k, h)  # 安排降序加入，就是排列可能性加入，安排顺序插入进去
                        print('w_key_sorted')
                        print(w_key_sorted)

                        # w_key_sorted[k:k] = [h]
            print('每次开始的是那个节点呢？')
            print(v)
            print('每一个的可能性是likehood')
            print(likelihood)
            posterior[v] = (decimal.Decimal(self.prior[v]) * decimal.Decimal(likelihood) * rumor_centralities[v])

        print('w_key_sorted')
        print(w_key_sorted)

        print('------------')
        print(rumor_centralities)
        print('看下这里的posterior')
        print(posterior)
        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        return self.sort_nodes_by_centrality()


if __name__ == "__main__":
    prior_detector1 = rc.RumorCenter()
    # gsba =GSBA(prior_detector1)
    methods = [GSBA(prior_detector1)]
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
    test_num = 3
    print(d.subgraph)
    # print(infected)
    # d.subgraph= d.graph

    d.subgraph = nx.Graph()
    d.subgraph = nx.subgraph(d.graph, ['1', '2', '4'])
    print('子图节点个数')
    print(d.subgraph.nodes())
    print(d.graph.nodes())

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()

    for m in experiment.methods:
        m.set_data(d)
        start_time = clock()
        result = m.detect()
        end_time = clock()
        print('result')
        print(result)





