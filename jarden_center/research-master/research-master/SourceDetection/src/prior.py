# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx

import method


class Uniform(method.Method):
    """The prior for a node to be the source is uniform.
    """

    def detect(self):
        """detect the source with the uniform prior.
        Returns:
            @rtype:int
            the detected source
        """
        self.reset_centrality()
        centrality = {u:1 for u in self.subgraph.nodes()}
        print('统一先验为')
        print(centrality)
        nx.set_node_attributes(self.subgraph, 'centrality', centrality)
        return self.sort_nodes_by_centrality()
