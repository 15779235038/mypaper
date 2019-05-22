import networkx as nx
import random

from queues1 import *


# from Girvan_Newman import GN #引用模块中的函数

# 读取文件中边关系，然后成为一个成熟的图,是有一个有效距离的。这里需要加


'''
有效距离的定义：度大点的传播距离较远。目前只有一个指标：根据度数的大小。度数越大，与他相连的边的权重越大。
越不容易传播、越可能在距离比较远的时间传播。以此为方法定义权重。
'''
from sklearn import preprocessing

import  numpy as np
np.set_printoptions(threshold=np.inf)
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
            randomnum=random.random()
            G.add_edge(edge[0], edge[1], weight=1)
            # G.add_edge(edge[0],edge[1],weight=effectDistance(randomnum))
    return G

import math



def  effectDistance(probily):
    return 1-math.log(probily)

def sigmoid(num):
    sig_L = 0
    sig_L=(1/(1+np.exp(-num)))
    return sig_L


def Normalization(x):
    return [(float(i)-min(x))/float(max(x)-min(x)) for i in x]


def Algorithm1(G, SourceList, time_sum):
    '''
    我们认为时间片是有问题的，这个时间片应该就是按照，不能是每隔一个时间片就传染一波。只能说每隔一个时间片就记录
    一线。传播也有有概率的。
    '''
    # 算法重写，需要有个时间片的概念。还要有
    #每个传播节点都需要传播，让我们看看那些节点都需要传播。
    simqueue = Queues()

    for j in range(len(SourceList)):
        '''
        每次传播是完全随机的，但是度大的点被传播和转发的概率比较低，按照一个度数来排列。'''

        for time in range(0, time_sum):
            infection_list = []
            infectilist_every_time = []
            simqueue.enqueue(SourceList[j])
            G.node[SourceList[j]]['SI'] = 1
            # while(not(simqueue.empty())):
            if simqueue.size() == 1:
                infectilist_every_time.append(simqueue.dequeue())
            else:
                for i in range(simqueue.size()):
                    # print ('输出每次的队列数目'+str(simqueue.size()))
                    infectilist_every_time.append(simqueue.dequeue())
            print ('每次需要传染的节点'+str(infectilist_every_time))
            print ('-----------------------------')
            for infectionNode in infectilist_every_time:
                G.node[infectionNode]['SI'] = 1
                for sourceNeightor in list(G.neighbors(infectionNode)):
                    if sourceNeightor not in infection_list:  # 感染过得节点就不要再感染了。
                            # randomnum=random.random()
                            # number__=1/G.adj[infectionNode][sourceNeightor]['weight']
                            # # print (number__)
                            # # print (number__)  #传播概率还是太小
                            # if  number__>randomnum:   #如果effection  distance对应的路程比它大，就可以传播过去。
                            #按照距离来估计能否被感染
                                G.node[sourceNeightor]['SI'] = 1  # 传染点
                                # 现在就要给那些观察点加时间了。
                                infection_list.append(sourceNeightor)  # 加入感染点
                                simqueue.enqueue(sourceNeightor)
                                # print (simqueue.size())
                                # 传染边
                                G.adj[infectionNode][sourceNeightor]['Infection']=2


    return G











#产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
def  contractSource(G,sourceNum,sourceMaxDistance):

    # # # 产生2个节点，看看。设定一个值3。表示这个点度比较小。且两个点距离较小。
    # flag=1
    # while(flag):
    #     rumorSourceList = []
    #     while  (len(rumorSourceList)!=2):
    #         random_RumorSource = random.randint(0, 4039)
    #         if random_RumorSource not in rumorSourceList:
    #             if G.degree(random_RumorSource) < 15:
    #                 rumorSourceList.append(random_RumorSource)
    #
    #     print('源点个数' + str(len(rumorSourceList)))
    #     #产生源点距离大于5.小于7
    #     if  len(nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))>6  and len(nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))<10 :
    #         flag=0
    #
    # # 查看产生随机源点的个数2，并且他们距离为3.
    # print('源点个数' + str(len(rumorSourceList)))
    # print ('源点距离'+str(nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight')))
    rumorSourceList=[796,950]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 950

    return rumorSourceList


import  csv

