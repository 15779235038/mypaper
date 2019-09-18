#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/18 6:37 下午

# @Author  : baozhiqiang

# @File    : test.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************



'''
统计好每个图的各种中心性输入到文件中。
'''
import  networkx as nx
def ContractDict( dir, G):
    '''
    :param dir:
    :param G:    从文件中拿点
    :return:
    '''
    with open(dir, 'r') as f:
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


def get_networkByFile(fileName):
        #  制造这个图
        Ginti = nx.Graph()
        # 构建图，这个图是有有效距离的。
        G = ContractDict(fileName, Ginti)
        # 因为邮件是一个有向图，我们这里构建的是无向图。
        print('一开始图的顶点个数', G.number_of_nodes())
        print('一开始图的边个数', G.number_of_edges())
        return G


'''
设计csv文件。
每一行都是我能发现的中心性。
 #本函数给出一个分级的图中点。除了单源定位的点，我这里的点都是分级的。明白？
 分级的意思就是我会设定一个各种中心性的最优秀点，以这个点为源点进行BFS。分层
 采样进行蒙特卡洛抽样。
'''
import csv
def ConvertGToCsv(G, dir):
        '''
        :param G:
        :param dir:
        :return:
        '''



        #介数中心性
        between_dict = nx.betweenness_centrality(G)
        sort_eccentricity_dict = sorted(between_dict.items(), key= lambda x:x[1],reverse=True)
        print('sort_eccenritci_dict', sort_eccentricity_dict)


        #   接近度中心性
        closeness_centrality = nx.closeness_centrality(G)
        sort_colse_centrality_dict = sorted(closeness_centrality.items(), key= lambda x:x[1],reverse=True)
        print('sort_colse_centrality_dict', sort_colse_centrality_dict)


        #   度中心性
        degree_centrality = nx.degree_centrality(G)
        sort_degree_centrality =sorted(degree_centrality.items(), key= lambda x:x[1],reverse=True)
        print('sort_degree_centrality', sort_degree_centrality)







        with open(dir, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(sort_eccentricity_dict)
            writer.writerow(sort_colse_centrality_dict)
            writer.writerow(sort_degree_centrality)





from collections import  defaultdict




'''

返回BFS每一层的节点，以键值对形式返回。层数：节点。

'''
def test_BFS_node(G,source_node= 686,depth= 3,):
    dfs_successor = nx.dfs_successors(G, source=source_node, depth_limit=depth)
    print(dfs_successor)
    stack = []
    dfs_result = defaultdict(list)
    depth = 0
    stack.append(source_node)
    while len(stack) > 0:
         node_list = stack
         temp = []
         for i in list(node_list):
            if i in dfs_successor.keys():
                for neighbour in dfs_successor[i]:
                     temp.append(neighbour)
                     dfs_result[depth].append(neighbour)
         depth += 1
         stack = temp

    print(dfs_result)
    return dfs_result









pre = '../data/'
last = '.txt'
# filename = 'facebook_combined'
# filename = 'email-Eu-core'
filename = 'treenetwork3000'
initG = get_networkByFile(pre+filename+last)
test_BFS_node(initG)
# ConvertGToCsv(initG, filename+'.csv')