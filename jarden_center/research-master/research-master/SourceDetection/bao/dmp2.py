# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import networkx as nx
import numpy as np

import method


class DynamicMessagePassing(method.Method):
    """detect the source with DynamicMessagePassing.
        Please refer to the following paper for more details.
        Lokhov, Andrey Y., et al. "Inferring the origin of an epidemic with a dynamic message-passing algorithm."
        Physical Review E 90.1 (2014): 012801.
    """

    def detect(self):
        """detect the source with DynamicMessagePassing.

        Returns:
            @rtype:int
            the detected source
        """
        self.reset_centrality()
        nodes = self.data.graph.nodes()
        nodes_infected = self.subgraph.nodes()
        n = self.data.graph.number_of_nodes()
        n_i = self.subgraph.number_of_nodes()
        a = nx.adjacency_matrix(self.data.graph, weight=None).todense()  # adjacent matrix
        weights = np.asarray(nx.adjacency_matrix(self.data.graph, weight='weight').todense()) # infection probability
        mu = np.zeros(n)  # recover probability
        diameter = 1* nx.diameter(self.subgraph)
        likelihoods = {}  # the likelihood, P(o|i), in Eq. 21.
        epsilon = 0.00001
        theta = np.ones([2, n, n])  # theta[k][i] as the probability that the infection signal has not been passed
        # from node k to node i up to time t in the dynamics Di
        phi = np.zeros([2, n, n])
        pij_s = np.zeros([2, n, n])
        p_sir = np.zeros([2, n_i, n, 3])  # time-source-node-state (SIR): probability
        ps0 = np.zeros([n, 3])  # the probability nodes i is s, i ,r at time 0

        for s in np.arange(n_i):
            """initialize"""
            theta[0, :, :] = 1
            theta[1, :, :] = 0
            phi[1, :, :] = 0
            pij_s[0, :, :] = 0
            s_index = self.data.node2index[nodes_infected[s]]
            p_sir[0, s, :, 0] = ps0[:, 0] = 1 # S
            p_sir[0, s, :, 1] = ps0[:, 1] = 0 # I
            p_sir[0, s, s_index, 0] = ps0[s_index, 0] = 0
            p_sir[0, s, s_index, 1] = ps0[s_index, 1] = 1
            p_sir[0, s, :, 2] = ps0[:, 2] = 0
            phi[0] = np.repeat(ps0[:,1], n).reshape(n,n)
            pij_s[0] = np.repeat(ps0[:,0], n).reshape(n,n)

            """estimate the probabilities, P_s P_r P_I at time t"""
            likelihoods[s] = np.ones([diameter + 1])
            t = 0
            while t < diameter:
                t += 1
                t_current = t % 2
                t_previous = (t - 1) % 2
                theta[t_current] = theta[t_previous] - np.multiply(weights, phi[t_previous])
                theta[t_current][np.where(np.abs(theta[t_current]) <= epsilon)] = epsilon

                p_sir[t_current, s, :, 0] = np.multiply(ps0[:, 0],
                                                np.exp((np.dot(a, np.log(theta[t_current, :, :]))).diagonal()))
                p_sir[t_current, s, :, 2] = 0  # nodes only have two states: susceptible, infected
                p_sir[t_current, s, :, 1] = 1 - p_sir[t_current, s, :, 0] - p_sir[t_current, s, :, 2]
                for i in np.arange(n):
                    denominator = np.multiply(theta[t_current, :, i], a[i, :])
                    denominator[np.where(denominator == 0)] = 1
                    pij_s[t_current, i] = np.divide(p_sir[t_current, s, i, 0], denominator)

                phi[t_current] = np.multiply(np.multiply(1 - weights, 1 - mu), phi[t_previous]) - (
                    pij_s[t_current] - pij_s[t_previous])

                """compute the likelihood by Eq. 21"""
                for v in self.data.graph.nodes():
                    if v in self.subgraph.nodes():
                        likelihoods[s][t] *= p_sir[t_current, s, self.data.node2index[v], 1]
                    else:
                        likelihoods[s][t] *= p_sir[t_current, s, self.data.node2index[v], 0]

        """select t0 to maximizes the partition function Z(t) = \sum_{node i}{P(o|i)}"""
        max_zt = -1
        t0 = 0
        for t in np.arange(1, diameter + 1):
            zt = np.sum(np.asarray(likelihoods.values())[:, t])
            # print zt
            if zt > max_zt:
                max_zt = zt
                t0 = t
        centrality = {}
        for v in np.arange(n_i):
            centrality[nodes_infected[v]] = likelihoods[v][t0]
        nx.set_node_attributes(self.subgraph, 'centrality', centrality)
        del theta, phi, pij_s, p_sir, ps0
        return self.sort_nodes_by_centrality()
