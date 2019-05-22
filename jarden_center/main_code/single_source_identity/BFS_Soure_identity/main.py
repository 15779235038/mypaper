import networkx as nx
import random


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




import community
import matplotlib.pyplot as plt
#使用Louvain分区,并返回每个分区的情况，以及每个分区的观察点



def  div(G):
    # better with karate_graph() as defined in networkx example.
    # erdos renyi don't have true community structure
    # G = nx.erdos_renyi_graph(30, 0.05)

    # first compute the best partition
    partition = community.best_partition(G)#   格式如下，就是每个节点属于哪个社区0: 0, 1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 2, 12: 2, 13: 4, 14: 5, 15: 6, 16: 3, 17: 0, 18: 0, 19: 2, 20: 3, 21: 3, 22: 3, 23: 4, 24: 4, 25: 4, 26: 4, 27: 4, 28: 4, 29: 4, 30: 4, 31: 4, 32: 4, 33: 4, 34: 4, 35: 4, 36: 4, 37: 4, 38: 4, 39: 4, 40: 4, 41: 5, 42: 3, 43: 2, 44: 2, 45: 6, 46: 6, 47: 4, 48: 4, 49: 3, 50: 3, 51: 5, 52: 7, 53: 5, 54: 1, 55: 1, 56: 1, 57: 1, 58: 1, 59: 1, 60: 7, 61: 7, 62: 3, 63: 1, 64: 5, 65: 5, 66: 3, 67: 3, 68: 3, 69: 3, 70: 3, 71: 3, 72: 3, 73: 0, 74: 0, 75: 4, 76: 4, 77: 3, 78: 3, 79: 5, 80: 3, 81: 3, 82: 3, 83: 3, 84: 3, 85: 0, 86: 5, 87: 3, 88: 1, 89: 1, 90: 3, 91: 3, 92: 3, 93: 4, 94: 5, 95: 5, 96: 4, 97: 6, 98: 6, 99: 6, 100: 6, 101: 6, 102: 1, 103: 7, 104: 7, 105: 3, 106: 3, 107: 3, 108: 3, 109: 3, 110: 3, 111: 3, 112: 3, 113: 4, 114: 4, 115: 4, 116: 4, 117: 3, 118: 3, 119: 4, 120: 0, 121: 3, 122: 7, 123: 4, 124: 6, 125: 6, 126: 1, 127: 3, 128: 5, 129: 5, 130: 5, 131: 1, 132: 1, 133: 5, 134: 8, 135: 4, 136: 4, 137: 1, 138: 1, 139: 6, 1
    # print (partition)    #键值对，如何找出跟其他节点相连的点作为监测点。
    size = float(len(set(partition.values())))
    print ('社区个数'+str(size) )  #社区个数
    '''
    制造出社区具体，哪个区的分的很清楚
    '''
    commitylist=[list() for m in range (int(size))]
    #键值对，根据分区的个数形成[社区id:节点id]
    # print (len(commitylist))
    for key,value in partition.items():
        # d.iterkeys(): an iterator over the keys of d
        # print (key,value)
        commitylist[value].append(key)
    # print (len(commitylist))

    '''
    找出观察点，需要G来帮忙啊，
    
    '''
    # commitylist_Observe = [list() for n in range(int(size))]
    commity_Observe=[]  #每个社区的观察点都在这里了，
    for  i in range(len(commitylist)):
        com=[]

        for j in range(len(commitylist[i])):
           if  len(list(set(list(G.neighbors(commitylist[i][j]))).difference(set( commitylist[i])))):
                com.append(commitylist[i][j])
        commity_Observe.append(list(set(com)))
    # print (len(coom))


    # for  j  in range(len(commitylist[1])):
    #     for sourceNeightor in list(G.neighbors(commitylist[1][j])):
    #         if sourceNeightor not in commitylist[1]:  # 如果它的邻居有节点不在自己社区，就可以认为是观察点
    #            print (commitylist[1][j])





    return  commitylist,commity_Observe       #返回分区的点下标，以及每个区的观点点下标。




    # #我需要测试下。
    # temp=[]
    # templist=[]
    # for sourceNeightor in list(G.neighbors( commity_Observe[1][1])):
    #     temp.append(sourceNeightor)
    #     if sourceNeightor not in commitylist[1]:  # 如果它的邻居有节点不在自己社区，就可以认为是观察点
    #         templist.append(sourceNeightor)
    #
    # print (temp)
    # print (templist)
    # print (commitylist[1])




    # # drawing
    # size = float(len(set(partition.values())))
    # # print (size)  用这个方法分的社区个数。
    # pos = nx.spring_layout(G)
    # count = 0.
    # for com in set(partition.values()):
    #     count = count + 1.
    #     list_nodes = [nodes for nodes in partition.keys()
    #                   if partition[nodes] == com]
    #     nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
    #                            node_color=str(count / size))
    #
    # nx.draw_networkx_edges(G, pos, alpha=0.5)
    # plt.show()



