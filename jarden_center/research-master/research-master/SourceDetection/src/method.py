# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx
import data

class Method:
    """the parent class (or interface) for all detection methods, such as rumor center, jordan center.
    It defines some common functions.
    """
    subgraph = nx.Graph()
    source = ''  # the detected source node
    method_name = ''
    data = ''

    def __init__(self):
        self.method_name = self.__class__
        self.reset_centrality()

    def __init__(self):
        """
        Args:
            @type data: data.Graph
        """
        self.method_name = self.__class__

    def set_data(self, data):
        self.data = data
        self.subgraph = data.subgraph
        self.reset_centrality()

    def reset_centrality(self):
        """reset the centrality for every node."""
        centrality = {u: 0 for u in nx.nodes(self.subgraph)}
        # print('centrality中心性初始化')
        # print(centrality)
        nx.set_node_attributes(self.subgraph, 'centrality', centrality)

    def detect(self):
        """detect the source.
        Returns:
            @rtype:int
            the detected source
        """
        return self.sort_nodes_by_centrality()

    def sort_nodes_by_centrality(self):
        result = nx.get_node_attributes(self.subgraph, 'centrality')
        result = sorted(result.items(), key=lambda d: d[1], reverse=True)

        print('sort_node_by_centrality调用，将RC先验放置')
        print('RC的中心性result')
        print(result)
        return result