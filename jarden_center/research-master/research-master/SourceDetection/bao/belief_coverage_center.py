#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : belief_coverage_center.py
# @Author: zhiqiangbao
# @Date  : 2019/12/6


# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""


from data import *
from  collections import  defaultdict
import math
from decimal import *


import method


from time import clock
import log
import logging
import networkx as nx
import data

from experiment import Experiment


class Belief_coverage_center(method.Method):
    '''
   基于覆盖率的置信算法实现
        思路：
            1 初始化每个点的一阶邻域覆盖率
            2 随机某个点i和它的邻居节点j1，j2，j3。（通过i来影响j）
            3 从i向j1，j2，j3发送消息。消息的定义公式一定要搞下，操。
            再重复2，3直到所有点都更新了。
            4 计算每个点的置信度，将它所收到的所有消息乘积起来。
            最大的就是谣言中心。




    '''

    visited = set()  # node set
    bfs_tree = nx.Graph()

    def detect(self):
        """detect the source with Rumor Centrality.

        Returns:
            @rtype:int
            the detected source
        """

        print('置信传播谣言中心检测')
        if self.subgraph.number_of_nodes() == 0:
            print 'subgraph.number_of_nodes =0'
            return

        self.reset_centrality()
        centrality = {}

        P_node_prominence = defaultdict(int)
        for infect_node in self.subgraph.nodes():
            # print('是哪个点')
            # print(infect_node)
            neigbour_node = nx.neighbors(self.data.graph, infect_node)
            neigbour_infect_node = [x for x in neigbour_node if x in self.subgraph.nodes()]
            Iv = len(neigbour_infect_node)
            Ov = len(neigbour_node)
            P_node_prominence[infect_node] = Iv * 1.0 / Ov * (1 + math.log(Ov))
            # print('输出权重')
            # 加一个对感染边权重的处理。
            # print(self.data.weights)
            # 分子
            molecule = 0
            for neigbour_infect in neigbour_infect_node:
                molecule += 1 - self.data.weights[
                    self.data.node2index[infect_node], self.data.node2index[neigbour_infect]]
            # print('分子是')
            # print(molecule)
            Denominator = 0
            for neigbour in neigbour_node:
                Denominator += 1 - self.data.weights[
                    self.data.node2index[infect_node], self.data.node2index[neigbour]]
            # print('分母是')
            # print(Denominator)
            factor = molecule * 1.0 / Denominator
            # print('看下factor')
            # print(factor)
            P_node_prominence[infect_node] *= factor


        # 开始置信传播。

        node_message = dict()
        # new_arrays = np.zeros((infectG.number_of_nodes(), infectG.number_of_nodes()))
        # 变成图版本，
        for edge in self.data.graph.edges():
            node_message[(edge[0], edge[1])] = 0
            node_message[(edge[1], edge[0])] = 0

        for i in range(0, 50):
            # 对每个点来说，向四周发送消息。消息为
            lists =list(self.subgraph.nodes())
            # print
            # print(lists)
            random.shuffle(lists)
            for node in lists:
                for neighbour_temp in list(nx.neighbors(self.subgraph, node)):
                    mutiplue = 0
                    # 制造list，除去邻居neighbor_temp的node其他邻居节点list
                    neighbour_temp_list = list(nx.neighbors(self.subgraph, node))
                    neighbour_temp_list.remove(neighbour_temp)
                    for neighbour_two in neighbour_temp_list:
                        mutiplue = mutiplue + P_node_prominence[neighbour_two]  # 改成了加，效果很好啊。还是需要再修改下，这个公式
                    # 消息更新
                    node_message[(node, neighbour_temp)] = mutiplue + P_node_prominence[node]  # 还是有问题，就是这里应该有加的。
        # 这个矩阵就是所有点相互之间发送的消息了。
        # node_belief_dict = defaultdict(int)
        # 现在计算每个点的置信度。
        for node_belief in list(self.subgraph.nodes()):
            mutiplue_belief = 1
            for neighbour_belief in list(nx.neighbors(self.subgraph, node_belief)):
                mutiplue_belief = mutiplue_belief * node_message[(neighbour_belief, node_belief)]  # 注意这里是反的，并不是正
            centrality[node_belief] =  Decimal(mutiplue_belief * P_node_prominence[node_belief])



        print('看下中心性')
        print(centrality)


        nx.set_node_attributes(self.subgraph, 'centrality',centrality)
        return self.sort_nodes_by_centrality()


if __name__ == "__main__":
    prior_detector1 = Belief_coverage_center()
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

