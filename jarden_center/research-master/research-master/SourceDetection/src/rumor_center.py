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


class RumorCenter(method.Method):
    """
        detect the source with Rumor Centrality.
        Please refer to the following paper for more details.
        Shah D, Zaman T. Detecting sources of computer viruses in networks: theory and experiment[J].
        ACM SIGMETRICS Performance Evaluation Review, 2010, 38(1): 203-214.
    """

    visited = set()  # node set
    bfs_tree = nx.Graph()

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
        for source in self.subgraph.nodes():
            self.bfs_tree = nx.bfs_tree(self.subgraph, source)
            self.visited.clear()
            self.get_number_in_subtree(source)
            centrality[source] = Decimal(math.factorial(self.bfs_tree.number_of_nodes())) \
                         / nx.get_node_attributes(self.bfs_tree, 'cumulativeProductOfSubtrees')[source]

        nx.set_node_attributes(self.subgraph, 'centrality',centrality)
        return self.sort_nodes_by_centrality()

    def get_centrality(self, u):
        """get centralities for all nodes by passing a message from the root to the children.

        Args:
            u:
        """
        self.visited.add(u)
        centrality = 0
        if u == self.source:
            """p is the root node in the bfs_tree."""
            centrality = Decimal(math.factorial(self.bfs_tree.number_of_nodes())) \
                         / nx.get_node_attributes(self.bfs_tree, 'cumulativeProductOfSubtrees')[u]
        else:
            parent = nx.get_node_attributes(self.bfs_tree, 'parent')[u]
            numberOfNodesInSubtree = nx.get_node_attributes(self.bfs_tree, 'numberOfNodesInSubtree')[u]
            centrality = nx.get_node_attributes(self.bfs_tree, 'centrality')[parent] * numberOfNodesInSubtree / (
                self.bfs_tree.number_of_nodes() - numberOfNodesInSubtree)
        centrality = centrality
        nx.set_node_attributes(self.bfs_tree, 'centrality', {u: centrality})
        nx.set_node_attributes(self.subgraph, 'centrality', {u: centrality})

        children = nx.all_neighbors(self.bfs_tree, u)
        for c in children:
            if c not in self.visited:
                self.get_centrality(c)

    def get_number_in_subtree(self, p):
        """passing messages from children nodes to the parent, to get the number of nodes in the subtree rooted by p,
        and the cumulative product of the size of the subtrees of all nodes in p' subtree.

        Args:
            p: parent node
        Returns:
            @rtype:Decimal()
        """
        self.visited.add(p)
        numberOfNodesInSubtree = 1  # for node p
        cumulativeProductOfSubtrees = Decimal(1)  # for node p

        children = nx.all_neighbors(self.bfs_tree, p)
        for u in children:
            if u not in self.visited:
                nx.set_node_attributes(self.bfs_tree, 'parent', {u: p})
                self.get_number_in_subtree(u)
                numberOfNodesInSubtree += nx.get_node_attributes(self.bfs_tree, 'numberOfNodesInSubtree')[u]
                cumulativeProductOfSubtrees *= nx.get_node_attributes(self.bfs_tree, 'cumulativeProductOfSubtrees')[u]
        cumulativeProductOfSubtrees = Decimal(cumulativeProductOfSubtrees)*Decimal(numberOfNodesInSubtree)
        nx.set_node_attributes(self.bfs_tree, 'numberOfNodesInSubtree', {p: numberOfNodesInSubtree})
        nx.set_node_attributes(self.bfs_tree, 'cumulativeProductOfSubtrees', {p: cumulativeProductOfSubtrees})
