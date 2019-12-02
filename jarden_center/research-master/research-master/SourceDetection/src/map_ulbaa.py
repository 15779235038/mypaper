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


class ULBAA(method.Method):
    """detect the source with lower and upper Bound Approximation.
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
            likelihood_upper = 1
            w = {}  # effective propagation probabilities: node->w
            w_key_sorted = blist()
            w[v] = 1
            w_key_sorted.append(v)
            while len(included) < n:
                w_sum = sum([w[j] for j in neighbours])
                u = w_key_sorted.pop()  # pop out the last element from w_key_sorted with the largest w
                likelihood_upper *= w[u] / w_sum
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
                    # h_neighbor = nx.neighbors(self.data.graph, h)
                    # w_h = 1
                    # for be in included.intersection(h_neighbor):
                    #     w_h *= 1 - self.data.get_weight(h, be)
                    # w[h] = 1 - w_h
                    """insert h into w_key_sorted, ranking by w from small to large"""
                    if h in infected_nodes:
                        if h in w_key_sorted:
                            w_key_sorted.remove(h)  # remove the old w[h]
                        k = 0
                        while k < len(w_key_sorted):
                            if w[w_key_sorted[k]] > w[h]:
                                break
                            k += 1
                        w_key_sorted.insert(k,h)
                        #w_key_sorted[k:k] = [h]

            """find the approximate lower bound by greedy searching"""
            included.clear()
            neighbours.clear()
            included.add(v)
            neighbours.add(v)
            likelihood_lower = 1
            w = {}  # effective propagation probabilities: node->w
            w_key_sorted = blist()
            w[v] = 1
            w_key_sorted.append(v)
            while len(included) < n:
                w_sum = sum([w[j] for j in neighbours])
                u = w_key_sorted.pop()  # pop out the last element from w_key_sorted with the largest w
                likelihood_lower *= w[u] / w_sum
                included.add(u)
                neighbours.remove(u)
                new = nx.neighbors(self.data.graph, u)
                for h in new:
                    if h in included:
                        continue
                    neighbours.add(h)
                    # compute w for h
                    w_h2u = weights[self.data.node2index[u], self.data.node2index[h]]
                    if h in w.keys():
                        w[h] = 1 - (1 - w[h]) * (1 - w_h2u)
                    else:
                        w[h] = w_h2u
                    """insert h into w_key_sorted, ranking by w from large to small"""
                    if h in infected_nodes:
                        if h in w_key_sorted:
                            w_key_sorted.remove(h)  # remove the old w[h]
                        k = 0
                        while k < len(w_key_sorted):
                            if w[w_key_sorted[k]] < w[h]:
                                break
                            k += 1
                        w_key_sorted.insert(k, h)
                        # w_key_sorted[k:k] = [h]
            likelihood = decimal.Decimal(likelihood_lower + likelihood_upper)*rumor_centralities[v]/2
            posterior[v] = decimal.Decimal(self.prior[v])* likelihood
        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        return self.sort_nodes_by_centrality()
