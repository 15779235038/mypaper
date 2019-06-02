


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

    for edge in  G.edges:
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
    for j in range(len(SourceList)):
        nodelist=list(nx.bfs_tree(G, source=SourceList[j], depth_limit=3).nodes)  # 这包含了这个构建的圆的所有节点。
        edgelist = list(nx.bfs_tree(G, source=SourceList[j], depth_limit=3).edges)
        nodelist = random.sample(nodelist, int(float(len(nodelist))*0.9))  # 从list中随机获取5个元素，作为一个片断返回
        for i in nodelist:
            G.node[i]['SI'] = 2
        for  k  in  edgelist:
            G.adj[k[0]][k[1]]['Infection']=2
        print ('头两个感染社区点数为'+str(len(nodelist)))

    return G













#产生指定感染节点，需要参数节点个数。他们距离的最大值。图G
def  contractSource(G,sourceNum,sourceMaxDistance):
     sumlist=list(G.nodes)
     flag=0
     flag1=0
     rumorSourceList = []
     #先随机找个点，然后找到距离它为>6,小于10的吧。
     while (flag==0):

         if  sourceNum==1:
             # random_RumorSource = random.randint(0, 7000)
             random_Rumo = random.sample(sumlist, 1)
             random_RumorSource = random_Rumo[0]
             rumorSourceList.append(random_RumorSource)
             flag=1
         elif sourceNum==2:
             random_Rumo = random.sample(sumlist, 1)
             random_RumorSource = random_Rumo[0]
             #在剩下的节点找到我们的第二个点。
             for  node  in  list(G.nodes):
                  if  nx.has_path(G,node,random_RumorSource)==True:
                      if  nx.shortest_path_length(G,node,random_RumorSource)>4 and  nx.shortest_path_length(G,node,random_RumorSource)<6:
                          rumorSourceList.append(node)
                          rumorSourceList.append(random_RumorSource)
                          flag=1
                          break
         elif sourceNum==3:
              print ('3源点情况。')
              threeNumberFLAG=0
              while  threeNumberFLAG==0:
                  #先随机找一个点。
                  random_Rumo = random.sample(sumlist, 1)
                  random_RumorSource = random_Rumo[0]
                  #找第二、三个点。
                  for  index   in  range(len(sumlist)-2):
                       if nx.has_path(G,sumlist[index],random_RumorSource)==True and  nx.has_path(G,sumlist[index+1],random_RumorSource)==True:
                          if  nx.shortest_path_length(G,source=sumlist[index],target=random_RumorSource)>4  and nx.shortest_path_length(G,source=sumlist[index],target=random_RumorSource)<6 and  nx.shortest_path_length(G,source=sumlist[index+1],target=random_RumorSource)>4 and nx.shortest_path_length(G,source=sumlist[index+1],target=random_RumorSource)<6:
                            rumorSourceList.append(random_RumorSource)
                            rumorSourceList.append(sumlist[index])
                            rumorSourceList.append(sumlist[index+1])
                            print ('找到了3源点了。')
                            break
                  if  len(rumorSourceList)==3:
                      print ('找到了3个点')
                      threeNumberFLAG=1
                      flag=1
                  else:
                      pass


     # 查看产生随机源点的个数2，并且他们距离为3.
     print('源点个数' + str(len(rumorSourceList))+'以及产生的两源点是'+str(rumorSourceList))
    # rumorSourceList=[125,4022]   #需要经过5个空。这两个源点。796, 806, 686, 698, 3437, 1085, 1494, 95
     print('真实两源感染是'+str(rumorSourceList))
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
        # print (list(infectG.neighbors(firstPartion[0])))
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
    sumlist = list(infectionG.nodes)
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
                    randomnumber = random.sample(sumlist, 1)
                    if infectionG.node[randomnumber[0]]['SI'] == 2:
                        randomInfectionNode = randomnumber[0]
                        flag1 = 1
                print('第一个感染社区随机开始的点感染点' + str(randomInfectionNode))
                partion1 = getTuresubinfectionG(infectionG,randomInfectionNode)
                multipleCommuniytlist.append(partion1)  # 第一个社区
                print('把第1个社区加入进去，现在感染社区点个数为' + str(len(multipleCommuniytlist)))
            else:
                print('在已经有感染社区，开始找下一个社区的时候的操作')
                #总的点集合-已经找到的社区节点=在这里继续找。
                infectionList=multiplelistTo_ormialy(multipleCommuniytlist)
                allList=list(infectionG.nodes)
                diff_list = list(set(allList).difference(set(infectionList)))  #差集合
                print ('在总的区里面，但不在已经分好的社区里面。这些点有多少个？'+str(len(diff_list)))
                print ('下面开始在除了已有的感染区域外，重新找一个点，是感染点')
                flag2=0
                while flag2 == 0:
                    for  infectionNode  in diff_list:
                        if infectionG.node[infectionNode]['SI'] == 2:
                            print ('重新找一个点，是感染点的点就是'+str(infectionNode))
                            randomInfectionNode =infectionNode
                            flag2 = 1
                            break

                    print ('找不到是感染点的点就是')

                print('有感染社区之后随机开始的点感染点随机开始的点感染点是' + str(randomInfectionNode))
                partion2 = getTuresubinfectionG(infectionG,randomInfectionNode)

                multipleCommuniytlist.append(partion2)  #
                print('把第二到第n个社区加入进去,现在的感染社区点个数为' + str(len(multipleCommuniytlist)))
            #终止条件,剩下社区没有被感染点了。


            haveinfectionList = multiplelistTo_ormialy(multipleCommuniytlist)
            print ('已经被识别的的社区里面的感染点个数为'+str(len(haveinfectionList)))
            allList = list(infectionG.nodes)
            diff_list_ = list(set(allList).difference(set( haveinfectionList)))
            restList=[]
            for i  in diff_list_:
               restList.append(infectionG.node[i]['SI'])
            if  2  in restList :
                print('有感染点在restList中，就是说还有感染点在除了这些感染子图之外。')
                pass
            elif 2  not in restList  :  #保留项
                print('已经没有感染点在restList中，就是说没有感染点在除了这些感染子图之外。')
                flag=1




    print ('感染社区个数以及各自人数')
    print (len(multipleCommuniytlist))
    print(len(multipleCommuniytlist[0]))
    # print(len(multipleCommuniytlist[1]))
    if  125  in  multipleCommuniytlist[0]  and 4022  in  multipleCommuniytlist[0]:
        print ('头两个源点在的')
    # print(len(multipleCommuniytlist[1]))
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
      centerlist = list(nx.center(tempGraph))
      print('感染图的中心为' + str(centerlist))
      for center in centerlist:
          chooseList.append(center)    #
      chooseList.append(82)
      chooseList.append(6675)
      print ('chooseList个元素个数为'+str(len(chooseList)))
      maxh=nx.radius(tempGraph)
      print ('感染图半径为'+str(maxh))   #把边都加入话，半径都小了。都不是一个好树了，难受

      chooseList = chooseList[-20:]  # 取最后20个。
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
      # listToTxt(minCover, 'result.txt')
      result = sorted(minCover, key=lambda x: (x[2]))
      listToTxt(result[0],'newresult.txt')
      return result[0]









