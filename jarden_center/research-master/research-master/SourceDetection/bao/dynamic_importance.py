# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx
import numpy as np
import numpy.linalg

import method


class DynamicImportance(method.Method):
    """detect the source with Dynamic Importance.
        Please refer to the following paper for more details.
        Fioriti V, Chinnici M. Predicting the sources of an outbreak with a spectral technique[J].
            arXiv preprint arXiv:1211.2333, 2012.
    """

    def detect(self):
        """detect the source with Dynamic Importance.

        Returns:
            @rtype:int
            the detected source centrality
        """
        print('光谱法，重置中心性')
        self.reset_centrality()
        print('获取邻接矩阵')
        adjacent_matrix = nx.adjacency_matrix(self.subgraph, weight='weight').toarray()
        print('获得邻接矩阵的特征值')
        eigenvalues = nx.adjacency_spectrum(self.subgraph, weight='weight')
        print('获得最大特征值')
        eigenvalue_max = max(eigenvalues)
        i = 0
        print('删除每个顶点，然后操作。')
        for u in nx.nodes(self.subgraph):
            adjacent_matrix_new = np.delete(adjacent_matrix, i, 0)  # remove the row for node u
            adjacent_matrix_new = np.delete(adjacent_matrix_new, i, 1)  # remove the column for node u
            eigenvalue_max_new = max(numpy.linalg.eigvals(adjacent_matrix_new))
            nx.set_node_attributes(self.subgraph, 'centrality',
                                   {u: abs(eigenvalue_max - eigenvalue_max_new) / eigenvalue_max})
            i += 1

        return self.sort_nodes_by_centrality()
