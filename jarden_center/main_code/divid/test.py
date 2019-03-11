import networkx as nx
import matplotlib.pyplot as plt
import  csv

import random


#读取文件中边关系，然后成为一个成熟的图
def  ContractDict(dir,G):

    with open(dir, 'r') as f:
        for line in f:
            line1=line.strip().split("\t")
            G.add_edge(int(line1[0]),int(line1[1]))
    # print (G.number_of_edges())
    return G






















#  制造这个图
Ginti = nx.Graph()
#初始化图
for index in range(0,6417):
    Ginti.add_node(index)

#构建图
G=ContractDict('as_Second.txt',Ginti)
print (list(G.neighbors( 0)))

#  先给全体的Cn、Scn的0的赋值。
for index in range(0,6417):
 G.add_node(index, Cn=0,Scn=1)
print (G.nodes[6416]['Scn'])


G.add_node(1,Cn=0)


G.add_node(1,Cn=1)
print (G.nodes[1]['Cn'])