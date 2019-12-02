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
        Please refer to the my paper for more details.
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
        weights = self.data.weights
        for v in infected_nodes:
            """find the approximate upper bound by greedy searching"""
            included.clear()
            neighbours.clear()
            included.add(v)
            neighbours.add(v)
            likelihood = 1
            w = {}  # effective propagation probabilities: node->w
            w[v] = 1
            w_sum = 1
            ratio_max_node = v
            while len(included) < n:
                # w_sum = sum([w[j] for j in neighbours])
                u = ratio_max_node
                likelihood *= w[u] / w_sum
                included.add(u)
                neighbours.remove(u)
                new = nx.neighbors(self.data.graph, u)
                for h in new:
                    if h in included:
                        continue
                    neighbours.add(h)
                    # compute w for h
                    w_h2u = weights[self.data.node2index[u],self.data.node2index[h]]
                    if h in w.keys():
                        w[h] = 1-(1-w[h])*(1-w_h2u)
                    else:
                        w[h] = w_h2u

                w_sum = sum([w[j] for j in neighbours])
                ratio_max = 0.0

                """select the next node to maximize the ratio of w/sum"""
                for h in neighbours:
                    r = w_sum-w[h]
                    h_neighbors = nx.neighbors(self.data.graph, h)
                    for k in h_neighbors:
                        if k in included:
                            continue
                        w_h2k = weights[self.data.node2index[h]][self.data.node2index[k]]
                        if k in neighbours:
                            r = r-w[k]+ 1-(1-w[h])*(1-w_h2k) # update previous w[k]
                        else:
                            r += w_h2k
                    r = w[h]/r
                    if r>ratio_max:
                        ratio_max = r
                        ratio_max_node = h



            posterior[v] = (decimal.Decimal(self.prior[v])* decimal.Decimal(likelihood) * rumor_centralities[v])
        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        return self.sort_nodes_by_centrality()
