# # encoding=utf-8
# from matplotlib import pyplot
# import matplotlib.pyplot as plt
#
#
# x = range(1, 6)
# y_train = [0.840, 0.839, 0.834, 0.832, 0.824]
# y_test = [0.838, 0.840, 0.840, 0.834, 0.8281]
# # plt.plot(x, y, 'ro-')
# # plt.plot(x, y1, 'bo-')
# # pl.xlim(-1, 11)  # 限定横轴的范围
# # pl.ylim(-1, 110)  # 限定纵轴的范围
#
# plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='our algorithm')
# plt.plot(x, y_test, marker='*', ms=10, label='uniprot90_test')
# plt.legend()  # 让图例生效
#
# plt.margins(0)
# plt.subplots_adjust(bottom=0.10)
# plt.xlabel('Number of sources')  # X轴标签
# plt.ylabel("Average error  (in hops)")  # Y轴标签
# plt.title("Wiki-Vote  data")  # 标题
# plt.savefig('f1.png')
# plt.show()
#


import random
list1 = ['佛山', '南宁', '北海', '杭州', '南昌', '厦门', '温州']
a = random.choice(list1)
print(type(a))





'''
这是找四源点的情况。
'''

import  networkx as nx
def ContractDict(dir, G):
    with open(dir, 'r') as f:
        for line in f:
            line1 = line.split()
            G.add_edge(int(line1[0]), int(line1[1]))

    # print (G.number_of_edges())

    #构建距离权重。
    #遍历节点，找到节点度为分布频率。在此基础上，将每个节点依照度大小排序。从而进行边的重定义。对它的边进行权重定义
    degreeList=[]

    for edge in  G.edges:
            G.add_edge(edge[0], edge[1], weight=1)
            # G.add_edge(edge[0],edge[1],weight=effectDistance(randomnum))

    #数据预处理，去掉0这个点。很容易坏事。
    # G.remove_node(0)
    # print (G.number_of_nodes())
    return G


Ginti = nx.Graph()
G = ContractDict('../data/Wiki-Vote.txt', Ginti)

# 因为邮件是一个有向图，我们这里构建的是无向图。
print('一开始图的顶点个数', G.number_of_nodes())
print('一开始图的边个数', G.number_of_edges())



#  先给全体的Cn、Scn,time的0的赋值。
for node in list(G.nodes):
    G.add_node(node, SI=1)


# 初始化所有边是否感染。Infection
for  edge  in  list(G.edges):
    G.add_edge(edge[0],edge[1], Infection=1)


#构图，找直径。先找外围，再找最长的一个路。



Gc = max(nx.connected_component_subgraphs(G), key=len)
nodelist=list(Gc)
print ('连通组件找到了')


subgrapn=nx.Graph()
#构建子图
for  edge in G.edges:
    if edge[0] in nodelist and edge[1] in nodelist:
        subgrapn.add_edges_from([edge],weight=1)


lists=nx.periphery(subgrapn)
print( lists)
max=0
resultlist=[]
for  node  in lists:
     for node1 in lists:
         if node!=node1:
             distance=nx.shortest_path_length(G,source=node,target=node1)
             print (distance)
             if  distance>max:
                 max= distance
                 resultlist.append([node,node1,max])



resultlist.sort()
print (resultlist)



