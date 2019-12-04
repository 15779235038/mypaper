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
import dynamic_message_passing as dmp
import jordan_center as jc
import map_gsba as gsba
import reverse_infection as ri
import rumor_center as rc
import dmp2
import map_bfsa_parallel as bfsa_p
import prior
import numpy as np
from experiment import Experiment
import map_ulbaa as ulbaa
import map_gslba as gslba
import map_gsba2 as gsba2

if __name__ == '__main__':

    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()
    # methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(),ri.ReverseInfection(), di.DynamicImportance(),
    #            gsba.GSBA(prior_detector1), gsba.GSBA(prior_detector3),gsba.GSBA(prior_detector4),]
    # methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(),
    #            gsba.GSBA(prior_detector1), gsba.GSBA(prior_detector3),gsba.GSBA(prior_detector4),
    #            ulbaa.ULBAA(prior_detector1), ulbaa.ULBAA(prior_detector3), ulbaa.ULBAA(prior_detector4),
    #            gslba.GSLBA(prior_detector1), gslba.GSLBA(prior_detector3), gslba.GSLBA(prior_detector4),
    #            gsba2.GSBA(prior_detector1), gsba2.GSBA( prior_detector3),gsba2.GSBA(prior_detector4),]

    methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(),
               gsba.GSBA(prior_detector1),gsba.GSBA(prior_detector3),gsba.GSBA(prior_detector4)]

    logger = log.Logger(logname='../data/main_wiki_vote.log', loglevel=logging.INFO, logger="experiment").get_log()
    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'

    start_time = clock()
    print "Starting..."
    d = data.Graph("../data/test.txt", weighted=1)
    d = data.Graph("../data/Wiki-Vote.gml", weighted=1)
    d.debug = False
    test_num = 100

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()
    test_category = experiment.RANDOM_TEST
    experiment.start(d, test_category, test_num, 10, 200, 10)
    # test_category = experiment.FULL_TEST
    # experiment.start(d, test_category, test_num, 10, 31, 5)

    end_time = clock()
    print "Running time:", end_time-start_time