# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import random
from time import clock
import log
import logging

import networkx as nx

import data
import distance_center as dc
import dynamic_importance as di
# import dynamic_message_passing as dmp
import jordan_center as jc
import map_gsba as gsba
import reverse_infection as ri
import rumor_center as rc
import dmp2
import map_bfsa_parallel as bfsa_p
import map_bfsa as bfsa
import prior
import numpy as np

class Experiment:
    precision = {}  # Detection Rate
    error = {}  # Detection Error
    topological_error = {}  # Detection topological Error
    ranking = {}  # Normalized Ranking
    methods = []
    propagation_model = 'IC'
    logger = logging.getLogger()

    def initialize_evaluation_measures(self):
        self.precision['full_test'] = {}
        self.precision['random_test'] = {}
        self.error['full_test'] = {}
        self.error['random_test'] = {}
        self.topological_error['full_test'] = {}
        self.topological_error['random_test'] = {}
        self.ranking['full_test'] = {}
        self.ranking['random_test'] = {}
        for m in self.methods:
            self.precision['full_test'][m.method_name] = list()
            self.precision['random_test'][m.method_name] = list()
            self.error['full_test'][m.method_name] = list()
            self.error['random_test'][m.method_name] = list()
            self.topological_error['full_test'][m.method_name] = list()
            self.topological_error['random_test'][m.method_name] = list()
            self.ranking['full_test'][m.method_name] = list()
            self.ranking['random_test'][m.method_name] = list()

    def detection_test(self, d, random_test=False, random_num=1):
        """Full test_category: each node is selected to be the source
            Random test_category: randomly select a node as the infection source
        """
        test = 'full_test'
        nodes = d.graph.nodes()
        number_of_nodes = len(nodes)
        if random_test:
            test = 'random_test'
            """randomly select the sources"""
            temp = list()
            v = 0
            while v < random_num:
                temp.append(nodes[random.randint(0, number_of_nodes - 1)])
                v += 1
            nodes = temp
            number_of_nodes = len(nodes)
        i = 0
        p = 0.1
        print test, len(nodes)
        for s in nodes:
            i += 1
            if abs(i - number_of_nodes * p) < 1:
                print '\t percentage: ', p
                p += 0.1
            if self.propagation_model == 'IC':
                infected = d.infect_from_source_IC(s)
            elif self.propagation_model == 'SI':
                infected = d.infect_from_source_SI(s)
            if infected.__len__()<=1:
                continue
            if d.debug:
                print 'source = ', s, infected
            for m in methods:
                m.set_data(d)
                result = m.detect()
                """evaluate the result"""
                if len(result) > 0:
                    if result[0][0] == s:
                        self.precision[test][m.method_name].append(1)
                    else:
                        self.precision[test][m.method_name].append(0)
                    # error['full_test'][m.method_name].append(distances[result[0][0]][s])
                    # topological_error['full_test'][m.method_name].append(topological_distances[result[0][0]][s])
                    self.error[test][m.method_name].append(
                        nx.dijkstra_path_length(d.subgraph, result[0][0], s, weight='weight'))
                    self.topological_error[test][m.method_name].append(
                        nx.dijkstra_path_length(d.subgraph, result[0][0], s, weight=None))
                    r = 0
                    for u in result:
                        r += 1
                        if u[0] == s:
                            self.ranking[test][m.method_name].append(r*1.0/len(result))
                            break

    def print_result(self, test):
        self.logger.info(self.precision)
        self.logger.info(self.error)
        self.logger.info(self.topological_error)
        self.logger.info(self.ranking)
        for m in methods:
            l = len(self.precision[test][m.method_name])*1.0
            if l==0 : continue
            r = sum(self.precision[test][m.method_name]) / l, sum(self.error[test][m.method_name]) / l, sum(
                self.topological_error[test][m.method_name]) / l, sum(self.ranking[test][m.method_name]) / l, m.method_name, l
            print r
            logger.info(r)

if __name__ == '__main__':
    logger = log.Logger(logname='../data/main.log', loglevel=logging.INFO, logger="experiment").get_log()
    experiment = Experiment()
    experiment.logger = logger

    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()
    methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(),ri.ReverseInfection(),prior_detector2,
               gsba.GSBA( prior_detector1),gsba.GSBA(prior_detector2), gsba.GSBA( prior_detector3),
               gsba.GSBA(prior_detector4), gsba.GSBA( prior_detector5)]
    methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(), ri.ReverseInfection(), di.DynamicImportance(), prior_detector2,
               gsba.GSBA(prior_detector0), gsba.GSBA(prior_detector1), gsba.GSBA( prior_detector3),
               gsba.GSBA(prior_detector4), gsba.GSBA( prior_detector5), gsba.GSBA(prior_detector2), bfsa_p.BFSA(prior_detector1)]
    #methods = [bfsa_p.BFSA(prior_detector1)]
    # methods = [dmp2.DynamicMessagePassing()]
    experiment.methods = methods

    start_time = clock()
    print "Starting..."
    # d = data.Graph("../data/test_category.txt", weighted=1)
    # d = data.Graph("../data/karate_club.gml")
    # d = data.Graph("../data/small-world.ws.v100.e500.gml", weighted=1)
    d = data.Graph("scale-free.ba.v500.e996.gml", weighted=1)
    #d = data.Graph("../data/power-grid.txt")
    d.debug = False
    random_num = 100
    experiment.propagation_model = 'SI'

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()
    test = "random_test"
    d.ratio_infected = 0.006
    logger.info(test)
    for i in np.arange(0,-1):
        experiment.initialize_evaluation_measures()
        str = 'd.ratio_infected', d.ratio_infected, d.ratio_infected*d.graph.number_of_nodes()
        logger.info(str)
        print str
        s_time = clock()
        experiment.detection_test(d, random_test=True, random_num=random_num)
        e_time = clock()
        print "Running time:", e_time-s_time
        logger.info(("Running time:", e_time-s_time))
        experiment.print_result(test)
        d.ratio_infected += 0.002
        print '\n'
        logger.info('\n')

    test = "full_test"
    d.ratio_infected = 0.018
    logger.info(test)
    for i in np.arange(0,4):
        experiment.initialize_evaluation_measures()
        str = 'd.ratio_infected', d.ratio_infected, d.ratio_infected*d.graph.number_of_nodes()
        logger.info(str)
        print str
        s_time = clock()
        experiment.detection_test(d)
        e_time = clock()
        print "Running time:", e_time-s_time
        logger.info(("Running time:", e_time-s_time))
        experiment.print_result(test)
        d.ratio_infected += 0.002
        print '\n'
        logger.info('\n')

    end_time = clock()
    print "Running time:", end_time-start_time