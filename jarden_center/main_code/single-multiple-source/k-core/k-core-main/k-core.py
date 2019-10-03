#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/10/2 12:46 下午

# @Author  : baozhiqiang

# @File    : k-core.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************

import  commons
import  networkx as nx
class findk_core:
    def __init__(self):
        pass

    def main(self, dir):
            '''
            走来不要那么难，先搞定树吧。才能继续搞定图。
            :return:
            '''
            pre = '../../data/'
            last = '.txt'
            self.initG = commons.get_networkByFile(fileName=pre + dir + last)  # 获取图，
            max_sub_graph = commons.judge_data(self.initG)
            source_list = commons.product_sourceList(max_sub_graph, self.fix_number_source)
            self.true_Source_list = source_list
            self.infectG = commons.propagation1(max_sub_graph, self.true_Source_list)  # 开始传染

            subinfectG = commons.get_subGraph(self.infectG)
            subinfectG.to_undirected()
            subinfectG.remove_edges_from(subinfectG.selfloop_edges())
            data = nx.core_number(subinfectG)

            # Graph.to_undirected()
            print('data', data)
            data_sort = sorted(data.items(), key= lambda x :x[1], reverse= True)
            print('data_sort', data_sort)
            print('max-core',data_sort[0][1])
            core_number1 = 0
            #看下源点在那一层。
            for  node,core_number in data_sort:
                if node in source_list:
                    print('node,core_number',[node,core_number])
                    core_number1 = core_number
            return core_number1

    def cal_distanceError(self, dir):
            self.fix_number_source = 1
            distance = 0
            for i in range(20):
                self.main(dir)
                distance += self.main(dir)
            result = distance / 20
            # 导入time模块
            import time
            # 打印时间戳
            # print(time.time())
            pre = './result/'
            last = '.txt'
            with open(pre + dir + 'first' + last, 'a') as f:
                f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
                f.write(str(20) + '     ' + str(dir) + '    ' + str(result))
            print(distance / 20)



test = findk_core()
filename = 'CA-GrQc'


test.cal_distanceError(filename)






