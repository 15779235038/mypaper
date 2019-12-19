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

不要GSBA构建的序列，也是直接谣言中心性乘以epa来算
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


class pagerank_vector_center(method.Method):
    """detect the source with Greedy Search Bound Approximation.
        Please refer to the my paper for more details.
    """

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
        首先用覆盖率和epa-weight作为先验作为pageRank迭代的起始值,然后再使用
        迭代,只用传播图来迭代吧?
        
        

        '''







        # epa带权重的东西
        self.reset_centrality()
        epa_weight_object = epa2.EPA_center_weight()
        epa_weight_object.set_data(self.data)
        epa_weight_object.detect()
        epa_weight_cnetralities = nx.get_node_attributes(self.subgraph, 'centrality')



        # 覆盖率中心
        self.reset_centrality()
        cc_object = cc.CoverageCenter()
        cc_object.set_data(self.data)
        cc_object.detect()
        coverage_centralities = nx.get_node_attributes(self.subgraph, 'centrality')












        self.reset_centrality()
        infected_nodes = set(self.subgraph.nodes())
        n = len(infected_nodes)
        initvalue={}
        for node in infected_nodes:
            initvalue[node] =float(epa_weight_cnetralities[node]*coverage_centralities[node])

        posterior=nx.pagerank(self.subgraph,alpha=0.85, personalization=None,
             max_iter=100, tol=1.0e-6, nstart=initvalue, weight='weight',
             dangling=None)
        print('posterior')
        print(posterior)
        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        return self.sort_nodes_by_centrality()


if __name__ == "__main__":
    prior_detector1 = rc.RumorCenter()

    # gsba =GSBA(prior_detector1)
    methods = [pagerank_vector_center(prior_detector1)]
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





