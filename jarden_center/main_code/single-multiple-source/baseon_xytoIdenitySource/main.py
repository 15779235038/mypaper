import networkx as nx
import random
from networkx.algorithms import community
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
            G.add_edge(edge[0], edge[1], weight=1)
            # G.add_edge(edge[0],edge[1],weight=effectDistance(randomnum))

    #数据预处理，去掉0这个点。很容易坏事。
    # G.remove_node(0)
    # print (G.number_of_nodes())
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


def Algorithm1(G, SourceList, time_sum,hlist):
    '''
    我们认为时间片是有问题的，这个时间片应该就是按照，不能是每隔一个时间片就传染一波。只能说每隔一个时间片就记录
    一线。传播也有有概率的。
    '''
    #this  are  two point to  传播
    #每个传播节点都需要传播，让我们看看那些节点都需要传播
    nodelist=[]
    edgelist=[]
    infectionNodelist=[]
    for j in range(len(SourceList)-1):
        nodelist=list(nx.bfs_tree(G, source=SourceList[j], depth_limit=3).nodes)  # 这包含了这个构建的圆的所有节点。
        edgelist = list(nx.bfs_tree(G, source=SourceList[j], depth_limit=3).edges)
        for i in nodelist:
            G.node[i]['SI'] = 2
        for  k  in  edgelist:
            G.adj[k[0]][k[1]]['Infection']=2
        print ('头两个感染社区点数为'+str(len(nodelist)))

    #第3个源点传播。
    nodelist=list(nx.bfs_tree(G, source=SourceList[2], depth_limit=2).nodes)
    edgelist = list(nx.bfs_tree(G, source=SourceList[2], depth_limit=2).edges)
    for j in nodelist:
        G.node[j]['SI'] = 2
    for l in edgelist:
        G.adj[l[0]][l[1]]['Infection'] = 2
    print('第三个感染社区点数为'+str(len(nodelist)))
    return G













#产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
def  contractSource(G,sourceNum,sourceMaxDistance):
    #now  I  want  produce  three  point ,   two  point  have  commbine  region with  each other,one  point have
    # more  distance with  that  two point ,in this algorithm .two point have,so  need to product a  point away form
    #two  point
    # # 产生2个节点，看看。设定一个值3。表示这个点度比较小。且两个点距离较小。
    # flag=1
    # while(flag):
    #     rumorSourceList = []
    #     while  (len(rumorSourceList)!=2):
    #         random_RumorSource = random.randint(0, 4039)
    #         if random_RumorSource not in rumorSourceList:
    #                 rumorSourceList.append(random_RumorSource)
    #     print('源点个数' + str(len(rumorSourceList)))
    #     #产生源点距离大于5.小于7
    #     if  len(nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))>6  and len(nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))<10 :
    #         flag=0
    #
    # # 查看产生随机源点的个数2，并且他们距离为3.
    # print('源点个数' + str(len(rumorSourceList)))
    # print ('源点距离'+str(nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight')))
    rumorSourceList=[125,4022]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 950


    #produce  a  point away form  rumorSourceList  that  distance are  6
    point =9999
    for  node  in G.nodes:
        try:
            if nx.shortest_path_length(G, node, rumorSourceList[0]) > 6 and nx.shortest_path_length(G, node,rumorSourceList[1]) >7:
                point = node
                break
        except:
            continue
    rumorSourceList.append(point)
    print('真实两源感染区域是'+str(rumorSourceList)+'另一个感染点区域是'+str(point))

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