#生成感染图，需要原图，源点，传播概率。总的传播时间片，以及观察点的list，就是让源点不不要在观察点钟诞生。


def Algorithm1(G,Source,probabilistic,time_sum,community_Obse_list):

    '''
    我们认为时间片是有问题的，这个时间片应该就是按照，不能是每隔一个时间片就传染一波。只能说每隔一个时间片就记录
    一线。传播也有有概率的。
    '''
    #算法重写，需要有个时间片的概念。
    print ('监控点个数')
    print (len(community_Obse_list))
    simqueue = Queue()
    simqueue.enqueue(Source)
    G.node[Source]['SIR'] = 1
    G.node[Source]['time'] = 0
    '''
    每次传播是完全随机的，但是度大的点被传播和转发的概率比较低，按照一个度数来排列。'''
    infection_list=[]
    for time  in range(0,time_sum):
        infectilist_every_time=[]
        # while(not(simqueue.empty())):
        if simqueue.size()==1:
            infectilist_every_time.append(simqueue.dequeue())
        else:
            for i  in  range(simqueue.size()):
                # print ('输出每次的队列数目'+str(simqueue.size()))
                infectilist_every_time.append(simqueue.dequeue())
        # print ('每次需要传染的节点'+str(infectilist_every_time))
        # print ('-----------------------------')

        for  infectionNode  in  infectilist_every_time:
            G.node[infectionNode]['SIR'] = 1
            for sourceNeightor in list(G.neighbors(infectionNode)):
                if sourceNeightor not in  infection_list:  #感染过得节点就不要再感染了。
                    random_num_I=random.random()
                    if  random_num_I>probabilistic:  #超过某一个概率，被传染。
                        G.node[sourceNeightor]['SIR']=1   #传染点
                        #现在就要给那些观察点加时间了。
                        infection_list.append(sourceNeightor)  #加入感染点
                        if  sourceNeightor  in community_Obse_list:
                          G.node[sourceNeightor]['time']=time
                          # print ('给这个节点加一个'+str(sourceNeightor)+'-----------'+str(time))
                        simqueue.enqueue(sourceNeightor)
                        # print (simqueue.size())
                        # 传染边
                        G.add_edges_from([(infectionNode, sourceNeightor)], Infection=1)
                    else:
                        simqueue.enqueue(sourceNeightor)
                        G.node[sourceNeightor]['time'] = time
        '''
        每一个时间点过去后，每个节点都要考虑是否需要恢复。而且恢复的节点周围边都要恢复过来。
        '''
        # 遍历这张图，如果对所有节点而言。大于某个概率就会恢复。当然

        # print ('被感染点恢复概率'+str(random_num_R))
        TEMP=[]
        for  node_num in range(len(list(G.nodes))):
            # print (G.node[node_num])
            TEMP.append(node_num)
            random_num_R = random.random()
            if  G.node[node_num]['SIR']==1:
                if node_num == Source or  node_num in community_Obse_list : #源点不可复原。
                    continue
                if random_num_R>0.7:  #超过某一个概率，恢复
                    G.node[node_num]["SIR"]=2
                    # #恢复后，要把它的邻边节点取消。
                    # for sourceNeightor in list(G.neighbors(node_num)):
                    #         # 恢复边
                    #         G.add_edges_from([(sourceItem_, sourceNeightor)], Infection=0)
                    #         # SG.remove_edge(sourceItem_,sourceNeightor)
        #看看这个吧。

    return  G





#把社区观察点的二级list变成以及list
def  Constr(community_Observe):
    com_list=[]
    for  i  in range(len(community_Observe)):
        for j in  range(len(community_Observe[i])):
            com_list.append(community_Observe[i][j])
    return com_list






