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
    G.remove_node(0)
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
    #每个传播节点都需要传播，让我们看看那些节点都需要传播
    infectionNodelist=[]
    for j in range(len(SourceList)):
        nodelist=list(nx.bfs_tree(G, source=SourceList[j], depth_limit=time_sum).nodes)  # 这包含了这个构建的圆的所有节点。
        edgelist = list(nx.bfs_tree(G, source=SourceList[j], depth_limit=time_sum).edges)
        for i in nodelist:
            G.node[i]['SI'] = 2
        for  k  in  edgelist:
            G.adj[k[0]][k[1]]['Infection']=2
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
    #             if G.degree(random_RumorSource) < 5:
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
    rumorSourceList=[125,4022]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 950
    print('真实的源点是'+str(rumorSourceList))
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


#从subinfectinG中寻找node的邻居中具有最小Eccentricity的节点。离心越近.就以他返回。
def findBigEccentricity(h,node,subinfectG,infectionG,TurerumorSource1,sourceh):

    # #这个感染图中，最小离心率是？这个暂时卡住了，怎么办？那么先假装实现，
    # minecceity=10
    # for  i  in  subinfectionG.nodes:
    #     if  nx.eccentricity(subinfectionG,i)<minecceity:
    #         minecceity=nx.eccentricity(subinfectionG,i)
    # print ('查看最小离心率'+str(minecceity))
    # print ('这个h下的错误节点为'+str(node))
    # minEccentricity=nx.eccentricity(subinfectionG,node)
    # print( '它的偏心率为'+str(minEccentricity))
    #
    # ecctemp=0
    # minEccentricitynnode=0
    # print('从他的邻居节点找离心率最小的')  #或者找离中心近的。
    # for  heighbour in  list(subinfectionG.neighbors(node)):
    #     ecctemp=nx.eccentricity(subinfectionG,heighbour)
    #     if ecctemp<minEccentricity:
    #         minEccentricity=ecctemp
    #         minEccentricitynnode=heighbour
    # #如果没有离心率更小的话，就返回源点。


    #直接从邻居中找一个当前h下能行不就可以吗？有时候邻居节点都不行，那就只能从整个感染子图中找了
    newnodes=5000
    for heighbour in list(subinfectG.neighbors(node)):   #这只能找一圈节点。
           print('那么这个点'+str(node)+'的邻居节点'+str(heighbour)+'试试看效果')
           if  isReceived(heighbour,h,subinfectG,infectionG)==True:
                print ('在邻居中找到的可行节点为'+str(heighbour))
                newnodes= heighbour
                break


    allnodelist=list(nx.bfs_tree(subinfectG,source=TurerumorSource1,depth_limit=sourceh).nodes)
    if newnodes==5000:
        print ('对不起，他的邻居节点找不到满足h='+str(h)+'的点了，从第一个感染点的感染区域中找了')
        for i in list( allnodelist):  # 这只能找一圈节点。
            print('从第一个感染图子图找到的第一个邻居节点是' + str(i))
            if isReceived(i, h, subinfectG, infectionG) == True:
                print('从第一个感染子图找到的可行节点为' + str(i))
                newnodes = i
                break

        if  newnodes==5000:
            print ('从第一个感染感染图都找不到了，返回原点吧')
            return node
        else:
            print('从第一个感染子图中找到了的节点为' + str( newnodes))
            print('重新找的节点为的偏心率' + str(nx.eccentricity(subinfectG,  newnodes)))
            return  newnodes


    else:
        print('找到邻居节点满足h=' + str(h) + '的点')
        print('重新找的节点为的偏心率' + str(nx.eccentricity(subinfectG, newnodes)))
        return newnodes

    # nodelist=[]
    # for  i  in subinfectG.nodes:
    #     nodelist.append(i)
    # index=0
    # resultNode=5000
    # heighbour=node
    # #从2节点开始找直到找到满足h的点。
    # while  isReceived(heighbour,h,subinfectG,infectionG)!=True and  index<4038:
    #      heighbour=nodelist[index]
    #      index = index + 1
    #      resultNode=heighbour






