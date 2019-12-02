# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx
import method


class JordanCenter(method.Method):
    """
        detect the source with Jordan centrality.
        Please refer to the following paper for more details.
        Jordan C. Sur les assemblages de lignes[J]. J. Reine Angew. Math, 1869, 70(185): 81.\
    """

    def detect(self):
        """detect the source with JordanCenter.

        Returns:
            @rtype:int
            the detected source
        """
        self.reset_centrality()
        distances = nx.all_pairs_dijkstra_path_length(self.subgraph, weight='weight')
        centrality = {}
        for u in nx.nodes(self.subgraph):
            row = dict(distances[u])
            k = max(row, key=row.get)
            centrality[u] = 1.0 / row[k]
        nx.set_node_attributes(self.subgraph, 'centrality', centrality)
        return self.sort_nodes_by_centrality()