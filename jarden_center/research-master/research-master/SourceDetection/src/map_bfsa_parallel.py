# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx
import numpy as np
from decimal import *
import method
import itertools
import multiprocessing

import copy_reg
import types
from functools import partial

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class BFSA(method.Method):
    """detect the source with Greedy Search Bound Approximation with parallel programming.
    It is more efficient than map_bfsa.py when the number of infected nodes is larger than 8.
        Please refer to the my paper for more details.
    """
    prior = ''
    prior_detector = None
    visited = set()  # node set

    def __init__(self, prior_detector):
        method.Method.__init__(self)
        self.method_name = self.__class__, prior_detector.method_name
        self.prior_detector = prior_detector
        self.bfs_trees = {}
        self.likelihoods = {}
        self.permutation_likelihood = {}
        self.depths = {}
        self.descendants = {}

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
        nodes = self.subgraph.nodes()
        self.weights = self.data.weights
        self.node2index = self.data.node2index
        n = len(nodes)
        for v in nodes:
            self.bfs_trees[v] = nx.bfs_tree(self.subgraph, v)
            self.likelihoods[v] = multiprocessing.Value('d', 0.0)
            #self.values[v] = multiprocessing.Value('d', 0.0)
            self.descendants[v] = {}
            self.depths[v] = {}
            self.visited.clear()
            self.find_descendants_bfs(v, v)

        multiprocessing.freeze_support()
        processes = list()
        for i in np.arange(0, n):
            nodes[0], nodes[i] = nodes[i], nodes[0]
            p = multiprocessing.Process(target=self.get_likelihood_by_BFSA, args=(nodes, 1, n - 1))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()

        #self.get_likelihood_by_BFSA2(nodes)
        #self.get_likelihood_by_BFSA(nodes, 0, len(nodes) - 1)

        posterior = {v: Decimal(self.prior[v]) * Decimal(self.likelihoods[v].value) for v in nodes}

        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        return self.sort_nodes_by_centrality()

    def find_descendants_bfs(self, root, u,depth=0):
        """Find the descendants and depth for a node in self.bfs_trees[root]"""
        self.depths[root][u] = depth
        self.descendants[root][u] = set()
        self.visited.add(u)
        children = nx.all_neighbors(self.bfs_trees[root], u)
        for c in children:
            if c not in self.visited:
                self.find_descendants_bfs(root, c, depth+1)
                self.descendants[root][u].update(self.descendants[root][c])
        self.descendants[root][u].add(u)

    def get_likelihood_by_BFSA2(self, nodes):
        permutations = itertools.permutations(nodes)
        n = len(nodes)
        for p in permutations:
            permitted = True
            for i in np.arange(1, n):
                # None of nodes[0,..,i-1] are descendants of nodes[i]
                result = [p[j] not in self.descendants[p[0]][p[i]] for j in np.arange(0, i)]
                if False in result:
                    permitted = False
                    break

                # for j in npy.arange(1, i):
                #     if p[j] in self.descendants[p[0]][p[i]]:
                #         permitted = False
                #         break
            if permitted:
                self.likelihoods[p[0]] += self.compute_likelihood(p)

    def get_likelihood_by_BFSA(self,  nodes, p, q ):
        """extends Heap's permutation generating algorithm.
        Permitted permutation: each node has a certain depth at which it will be found.
        Args:
            nodes: a list of all nodes
            p: the starting index
            q: the end index
        Returns:
        """
        if p == q:
            for i in np.arange(1, q+1):
                # None of nodes[0,..,i-1] are descendants of nodes[i]
                result = [nodes[j] not in self.descendants[nodes[0]][nodes[i]] for j in np.arange(0, i)]
                if False in result:
                    return

                # for j in npy.arange(1, i):
                #     if nodes[j] in self.descendants[nodes[0]][nodes[i]]:
                #         return
            l = self.compute_likelihood(nodes)
            self.likelihoods[nodes[0]].value += l
            # self.permutation_likelihood[nodes[0]].append(l)
            # self.values[nodes[0]].value = self.values[nodes[0]].value+l
            # print nodes, l, self.likelihoods[nodes[0]]
            return l
        else:
            for i in np.arange(p, q + 1):
                nodes[p], nodes[i] = nodes[i], nodes[p]
                self.get_likelihood_by_BFSA(nodes, p + 1, q)
                nodes[p], nodes[i] = nodes[i], nodes[p]

    def compute_likelihood(self, nodes):
        """get P(G|v) by Equation (11);
        Args:
            nodes: a permitted permutation
        Returns:
        """
        likelihood = 1
        neighbours = set()
        neighbours.add(nodes[0])
        w = {} # effective propagation probabilities: node->w
        w[nodes[0]] = 1
        visited = set()
        for i in np.arange(0, len(nodes)):
            u = nodes[i]
            visited.add(u)
            w_sum = sum([w[j] for j in neighbours])
            likelihood *= w[u]/w_sum
            neighbours.remove(u)
            new = nx.neighbors(self.data.graph, u)

            for h in new:
                if h in visited:
                    continue
                # compute w for h
                w_h2u = self.weights[self.node2index[u]][self.node2index[h]]
                if w.has_key(h):
                    w[h] = 1 - (1 - w[h]) * (1 - w_h2u)
                else:
                    w[h] = w_h2u
                neighbours.add(h)
        return likelihood