import   numpy as np


#计算分数
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())



















#  制造这个图
Ginti = nx.Graph()
#初始化图,加很多节点
# for index in range(1,1005):
#     print (index)
#     Ginti.add_node(index)

#构建图
G=ContractDict('data/facebook_combined.txt',Ginti)

#因为邮件是一个有向图，我们这里构建的是无向图。
print ('一开始图的顶点个数',G.number_of_nodes())
print ('一开始图的边个数',G.number_of_edges())

#用Louvain构建社区画图看看

community,community_Observe=div(G)

#将comm_Observe构建成一个list，不要那种每个社区一个小list。麻烦

community_Obse_list=Constr(community_Observe)


#
# print ('度'+str(G.degree(807)))
#

'''
生成一个感染节点。也就是谣言源点。每个节点有Cn以及Scn属性。

Cn就是感染了，SIR模型。有SIR,分别有三个属性，都赋值为SIR。其中0为没被感染，1为被感染，2为感染后恢复。
'''

#  先给全体的Cn、Scn,time的0的赋值。
for index in range(0,4039):
    G.add_node(index, SIR=0)

for index in range(0,4039):
    G.add_node(index, time=1000)

# 初始化所有边是否感染。Infection

for  edge  in  list(G.edges):
    G.add_edges_from([(edge[0],edge[1])], Infection=0)






#初始化感染点序号,这里注意不能存在观察节点作为源点情况。
random_RumorSource=random.randint(0, 4039)
while random_RumorSource  in community_Obse_list:
       random_RumorSource = random.randint(0, 4039)
print ('感染点序号',random_RumorSource)

#生成感染图,源点和观察点不可恢复。
GResult=Algorithm1(G,random_RumorSource,0.7,4,community_Obse_list)


'''
对感染图而言，查看每个社区那些观察点那些被感染很重要,下面代码是找出最早开始的时间的观察点。定下要

寻找的社区。

'''
time_min=200
commity_ID=1000
time_lists=[]
print ('社区个数检测版本'+str(len(community_Observe)))
for  i in range(len(community_Observe)):
    for j in range(len(community_Observe[i])):
            time_lists.append(GResult.node[community_Observe[i][j]]['time'])
            if  GResult.node[community_Observe[i][j]]['time']<time_min:
                # print (GResult.node[community_Observe[i][j]]['time'])
                print ('看看有多少次寻找时间最短'+str(time_min))
                time_min=GResult.node[community_Observe[i][j]]['time']
                commity_ID=i #社区id

print ('看看有多少个检测点被感染并且有时间'+str(len(time_lists)))
print ('最早的时间'+str(time_min))
print ('社区ID就是我们这个ID')
print (commity_ID)   #社区id，从0开始。所以这个commity_ID为3的话，指的其实是4这个社区。






'''
那么现在只需要那个社区的观察点，以及所有节点。再针对所有节点判断。构建路径，
'''

if  random_RumorSource in community[commity_ID]:
    print ("源点在这个社区的，那么现在构建这个社区图。")

print('社区所有id个数'+'-----------'+str(len(community[commity_ID])))
print('社区观察点个数'+'-------------------'+str(len(community_Observe[commity_ID])))
print (community[commity_ID])
print (community_Observe[commity_ID])







#先输出这个社区检测点的time

community_observe_dict={}
for  i   in  community_Observe[commity_ID]:
    if  GResult.node[i]['time']!= 1000:
        community_observe_dict[i]=GResult.node[i]['time']
        # print (GResult.node[i]['time'])
#把监测点按照时间排序
Observe_dit_sort=sorted(community_observe_dict.items(),key=lambda  item:item[1])
print (Observe_dit_sort)




#构造只有这个社区图（只有这个社区节点，以及社区节点之间边），没有连到外界的边。
community_infection=nx.Graph()

for  i   in  community[commity_ID]:
    for sourceNeightor in list(GResult.neighbors(i)):
        if  sourceNeightor in   community[commity_ID]:
            community_infection.add_edges_from([(i ,sourceNeightor)], weigth=1)

print (community_infection.nodes.__len__())
print (community_infection.edges.__len__())