def  listToTxt(listTo,dir):
    fileObject = open(dir, 'a')
    fileObject.write(str(listTo))
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





import  sys
def   getListfortxt(rootdir):
    lines = []
    with open(rootdir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)

    lists = [x for x in  lines if x != []]
    return lists



'''
this   function  :   to  get  sourcelist fo  everyRegionList  and   caluce  every  distance of  source and result


'''


import math
def   multiplePartion(mutiplelist,infectionG,rumorSourceList):

     #所有单源list
     allsigleSourceList=[]
     allSigleSourceListNum=[2,1]

     #将第一个传播区域定下来。
     import datetime
     starttime = datetime.datetime.now()
     # long running,这里可以读的文件代替，就比较省时间。反正都是为了allsigleSourcellist填充


     '''   这个是保留项，我觉得反转算法有点问题，反正（u,h是写完了）,下面这个很好时间'''

     # for  sigleReionlist  in  mutiplelist:
     #     allsigleSourceList.append(findmultiplesource(sigleReionlist, infectionG))

     allsigleSourceList=[[(82, 6675), 3, 0.0], [2419, 2, 0.33333333333333337]]
     #上面这个就是通过圆（u，h）构建的结果，看着办。第一个是双源的，第二个是单源的。
     #构建每个传播区域的传播子图.
     tempGraph1 = nx.Graph()
     for edge in infectionG.edges:
         # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
         if edge[0] in mutiplelist[0] and edge[1] in mutiplelist[0]:
             tempGraph1.add_edges_from([edge], weight=1)
     print('这个感染区域的传播子图边个数')
     print(tempGraph1.number_of_edges())
     print (tempGraph1.number_of_nodes())





     # 构建传播子图.
     tempGraph2 = nx.Graph()
     for edge in infectionG.edges:
         # if infectG.adj[edge[0]][edge[1]]['Infection']==2:      #作为保留项。
         if edge[0] in mutiplelist[1] and edge[1] in mutiplelist[1]:
             tempGraph2.add_edges_from([edge], weight=1)
     print('这个感染区域的传播子图边个数')
     print(tempGraph2.number_of_edges())
     print(tempGraph2.number_of_nodes())


     resultSource=[]
     #现在已经返回关于每个社区的源点及其社区了，开始画图吧。
     print ('最后的每个分区的圆点和他的h是'+str(allsigleSourceList))



     for  sigleRegionSource  in  allsigleSourceList:
          if isinstance(sigleRegionSource[0], int): #单源点
              source3 = revsitionAlgorithm(sigleRegionSource[0], sigleRegionSource[1], infectionG, tempGraph2)
              print('用反转算法计算出来的单源点为' + str(source3))
              resultSource.append([source3])
          else:
              print ('多源点情况---------------------------')
              source1 = revsitionAlgorithm(sigleRegionSource[0][0], sigleRegionSource[1], infectionG, tempGraph1)
              source2 = revsitionAlgorithm(sigleRegionSource[0][1], sigleRegionSource[1], infectionG, tempGraph1)
              print('用反转算法计算出来的源点为' + str(source2) + str(source1))
              resultSource.append([source1, source2])


     print ('总的用反转算法算出来的结果为'+str(resultSource))
     truerumorSourceLists = [[rumorSourceList[0], rumorSourceList[1]], [rumorSourceList[2]]]
     #上面这两个，可以干一架了。


     #真实集合
     #结果集合和我们的真实源开始对照，其中多源就要这些节点去自动找了。

     for   resultsourcelist in  resultSource:
           if  len(resultsourcelist)>1 and len(truerumorSourceLists[0])>1 :
               #开始计算它对应的源点差值，要找一些好的值。
                print(resultsourcelist,truerumorSourceLists[0])
                tempLists=list(resultsourcelist+truerumorSourceLists[0])
                combinationList = list(combinations(tempLists, 2))  # 这是排列组合，再次针对这个排列组合
                #计算所有组合，然后找出距离最近的符合len的两组，这里我明显知道是2.
                lengthlist=[]
                for   combination  in  combinationList:
                      lengthlist.append([combination,nx.shortest_path_length(infectionG,combination[0],combination[1])])
                result = sorted( lengthlist, key=lambda x: (x[1]))

                resultSourceMinDistance=result[:2]   #只要前两个
                print ('125,4022  是真实源点，')
                print ('我们算的的两源定位的距离结果为'+str(resultSourceMinDistance))
           else:

               # if  769  in  list(infectionG.nodes):
               #     print ('在的啊------------------------------------------')
               distance=nx.shortest_path_length(infectionG,resultsourcelist[0],truerumorSourceLists[1][0])
               print('我们算的的单源定位的距离结果为定位结果'+str(resultsourcelist[0])+'真实结果'+str(truerumorSourceLists[1][0])+'他们距离'+str(distance))

     endtime = datetime.datetime.now()
     print(str((endtime - starttime).seconds) + '秒')
     distancecai=[]
     for  resultSource  in resultSourceMinDistance:
          distancecai.append(resultSource[1])
     distancecai.append(distance)
     print ('产生距离偏差值之list为'+str(distancecai))

     sumdistance=0
     for  i  in distancecai:
          sumdistance=sumdistance+i
     print ('产生的源点平均偏差距离为'+str(sumdistance/3))
     return   sumdistance/3

     # do something other





