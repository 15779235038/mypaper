# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import logging
import pickle
import random
from time import clock

import networkx as nx
import numpy as np

import data as mydata


class Experiment:
    """Conduct experiments with simulations about information propagation under two test_category categories:
    Full test_category: each node is selected to be the source.
    Random test_category: randomly select a node as the infection source.
    """
    precision = {}  # Detection Rate
    error = {}  # Detection Error
    topological_error = {}  # Detection topological Error
    ranking = {}  # Normalized Ranking
    methods = []
    running_time = {}
    propagation_model = 'IC'
    logger = logging.getLogger()
    RANDOM_TEST = 'random test'
    FULL_TEST = 'full test'

    def __init__(self, methods, logger):
        self.methods = methods
        self.logger = logger

    def initialize_evaluation_measures(self, test_category):
        self.precision[test_category] = {}
        self.error[test_category] = {}
        self.topological_error[test_category] = {}
        self.ranking[test_category] = {}
        self.running_time[test_category] = {}
        for m in self.methods:
            self.precision[test_category][m.method_name] = list()
            self.error[test_category][m.method_name] = list()
            self.topological_error[test_category][m.method_name] = list()
            self.ranking[test_category][m.method_name] = list()
            self.running_time[test_category][m.method_name] = list()


    def start(self, d, test_category, test_num, start,end,step):
        """
        start the experiment
        Args:
            d: mydata.Graph
            test_category: {'full test', 'random test'}
            test_num: the number of random test times
            start: the minimal number of infected nodes
            end: the maximal number of infected nodes
            step: the increasing step
        """

        '''测试的点也太少了把 '''
        self.logger.info(test_category)
        self.logger.info('测试生成原点数目'+str(test_num))
        print('这里居然每个数量的感染点都测试100遍。不过，有点少，只有10到41.')
        for infected_size in np.arange(start, end, step):
            print('初始化结果测试方案')
            self.initialize_evaluation_measures(test_category)
            s_time = clock()
            print('使用实时生成的有关信息传播的模拟进行随机（或完整）测试。')
            self.detect_generated(d, test_category, test_num, infected_size)
            e_time = clock()
            print "Running time:", e_time - s_time
            # self.logger.info(("Running time:", e_time - s_time))
            print('打印出结果')
            self.print_result(test_category)
            print '\n'
            self.logger.info('\n')

    def detect_generated(self, data, test_category, test_num=1, infected_size=None):
        """
        do random (or full) test with real-time generated simulations about information propagation.
        Args:
            data: mydata.Graph  图对象
            test_category: {'full_test', 'random_test'}          #检测策略
            test_num:   int                 #生成源点数目
            infected_size: int                  #感染点数目，这里只有10~40的范围，说明这个应用有限吧？
        """
        print('进行传播')
        nodes = data.graph.nodes()

        # print('nodes',nodes)
        print(type(nodes))
        n = len(nodes)
        sources = list()  # source nodes' index
        if test_category is self.RANDOM_TEST:
            """randomly select the sources"""
            v = 0
            while v < test_num:
                # print('source',nodes[random.randint(0, n - 1)])
                sources.append(nodes[random.randint(0, n - 1)])
                v += 1
        else:
            sources = nodes

        print('从所有点中挑选一个点进行传播SI传播。')
        n_i = len(sources)
        print('输出传播策略，源点选择数目，感染点数量')
        print test_category, len(sources), infected_size
        self.logger.info((test_category, len(sources), infected_size))
        i = 0
        p = 0.1
        # print('sources',sources)
        count  = 0
        for s in sources:
            count +=1
            # print('这是第多少次测试')
            # print(count)
            # print('---------------------------------------')
            # print('本次选中的源为')
            # print(s)
            i += 1
            if abs(i - n_i * p) < 1:
                print '\t percentage: ', p
                p += 0.1
            if self.propagation_model is 'IC':
                infected = data.infect_from_source_IC(s, infected_size=infected_size)
            elif self.propagation_model is 'SI':
                # print('source',s)
                infected = data.infect_from_source_SI(s, infected_size=infected_size)
            if infected_size is not None and len(infected)<infected_size-1:
                # print('如果传播的点没有达到要求，本次传播结束')
                continue

            # print('感染点的数目是多少')
            print(len(infected))

            # print('传播完之后，作者使用各种方法来实验,每种方法都会有其各种尺度的测试方案')
            for m in self.methods:
                m.set_data(data)
                start_time = clock()
                result = m.detect()
                end_time = clock()
                self.running_time[test_category][m.method_name].append(end_time - start_time)
                """evaluate the result"""
                if len(result) > 0:
                    if result[0][0] == s:
                        # print('准确率测试')
                        self.precision[test_category][m.method_name].append(1)
                    else:
                        self.precision[test_category][m.method_name].append(0)
                        # print('平均距离测试')
                    self.error[test_category][m.method_name].append(
                        nx.dijkstra_path_length(data.subgraph, result[0][0], s, weight='weight'))
                    # print('拓扑结果测试')
                    self.topological_error[test_category][m.method_name].append(
                        nx.dijkstra_path_length(data.subgraph, result[0][0], s, weight=None))
                    r = 0
                    # print('rank测试')
                    for u in result:
                        r += 1
                        if u[0] == s:
                            self.ranking[test_category][m.method_name].append(r * 1.0 / len(result))
                            break

    def detect_loaded(self, network, test_category, infected_size, test_num=1):
        """
        do random (or full) test with loaded simulations about information propagation.
        Args:
            data: mydata.Graph
            test_category: {'full_test', 'random_test'}
            test_num:   int
            infected_size: int
        """
        """Read the network and generate source nodes according to the test_category category"""
        d = mydata.Graph("../data/%s" % network, weighted=1)
        nodes = d.graph.nodes()
        n = d.graph.number_of_nodes()
        sources = list()  # source nodes' index
        self.initialize_evaluation_measures(test_category)
        if test_category is self.RANDOM_TEST:
            v = 0
            while v < test_num:
                sources.append(random.randint(0, n - 1))
                v += 1
        else:
            sources = np.arange(0, n)
        n = len(sources)

        """run the test_category"""
        print test_category, len(nodes), d.graph.number_of_edges(), infected_size, test_num
        for m in self.methods:
            print '\t', m.method_name
            start_time = clock()
            percentage = 0.2
            i = 0
            for s in sources:
                i += 1
                if abs(i - n * percentage) < 1:
                    print '\t\t percentage: ', percentage
                    percentage += 0.2
                file = "../data/simulation/%s.i%s.s%s.subgraph" % (network, infected_size, s)
                reader = open(file, "r")
                data = pickle.load(reader)
                """@type data: mydata.Graph"""
                reader.close()
                data.weights = d.weights
                m.set_data(data)
                result = m.detect()
                """evaluate the result"""
                if len(result) > 0:
                    if result[0][0] == nodes[s]:
                        self.precision[test_category][m.method_name].append(1)
                    else:
                        self.precision[test_category][m.method_name].append(0)
                    self.error[test_category][m.method_name].append(
                        nx.dijkstra_path_length(d.subgraph, result[0][0], nodes[s], weight='weight'))
                    self.topological_error[test_category][m.method_name].append(
                        nx.dijkstra_path_length(d.subgraph, result[0][0], nodes[s], weight=None))
                    r = 0
                    for u in result:
                        r += 1
                        if u[0] == nodes[s]:
                            self.ranking[test_category][m.method_name].append(r * 1.0 / len(result))
                            break
            end_time = clock()
            self.running_time[test_category][m.method_name] = end_time - start_time

    def print_result(self, test):




        print('作者给出了5个指标，包括准确率，带权重的距离，误差步长，等级距离，运行时间。')
        print('输出到log中')

        self.logger.info('作者给出了5个指标，包括准确率，带权重的距离，误差步长，等级距离，运行时间')
        self.logger.info(self.precision)
        print('precision')
        print(self.precision)
        self.logger.info(self.error)
        self.logger.info(self.topological_error)
        self.logger.info(self.ranking)
        self.logger.info(self.running_time)

        for m in self.methods:
            l = len(self.precision[test][m.method_name]) * 1.0
            print('l是什么，就是500次')
            print(l)
            if l == 0: continue
            r = sum(self.precision[test][m.method_name]) / l, sum(self.error[test][m.method_name]) / l, sum(
                self.topological_error[test][m.method_name]) / l, sum(
                self.ranking[test][m.method_name]) / l,sum(self.running_time[test][m.method_name])/l, m.method_name, l
            print "%.4f\t%.4f\t%.4f\t%.4f\t%.5f\t%s\t%d"%r

            self.logger.info(r)
