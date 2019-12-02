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
import jordan_center as jc
import reverse_infection as ri
import rumor_center as rc
import dmp2
import map_gsba as gsba
import map_gsba_old as gsba_old
import map_bfsa as bfsa
import map_bfsa_parallel as bfsa_p
import prior
import map_ulbaa as ulbaa
import map_gslba as gslba
import map_gsba2 as gsba2

import numpy as np
from experiment import Experiment

if __name__ == '__main__':

    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()
    methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(), ri.ReverseInfection(), di.DynamicImportance(), #prior_detector2,
               gsba.GSBA(prior_detector1),gsba.GSBA(prior_detector4),gsba_old.GSBA(prior_detector1),gsba_old.GSBA(prior_detector4)]
    # methods = [gsba_old.GSBA(prior_detector1),gsba_old.GSBA(prior_detector4)]

    logger = log.Logger(logname='../data/main_gsba_old_VS_new.log', loglevel=logging.INFO, logger="experiment").get_log()
    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'

    start_time = clock()
    print "Starting..."
    d = data.Graph("../data/scale-free.ba.v500.e996.gml", weighted=1)
    d.debug = False
    test_num = 100

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()
    test_category = experiment.RANDOM_TEST
    experiment.start(d, test_category, test_num, 10, 100, 10)

    # test_category = experiment.FULL_TEST
    # experiment.start(d, test_category, test_num, 3, 11, 1)

    end_time = clock()
    print "Running time:", end_time-start_time