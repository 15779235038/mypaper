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
import pytrie

class BFSA(method.Method):
    """detect the source with Greedy Search Bound Approximation.
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
        self.depths = {}
        self.descendants = {}
        self.permutation_likelihood = {}  # key->value(prefix_likelihood, neighbours, w)

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
        for v in nodes:
            self.bfs_trees[v] = nx.bfs_tree(self.subgraph, v)
            self.likelihoods[v] = 0
            self.descendants[v] = {}
            self.depths[v] = {}
            self.visited.clear()
            self.find_descendants_bfs(v, v)
        # for i in npy.arange(1, len(nodes)):
        #     nodes[0], nodes[i] = nodes[i], nodes[0]
            # self.get_likelihood_by_BFSA(nodes, 1, len(nodes) - 1)
        self.get_likelihood_by_BFSA2(nodes)
        #self.get_likelihood_by_BFSA(nodes, 0, len(nodes) - 1)
        posterior = {v: Decimal(self.prior[v]) * Decimal(self.likelihoods[v]) for v in nodes}
        nx.set_node_attributes(self.subgraph, 'centrality', posterior)
        self.permutation_likelihood.clear()
        self.bfs_trees.clear()
        self.descendants.clear()
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


    def get_likelihood_by_BFSA(self, nodes, p, q):
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

            self.likelihoods[nodes[0]] += self.compute_likelihood(nodes)
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
        w = {}  # effective propagation probabilities: node->w
        w[nodes[0]] = 1
        visited = set()

        for i in np.arange(0, len(nodes)):
            u = nodes[i]
            w_sum = sum([w[j] for j in neighbours])
            likelihood *= w[u] / w_sum
            neighbours.remove(u)
            new = nx.neighbors(self.data.graph, u)
            visited.add(u)

            for h in new:
                if h in visited:
                    continue
                # compute w for h
                w_h2u = self.weights[self.data.node2index[u]][self.data.node2index[h]]
                if w.has_key(h):
                    w[h] = 1 - (1 - w[h]) * (1 - w_h2u)
                else:
                    w[h] = w_h2u
                neighbours.add(h)
        return likelihood

    def compute_likelihood_buffered(self, nodes):
        """get P(G|v) by Equation (11);
        Args:
            nodes: a permitted permutation
        Returns:
        """
        likelihood = 1
        neighbours = set()
        w = {} # effective propagation probabilities: node->w

        "load likelihood, neighbours, w from buffers"
        start_index = -1
        for i in range(len(nodes), 0, -1):
            if self.permutation_likelihood.has_key(nodes[0:i]):
                start_index = i
                # prefix = self.permutation_likelihood[nodes[0:i]]
                likelihood, neighbours, w = self.permutation_likelihood[nodes[0:i]]
                neighbours = neighbours.copy()
                w = w.copy()
                break
        if start_index is -1:
            neighbours.add(nodes[0])
            w[nodes[0]] = 1
            start_index = 0

        visited = set()
        visited.update(nodes[0:start_index])

        for i in np.arange(start_index, len(nodes)):
            u = nodes[i]
            w_sum = sum([w[j] for j in neighbours])
            likelihood *= w[u]/w_sum
            neighbours.remove(u)
            new = nx.neighbors(self.data.graph, u)
            visited.add(u)

            for h in new:
                if h in visited:
                    continue
                # compute w for h
                w_h2u = self.weights[self.data.node2index[u]][self.data.node2index[h]]
                if w.has_key(h):
                    w[h] = 1 - (1 - w[h]) * (1 - w_h2u)
                else:
                    w[h] = w_h2u
                neighbours.add(h)
            if i<6:
                "add to buffers"
                self.permutation_likelihood[nodes[0:(i+1)]] = likelihood, neighbours.copy(), w.copy()
        return likelihood