#从subinfectinG中寻找node的邻居中具有最小Eccentricity的节点。离心越近.就以他返回。
def findBigEccentricity1(h,node,subinfectG,infectionG,TurerumorSource2,sourceh):

    # #这个感染图中，最小离心率是？这个暂时卡住了，怎么办？那么先假装实现，
    # minecceity=10
    # for  i  in  subinfectionG.nodes:
    #     if  nx.eccentricity(subinfectionG,i)<minecceity:
    #         minecceity=nx.eccentricity(subinfectionG,i)
    # print ('查看最小离心率'+str(minecceity))
    # print ('这个h下的错误节点为'+str(node))
    # minEccentricity=nx.eccentricity(subinfectionG,node)
    # print( '它的偏心率为'+str(minEccentricity))
    #
    # ecctemp=0
    # minEccentricitynnode=0
    # print('从他的邻居节点找离心率最小的')  #或者找离中心近的。
    # for  heighbour in  list(subinfectionG.neighbors(node)):
    #     ecctemp=nx.eccentricity(subinfectionG,heighbour)
    #     if ecctemp<minEccentricity:
    #         minEccentricity=ecctemp
    #         minEccentricitynnode=heighbour
    # #如果没有离心率更小的话，就返回源点。


    #直接从邻居中找一个当前h下能行不就可以吗？有时候邻居节点都不行，那就只能从整个感染子图中找了
    newnodes=5000
    for heighbour in list(subinfectG.neighbors(node)):   #这只能找一圈节点。
           print('那么这个点'+str(node)+'的邻居节点'+str(heighbour)+'试试看效果')
           if  isReceived(heighbour,h,subinfectG,infectionG)==True:
                print ('在邻居中找到的可行节点为'+str(heighbour))
                newnodes= heighbour
                break

    allnodelist = list(nx.bfs_tree(subinfectG, source=TurerumorSource2, depth_limit=sourceh).nodes)
    if newnodes==5000:
        print ('对不起，他的邻居节点找不到满足h='+str(h)+'的点了，从第2个感染点的感染区域中找了')
        for i in list(allnodelist):  # 这只能找一圈节点。
            print('从第2个感染点的感染区域图子图找到的第一个邻居节点是' + str(i))
            if isReceived(i, h, subinfectG, infectionG) == True:
                print('在从第2个感染点的感染区域感染子图找到的可行节点为' + str(i))
                newnodes = i
                break

        if  newnodes==5000:
            print ('从第2个感染点的感染区域感染图都找不到了，返回原点吧')
            return node
        else:
            print('从第2个感染点的感染区域子图中找到了的节点为' + str( newnodes))
            print('重新找的节点为的偏心率' + str(nx.eccentricity(subinfectG,  newnodes)))
            return  newnodes


    else:
        print('找到邻居节点满足h=' + str(h) + '的点')
        print('重新找的节点为的偏心率' + str(nx.eccentricity(subinfectG, newnodes)))
        return newnodes



























#
def   contactu1h1u2h2(subinfectG,infectionG,rumorSourceList,sourceh,testh):  #参数这里的真实源点的sourceh,而testh是一步一步增大的h
    print('先随机找到两个源点就行了')
    sourclist = randomSourcelist(subinfectG)  #先随机找到点就行了
    max=0
    lasth=0
    resultheavyCenterlist=[]
    #从0到100赋予h作为值。
    for h  in range(1,testh):  #这个h最大值传播子图某个源点的最大传播路径，就是3左右。因为我们真实源点传播h就是3.
        print ('h为'+str(h)+'的情况'+'----------------------------------------')
        #需要根据h找到一些随机源点。把能形成这个圆（u1,h1）的所有点定下。
        #构建这样两个圆出来
        print ('随机选两个的源点是'+str(sourclist))
        print ('他们各自的偏心率')
        print(nx.eccentricity(subinfectG, sourclist[1]))
        print(nx.eccentricity(subinfectG, sourclist[0]))
        flag1=False
        flag2=False
        #用一个while计算直到两个flag都为1,就是两个圆都满足。
        while flag1!=True or  flag2!=True:
            flag1 = isReceived(sourclist[0], h, subinfectG, infectionG)
            flag2 = isReceived(sourclist[1], h, subinfectG, infectionG)
            while  flag1==False:  #随机源点不行就要找当前h下的更好随机源点。
                print ("很明显啊，这里的flage1是false--------------------------------------------------------------------------")
                newnode=findBigEccentricity(h,sourclist[0],subinfectG,infectionG,rumorSourceList[0],sourceh)  #从邻居中找的新点
                if  sourclist[0]!=newnode  and  nx.shortest_path_length(subinfectG,newnode,sourclist[1])>3:
                    print('找到的新源点1是'+str(newnode)+'跟原来不一样,并且和第二点'+str(sourclist[1])+'有3的距离这才是有用的的点')
                    sourclist[0] = newnode
                    flag1 = True
                elif nx.shortest_path_length(subinfectG,newnode,sourclist[1])<3:
                    print('找到的新源点1是' + str(newnode) + '跟原来不一样,并且和第二点' + str(sourclist[1]) + '没有有3的距离这个不行的')
                    sourclist[0] = newnode
                    flag1 = False
                else:
                    print('找到的新源点1跟原来一样,没得办法，只能用这个点了')
                    sourclist[0] = newnode
                    flag1 = True



            if flag2==False:
                print("很明显啊，这里的flage2是false---------------------------------------------------------------")
                newnode1 = findBigEccentricity1(h,sourclist[1],subinfectG,infectionG,rumorSourceList[1],sourceh)  # 从邻居中找的
                if sourclist[1] != newnode1 and  nx.shortest_path_length(subinfectG,newnode1,sourclist[0])>3:
                    print('找到的新源点2跟第一次的不一样，并且有距离。跟第一个源点有3的距离是可以的')
                    sourclist[1] = newnode1
                    flag2 = True
                elif nx.shortest_path_length(subinfectG, newnode1, sourclist[0]) < 3:
                    print('找到的新源点2是' + str(newnode1) + '跟原来不一样,并且和第一个点' + str(sourclist[0]) + '没有有3的距离这个不行的')
                    sourclist[1] = newnode1
                    flag1 = False
                else:
                    print('找到的新源点1跟原来一样,没得办法，只能用这个点了')
                    sourclist[1] = newnode1
                    flag1 = True




        print  ('到这里我们是找到了这两个源点，开始计算他们更好的分数吧。')
        print ('新找到的源点是'+str(sourclist))
        print ('源点2的偏心率为'+str(nx.eccentricity(subinfectG,sourclist[1])))
        print('源点1的偏心率为'+str(nx.eccentricity(subinfectG, sourclist[0])))
        sum=calEu1h1u2h2(sourclist[0], h, sourclist[1], h, subinfectG)
        print ('计算它们在这个u,，h下的分数'+str(sum))
        if  sum>max:
            max=sum
            lasth=h
            resultheavyCenterlist=sourclist

    print ('我们测试的heave center点跟真实源点测下距离看看')
    print (resultheavyCenterlist)
    print('测试距离为'+str(nx.shortest_path_length(subinfectG,125,resultheavyCenterlist[0])))
    print('测试距离为' + str(nx.shortest_path_length(subinfectG, 125, resultheavyCenterlist[1])))
    print('测试距离为' + str(nx.shortest_path_length(subinfectG, 4022, resultheavyCenterlist[0])))
    print('测试距离为' + str(nx.shortest_path_length(subinfectG, 4022, resultheavyCenterlist[1])))
    #目前为止我们只需要得到感染区域。就是以resultheavyCenterlist为源点，长度为h的两个树。

    return   resultheavyCenterlist,lasth
    # return slice




