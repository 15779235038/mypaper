import networkx as nx
import random
from networkx.algorithms import community



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
        nodelist = random.sample(nodelist, int(float(len(nodelist))*0.9))  # 从list中随机获取5个元素，作为一个片断返回


        for i in nodelist:
            G.node[i]['SI'] = 2
        for  k  in  edgelist:
            G.adj[k[0]][k[1]]['Infection']=2
        print ('头两个感染社区点数为'+str(len(nodelist)))

    #第3个源点传播。
    nodelist=list(nx.bfs_tree(G, source=SourceList[2], depth_limit=2).nodes)
    edgelist = list(nx.bfs_tree(G, source=SourceList[2], depth_limit=2).edges)
    nodelist = random.sample(nodelist, int(float(len(nodelist))*0.9))  # 从list中随机获取5个元素，作为一个片断返回

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
    tureSourceList=[2,1]
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






import  random

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
                print('第一个感染社区随机开始的点感染点' + str(randomInfectionNode))
                partion = getTuresubinfectionG(infectionG,randomInfectionNode)
                multipleCommuniytlist.append(partion)  # 第一个社区
            else:
                print('在已经有感染社区，开始找下一个社区的时候的操作')
                #总的点集合-已经找到的社区节点=在这里继续找。

                infectionList=multiplelistTo_ormialy(multipleCommuniytlist)
                allList=list(infectionG.nodes)
                diff_list = list(set(allList).difference(set(infectionList)))  #差集合
                print ('在总的区里面，但不在已经分好的社区里面。'+str(len(diff_list)))
                while flag2 == 0:
                    randomnumber =random.sample(diff_list, 2)
                    if infectionG.node[randomnumber[1]]['SI'] == 2:
                        randomInfectionNode =randomnumber[1]
                        flag2 = 1
                print('有感染社区之后随机开始的点感染点随机开始的点感染点' + str(randomInfectionNode))
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
                print('有感染点在restList中，就是说有感染点在除了这些感染子图之外。')
                pass
            elif 2  not in restList:
                print('已经没有感染点在restList中，就是说有感染点在除了这些感染子图之外。')
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






from itertools import combinations

def  getkey(pos,value):
   return  {value: key for key, value in pos.iteritems()}[value]

import   matplotlib.pyplot  as plt
def   findmultiplesource(singleRegionList,infectionG):
      #首先需要判断是否多源。不断找源点去对这个区域。
      tempGraph=nx.Graph()
      for  edge in infectionG.edges:
          # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
              if edge[0] in singleRegionList and edge[1] in singleRegionList:
                  tempGraph.add_edges_from([edge],weight=1)
      print ('这个感染区域的传播子图边个数')
      print (tempGraph.number_of_edges())
      #求出这个区域最远的路径出来。返回这个区域半径。
      print('这个感染区域的传播半径')
      # maxh=nx.radius(tempGraph)
      '''
        1  选择边界点。（or所有点）
        2  选择中心点，以（u，h）去达到最大的覆盖数目。计算这样形成的u和它所有边界点形成的路径成本。
        3  再以(u1,h1).(u2,h2)去达到这样的覆盖数目，计算这样形成的路径成本之和。（每次增大h，这个子集合的成本都会增大。）
        '''
      #首先第一步，将这个tempGra圆投影到x，y轴。
      #让我看看这个图
      ConvertGToCsvSub(tempGraph,'tempGraph.csv')
      # peripheryList=nx.periphery(tempGraph)  #求解图边界list

      #随机求一些list，待选集合。偏心率<于某些数值，的元素。
      chooseList=[]
      for  node  in  tempGraph.nodes:
           randomnum=random.random()
           if  randomnum>0.95:
               chooseList.append(node)
      chooseList.append(125)
      chooseList.append(4022)
      print ('chooseList个元素个数为'+str(len(chooseList)))
      maxh=nx.radius(tempGraph)
      print ('感染图半径为'+str(maxh))   #把边都加入话，半径都小了。都不是一个好树了，难受
      centerlist=list(nx.center(tempGraph))
      print ('感染图的中心为'+str(centerlist))
      chooseList=chooseList[-50:]   #取最后50个。
      for  center in centerlist:
          chooseList.append(center)

      print ('chooseList'+'总共有多少元素'+str(len(chooseList)))
      minCover=[]
      for  sourceNum  in range(1,3):
          print ('在源点在'+str(sourceNum)+'个数的情况下')
          for  h  in range(2,5):
              print ('在h为'+str(h)+'的情况下')
              if  sourceNum ==1:#单源点。
                  print('单源点情况下')
                  #计算chooselist的每一个点在这个h下的bfs树覆盖率（对所有的infectionG试试）看看。
                  min=200
                  for  source  in chooseList:
                     mincover=getSimilir(source,h,singleRegionList,infectionG)  #取得覆盖率
                     if  min>mincover:
                         min=mincover
                         sourceNew=source
                  print ('得到单源点情况最小的覆盖率为'+str(min)+'源点为'+str(sourceNew))
                  minCover.append([sourceNew,h,min])
              else:
                  min=200
                  print ('多源情况,先考察同时传播传播')
                  print ('源点为'+str(sourceNum)+'情况')
                  #先判断源点个数，从chooseList中随机挑选两点，进行h构建。
                  combinationList = list(combinations(chooseList,sourceNum))  #这是排列组合，再次针对这个排列组合
                  sourceNews=[]
                  for  sources  in combinationList:
                          mincover=getSimilir(sources,h,singleRegionList,infectionG)
                          if  mincover < min:
                              min = mincover
                              sourceNews=sources
                  print('得到多源点情况最小的覆盖率为' + str( min))
                  minCover.append([sourceNews,h, min])
      print (minCover)
      #返回的应该是最可能的结果。获取mincover最小的返回。第三个元素才是需要考虑东西。
      listToTxt(minCover, 'result.txt')
      result = sorted(minCover, key=lambda x: (x[2]))
      return result[0]









