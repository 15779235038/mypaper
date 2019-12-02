# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx

import method


class ReverseInfection(method.Method):
    """detect the source with ReverseInfection.
        Please refer to the following paper for more details.
        Zhu K, Ying L. Information source detection in the SIR model: a sample-path-based approach[J].
        IEEE/ACM Transactions on Networking, 2016, 24(1): 408-421.
    """

    def detect(self):
        """detect the source with ReverseInfection.

        Returns:
            @rtype:int
            the detected source
        """
        self.reset_centrality()
        stop = 0
        t = 0
        n = len(nx.nodes(self.subgraph))
        ids_received = {}  # the ids and corresponding time one node has received
        ids_waiting = {}  # the ids and time one node will received in the next round

        """initialize"""
        for u in nx.nodes(self.subgraph):
            ids_received[u] = dict()
            ids_waiting[u] = dict()
            ids_waiting[u][u] = {'level': 0, 'time': 0}
            # for w in neighbors:
            #     ids_waiting[w][u] = t+1

        weight = nx.get_edge_attributes(self.subgraph, 'weight')
        while stop < n:
            # print 't=', t
            for u in nx.nodes(self.subgraph):
                for v in ids_waiting[u].keys():
                    if ids_waiting[u][v]['level'] == t:
                        if v not in ids_received[u].keys():
                            ids_received[u][v] = ids_waiting[u][v]['time']
                            # u send v to its neighbours
                            neighbors = nx.all_neighbors(self.subgraph, u)
                            for w in neighbors:
                                if v not in ids_received[w].keys():
                                    if (u,w) in weight.keys():
                                        delay = weight[(u,w)]
                                    else:
                                        delay = weight[(w,u)]
                                    ids_waiting[w][v] = {'level': t+1, 'time': ids_received[u][v] + delay}
                        ids_waiting[u].pop(v)
                # print ids_received[u], u
                # print ids_waiting[u]
                if len(ids_received[u]) == n:
                    nx.set_node_attributes(self.subgraph, 'centrality', {u: 1 / sum(ids_received[u].values())})
                    stop += 1

            t += 1

        return self.sort_nodes_by_centrality()
