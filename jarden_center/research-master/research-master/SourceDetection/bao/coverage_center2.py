# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import math
from decimal import *

import method
from data import *


class CoverageCenter(method.Method):
    """
        detect the source with Rumor Centrality.
        Please refer to the following paper for more details.
        Shah D, Zaman T. Detecting sources of computer viruses in networks: theory and experiment[J].
        ACM SIGMETRICS Performance Evaluation Review, 2010, 38(1): 203-214.
    """

    visited = set()  # node set
    bfs_tree = nx.Graph()


    '''   
    1 加二阶邻域覆盖率，给每个点加一个覆盖率就是覆盖率参数。
    2 

    '''
    def detect(self):
        """detect the source with Rumor Centrality.
        Returns:
            @rtype:int
            the detected source
        """
        if self.subgraph.number_of_nodes() == 0:
            print 'subgraph.number_of_nodes =0'
            return

        self.reset_centrality()
        centrality = {}
        for source in self.subgraph.nodes():
            neighors = nx.neighbors(self.data.graph,source)
            neighors2_list=[]
            for node in neighors:
                neighors2=nx.neighbors(self.data.graph,node)
                neighors2_list.extend(neighors2)
            neighors2_list.extend(neighors)
            sets = set(list(neighors2_list))
            infect_nei = [ x for x in sets if x in self.subgraph.nodes()]
            infect_neilen = len(infect_nei)-1
            print('附近2层节点')
            print(sets)
            print('被感染有多少个')
            print(infect_neilen)

            centrality[source] = Decimal(infect_neilen*1.0/len(sets))
        nx.set_node_attributes(self.subgraph, 'centrality',centrality)
        return self.sort_nodes_by_centrality()





