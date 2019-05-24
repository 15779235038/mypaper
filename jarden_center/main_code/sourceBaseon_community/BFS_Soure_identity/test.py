import networkx as nx
import random

import pandas as pd
from queues import *
# from Girvan_Newman import GN #引用模块中的函数

#读取文件中边关系，然后成为一个成熟的图
def  ContractDict(dir,G):
    with open(dir, 'r') as f:
        for line in f:
            line1=line.split()
            # print (line1)
            G.add_edge(int(line1[0]),int(line1[1]))
    # print (G.number_of_edges())
    return G




import csv

def  txt_Csv(dir):
    sourceNode=[]
    tailNode=[]
    weight=[]
    with open(dir, 'r') as f:
        for line in f:
            line1=line.strip().split(' ')
            print (len(line1))
            sourceNode.append(int(line1[0]))
            tailNode.append(int(line1[1]))
            weight.append(1)
    # 字典中的key值即为csv中列名
    dataframe = pd.DataFrame({'source': sourceNode, 'target': tailNode,'weight':weight})
    # 将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("G.csv", index=False, sep=',')

    return 1






G=nx.Graph
GRetrun=txt_Csv('data/facebook_combined.txt')

