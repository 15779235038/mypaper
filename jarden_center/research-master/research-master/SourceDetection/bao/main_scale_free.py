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

import numpy as np
from experiment import Experiment

import map_gsba_old as gsba_old

import map_gsba_bao as gsba_bao
if __name__ == '__main__':

    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()
    prior_detector6 = di.DynamicImportance()


    '''
        这是为了检测所有的东西，然后评测性能的。
    
    '''
    methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(), ri.ReverseInfection(), di.DynamicImportance(), prior_detector2,
               gsba.GSBA(prior_detector0), gsba.GSBA(prior_detector1), gsba.GSBA( prior_detector3),
               gsba.GSBA(prior_detector4), gsba.GSBA( prior_detector5), gsba.GSBA(prior_detector2), bfsa_p.BFSA(prior_detector1),
               gsba_bao.GSBA_coverage(prior_detector1)

               ]
    '''
        而底下的这些方法是为了验证先验有没有提高的意思，如果我们需要做修改的话，
        我们需要做全面对比，但是我们的方法也是有侧重点的。


        '''
    # methods = [rc.RumorCenter(), dc.DistanceCenter(), jc.JordanCenter(),
    #            gsba.GSBA(prior_detector1),gsba.GSBA(prior_detector3),gsba.GSBA(prior_detector4),
    #            gsba_bao.GSBA_coverage(prior_detector1)
    #
    #            ]


    # methods = [gsba_old(prior_detector1)]

    logger = log.Logger(logname='../data/main_scale_free20191204.log', loglevel=logging.INFO, logger="experiment").get_log()
    experiment = Experiment(methods, logger)
    experiment.propagation_model = 'SI'

    start_time = clock()
    print "Starting..."
    d = data.Graph("../data/scale-free.ba.v500.e996.gml", weighted=1)
    d.debug = False

    test_num =100

    print 'Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges()

    '''
    不加BFSA的大数据集，40到60
    '''
    # test_category = experiment.RANDOM_TEST
    # experiment.start(d, test_category, test_num, 20, 46, 5)

    # test_category = experiment.FULL_TEST
    # experiment.start(d, test_category, test_num, 20, 46, 5)

    '''
    
    1 加BFSA的小数据集
    '''
    test_category = experiment.RANDOM_TEST
    experiment.start(d, test_category, test_num, 5, 10, 1)
    end_time = clock()
    print "Running time:", end_time-start_time


