# coding=utf-8


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : data_graph.py
# @Author: zhiqiangbao
# @Date  : 2019/12/23




import   networkx as nx
import matplotlib.pyplot as plt
def listToTxt(listTo, dir):
    fileObject = open(dir, 'a')
    fileObject.write(str(listTo).replace('(','').replace(')','').replace(',',' '))
    fileObject.write('\n')
    fileObject.close()

def ContractDict(dir, G):
    with open(dir, 'a') as f:
        for line in f:
            line1 = line.split()
            G.add_edge(int(line1[0]), int(line1[1]))
    for edge in G.edges:
        G.add_edge(edge[0], edge[1], weight=1)
        # G.add_edge(edge[0],edge[1],weight=effectDistance(randomnum))
    print(len(list(G.nodes)))
    # G.remove_node(0)
    print(len(list(G.nodes)))
    return G

# G=nx.full_rary_tree(3,2000)   #生成规定节点数目的3叉树



# G=nx.fast_gnp_random_graph(5000,p=0.05) #生成随即图

G=nx.random_graphs.barabasi_albert_graph(500,2)  #生成无标度图，

print('isconnect？',nx.is_connected(G))
Gc = max(nx.connected_component_subgraphs(G), key=len)

for  edge  in Gc.edges():
    listToTxt(edge,'scale_network/500/500scale_free2.txt')










