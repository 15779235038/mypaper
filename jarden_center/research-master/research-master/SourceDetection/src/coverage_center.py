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
    1 加覆盖率，给每个点加一个覆盖率就是覆盖率参数。
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
            neighors=nx.neighbors(self.data.graph,source)
            # print(source)
            # print('source和它的邻居')
            # print(neighors)
            infect_nei = [ x for x in neighors if x in self.subgraph.nodes()]
            infect_neilen = len(infect_nei)
            centrality[source] = Decimal(infect_neilen*1.0/len(neighors))
        nx.set_node_attributes(self.subgraph, 'centrality',centrality)




        return self.sort_nodes_by_centrality()