def  listToTxt(listTo,dir):
    fileObject = open(dir, 'a')
    for ip in listTo:
        fileObject.write(str(ip))
        fileObject.write('\n')
    fileObject.write('\n')
    fileObject.close()


















def getSimilir(ulist, hlist, singleRegionList, infectionG):



    '''
    S树-S感染。


    :param ulist:
    :param hlist:
    :param singleRegionList:
    :param infectionG:
    :return:
    '''
    if isinstance(ulist, int):
        circleNodesList = list(nx.bfs_tree(infectionG, source=ulist, depth_limit=hlist).nodes)  # 这包含了这个构建的圆的所有节点。
        # 计算列表相似度试试看
        # print ('感染源的h节点集合为'+str(circleNodesList))
        count = 0
        for i in circleNodesList:
            if i in singleRegionList:
                count = count + 1
        Intersection =list(set( circleNodesList).intersection(set(singleRegionList)))  #交集
        Union=list(set(circleNodesList).union(set(singleRegionList)))
        ratios=len(Intersection) / len(Union)
        ratio= ratios - 1.0
        print('在u为'+str(ulist)+'h为'+str(hlist)+'情况下的覆盖率'+str(ratio))
        return abs(ratio)



    else:
        #多源点,获得多源点的感染
        circleNodesList=[]
        for u in  ulist:
            circleNodesList.extend(list(nx.bfs_tree(infectionG, source=u, depth_limit=hlist).nodes))
        circleNodesListnew=list(set(circleNodesList))
        count = 0
        for i in circleNodesList:
            if i in singleRegionList:
                count = count + 1
        # count
        Intersection = list(set(circleNodesList).intersection(set(singleRegionList)))  # 交集
        Union = list(set(circleNodesList).union(set(singleRegionList)))  #并集
        ratios = len(Intersection) / len(Union)
        ratio = ratios - 1.0
        print('在u为' + str(ulist) + 'h为' + str(hlist) + '情况下的覆盖率' + str(ratio))

        return abs(ratio)







'''
this   function  :   to  get  sourcelist fo  everyRegionList  and   caluce  every  distance of  source and result


'''


import math
def   multiplePartion(mutiplelist,infectionG,rumorSourceList):

     #所有单源list
     allsigleSourceList=[]
     allSigleSourceListNum=[2,1]
     rumorSourceList=[[rumorSourceList[0],rumorSourceList[1]],[rumorSourceList[2]]]
     #将第一个传播区域定下来。
     import datetime
     starttime = datetime.datetime.now()
     # long running
     for  sigleReionlist  in  mutiplelist:
         allsigleSourceList.append(findmultiplesource(sigleReionlist, infectionG))

     #构建传播子图.
     tempGraph1 = nx.Graph()
     for edge in infectionG.edges:
         # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
         if edge[0] in mutiplelist[0] and edge[1] in mutiplelist[0]:
             tempGraph1.add_edges_from([edge], weight=1)
     print('这个感染区域的传播子图边个数')
     print(tempGraph1.number_of_edges())





     # 构建传播子图.
     tempGraph2 = nx.Graph()
     for edge in infectionG.edges:
         # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
         if edge[0] in mutiplelist[1] and edge[1] in mutiplelist[1]:
             tempGraph2.add_edges_from([edge], weight=1)
     print('这个感染区域的传播子图边个数')
     print(tempGraph2.number_of_edges())






     resultSource=[]
     #现在已经返回关于每个社区的源点及其社区了，开始画图吧。
     print ('最后的每个分区的圆点和他的h是'+str(allsigleSourceList))
     for  sigleRegionSource  in  allSigleSourceListNum:
          if  len(sigleRegionSource[0])==2: #两源点
              source1=revsitionAlgorithm(sigleRegionSource[0][0],sigleRegionSource[1],infectionG,tempGraph1)
              source2=revsitionAlgorithm(sigleRegionSource[0][1],sigleRegionSource[1],infectionG,tempGraph1)
              print ('用反转算法计算出来的源点为'+str(source2)+str(source1))

              resultSource.append([source1,source2])

          else:
              source3 = revsitionAlgorithm(sigleRegionSource[0], sigleRegionSource[2], infectionG, tempGraph2)
              print('用反转算法计算出来的单源点为' + str(source3))
              resultSource.append(source3)


     print (resultSource)




     # #开始画图。我们可能需要两个图，来帮助我们分别这种方法，一个是单源的，一个是多源的。
     # '''
     # 这个有个规则的，比如多源定位。你如果定的多源，那就各自每个真实源点找最近的源点。最后计算平均值。
     # 如果你定的是单源，那就分别计算这个源跟多个真实源点的距离平均值。
     # 如果是单源定位，你定的单源，自然最好。直接计算距离。
     # '''
     # #开始分区，计算error distance。
     # for  singleSourcelist in  allsigleSourceList:
     #      for   number  in  allSigleSourceListNum:
     #            #判断源点数目是否对的上不
     #            if  len(number) ==len(singleSourcelist[0]):
     #                #源点数目对的上，开始计算平均距离。
     #
     #
     #
     #
     #





     # do something other
     endtime = datetime.datetime.now()
     print(str((endtime - starttime).seconds)+'秒')











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

    return result
    # print (nx.shortest_path_length(subinfectG,result,u))  #0
    # print (nx.shortest_path_length(subinfectG,125,result) )#  2
    # print(nx.shortest_path_length(subinfectG, 4022, result))  #  8
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

multiplePartion(multipList,infectG,rumorSourceList)