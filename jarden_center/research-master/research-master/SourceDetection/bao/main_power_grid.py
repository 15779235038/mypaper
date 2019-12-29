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
import map_gsba_old as gsba_old
import reverse_infection as ri
import rumor_center as rc
import dmp2
import map_bfsa_parallel as bfsa_p
import prior
import  coverage_center_all as coverage
import numpy as np
from experiment import Experiment
import  EPA_center as epa
import map_ulbaa as ulbaa
import  EPA_center_Weights2 as epa2

import map_gsba_bao as gsba_bao
import  map_gsba_bao3 as gsba_bao3
import  map_gsba_bao5 as gsba_bao5
import  map_gsba_bao2 as gsba_bao2
import map_gsba_bao6 as gsba_bao6
import  map_gsba_bao7 as gsba_bao7
import  map_gsba_bao8 as gsba_bao8
import  map_gsba_bao9 as gsba_bao9
if __name__ == '__main__':

    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()
    prior_detector7 = epa.EPA_center()
    prior_detector8 = epa2.EPA_center_weight()  # 有权重版本

    '''
    以下是比较prior的性能的，为源代码所为。
    
    '''
    # methods = [
    #     rc.RumorCenter(),
    #     dc.DistanceCenter(),
    #     jc.JordanCenter(),
    #     ri.ReverseInfection(),
    #     di.DynamicImportance(),
    #     prior_detector7,
    #     # prior_detector9,
    #     prior_detector1,
    #     prior_detector8,
    #     gsba.GSBA(prior_detector1),
    #     gsba_bao.GSBA_coverage(prior_detector1),
    #     gsba_bao7.GSBA_coverage_7(prior_detector1),
    #     gsba_bao9.GSBA_coverage_9(prior_detector1)
    #
    # ]
    methods =[
            rc.RumorCenter(),
            dc.DistanceCenter(),
            jc.JordanCenter(),
            ri.ReverseInfection(),
            di.DynamicImportance(),
            prior_detector8,
            gsba.GSBA(prior_detector1),
            gsba_bao7.GSBA_coverage_7(prior_detector1),
            gsba_bao9.GSBA_coverage_9(prior_detector1)
    ]


    '''
    以下是综合比较的，我用比较大数据集,我写的
    
    
    '''

    # methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(), ri.ReverseInfection(), di.DynamicImportance(),
    #            prior_detector2,
    #            prior_detector7,
    #            gsba.GSBA(prior_detector0), gsba.GSBA(prior_detector1), gsba.GSBA(prior_detector3),
    #            gsba.GSBA(prior_detector4), gsba.GSBA(prior_detector5), gsba.GSBA(prior_detector2),
    #            bfsa_p.BFSA(prior_detector1),
    #            gsba.GSBA(prior_detector7),
    #            gsba_bao.GSBA_coverage(prior_detector1)
    #
    #            ]
    # methods = [dc.DistanceCenter()]
    #methods = [bfsa_p.BFSA(prior_detector1)]
    # methods = [dmp2.DynamicMessagePassing()]

    logger = log.Logger(logname='../data/main_power_grid20191221.log', loglevel=logging.INFO, logger="experiment").get_log()
    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'

    start_time = clock()
    print "Starting..."
    # d = data.Graph("../data/power-grid.txt")
    d = data.Graph("../data/power-grid.gml", weighted=1)
    d.debug = False
    test_num = 100

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()
    test_category = experiment.RANDOM_TEST
    experiment.start(d, test_category, test_num,20, 350, 40)
    # test_category = experiment.FULL_TEST
    # experiment.start(d, test_category, test_num, 10, 46, 5)

    end_time = clock()
    print "Running time:", end_time-start_time