def   calEu1h1u2h2(u1,h1,u2,h2,subinfecG):

    print ('计算'+str(u1)+str(h1)+str(u2)+str(h2)+'所包含的圆的大小')
    #其实就是bfs树。
    # 对u进行长达h的圆构建
    circleNodesList1 = list(nx.bfs_tree(subinfecG, source=u1, depth_limit=h1).nodes)  # 这包含了这个构建的圆的所有节点。
    nodesum1=len(circleNodesList1)

    circleNodesList2 = list(nx.bfs_tree(subinfecG, source=u2, depth_limit=h2).nodes)  # 这包含了这个构建的圆的所有节点。
    nodesum2=len(circleNodesList2)
    # # 复现当前单源定位,参数如何设置。 subinfecG以及u1以及感染点集合。计算u1在当前感染点下源点概率。
    # print ('图中心')
    # print(nx.center(subinfectG))

    #测试两个圆和我们的subinfecG重合的点数即可。最大就是源点了
    #评判标准不对，很明显是不行的。会找到两个点[0,311]这样的话。0，311每个节点再一定4的h下都可以传染到所有节点。

    print ('第一个、二个圆点重合个数是加起来'+str(nodesum1)+'--------'+str(nodesum2))
    print ('让我们看看是多少，算下源点距离')
    return  nodesum1+nodesum2





import difflib

#必须设计一个函数，来测试u，h是否可以适用。

def  isReceived(u,h,subinfectionG,infectionG):
     #对u进行长达h的圆构建
     circleNodesList=list(nx.bfs_tree(infectionG, source=u, depth_limit=h).nodes)  #这包含了这个构建的圆的所有节点。
     subinfectionList=list(subinfectionG.nodes)   #传染子图的所有点。
     #计算列表相似度试试看
     # print ('感染源的h节点集合为'+str(circleNodesList))

     count =0
     for  i  in circleNodesList:
         if  i  in subinfectionList:
             count=count+1
     similir=count/len(circleNodesList)
     print ('u,h对应圆重和subinfectionG图的重合比例为'+str( similir))
     if similir>0.9:
         print('这里的'+str(u)+'和h是'+str(h)+'是可以在subinfection中存在的')
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






