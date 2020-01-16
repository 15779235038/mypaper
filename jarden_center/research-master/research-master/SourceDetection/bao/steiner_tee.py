#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : steiner_tee.py
# @Author: zhiqiangbao
# @Date  : 2020/1/13
import  networkx as nx




import decimal
import networkx as nx


from time import clock

import logging
import networkx as nx
import data



from itertools import combinations, chain
from itertools import tee, chain

def pairwise(iterable, cyclic=False):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = tee(iterable)
    first = next(b, None)
    if cyclic is True:
        return zip(a, chain(b, (first,)))
    return zip(a, b)
from networkx.utils import  not_implemented_for
def metric_closure(G, weight='weight'):
    """  Return the metric closure of a graph.

    The metric closure of a graph *G* is the complete graph in which each edge
    is weighted by the shortest path distance between the nodes in *G* .

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    NetworkX graph
        Metric closure of the graph `G`.

    """
    M = nx.Graph()

    Gnodes = set(G)

    # check for connected graph while processing first node
    # nx.all_pairs_shortest_path()
    all_paths_iter = nx.all_pairs_dijkstra(G, weight=weight)
    nx.all_pairs_dijkstra_path()
    print("nihao")
    print(all_paths_iter)
    for i in all_paths_iter:
        print(i)
        print()


    u, (distance, path) = next(all_paths_iter)
    if Gnodes - set(distance):
        msg = "G is not a connected graph. metric_closure is not defined."
        raise nx.NetworkXError(msg)
    Gnodes.remove(u)
    for v in Gnodes:
        M.add_edge(u, v, distance=distance[v], path=path[v])

    # first node done -- now process the rest
    for u, (distance, path) in all_paths_iter:
        Gnodes.remove(u)
        for v in Gnodes:
            M.add_edge(u, v, distance=distance[v], path=path[v])

    return M




def steiner_tree(G, terminal_nodes, weight='weight'):
    """ Return an approximation to the minimum Steiner tree of a graph.

    Parameters
    ----------
    G : NetworkX graph

    terminal_nodes : list
         A list of terminal nodes for which minimum steiner tree is
         to be found.

    Returns
    -------
    NetworkX graph
        Approximation to the minimum steiner tree of `G` induced by
        `terminal_nodes` .

    Notes
    -----
    Steiner tree can be approximated by computing the minimum spanning
    tree of the subgraph of the metric closure of the graph induced by the
    terminal nodes, where the metric closure of *G* is the complete graph in
    which each edge is weighted by the shortest path distance between the
    nodes in *G* .
    This algorithm produces a tree whose weight is within a (2 - (2 / t))
    factor of the weight of the optimal Steiner tree where *t* is number of
    terminal nodes.

    """
    # M is the subgraph of the metric closure induced by the terminal nodes of
    # G.
    M = metric_closure(G, weight=weight)
    # Use the 'distance' attribute of each edge provided by the metric closure
    # graph.
    H = M.subgraph(terminal_nodes)
    mst_edges = nx.minimum_spanning_edges(H, weight='distance', data=True)
    # Create an iterator over each edge in each shortest path; repeats are okay
    edges = chain.from_iterable(pairwise(d['path']) for u, v, d in mst_edges)
    T = G.edge_subgraph(edges)

    return T


'''
基于度量的最小steiner树版本。
1 生成完全图，
2 找出最小生成树的图


两个参数： 一个是传播子树，一个是终端节点

'''
def  MSTbyMetric_closure(G,terminal_nodes):
    M = nx.Graph()
    Gnodes = set(G)
    for u in  Gnodes:
        for v in Gnodes:
            if u!=v:
                weigth_temp=nx.dijkstra_path_length(G,source=u,target=v,weight='weight')
                M.add_edge(u,v,weight=weigth_temp)

    '''      M是完全图，其中每个点到其他店都有边，边权重是是其在原图的最短路径距离。'''
    H = M.subgraph(terminal_nodes)
    mst_edges = nx.minimum_spanning_edges(H, weight='weight', data=True)

    '''              基于我们构建的完全图的最小生成树边'''
    # F=M.subgraph(terminal_nodes)
    F= nx.Graph()
    edge_list =[]
    for edge_shortest in mst_edges:
        #找出其路径,最小mst——edges树
        print('edge_shortest')
        path=nx.dijkstra_path(G,source=edge_shortest[0],target=edge_shortest[1],weight='weight')
        for i  in range(len(path)-1):
            edge_list.append([path[i],path[i+1]])
    print('最后找到的edge_list')
    print(edge_list)
    for edge in edge_list:
        F.add_edge(edge[0],edge[1],weight=G[edge[0]][edge[1]]['weight'])

    print(F.number_of_edges())
    return F



















    pass









if __name__ == "__main__":


    start_time = clock()
    print("Starting...")
    # data就是我们的图，我们可以做一些操作。      创建一个简单的图。试试看结果。
    ''' 
    1 创建例子的图
    2 给定传播点子图

    '''

    infected = set()
    infected.add(1)
    infected.add(2)
    infected.add(4)
    d = data.Graph("../data/test.txt", weighted=1)
    print(d.graph.number_of_edges())
    print(d)
    d.debug = False
    test_num = 1
    print(d.subgraph)
    # print(infected)
    # d.subgraph= d.graph

    d.subgraph = nx.Graph()
    d.subgraph = nx.subgraph(d.graph, ['1', '2', '4'])
    print('子图节点个数')
    print(d.subgraph.nodes())
    print(d.graph.nodes())

    print('Graph size: ', d.graph.number_of_nodes(), d.graph.number_of_edges())
    T=MSTbyMetric_closure(d.graph,['1', '2', '4'])
    print('T是什么？')
    print(T.number_of_nodes())