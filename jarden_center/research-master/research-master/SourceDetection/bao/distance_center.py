# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx

import method


class DistanceCenter(method.Method):
    """
        detect the source with distance centrality.
        The distance centrality of node v is the reciprocal of its Closeness Centrality.
        Please refer to the following paper for more details about Closeness Centrality .
        Freeman L C. Centrality in social networks conceptual clarification[J]. Social networks, 1978, 1(3): 215-239.
    """

    def detect(self):
        """detect the source with distance centrality.

        Returns:
            @rtype:int
            the detected source
        """
        self.reset_centrality()
        centrality = nx.closeness_centrality(self.subgraph, distance='weight')
        nx.set_node_attributes(self.subgraph, 'centrality', centrality)
        return self.sort_nodes_by_centrality()