#设计反向传播算法，接收参数。u，h，infectG。
def  revsitionAlgorithm(u,h,infectG,subinfectG):
    nodelist=list(nx.bfs_tree(subinfectG,source=u,depth_limit=h).nodes)
    source1G=nx.Graph()  #构建新的单源传播圆出来
    for edge in  subinfectG.edges:
        if edge[0]  in  nodelist  and edge[1]  in  nodelist:
            source1G.add_edge(edge[0],edge[1])

    print  ('传播子图为source1G,它的点数和边数为'+str(source1G.number_of_nodes())+'-------'+str(source1G.number_of_edges()))
    #在nodelist找出源点来。
    times=6   #时间刻多点
    IDdict={}
    IDdict_dup = {}
    # 先赋予初始值。
    for  node  in  list(source1G.nodes):
        # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
        IDdict[node]=[node]
        IDdict_dup[node] = [node]
    allnodelist_keylist = []  #包含所有接受全部节点id的键值对的key
    for  t  in  range(times):
        print ('t为'+str(t)+'的时候-----------------------------------------------------------------------------')
        for  node  in  nodelist:  #对每一个节点来说
            for heighbour in   list(source1G.neighbors(node)):   #对每一个节点的邻居来说
                  retD=list(set(IDdict[heighbour]).difference(set( IDdict[node])))  #如果邻居中有这个node没有的，那就加到这个node中去。
                  if  len(retD)!=0:   #表示在B中，但不在A.是有的，那就求并集
                            #求并集,把并集放进我们的retC中。
                            # print ('并集就是可使用'+str(retD))
                            retC = list(set(IDdict[heighbour]).union(set(IDdict[node])))
                            IDdict_dup[node] = list(set(IDdict_dup[node] + retC))  #先用一个dict把结果装入,然后这个时间过去再加回去。

        for key, value in IDdict_dup.items():
            IDdict[key] = IDdict_dup[key]
        # for key, value in IDdict.items():
        #     print(key, value)
    #在每一个时间刻检查是否有节点满足获得所有的id了。

        flag=0
        for key, value in IDdict.items():
            # d.iteritems: an iterator over the (key, value) items
            if   sorted(IDdict[key])==sorted(nodelist):
                 print ('在t为'+str(t)+'的时间的时候，我们有了接受全部node的ID的人')
                 print ('它的key为'+str(key))
                 allnodelist_keylist.append(key)
                 print ('有了接受所有的节点了这样的节点了')
                 flag=1

        if  flag==1:
            break
    # print (IDdict)
    print (allnodelist_keylist)

    result=0
    resultlist=[]
   #如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
    if  len(allnodelist_keylist)==1:
        print ('那就是这个源点了')
        result=allnodelist_keylist[0]
    else:
        #构建样本路径
        print ('构建样本路径看看')
        jarcenlist=[]
        for  i  in  allnodelist_keylist:
            jarcenlist.append([i,nx.eccentricity(source1G,i)])  #按照离心率进行排序,最小离心率的就是源点。
            resultlist = sorted(jarcenlist, key=lambda x: x[1])
        result=resultlist[0][0]
        print('构建样本路径之后结果为'+str(resultlist[0][0]))


    print (nx.shortest_path_length(subinfectG,result,u))  #0
    print (nx.shortest_path_length(subinfectG,125,result) )#  2
    print(nx.shortest_path_length(subinfectG, 4022, result))  #  8




















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
    G.add_edge(edge[0],edge[1], Infection=1)




rumorSourceList=contractSource(G,2,3)  #产生源点。图，源点个数，源点差距距离。
infectG=Algorithm1(G,rumorSourceList,5 )  #产生感染图，深度是3

#gephi 查看infectG转成csv情况。
ConvertGToCsv(infectG,'G.csv')





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


print ('#查看感染图半径'+str(nx.radius(subinfectG)))
print ('查看感染图中心'+str(nx.center(subinfectG)))
print ('查看感染图直径'+str(nx.diameter(subinfectG)))
# print ('查看感染图图外围'+str(nx.periphery(subinfectG)))
# print ('查看感染图某点偏心率'+str(nx.eccentricity(G,125)))


#随机生成u1，h1,u2.h2来让E(u1,h1,u2,h2)最大。

resutltList,lasth=contactu1h1u2h2(subinfectG,infectG,rumorSourceList,5,6)        #这里的后三个参数。第一个是真实两源源点，第三个是这个源点的传播h，最后一个是试探h。
#返回的结果是两个heav center以及它的h，因为这里的h是一样的。

#现在分别计算在每个点下，找源点。看看reverse infection algorithm，试下第一个点

#第一步

print ('结果为'+str(resutltList)+'h为'+str(lasth))     #以这两个为中心的点的话，就是各自进行单源定位。
revsitionAlgorithm(resutltList[0],lasth,infectG,subinfectG)   #参数是第一个heavey center，和h。为了确定感染区域。
revsitionAlgorithm(resutltList[1],lasth,infectG,subinfectG)