def  getTuresubinfectionG(infectG,randomInfectionsource):
    #put  nehibour  infectNode in this partion, stop by  this  infect  communiy  hehibour  have no  infectNode
    firstPartion=[]
    firstPartion.append(randomInfectionsource)
    flag=0
    while(flag==0):
        print('这个firstpartion是多少？'+str(firstPartion))
        print (list(infectG.neighbors(firstPartion[0])))
        for  infetcionnode  in firstPartion:
            for  neighbor  in  list(infectG.neighbors(infetcionnode)):
                if infectG.node[neighbor]['SI']==2:
                    # print('这个点是' + '已经被感染的')
                    if neighbor not in  firstPartion:  # 已经加过过得节点就不要再感染了。
                        firstPartion.append(neighbor)
        # print ('这一圈形成的firstpartion是'+str(len(firstPartion)))
        #chenk in  firstPartion ,who have no  infectionNode  in  neighbor
        neighborList=[]
        for node  in firstPartion:
            for   neighbor  in  list(infectG.neighbors(node)):
                    if  neighbor not in  firstPartion:
                        neighborList.append(infectG.node[neighbor]['SI'])
        if  2  in neighborList:
            print ('这个社区周围还有被感染点')
            pass
        elif  2 not in neighborList:
            print('这个社区周围没有被感染点')
            flag=1


    print ('输出这个感染社区'+str(len(firstPartion)))
    return firstPartion








def  multiplelistTo_ormialy(mutiolist):
    alllist=[]
    for  i  in  range(len(mutiolist)):
        for j  in  range(len(mutiolist[i])):
            alllist.append(mutiolist[i][j])
    return alllist








def  getmultipleCommunity(infectionG):
    #return  multipleCommuniytlist
    multipleCommuniytlist=[]

    # start  by  a  random  SInode
    randomInfectionNode = 0
    # sum  nodes  in  infect G:
    sum = infectionG.number_of_nodes()
    flag1= 0
    flag2=0
    flag=0
    while flag == 0:

            infectionList=[]
            allList=[]
            diff_list=[]
            #刚开始啥社区都没有
            if  len(multipleCommuniytlist)==0:
                print ('在没有社区的操作')
            #刚开始随机产生一个点。
                while flag1 == 0:
                    randomnumber = random.randint(1, sum)
                    if infectG.node[randomnumber]['SI'] == 2:
                        randomInfectionNode = randomnumber
                        flag1 = 1
                print('随机开始的点感染点' + str(randomInfectionNode))
                partion = getTuresubinfectionG(infectionG,randomInfectionNode)
                multipleCommuniytlist.append(partion)  # 第一个社区
            else:
                print('在已经有社区的操作')
                #总的点集合-已经找到的社区节点=在这里继续找。

                infectionList=multiplelistTo_ormialy(multipleCommuniytlist)
                allList=list(infectionG.nodes)
                diff_list = list(set(allList).difference(set(infectionList)))
                print ('在总的区里面，但不在已经分好的社区里面。'+str(len(diff_list)))
                while flag2 == 0:
                    randomnumber =random.sample(diff_list, 1)
                    if infectionG.node[randomnumber[0]]['SI'] == 2:
                        randomInfectionNode =randomnumber[0]
                        flag2 = 1
                print('随机开始的点感染点' + str(randomInfectionNode))
                partion = getTuresubinfectionG(infectionG,randomInfectionNode)
                multipleCommuniytlist.append(partion)  #
            #终止条件,剩下社区没有被感染点了。
            haveinfectionList = multiplelistTo_ormialy(multipleCommuniytlist)
            allList = list(infectionG.nodes)
            diff_list_ = list(set(allList).difference(set( haveinfectionList)))
            restList=[]
            for i  in diff_list_:
               restList.append(infectionG.node[i]['SI'])
            if  2  in restList:
                print('有感染点在restList中，')
                pass
            elif 2  not in restList:
                print('已经没有感染点在restList中，')
                flag=1

    print ('感染社区个数以及各自人数')
    print (len(multipleCommuniytlist))
    print(len(multipleCommuniytlist[0]))
    if  125  in  multipleCommuniytlist[0]  and 4022  in  multipleCommuniytlist[0]:
        print ('头两个源点在的')
    print(len(multipleCommuniytlist[1]))
    return multipleCommuniytlist



#随机产生一个源点。
def  randomSourcelist(subinfectG):
    nodelist = []
    for node in subinfectG:
        nodelist.append(node)
    slice = random.sample(nodelist, 1)
    print('随机产生的源点是' + str(slice))
    sllietemp=slice[0]
    return  sllietemp



