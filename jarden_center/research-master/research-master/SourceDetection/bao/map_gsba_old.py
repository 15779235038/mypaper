# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import decimal

import networkx as nx

import method
import rumor_center
import math
from blist import blist


class GSBA(method.Method):
    """detect the source with Greedy Search Bound Approximation.
        Please refer to the conference paper for more details.
    """
    prior = ''
    prior_detector = None

    def __init__(self, prior_detector):
        method.Method.__init__(self)
        self.method_name = self.__class__, prior_detector.method_name
        self.prior_detector = prior_detector

    def detect(self):
        """detect the source with GSBA.

        Returns:
            @rtype:int
            the detected source
        """
        self.reset_centrality()
        self.prior_detector.set_data(self.data)
        self.prior_detector.detect()
        self.prior = nx.get_node_attributes(self.subgraph, 'centrality')

        self.reset_centrality()
        rc = rumor_center.RumorCenter()
        rc.set_data(self.data)
        rc.detect()
        rumor_centralities = nx.get_node_attributes(self.subgraph, 'centrality')

        self.reset_centrality()
        infected_nodes = set(self.subgraph.nodes())
        n = len(infected_nodes)
        posterior = {}
        included = set()
        neighbours = set()
        # weights = self.data.weights
        weights = 0.1 # for unweighted graphs
        for v in infected_nodes:
            """find the approximate upper bound by greedy searching"""
            included.clear()
            neighbours.clear()
            included.add(v)
            neighbours.add(v)
            likelihood = 1
            while len(included) < n-1:
                max_num_bridge_edges = -1
                max_num_bridge_edges_ratio = -1
                max_id = None
                for u in neighbours:
                    if max_id is None:
                        max_id = u
                    count = 0
                    new = nx.neighbors(self.data.graph, u)
                    for h in new:
                        if h in included:
                            count += 1
                    temp = count*1.0/(len(neighbours)+len(new)-2*count)
                    if temp>max_num_bridge_edges_ratio:
                        max_num_bridge_edges_ratio = temp
                        max_num_bridge_edges = count
                        max_id = u
                if max_num_bridge_edges == 0:
                    likelihood = 1
                else:
                    likelihood *= max_num_bridge_edges*1.0/len(neighbours)
                neighbours.remove(max_id)
                included.add(max_id)
                new = nx.neighbors(self.subgraph, max_id)
                for h in new:
                    if h not in included:
                        neighbours.add(h)
            posterior[v] = (decimal.Decimal(self.prior[v])* decimal.Decimal(likelihood) * rumor_centralities[v])
        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        return self.sort_nodes_by_centrality()