def   ConvertGToCsv(G,dir):
    # python2可以用file替代open
    with open(dir, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source", "target", "weight"])
        for u, v in G.edges():
            # print (G.adj[u][v]['Infection'])
            writer.writerow([u, v, G.adj[u][v]['Infection']])
#传播子图代入

def   ConvertGToCsvSub(G,dir):
    # python2可以用file替代open
    with open(dir, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["source", "target", "weight"])
        for u, v in G.edges():
            # print (G.adj[u][v]['Infection'])
            writer.writerow([u, v, G.adj[u][v]['weight']])






#随机产生两源点。
def  randomSourcelist(subinfectG):
    nodelist = []
    for node in subinfectG:
        nodelist.append(node)
    slice = random.sample(nodelist, 2)
    print('随机产生的源点是' + str(slice))
    return  slice




#
def   contactu1h1u2h2(subinfectG):
    max=0
    #如何找到如何找到一个图的边界。
    #从0到100赋予h作为值。
    for h  in range(3,10):
        #需要根据h找到一些随机源点。把能形成这个圆（u1,h1）的所有点定下。
        #构建这样两个圆出来
        sourclist = randomSourcelist(subinfectG)
        if calEu1h1u2h2( sourclist[0],h,sourclist[1],h,subinfectG)>max:
            max=calEu1h1u2h2( sourclist[0],h,sourclist[1],h,subinfectG)
    print (max)
    return slice




def   calEu1h1u2h2(u1,h1,u2,h2,subinfecG):
    # 首先要验证这个u1和h1以及u2以及h2是否可以。
    queue=Queues()
    #将u1，u2附近的离它有h远的点加入这个集合。计算它作为源点的概率。
    u1InfectionList=[]
    #其实就是bfs树。
    print(5)
    return  5







#必须设计一个函数，来测试u，h是否可以适用。

def  isReceived(u,h,subinfectionG,infectionG):
     #对u进行长达h的圆构建
     print(9)
     circleNodesList=list(nx.bfs_tree(infectionG, source=u, depth_limit=h).nodes)  #这包含了这个构建的圆的所有节点。
     if  set(circleNodesList) < set(subinfectionG): #圆是子集的话就可以
        return  True
     else:
         return False









# def  getSubInfectG(G):
#
#     #如何取出这个G中的多个传播子图呢？
#

#  制造这个图
Ginti = nx.Graph()
# 初始化图,加很多节点
# for index in range(1,1005):
#     print (index)
#     Ginti.add_node(index)

# 构建图，这个图是有有效距离的。
G = ContractDict('../data/facebook_combined.txt', Ginti)

# 因为邮件是一个有向图，我们这里构建的是无向图。
print('一开始图的顶点个数', G.number_of_nodes())
print('一开始图的边个数', G.number_of_edges())



# #  先给全体的Cn、Scn,time的0的赋值。
# for index in range(0,4039):
#     G.add_node(index, SI=0)


# 初始化所有边是否感染。Infection

for  edge  in  list(G.edges):
    G.add_edges_from([(edge[0],edge[1])], Infection=1)




rumorSourceList=contractSource(G,2,3)  #产生源点。图，源点个数，源点差距距离。
infectG=Algorithm1(G,rumorSourceList,3)   #产生感染图，

#gephi 查看infectG转成csv情况。
ConvertGToCsv(infectG,'G.csv')




#取出感染子图，
SubInfectG=[]
# SubInfectG=getSubInfectG(infectG)

subinfectG=nx.Graph()

# for  node  in  infectG.nodes:
#     if infectG.node[node]['SI']==1:
#         subinfectG.add_node(node)
#


count=1
count1=1
for  edge in  infectG.edges:
    # print (edge)\
    if  infectG.adj[edge[0]][edge[1]]['Infection']==1:
       count1 =count1+1
    if  infectG.adj[edge[0]][edge[1]]['Infection']==2:
        count = count + 1
        subinfectG.add_edges_from([(edge[0],edge[1])],weight= infectG.adj[edge[0]][edge[1]]['weight'])

print (count)
print (count1)
# 因为邮件是一个有向图，我们这里构建的是无向图。
print('传染子图的顶点个数',  subinfectG.number_of_nodes())
print('传染子图的边个数',  subinfectG.number_of_edges())


ConvertGToCsvSub(subinfectG,'SubInfectionG.csv')
#

#检测是否是有相互感染到。



print (nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))
print (nx.shortest_path(subinfectG, rumorSourceList[0], rumorSourceList[1], weight='weight'))


# all_short_length=[]
# #求任意两点之间的最短路径。
# for  node1 in subinfectG.nodes:
#     for node2 in  subinfectG.nodes:
#         if node1==node2:
#             pass
#         else:
#             all_short_length.append(nx.dijkstra_path_length(G, node1, node2, weight='weight'))  # 求最短距离
#
# print (max(all_short_length))


#随机生成u1，h1,u2.h2来让E(u1,h1,u2,h2)最大。

# contactu1h1u2h2(subinfectG)