#单源就从离心率找吧
#从subinfectinG中寻找node的邻居中具有最小Eccentricity的节点。离心越近.就以他返回。
def findBigEccentricity(h,node,subinfectG,infectionG):

    #这个感染图中，最小离心率是？这个暂时卡住了，怎么办？那么先假装实现，
    minecceity=10
    for  i  in subinfectG.nodes:
        if  nx.eccentricity(subinfectG,i)<minecceity:
            minecceity=nx.eccentricity(subinfectG,i)
    print ('查看最小离心率'+str(minecceity))
    print ('这个h下的错误节点为'+str(node))
    minEccentricity=nx.eccentricity(subinfectG,node)
    print( '它的偏心率为'+str(minEccentricity))

    ecctemp=0
    minEccentricitynnode=0
    print('从他的邻居节点找离心率最小的')  #或者找离中心近的。
    for  heighbour in  list(subinfectG.neighbors(node)):
        ecctemp=nx.eccentricity(subinfectG,heighbour)
        if ecctemp<minEccentricity:
            minEccentricity=ecctemp
            minEccentricitynnode=heighbour
    #如果没有离心率更小的话，就返回源点。
    return  minEccentricitynnode

    #
    # #直接从邻居中找一个当前h下能行不就可以吗？有时候邻居节点都不行，那就只能从整个感染子图中找了
    # newnodes=5000
    # for heighbour in list(subinfectG.neighbors(node)):   #这只能找一圈节点。
    #        print('那么这个点'+str(node)+'的邻居节点'+str(heighbour)+'试试看效果')
    #        if  isReceived(heighbour,h,subinfectG,infectionG)==True:
    #             print ('在邻居中找到的可行节点为'+str(heighbour))
    #             newnodes= heighbour
    #             break
    #
    #
    # allnodelist=list(nx.bfs_tree(subinfectG,source=TurerumorSource1,depth_limit=sourceh).nodes)
    # if newnodes==5000:
    #     print ('对不起，他的邻居节点找不到满足h='+str(h)+'的点了，从第一个感染点的感染区域中找了')
    #     for i in list( allnodelist):  # 这只能找一圈节点。
    #         print('从第一个感染图子图找到的第一个邻居节点是' + str(i))
    #         if isReceived(i, h, subinfectG, infectionG) == True:
    #             print('从第一个感染子图找到的可行节点为' + str(i))
    #             newnodes = i
    #             break
    #
    #     if  newnodes==5000:
    #         print ('从第一个感染感染图都找不到了，返回原点吧')
    #         return node
    #     else:
    #         print('从第一个感染子图中找到了的节点为' + str( newnodes))
    #         print('重新找的节点为的偏心率' + str(nx.eccentricity(subinfectG,  newnodes)))
    #         return  newnodes
    #
    #
    # else:
    #     print('找到邻居节点满足h=' + str(h) + '的点')
    #     print('重新找的节点为的偏心率' + str(nx.eccentricity(subinfectG, newnodes)))
    #     return newnodes






def isReceived(u, h, subinfectionG, infectionG):
    # 对u进行长达h的圆构建
    circleNodesList = list(nx.bfs_tree(infectionG, source=u, depth_limit=h).nodes)  # 这包含了这个构建的圆的所有节点。
    subinfectionList = list(subinfectionG.nodes)  # 传染子图的所有点。
    # 计算列表相似度试试看
    # print ('感染源的h节点集合为'+str(circleNodesList))

    count = 0
    for i in circleNodesList:
        if i in subinfectionList:
            count = count + 1
    similir = count / len(circleNodesList)
    print('u,h对应圆重和subinfectionG图的重合比例为' + str(similir))
    if similir > 0.9:
        print('这里的' + str(u) + '和h是' + str(h) + '是可以在subinfection中存在的')
        return True
    else:
        print('这里的' + str(u) + '和h是' + str(h) + '是不可以在subinfection中存在的，返回false')
        return False

    # if  set(circleNodesList) < set(subinfectionList): #圆是子集的话就可以，这里是可以放宽条件的。比如说只要重合概率达到90%就可以
    #    print ('这里的u，h是可以在subinfection中存在的')
    #    return  True
    # else:
    #     print('这里的u，h是不行的在subinfection中')
    #     return False