#分别计算这个社区从时间最小的检测点开始，依次从他的附近节点开始计算。除了检测点之外的点，计算他们

#求出感染社区非检查点的其他点。
non_Observe = list(set(community_infection.nodes).difference(set(community_Observe[commity_ID])))
if  random_RumorSource  in non_Observe :
    print ('是的,感染点在非检测点里面。')
# print  (non_Observe)

#构建关于非检测点字典，包括[node,score]

# non_Observe_list_score=[list() for m in range (int(len(non_Observe)))]
# for  i  in  range(len(non_Observe_list_score)):
#     non_Observe_list_score[i].append(non_Observe[i])
#
#
# for key in  non_Observe_list_score:
#     # d.iteritems: an iterator over the (key, value) items
#     print( key)
#
#
#

max=0


#选择最先的那个检测节点出来，
k=list(community_observe_dict.items())[0]
print ('最先达到的点的id是')
print (k[0])
community__list_observe=sorted(list(community_observe_dict.items()),key=lambda x:x[1])   #这是本社区所有观测点的以及时间list

# print (community__list_observe)   #按照时间排序的这个社区观测点，格式为【观察点id：时间】

all_temp=[]

sourceNeightor_source={}
score=0
#从最先那个点的邻居开始找。统计邻居节点到其他检测点的距离。






sourceNeightor_score=[]
maybe_source=k[0]
sourceNeightor_score.append([maybe_source,1000])

sourceNeightor_score_dict={}
sourceNeightor_score_dict[maybe_source]=1000


isTure=0
while isTure!=1:
    for  sourceNeightor  in   list(community_infection.neighbors(maybe_source)):
        temp_list=[]
        if  sourceNeightor in non_Observe:
            #构建邻点到其他检测点的最短距离。BFS，计算分
            for  i in  community__list_observe:
                 temp_list.append([sourceNeightor,i[0],nx.dijkstra_path_length(community_infection, sourceNeightor, i[0]  , weight='weight')] ) # 求最短距离)
            #将邻点与其他检测点的最短距离跟检测点的时间做方差。得到每个邻点分数。方差越小就越是下一个被选节点。
            length = [x[2] for x in  temp_list]
            time_delay=[x[1] for x in  community__list_observe]
            score=rmse(np.array(length),np.array(time_delay))
        sourceNeightor_score.append([sourceNeightor,score])
        sourceNeightor_score_dict[sourceNeightor]=score

            # sourceNeightor_source[sourceNeightor]=score
        #找出邻居节点分数最低的那个节点，如果比本身还低。就终止，反之就继续。从最高的那个节点开始找。
    sourceNeightor_score_sort = sorted( sourceNeightor_score, key=lambda x:  x[1])
    print (sourceNeightor_score_sort)
    sourceNeightor_score_first=[x[0] for x in   sourceNeightor_score]
    if  sourceNeightor_score_sort[0][1]< sourceNeightor_score_dict[maybe_source]:   #邻居最低的那个点比源点低。就从他开始
        maybe_source=sourceNeightor_score_sort[0][0]
    else:
        print ('定位的源点位置'+str(maybe_source))
        isTure=1


print (sourceNeightor_score_dict[maybe_source])  #这是最先达到节点的邻居的分数，其实就是他们分别的方差啦。


#现在算下我们的源点与真正源点距离。


error_dist=nx.dijkstra_path_length(GResult, maybe_source, random_RumorSource, weight='weight') # 求最短距离)
print ('我所定位的源点与真实源点距离'+str(error_dist))
























SIR1=0  #被感染店数目
SIR2=0   #被感染后恢复点数目
SIR3=0   #没有任何感染点数目
for  node in range(len(list(GResult.nodes))):
     if GResult.node[node]['SIR']==1:
        SIR1=SIR1+1
     elif GResult.node[node]['SIR']==2:
         SIR2=SIR2+1
     elif GResult.node[node]['SIR']==0:
         SIR3=SIR3+1

SIR4=0
for edge in GResult.edges.data('Infection'):
   if edge[2]==1:
       SIR4=SIR4+1
print ('被感染点数目'+str(SIR1))
print ('被感染后恢复点数目'+str(SIR2))
print ('没有任何感染点数目'+str(SIR3))
# print ('感染母图被感染的边的个数'+str(SIR4))




print ('----------------------------------')
































