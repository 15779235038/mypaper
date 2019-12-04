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

        # 进行所有点有向树构建，再进行层次遍历。针对每一层都进行传播点/全部的比例计算。
        node_every_ratio = []
        for node_every in list(subInfectG.nodes()):
            # 进行BFS树构造，
            tree = nx.bfs_tree(infectG, source=node_every)
            # 进行层次遍历。返回每一层顶点。
            BFS_nodes = self.BFS_nodes(tree, node_every, infectG)
            ratio_all = 0
            for layer_node in BFS_nodes:
                infect_node_len = len([x for x in layer_node if infectG.node[x]['SI'] == 2])
                # print('infect_node_len',infect_node_len)
                infect_node_not = len([x for x in layer_node if infectG.node[x]['SI'] == 1])
                # print('infect_node_not', infect_node_not)
                infect_ratio = infect_node_len / len(layer_node)  # 感染点的比例
                ratio_all += infect_ratio
            ratio_average = ratio_all / len(BFS_nodes)
            node_every_ratio.append([node_every, ratio_average])

        node_every_ratio_sort = sorted(node_every_ratio, key=lambda x: x[1], reverse=True)
        print(node_every_ratio_sort)






        temp_nodes = self.subgraph.nodes()
        for source in self.subgraph.nodes():
            # 进行BFS树构造，
            tree = nx.bfs_tree(self.data.graph, source=source)
            # 进行层次遍历。返回每一层顶点。
            BFS_nodes = self.BFS_nodes(tree, source, self.data.graph,self.subgraph)
            ratio_all = 0
            for layer_node in BFS_nodes:
                infect_node_len = len([x for x in layer_node if x in temp_nodes])
                infect_ratio = infect_node_len / len(layer_node)  # 感染点的比例
                ratio_all += infect_ratio
            ratio_average = ratio_all / len(BFS_nodes)
            centrality[source] = Decimal(ratio_average)

        print('让我看下这个ratio _average的centiality')
        print(centrality)
        nx.set_node_attributes(self.subgraph, 'centrality',centrality)
        return self.sort_nodes_by_centrality()



    def BFS_nodes(self,tree, source, infectG,subgraph):
        queue = []
        queue.append(source)
        layer_node = []
        layer_node.append([source])
        while queue:
            temp_layer_node = []
            for i in queue:
                for neighbour in list(nx.neighbors(tree, i)):
                    if neighbour != i:
                        temp_layer_node.append(neighbour)
            # 如果某一层的被感染点为0，就退出。不用再加了。
            if len([x for x in temp_layer_node if x in subgraph.nodes() ])== 0:
                break
            layer_node.append(temp_layer_node)
            queue = temp_layer_node

        return layer_node

