#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : map_gsba_bao5.py
# @Author: zhiqiangbao
# @Date  : 2019/12/10

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : map_gsba_bao4.py
# @Author: zhiqiangbao
# @Date  : 2019/12/9

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : map_gsba_bao3.py
# @Author: zhiqiangbao
# @Date  : 2019/12/9

'''
以epa作为选择贪心方法
'''

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
import EPA_center_Weights2 as epa2

'''
一阶覆盖率
'''
# import  coverage_center as cc
'''
二阶覆盖率
'''
# import  coverage_center2 as cc
'''
全部覆盖率
'''
import coverage_center_all as cc


class GSBA_coverage_6(method.Method):
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
        这是什么时候调用的？这是公式需要，对别的来说，就不是这个了。所有对于贪心是有两个

        先验的，一个是要谣言中心性，一个是其他。
        我们要加我们的就是加一个先验的，比如覆盖的操作，模仿其谣言定位方式，自己写一个
        然后作为先验，放在先验中。

        '''
        self.reset_centrality()
        self.prior_detector.set_data(self.data)
        self.prior_detector.detect()
        self.prior = nx.get_node_attributes(self.subgraph, 'centrality')

        # print('先验检测器是什么？')
        # print(self.prior)


        #覆盖率中心
        self.reset_centrality()
        cc_object = cc.CoverageCenter()
        cc_object.set_data(self.data)
        cc_object.detect()
        coverage_centralities = nx.get_node_attributes(self.subgraph, 'centrality')



        # epa带权重的东西
        self.reset_centrality()
        epa_weight_object = epa2.EPA_center_weight()
        epa_weight_object.set_data(self.data)
        epa_weight_object.detect()
        epa_weight_cnetralities = nx.get_node_attributes(self.subgraph, 'centrality')




        self.reset_centrality()
        infected_nodes = set(self.subgraph.nodes())
        n = len(infected_nodes)
        # print(infected_nodes)
        # print('infected_nodes')

        posterior = {}
        included = set()
        neighbours = set()
        weights = self.data.weights

        for v in infected_nodes:
            posterior[v] = (decimal.Decimal(  epa_weight_cnetralities[v]* coverage_centralities[v] ))

        # print('w_key_sorted')
        # print(w_key_sorted)
        #
        # print('------------')
        # print(coverage_centralities)
        # print('看下这里的posterior')
        # print(posterior)
        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        return self.sort_nodes_by_centrality()


if __name__ == "__main__":
    prior_detector1 = rc.RumorCenter()

    # gsba =GSBA(prior_detector1)
    methods = [GSBA_coverage_6(prior_detector1)]
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





