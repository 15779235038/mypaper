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
import EPA_center as epa

import map_ulbaa as ulbaa
import EPA_center_Weights2 as epa2
import map_gsba_bao as gsba_bao
import belief_coverage_center as bc
import map_gsba_bao2 as gsba_bao2
import map_gsba_bao3 as gsba_bao3
import map_gsba_bao4 as gsba_bao4
import rumor_EPA_center as rumor_epa
import rumor_coverage_center as rumor_coverage
import map_gsba_bao5 as gsba_bao5
import map_gsba_bao6 as gsba_bap6
import map_gsba_bao7 as gsba_bao7
import  map_gsba_bao8 as gsba_bao8
import  map_gsba_bao9 as gsba_bao9

import  map_gsba_bao15 as gsba_bao15
if __name__ == '__main__':
    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()

    prior_detector7 = epa.EPA_center()
    prior_detector8 = epa2.EPA_center_weight()  # 有权重版本
    prior_detector9 = bc.Belief_coverage_center()  # 置信传播算法。


    # methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(),ri.ReverseInfection(),prior_detector2,
    #            gsba.GSBA( prior_detector1),gsba.GSBA(prior_detector2), gsba.GSBA( prior_detector3),
    #            gsba.GSBA(prior_detector4), gsba.GSBA( prior_detector5)]
    # methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(), ri.ReverseInfection(), di.DynamicImportance(),
    #            gsba.GSBA(prior_detector1),gsba.GSBA(prior_detector3),gsba.GSBA(prior_detector4),]

    '''
    它的东西

    '''
    # methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(),
    #            gsba.GSBA(prior_detector1),gsba.GSBA(prior_detector3),gsba.GSBA(prior_detector4)]

    '''
    我的比较所有方法

    '''
    #
    # methods = [
    #     rc.RumorCenter(),
    #     dc.DistanceCenter(),
    #     jc.JordanCenter(),
    #     ri.ReverseInfection(),
    #     di.DynamicImportance(),
    #     prior_detector8,
    #     gsba.GSBA(prior_detector1),
    #     gsba_bao7.GSBA_coverage_7(prior_detector1),
    #     gsba_bao9.GSBA_coverage_9(prior_detector1)
    # ]


    #验证先验性的方法。综合比较7种方法
    methods = [
       # rumor_coverage.rumor_coverage(prior_detector1),
       #  prior_detector8,
       #  gsba.GSBA(prior_detector1),
       # #  gsba_bao7.GSBA_coverage_7(prior_detector1),
       # #  gsba_bao8.GSBA_coverage_8(prior_detector1),
       #  gsba_bao9.GSBA_coverage_9(prior_detector1),
        gsba_bao15.GSBA_coverage_15(prior_detector1)
    ]

    logger = log.Logger(logname='../data/main_500scale_free20107.log', loglevel=logging.INFO, logger="experiment").get_log()
    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'

    start_time = clock()
    print "Starting..."
    d = data.Graph("../data/scale_network/500/500scale_free2.txt", weighted=0)
    d.debug = False
    test_num = 10

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()
    test_category = experiment.RANDOM_TEST
    experiment.start(d, test_category, test_num, 20, 350, 40)
    # test_category = experiment.FULL_TEST
    # experiment.start(d, test_category, test_num, 200, 400,100)

    end_time = clock()
    print "Running time:", end_time - start_time