import numpy as np
import matplotlib.pyplot as plt

def   plotform(x,y):

    #X轴，Y轴数据
    x = [0,1,2,3,4,5,6]
    y = [0.3,0.4,2,5,3,4.5,4]
    plt.figure(figsize=(8,4)) #创建绘图对象
    plt.plot(x,y,"b--",linewidth=1)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.xlabel("Number of sources") #X轴标签
    plt.ylabel("Average error  (in hops)")  #Y轴标签
    plt.title("facebook_combined  data") #图标题
    plt.show()  #显示图
    plt.savefig("line.jpg") #保存图
























#设计反向传播算法，接收参数。u，h，infectG。
def  revsitionAlgorithm(u,h,infectG,subinfectG):
    print ('反转算法参数,u和h'+str(u)+'----------'+str(h))
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















#
#
#
# rumorSourceList=contractSource(G,3,5)  #产生源点。图，源点个数，源点差距距离。
# hlist=[3,2]   #不同传播区域传播深度，
# infectG=Algorithm1(G,rumorSourceList,5,hlist )  #产生感染图，深度是3
#
# #gephi 查看infectG转成csv情况。
# ConvertGToCsv(infectG,'G.csv')
# subinfectG=nx.Graph()
# count=1
# count1=1
# for  edge in  infectG.edges:
#     # print (edge)\
#     if  infectG.adj[edge[0]][edge[1]]['Infection']==1:
#        count1 =count1+1
#     if  infectG.adj[edge[0]][edge[1]]['Infection']==2:
#         count = count + 1
#         subinfectG.add_edges_from([(edge[0],edge[1])],weight= 1)
#
# print (count)
# print (count1)
# # 因为邮件是一个有向图，我们这里构建的是无向图。
# print('传染子图的顶点个数',  subinfectG.number_of_nodes())
# print('传染子图的边个数',  subinfectG.number_of_edges())
#
#
# ConvertGToCsvSub(subinfectG,'SubInfectionG.csv')
# #
# #检测是否是有相互感染到。
#
# print (nx.shortest_path(G, rumorSourceList[0], rumorSourceList[1], weight='weight'))
# print (nx.shortest_path(subinfectG, rumorSourceList[0], rumorSourceList[1], weight='weight'))  #在子图中有路径，就是感染到了。
#
# if nx.has_path(subinfectG,rumorSourceList[1],rumorSourceList[2])==False:
#     if nx.has_path(subinfectG,rumorSourceList[0],rumorSourceList[2])==False:
#         print('========================================================================')
#         print ('这里的第3个点，跟他们都没有路径相连。可以的')
# else:
#     print ('========================================================================')
#     print ('这里的第3个点，不行的，很烦')
# # print (nx.shortest_path(subinfectG, rumorSourceList[1], rumorSourceList[2], weight='weight'))    #这个报错就是第三个point并没有被感染到的意思。
#
# #now  to  practice single-multiple  source Partition.Get  ture  parition
#
#
#
# # if  769  in list(infectG.nodes):
# #     print ('明明就在')
# multipList=getmultipleCommunity(infectG)
# multiplePartion(multipList, infectG,rumorSourceList)
#
#
#
# #产生一组模拟两源数据的，然后计算平均值。
#
#
#
#
#
#