import   matplotlib
def   findmultiplesource(singleRegionList,infectionG):
      #首先需要判断是否多源。不断找源点去对这个区域。
      tempGraph=nx.Graph()
      for  edge in infectionG.edges:
          if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
              if edge[0] in singleRegionList and edge[1] in singleRegionList:
                  tempGraph.add_edges_from([edge],weight=1)
      print ('这个感染区域的传播子图边个数')
      print (tempGraph.number_of_edges())


      #求出这个区域最远的路径出来。返回这个区域半径。
      print('这个感染区域的传播半径')
      # maxh=nx.radius(tempGraph)
      '''请将tempGrap投影到x，y轴上，利用gephi图的方法。然后将这个图的边界点都挑选出来。
      1  构建垂直平分线。
      2  通过多个边界点构建的垂直平分线确定圆心，如果构建的圆心list都集中某个区域，就认为是单源。
      #   如果这个构建的heart list太离谱，小于某个阙值。就认为多源。再重新取局部边界顶点，确立新的圆心list。多源定位。
      4  这样单源就确立了，直接jarder  center  。如果多源的话，通过刚才确定的圆心和边界点。确立感染区域，重新jarder center定位。
      '''
      #首先第一步，将这个tempGra圆投影到x，y轴。
      #让我看看这个图
      ConvertGToCsvSub(tempGraph,'tempGraph.csv')
      nx.draw_kamada_kawai(tempGraph)















def   multiplePartion(mutiplelist,infectionG):

     #所有单源list
     allsigleList=[]
     siglelist=[]
     #将第一个传播区域定下来。
     iglelist=findmultiplesource(mutiplelist[0],infectionG)











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



#  先给全体的Cn、Scn,time的0的赋值。
for index in range(G.number_of_nodes()):
    G.add_node(index, SI=1)


# 初始化所有边是否感染。Infection
for  edge  in  list(G.edges):
    G.add_edge(edge[0],edge[1], Infection=1)




rumorSourceList=contractSource(G,3,5)  #产生源点。图，源点个数，源点差距距离。
hlist=[3,2]   #不同传播区域传播深度，
infectG=Algorithm1(G,rumorSourceList,5,hlist )  #产生感染图，深度是3

#gephi 查看infectG转成csv情况。
ConvertGToCsv(infectG,'G.csv')
subinfectG=nx.Graph()
count=1
count1=1
for  edge in  infectG.edges:
    # print (edge)\
    if  infectG.adj[edge[0]][edge[1]]['Infection']==1:
       count1 =count1+1
    if  infectG.adj[edge[0]][edge[1]]['Infection']==2:
        count = count + 1
        subinfectG.add_edges_from([(edge[0],edge[1])],weight= 1)

print (count)
print (count1)
# 因为邮件是一个有向图，我们这里构建的是无向图。
print('传染子图的顶点个数',  subinfectG.number_of_nodes())
print('传染子图的边个数',  subinfectG.number_of_edges())


ConvertGToCsvSub(subinfectG,'SubInfectionG.csv')
#
#检测是否是有相互感染到。

print (nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))
print (nx.shortest_path(subinfectG, rumorSourceList[0], rumorSourceList[1], weight='weight'))  #在子图中有路径，就是感染到了。

try:
   print(nx.shortest_path(subinfectG, rumorSourceList[1], rumorSourceList[2], weight='weight'))

except:
    print ('嗯，这里选的第三个点跟第2个源点是可以的，放心。图并没有连通。')
    try:
        print(nx.shortest_path(subinfectG, rumorSourceList[0], rumorSourceList[2], weight='weight'))

    except:
        print('嗯，这里选的第三个点跟第1个源点是可以的，放心。图并没有连通。')
# print (nx.shortest_path(subinfectG, rumorSourceList[1], rumorSourceList[2], weight='weight'))    #这个报错就是第三个point并没有被感染到的意思。

#now  to  practice single-multiple  source Partition.Get  ture  parition

multipList=getmultipleCommunity(infectG)

multiplePartion(multipList,infectG)