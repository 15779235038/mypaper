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
import map_bfsa as bfsa
import map_bfsa_parallel as bfsa_p
import prior
import map_ulbaa as ulbaa
import map_gslba as gslba
import map_gsba2 as gsba2
import  EPA_center as epa
import numpy as np
from experiment import Experiment

import map_gsba_old as gsba_old
import  EPA_center_Weights2 as epa2
import map_gsba_bao as gsba_bao
import  belief_coverage_center as bc
import  map_gsba_bao2 as gsba_bao2
import  map_gsba_bao3 as gsba_bao3
import  map_gsba_bao4 as gsba_bao4
import  rumor_EPA_center as rumor_epa
import  rumor_coverage_center as rumor_coverage
import  map_gsba_bao5  as gsba_bao5
import  map_gsba_bao6 as gsba_bao6
import  Completion_rumor_center as cr
import  map_gsba_bao7 as gsba_bao7
import  map_gsba_bao8 as gsba_bao8
import  pagerank_vector_center as pvc
if __name__ == '__main__':

    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()
    prior_detector6 = di.DynamicImportance()
    prior_detector7 = epa.EPA_center()
    prior_detector8 = epa2.EPA_center_weight()  #有权重版本
    prior_detector9=bc.Belief_coverage_center()  #置信传播算法。
    prior_detector10 =pvc.pagerank_vector_center()

    '''
        这是为了检测所有的东西，然后评测性能的。
    
    '''
    # methods = [
    #            # rc.RumorCenter(),
    #            # dc.DistanceCenter(),
    #            # jc.JordanCenter(),
    #            # ri.ReverseInfection(),
    # #            di.DynamicImportance(),
    #            # prior_detector7,
    #            # prior_detector9,
    #            prior_detector8,
    #
    #
    #            # gsba.GSBA(prior_detector0),
    #            gsba.GSBA(prior_detector1),
    #
    #            gsba_bao.GSBA_coverage(prior_detector1),
    #            # cr.Completion_Center(prior_detector1),
    #            #  gsba_bao5.GSBA_coverage_5(prior_detector1),
    #            #  gsba_bao6.GSBA_coverage_6(prior_detector1),
    #              gsba_bao7.GSBA_coverage_7(prior_detector1),
    #             gsba_bao8.GSBA_coverage_8(prior_detector1)
    #            ]
    '''
        而底下的这些方法是为了验证先验有没有提高的意思，如果我们需要做修改的话，
        我们需要做全面对比，但是我们的方法也是有侧重点的。
        '''
    # methods = [
    #     rc.RumorCenter(),
    #     dc.DistanceCenter(),
    #     jc.JordanCenter(),
    #     ri.ReverseInfection(),
    #     di.DynamicImportance(),
    #     prior_detector8,
    #     gsba.GSBA(prior_detector1),
    #     gsba_bao7.GSBA_coverage_7(prior_detector1),
    #
    # ]


    methods = [
              prior_detector10,
               gsba_bao7.GSBA_coverage_7(prior_detector1),
                 prior_detector4
               ]

    logger = log.Logger(logname='../data/main_scale_free20191212.log', loglevel=logging.INFO, logger="experiment").get_log()
    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'

    start_time = clock()
    print "Starting..."
    d = data.Graph("../data/scale-free.ba.v500.e996.gml", weighted=1)
    d.debug = False

    test_num =10

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()

    '''
    不加BFSA的大数据集，40到60
    '''
    # test_category = experiment.RANDOM_TEST
    # experiment.start(d, test_category, test_num, 20, 46, 5)

    # test_category = experiment.FULL_TEST
    # experiment.start(d, test_category, test_num, 20, 46, 5)

    '''
    
    
    1 没加BFSA的正常搞
    '''
    test_category = experiment.RANDOM_TEST
    experiment.start(d, test_category, test_num, 20, 110, 10)
    end_time = clock()
    print "Running time:", end_time-start_time


