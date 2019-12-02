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
import map_gsba3 as gsba3
import map_rsa as rsa

import numpy as np
from experiment import Experiment
import  sys
if __name__ == '__main__':
    print( '先验知识的源点定位')
    prior_detector0 = prior.Uniform()
    prior_detector1 = rc.RumorCenter()
    prior_detector2 = dmp2.DynamicMessagePassing()
    prior_detector3 = dc.DistanceCenter()
    prior_detector4 = jc.JordanCenter()
    prior_detector5 = ri.ReverseInfection()


    print('      只有0，1，3，4作为先验了，                  2，和5的消息传播和反转算法没有作为先验知识，可能是因为他们的点没有分数')
    methods = [gsba.GSBA(prior_detector0), gsba.GSBA(prior_detector1), gsba.GSBA( prior_detector3),
               gsba.GSBA(prior_detector4), gsba3.GSBA(prior_detector0), gsba3.GSBA(prior_detector1), gsba3.GSBA( prior_detector3),
               gsba3.GSBA(prior_detector4)]






    print ()
    print('输出日志')

    logger = log.Logger(logname='../data/main_scale_free3.log', loglevel=logging.INFO, logger="experiment").get_log()



    print    ('跑实验了，打logger。 这是实验类对象，只初始化而已')
    experiment = Experiment(methods, logger)
    print   ('定义传播模型      ')
    experiment.propagation_model = 'SI'

    start_time = clock()
    print ("Starting...")
    # print(sys.path)
    print ('构建图' )
    d = data.Graph("scale-free.ba.v500.e996.gml", weighted=1)
    d.debug = False
    print('测试数量为100')
    test_num = 3
    print('输出图的大小，和边数目')
    print ('Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges())
    print('测试策略是随机测试，随机挑选一个点作为源点')
    test_category = experiment.RANDOM_TEST
    print('开始实验')
    experiment.start(d, test_category, test_num, 10, 41, 1)
    print('测试策略是完全，每个点都有机会成为源点')
    test_category = experiment.FULL_TEST
    print ('开始实验')
    experiment.start(d, test_category, test_num, 10, 41, 1)
    end_time = clock()
    print( "Running time:", end_time-start_time)