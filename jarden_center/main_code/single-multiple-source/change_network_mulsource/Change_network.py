#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/11 2:05 上午

# @Author  : baozhiqiang

# @File    : Different_time.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************





'''

1  生成一系列静态网络，代表传播过程。可直接利用一个小数据构建。设定一个5%的增加边，在动态之中寻找源点。
    这样可以构建t0，t1，。。。。。tn的矩阵，每一个都是m维的向量。t0，t1为固定时间间隔。
        （m是网络节点个数）

2  矩阵构建完毕，我们知道整个传播过程这是一个m*n矩阵。但是我们只知道我们只能获取谣言已经发生的某些
    比如t5，t6，t7的连续一段传播情况。我们也不知道5的存在。

3  那么这个好像高中学过的，给一列有规律的数，取其中一段，请写出第一个数字是多少。每个数字之间靠的
动态传播。不过我们这里是其中一段的传播情况，包含第一个到第几个元素数字在里面。




'''



'''
思路2：
    构建多个网络，每个时间段都会动态增删一定数量的边。进行传播。
    对第一个网络进行BFS构建，找到k个源点。
    第二个网络帮助对k的M远的点进行BFS构建。
            首先对形成的k个图第一个进行BFS，确定源点。然后第二个图只进行那几个源点的
   M远的点进行BFS构建即可。
考虑：这样的话，那多个网络只是让结果跟精确一点？没体现价值啊？

'''
class  FindSource:
    def __init__(self,  G):
        self.initG = G  #原始图
        self.k = None   #k个图
        self.change_ratio = None  #动态图改动比例
        self.infect_ratio = None #初始图感染比例
        self.findSource_list = None  #当前找到的源的list
        self.findSource_set = None    #当前找到的源的set
        self.infecG = None # 感染图
        self.fix_number_source = None  #确定的源数目
        self.source_list  = None #确定下来的源数目。

    def   constract_Infection_netWork(self,G,infect_ratio):
        '''

        :param G:
        :param infect_ratio:
        :return:  按照感染比例感染的图
        '''


    def  Constract_ManynetWrok(self, infectG, K, ratio):
        '''
        :param infectG:   #感染图
        :param K:           #再次改动K次
        :param ratio:       #每次改动比例
        :return:            #返回每次改动的传染图
        '''
        # for i  in range(K):



    def Constract_BFS(self,infectG, fix_Number_source):
        '''

        :param infectG:    #感染图
        :param fix_Number_source:  #确定的源数目
        :return:                #返回源的id
        '''




