import networkx as nx
import random

from Girvan_Newman import GN #引用模块中的函数

#读取文件中边关系，然后成为一个成熟的图
def  ContractDict(dir,G):
    with open(dir, 'r') as f:
        for line in f:
            line1=line.strip().split(",")
            # print (line1)
            G.add_edge(int(float(line1[0])),int(float(line1[1])))
    # print (G.number_of_edges())
    return G











#生成感染图，我们看看感染图是什么样子。


def Algorithm1(G,basesore,sourceList):

    SG=nx.Graph()
    print ("感染列表送入，为啥加不进去",sourceList)
    for index in range(0,6):
        for sourceItem in list(sourceList):
            SG.add_node(sourceItem)
            for sourceNeightor in list(G.neighbors(sourceItem)):
                #  将感染点邻接点以一定概率加入到感染节点当中。
                # random_number=random.random()
                # if  random_number>0.6:

                #他们的传染边还要加上特别的属性，比如方向传播属性。
                G.add_node(sourceNeightor, Cn=1)
                SG.add_node(sourceNeightor)
                SG.add_edge(sourceItem,sourceNeightor)
                if G.node[sourceNeightor]['Cn']==1:
                        G.node[sourceNeightor]['Scn']+=G.nodes[sourceItem]['Scn']
    #对所有n<V(就是分数达到阕值的节点感染）算是谣言的不同之处吧。更新。
    for index in  range(1,35):
        if G.node[index]['Scn']>basesore:
            G.add_node(index, Cn=1)

    return  G,SG




#产生head以及tail中的一个随机数。
def  randomNum(head,tail):
    random.random()





#遍历这个文件中每一条边，也就是行。然后在被传染或者恢复的边中。选中其中一些边作为
#已经传染，或者已经被传染，这需要g以及对文件的操作。





def   Product_infection_Graph(G,dir):
    GInfetion = nx.Graph()
    #获取所有关于这个已经感染总图的被感染子图。
    infection=[]
    count=1
    for  index  in range(1,35):
        if G.nodes[index]['Cn'] == 1:
            infection.append(index)
            count+=1
    # print ('cont',count)
    # print ('indexlist',len(infection))
    with open(dir, 'r') as f:
        for line in f:
                line1=line.strip().split(",")
                if int(float(line1[0])) in infection and int(float(line1[1])) in infection:
                    GInfetion.add_node(int(float(line1[0])))
                    GInfetion.add_node(int(float(line1[1])))
                    GInfetion.add_edge(int(float(line1[0])),int(float(line1[1])))
    return  GInfetion










#定义函数来进行分区后的谣言定位
'''
parameter：多个社区的分区，以及被传播的节点，现在分别计算度以及中心性，进行源头判断。

'''


def    cal_source(G,infectList):
    #按照分区的来进行判断源点。
    # print (len(infectList))
    # print('感染图，节点总数', G.number_of_nodes())
    # print('感染图，边总数', G.number_of_edges())
    # print('感染图，边总数', G.edges())
    lists = [[] for _ in range(len(infectList))]

    centrality = nx.betweenness_centrality(G)
    # print(sorted((v, '{:0.2f}'.format(c)) for v, c in centrality.items()))
    for v, c in centrality.items():
        for i in range(len(infectList)):
         if  v in infectList[i]:
             lists[i].append([v,c])

    #对lists进行排序。
    for i  in range(len(lists)):
       secList=sorted(lists[i],key=lambda x:(str(x[1]).lower(),x[0]),reverse = True )
       print (secList)
    # for i in range(len(lists)):
    #    print (lists[i])

























#  制造这个图
Ginti = nx.Graph()
#初始化图
for index in range(1,35):
    Ginti.add_node(index)
    print (index)

#构建图
G=ContractDict('karate_[Edges].csv',Ginti)


print ('一开始图的顶点个数',G.number_of_nodes())
print ('一开始图的边个数',G.number_of_edges())

'''
生成若干个感染节点。也就是谣言源点。每个节点有Cn以及Scn属性。
'''

#  先给全体的Cn、Scn的0的赋值。
for index in range(1,35):

    G.add_node(index, Cn=0,Scn=0)
# print (G.nodes[6416])



# 随机产生5个感染点。
sourceList=[]
for index in range(1,6):
    random_RumorSource=0
    random_RumorSource=random.randint(1, 34)
    sourceList.append(random_RumorSource)
    G.add_node(random_RumorSource,Cn=1)
print ('感染点列表',sourceList)





#  图形化还差得远。很烦。
#  开始送入我们的算法中，就G和basesore,还有感染源list三个参数
GResult,SGResult=Algorithm1(G,5,sourceList)





#打印出所传染的节点个数

Infected_node=[]
for i  in range(1,35):
    if  G.node[i]['Cn']== 1:
        Infected_node.append(i)

print ('感染点计数，以及他们',len(Infected_node),Infected_node)


# #打印出Csn
# for i  in range(1,35):
#     if  G.node[i]['Cn']== 1:
#
#         print ('print Scn',G.node[i]['Scn'])
#


#  生成感染图(注意，这里的感染图。是有所有接触过的顶点） ,不包括之前的未感染的边。
GInfection=Product_infection_Graph(G,'karate_[Edges].csv')
#我想看看感染图，
nx.write_gml(GInfection,'test.gml')


#copy防止引用
import copy

SGResult_copy=copy.deepcopy(SGResult)

print ('感染图，节点总数',SGResult.number_of_nodes())
print  ('感染图，边总数',SGResult.number_of_edges())
print  ('感染图，点显示',SGResult.nodes())
print  ('感染图，边总数',SGResult.edges())





import csv

#python2可以用file替代open
with open("test.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    cout=1
    writer.writerow(["source","target","type","Id"])
    for  u,v  in SGResult.edges():
        cout+=1
        writer.writerow([u,v,"Directed",cout])


#python2可以用file替代open
with open("test1.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id","label"])
    for  u  in SGResult.nodes():
        if u in sourceList:
           writer.writerow([u,'source'])
        else:
            writer.writerow([u])









#  将感染图，进行GN分区。

# algorithm = GN(GInfection)
algorithm = GN(SGResult)
partition, all_Q, max_Q=algorithm.run()
#暂时不需要画图
# algorithm.draw_Q()
algorithm.add_group()
algorithm.to_gml()





# 现在已经知道被感染的节点，那么问题来了，如何在被感染的分区之后的一些节点中找到
#源?


#prepare   parameter：准备参数，也就是我们的。


cal_source(SGResult_copy,partition)