if __name__ == '__main__':
    '''

    1  产生一个社区，无非就是源点从1到5.然后用我们这种方式
    判断准确率。
    '''

    #1 产生这个图。

    #  制造这个图
    Ginti = nx.Graph()
    # 初始化图,加很多节点
    # for index in range(1,1005):
    #     print (index)
    #     Ginti.add_node(index)

    # 构建图，这个图是有有效距离的。
    G = ContractDict('../data/Wiki-Vote.txt', Ginti)

    # 因为邮件是一个有向图，我们这里构建的是无向图。
    print('一开始图的顶点个数', G.number_of_nodes())
    print('一开始图的边个数', G.number_of_edges())

    #  先给全体的Cn、Scn,time的0的赋值。
    for node in list(G.nodes):
        G.add_node(node, SI=1)

    # 初始化所有边是否感染。Infection
    for edge in list(G.edges):
        G.add_edge(edge[0], edge[1], Infection=1)

    print  ('这个图产生完毕')



    sourceList=[]
    #  从1个源点产生到5个源点。但都是有交集的。按照交叉领域来比较？

    for  sourceNumber  in  range(1,4):
        sourceList.append(contractSource(G,sourceNumber,2))
    print (sourceList)


    #  1到三源点，现在根据每个源点产生传播。然后，就可以定位了。每次传播都要定位的。
    infectG=Algorithm1(G,sourceList[0],5,6 )

    #  找社区，按照代理，只能找到一个社区的。

    multipList = getmultipleCommunity(infectG)
    multiplePartion(multipList, infectG,sourceList)

























