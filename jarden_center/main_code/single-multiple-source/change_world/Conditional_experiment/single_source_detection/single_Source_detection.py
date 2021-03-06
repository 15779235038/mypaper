import random
import math
import networkx  as nx
from collections import defaultdict
import commons
from jordan_center import jordan_centrality
import  rumor_centrality_graph_main
import  numpy as np
class Single_source:
    def __init__(self):
        pass

    # 这是sample-path，也就是commons挖过来的
    def revsitionAlgorithm_singlueSource(self,subinfectG):
        # print('反转算法参数,u和h' + str(u) + '----------' + str(h))
        nodelist = list(subinfectG.nodes)
        source1G = nx.Graph()  # 构建新的单源传播圆出来
        source1G = subinfectG
        print('传播子图为source1G,它的点数和边数为' + str(source1G.number_of_nodes()) + '-------' + str(
            source1G.number_of_edges()))
        # 在nodelist找出源点来。
        times = 50  # 时间刻多点
        IDdict = {}

        IDdict_dup = {}
        # 先赋予初始值。
        for node in list(source1G.nodes):
            # subinfectG.node[node]['ID']=list(node)   #赋予的初始值为list
            IDdict[node] = [node]
            IDdict_dup[node] = [node]
        allnodelist_keylist = []  # 包含所有接受全部节点id的键值对的key
        for t in range(times):
            print(
                't为' + str(t) + '的时候-----------------------------------------------------------------------------')
            for node in nodelist:  # 对每一个节点来说
                for heighbour in list(nx.all_neighbors(source1G,node)):  # 对每一个节点的邻居来说
                    retD = list(
                        set(IDdict[heighbour]).difference(set(IDdict[node])))  # 如果邻居中有这个node没有的，那就加到这个node中去。
                    if len(retD) != 0:  # 表示在B中，但不在A.是有的，那就求并集
                        # 求并集,把并集放进我们的retC中。
                        # print ('并集就是可使用'+str(retD))
                        retC = list(set(IDdict[heighbour]).union(set(IDdict[node])))
                        IDdict_dup[node] = list(set(IDdict_dup[node] + retC))  # 先用一个dict把结果装入,然后这个时间过去再加回去。

            for key, value in IDdict_dup.items():
                IDdict[key] = IDdict_dup[key]
            # for key, value in IDdict.items():
            #     print(key, value)
            # 在每一个时间刻检查是否有节点满足获得所有的id了。

            flag = 0
            for key, value in IDdict.items():
                # d.iteritems: an iterator over the (key, value) items
                if sorted(IDdict[key]) == sorted(nodelist):
                    print('在t为' + str(t) + '的时间的时候，我们有了接受全部node的ID的人')
                    print('它的key为' + str(key))
                    allnodelist_keylist.append(key)
                    print('有了接受所有的节点了这样的节点了')
                    flag = 1
                # 如果有收集到了50%的节点，那么就到了。

            if flag == 1:
                break
        # print (IDdict)
        print(allnodelist_keylist)

        result = 0
        resultlist = []
        # 如果在一个t的时候只有一个点。那就认为是节点，否则认为是多个节点。就要排序了
        if len(allnodelist_keylist) == 1:
            print('那就是这个源点了')
            result = allnodelist_keylist
        else:
            '''
            之前只返回某一个节点的
            '''
            # 构建样本路径
            print('构建样本路径看看')
            jarcenlist = []
            for i in allnodelist_keylist:
                jarcenlist.append([i, nx.eccentricity(source1G, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                resultlist = sorted(jarcenlist, key=lambda x: x[1])
            result = [resultlist[0][0]]
            print('构建样本路径之后结果为' + str(resultlist[0][0]))

            '''
            现在返回所有能接收到所有源点的。
            '''
            # result = allnodelist_keylist

        return result  #只返回最好的node



    '''
    
    第二种单源定位方法。
    我们提出一种新的单源定位方法，基于覆盖率计算的。
    统计每个点对于整个感染图的每个点计算公式，包括距离中心和覆盖率中心的综合计算方式。
    公式等于覆盖率/距离,越大越好。
    
    思路：从每个点计算一次djstra方法，统计距离。
    传入的是原始图
    '''

    def  single_source_bydistance_coverage(self,infectG,subinfectG,true_source):
        sort_dict = commons.partion_layer_dict(infectG, 10)  # 分层
        print('sort_list', sort_dict)
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode,ditance in length_dict.items():
                lens_degree = len(list(nx.neighbors(infectG,othernode)))
                node_import += sort_dict[othernode]*lens_degree / (ditance+1)
            node_cal.append([node,node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1], reverse=True)

        print(sort_list)
        # print('在的',[x[0] for x  in sort_list[:200] if x[0] ==true_source])
        return  sort_list[0]










    #种子节点的看看都在那里
    def single_source_bydistance_coverage_SECOND(self, infectG, subinfectG, true_source):
        sort_dict = commons.partion_layer_dict(infectG, 10)  # 分层
        print('sort_list', sort_dict)
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode, ditance in length_dict.items():
                lens_degree = len(list(nx.neighbors(infectG, othernode)))
                node_import += sort_dict[othernode] * lens_degree / (ditance + 1)
            node_cal.append([node, node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1], reverse=True)
        print(sort_list)
        print('在的', [x[0] for x in sort_list[:200] if x[0] == true_source])
        return sort_list[0]

    '''
    第3种单源定位方法。距离中心
    就是每个点距离其他点最近的距离中心。就是了的。

    '''
    def  single_source_bydistance(self,subinfectG):
        node_cal = []
        for node in subinfectG:
            node_import = 0
            length_dict = nx.single_source_bellman_ford_path_length(subinfectG, node, weight='weight')
            for othernode,ditance in length_dict.items():
                node_import += ditance
            node_cal.append([node,node_import])
        sort_list = sorted(node_cal, key=lambda x: x[1])
        print(sort_list)
        return  sort_list[0]

    '''
    第5种单源定位方法，
    利用边界点做一个k-core想法。
    '''

    def effectDistance(self, probily):
        return 1 - math.log(probily)

    '''
    
    第6种方法，就是利用2018年的那篇。
    Classifying Quality Centrality for Source
    
    1 找出原始图最大子图，然后找出所有感染点为M+，所有非感染点为M-。
    2 遍历每个点，计算每个点跟它们的距离。再计算平均值。
    '''
    def  single_source_byQuality_centrality(self,infectG,subinfectG):
        #你好，再见
        for edge in infectG.edges:
            # G.add_edge(edge[0], edge[1], weight=1)
            randomnum = random.random()
            infectG.add_edge(edge[0], edge[1], weight=self.effectDistance(randomnum))
        m_list_add = [x for x in list(infectG.nodes()) if infectG.node[x]['SI']== 2]
        m_list_dif = [x for x in list(infectG.nodes()) if infectG.node[x]['SI'] == 1]
        print('len(m_list_dif',len(m_list_add))
        print(subinfectG.number_of_nodes())
        len_add= len(m_list_add)
        len_dif = len(m_list_dif)
        CQ_dict = defaultdict(int)
        for node_temp in m_list_add:
            length_dict = nx.single_source_bellman_ford_path_length(infectG,source=node_temp,weight='weight')
            d_add_all = 0
            d_dif_all = 0
            d_dif_avg = 0
            d_add_avg = 0
            for add in m_list_add:
                d_dif_all += length_dict[add]
            for dif in m_list_dif:
                d_add_all += length_dict[dif]

            d_dif_avg = d_dif_all/len_dif
            d_add_avg = d_add_all/len_add
            CQ_dict[node_temp] = (d_dif_avg -d_add_avg)/d_add_avg

        CQ_dict_sort = sorted(CQ_dict.items(), key=lambda x: x[1],reverse=True)
        print('CQ_dict_sort', CQ_dict_sort)
        return CQ_dict_sort[0]
        # pass








    #几种中心性的性质都试一试吧。hhhh
    def single_source_bybetweenness_centrality(self,subinfectG):
        # 介数中心性
        between_dict = nx.betweenness_centrality(subinfectG)
        sort_eccentricity_dict = sorted(between_dict.items(), key=lambda x: x[1], reverse=True)
        print('sort_eccenritci_dict', sort_eccentricity_dict)



        # #特征向量中心性。
        # centrality = nx.eigenvector_centrality(subinfectG)
        # sort_eigener_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        # print('eigenvector_centrality', sort_eigener_centrality)
        # # self.center = sort_eigener_centrality[0][0]

        # Kaza中心性
        # G = nx.path_graph(4)
        # maxnumber = max(nx.adjacency_spectrum(subinfectG))
        # print(maxnumber)
        # phi = (1 + math.sqrt(5)) / 2.0  # largest eigenvalue of adj matrix
        # centrality = nx.katz_centrality(subinfectG, 1/ maxnumber -0.01)
        # katz_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        # print('katz_centrality',katz_centrality)

        # center_list = []
        # center_list.append(sort_eccentricity_dict[0][0])
        # center_list.append(sort_colse_centrality_dict[0][0])
        # center_list.append(sort_degree_centrality[0][0])
        # center_list.append(sort_eigener_centrality[0][0])
        # center_list.append(katz_centrality[0][0])

        # return center_list
        return sort_eccentricity_dict[0]

    #接近度中心性
    def  single_source_bycloseness_centrality(self,subinfectG):

        #   接近度中心性
        closeness_centrality = nx.closeness_centrality(subinfectG)
        sort_colse_centrality_dict = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)
        print('sort_colse_centrality_dict', sort_colse_centrality_dict)

        return sort_colse_centrality_dict[0]

    #degree_centrali
    def  single_source_bydegree_centrality(self,subinfectG):

        #   度中心性，这个效果最好，简直了。
        degree_centrality = nx.degree_centrality(subinfectG)
        sort_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        print('sort_degree_centrality', sort_degree_centrality)

        return sort_degree_centrality[0]

    #特征向量中心性
    def single_source_byeigenvector_centrality(self, subinfectG):

        #特征向量中心性。
        centrality = nx.eigenvector_centrality(subinfectG,max_iter=1000)
        sort_eigener_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        print('eigenvector_centrality', sort_eigener_centrality)
        # self.center = sort_eigener_centrality[0][0]
        return sort_eigener_centrality[0]



    '''
    1  知道自己的传播时间t，判断jarden center是否可以加上时间t来做。
        
    
    
    
    '''

    def  single_source_get_T_jarden_center(self,t,subinfectG):





        pass


    '''
    1 谣言中心实现。目前只能处理树，处理树直接送进去就可以了。
    
    2 如果要处理图，就要面临随机挑选一个点作为源点构成BFS结构的问题。
    我们实现的是基于贪心BFS的方法，就是选择每个点进行BFS，但是挑选其中谣言中心性最高的作为结果。
    
    
    '''

    def  rumor_center(self,infectG,subiG,source_true):

        if nx.is_tree(subiG) ==True:

            rumor_center_object= rumor_centrality_graph_main.rumor_center()
            rumor_center, center=rumor_center_object.rumor_centrality(subiG)
            return [rumor_center]
        else:
            #这里做一个改进。对于一个图来说。
            # 有两个方案，
            # 1  一种是随机取一个点作为BFS树，然后计算中心性

            # 2 一种是每一个做一个BFS树，谣言中心性。选谣言中心性最大的为结果.我们复现的是这个。
            rumo_ceterAndcenter =[]
            rumor_center_object = rumor_centrality_graph_main.rumor_center()
            for  bfs_source_node in list(subiG.nodes()):
                direct_tree = nx.bfs_tree(subiG,source=bfs_source_node)
                subinfectG  = direct_tree.to_undirected()
                rumor_center, center = rumor_center_object.rumor_centrality(subinfectG)
                rumo_ceterAndcenter.append([bfs_source_node,rumor_center,center])

            sort_rumor_center = sorted(rumo_ceterAndcenter,key = lambda x:x[2],reverse= True)
            #
            print('sort_rumor_center',sort_rumor_center)

            return [sort_rumor_center[0][0]]


    '''
    1 乔丹中心实现。
    '''

    def jarden_center(self, infectG, subiG, source_true):
        # 将图构造成两个list，一个是感染点list，一个是感染和它的邻居点构造成的list
        infect_node = []
        infect_neighbour_list = []
        print(infectG.number_of_nodes())
        random_node = random.choice(list(subiG.nodes()))
        subinfectG = nx.bfs_tree(subiG, source=source_true)
        # who_infected =  [[] for i in range(infectG.number_of_nodes())]
        # 找出最大的id数目。
        maxs = 0
        for node_index in list(infectG.nodes):
            if node_index > maxs:
                maxs = node_index
        print('maxs', maxs)
        for node in list(subinfectG.nodes()):
            infect_node.append(node)
        who_infected = [[] for i in range(maxs + 1)]

        i = 0
        for node_temp in infect_node:
            neighbour_list = list(nx.all_neighbors(subinfectG, node_temp))
            neighbour_list_index = []
            for neighbour in neighbour_list:
                neighbour_list_index.append(infect_node.index(neighbour))
            who_infected[i] = neighbour_list_index
            i += 1
        print('infect_node', infect_node)
        print('who_infected', who_infected)
        jordan_center_object = jordan_centrality.jordan()
        jordan_center = jordan_center_object.jordan_centrality(who_infected)
        print(' jordan_center',  jordan_center)
        # print('center', center)
        return [infect_node[jordan_center]]




    '''
    1 乔丹中心直接实现
    '''

    def jarden_cente_networkx(self, infectG, subiG, source_true):
       dict = nx.eccentricity(subiG)
       print('dict',dict)
       sort_dict = sorted(dict.items(),key= lambda  x:x[1])
       print('sort_dict',sort_dict)
       print('源是',[sort_dict[0][0]])
       return [sort_dict[0][0]]




    def  Gromov_matrix(self,infectG,subiG,ture_source):

        pass






    '''
    覆盖率种子节点+传播子图BFS构建+单源定位。
    
    思路：
    1 覆盖率确定那个源点，如何利用覆盖率呢？就是对每个点进行BFS树构建。
    如果某一层的未感染点多于某个比例，就停止扩散。类似于随机游走。
    
    用这个：或者以所有点进行BFS到全部点（传播点+未传播点）某一层，这一层没有感染点就停止了。
    ，计算每一层的未感染点比例。计算
    平均值作为这个点的一个指标。
    2 然后对那个源点进行BFS树构建
    3 单源定位。
    '''
    def  coverage_BFS_single_source(self, infectG, subInfectG,source_ture):
        # 进行所有点有向树构建，再进行层次遍历。针对每一层都进行传播点/全部的比例计算。
        node_every_ratio = []
        for node_every in list(subInfectG.nodes()):
            #进行BFS树构造，
            tree=nx.bfs_tree(infectG, source=node_every)
            #进行层次遍历。返回每一层顶点。
            BFS_nodes = commons.BFS_nodes(tree, node_every, infectG)
            ratio_all =0
            for layer_node in BFS_nodes:
                infect_node_len=len([x for x in layer_node if infectG.node[x]['SI']==2])
                # print('infect_node_len',infect_node_len)
                infect_node_not = len([x for x in layer_node if infectG.node[x]['SI'] == 1])
                # print('infect_node_not', infect_node_not)
                infect_ratio = infect_node_len/len(layer_node) #感染点的比例
                ratio_all += infect_ratio
            ratio_average = ratio_all / len(BFS_nodes)
            node_every_ratio.append([node_every, ratio_average])

        node_every_ratio_sort = sorted(node_every_ratio, key=lambda x : x[1], reverse=True)
        print(node_every_ratio_sort)

        print('distacne',nx.shortest_path_length(infectG,source=node_every_ratio_sort[0][0],target=source_ture))
        #以第一个点进行BFS树构建，然后单源定位。

        # plot_main. plot_G_node_color(subInfectG,[1])(infectG, subInfectG, source_ture, [node_every_ratio_sort[0][0]])
        print('isTree,',nx.is_tree(subInfectG))
        subinfectG = nx.bfs_tree(subInfectG, source=node_every_ratio_sort[0][0])
        print('isTree,', nx.is_tree(subinfectG))
        count_number = 0
        undirectG=subinfectG.to_undirected()
        result_node = self.revsitionAlgorithm_singlueSource(undirectG)
        return result_node






    '''
    1 基于覆盖率的置信算法实现
    思路：
        1 初始化每个点的一阶邻域覆盖率
        2 随机某个点i和它的邻居节点j1，j2，j3。（通过i来影响j）
        3 从i向j1，j2，j3发送消息。消息的定义公式一定要搞下，操。
        再重复2，3直到所有点都更新了。
        4 计算每个点的置信度，将它所收到的所有消息乘积起来。
        最大的就是谣言中心。
    '''
    def belief_algorithm(self,infectG,subinfectG,true_source):
        # 初始化所有的点的覆盖率，有初始值。
        node_coverage = defaultdict(int)
        for node_index in list(infectG.nodes()):
            if infectG.node[node_index]['SI'] == 2:
                neighbour = list(nx.neighbors(infectG, node_index))
                SI_len = len([x for x in neighbour if infectG.node[x]['SI'] == 2])
                # if SI_len != len(neighbour):
                #     print('不是啊啊发士大夫')
                node_coverage[node_index] = SI_len / len(neighbour)
        print('node_coverage', node_coverage)

        # node_message = defaultdict(list)  # 这个会根据无向图的所有点和度生成一个空的度。
        # 直接有一个矩阵不就好了嘛。
        node_message = dict()
        # new_arrays = np.zeros((infectG.number_of_nodes(), infectG.number_of_nodes()))
        # 变成图版本，
        for edge in infectG.edges():
            node_message[(edge[0], edge[1])] = 1
            node_message[(edge[1], edge[0])] = 1

        for i in range(0, 10):
            node_message_temp = dict()
            for edge in infectG.edges():
                node_message_temp[(edge[0], edge[1])] = 1
                node_message_temp[(edge[1], edge[0])] = 1

            # 对每个点来说，向四周发送消息。消息为
            lists = list(subinfectG.nodes)
            random.shuffle(lists)
            for node in lists:
                for neighbour_temp in list(nx.neighbors(subinfectG, node)):
                    mutiplue = 1
                    # 制造list，除去邻居neighbor_temp的node其他邻居节点list
                    neighbour_temp_list = list(nx.neighbors(subinfectG, node))
                    neighbour_temp_list.remove(neighbour_temp)
                    for neighbour_two in neighbour_temp_list:
                        mutiplue = mutiplue +node_message[neighbour_two,node]  # 改成了加，效果很好啊。还是需要再修改下，这个公式
                    # 消息更新
                    node_message_temp[(node, neighbour_temp)] = mutiplue * node_coverage[node]  # 还是有问题，就是这里应该有加的。
            # 还是有问题，就是这里应该有加的。
            # print('node_message_temp',node_message_temp)
            node_message =node_message_temp

            # print('node_message',node_message)
            print('-----------------------')
            count  = 0
            for k,v in node_message.items():
                if count > 10:
                    break
                print('k,v',(k,v))
                count += 1

        # 这个矩阵就是所有点相互之间发送的消息了。
        node_belief_dict = defaultdict(int)
        # 现在计算每个点的置信度。
        for node_belief in list(subinfectG.nodes):
            mutiplue_belief = 1
            for neighbour_belief in list(nx.neighbors(subinfectG, node_belief)):
                mutiplue_belief = mutiplue_belief * node_message[(neighbour_belief, node_belief)]  # 注意这里是反的，并不是正
            node_belief_dict[node_belief] = mutiplue_belief * node_coverage[node_belief]


        node_belief_dict_sort = sorted(node_belief_dict.items(), key=lambda x: x[1], reverse=True)
        print('node_belief_dict', node_belief_dict_sort)
        print('distance', nx.shortest_path_length(infectG, source=node_belief_dict_sort[0][0], target=true_source))
        same_belief_list = []
        same_belief_list.append(node_belief_dict_sort[0][0])
        for index in range(0, len(node_belief_dict_sort) - 1):
            if node_belief_dict_sort[index][1] == node_belief_dict_sort[0][1]:
                same_belief_list.append(node_belief_dict_sort[index][0])

        # for source_index in same_belief_list:
        #     print(nx.shortest_path_length(infectG, source=source_index, target=true_source))

        jarcenlist = []
        resultlist = []
        for i in same_belief_list:
            jarcenlist.append([i, nx.eccentricity(subinfectG, i)])  # 按照离心率进行排序,最小离心率的就是源点。
            resultlist = sorted(jarcenlist, key=lambda x: x[1])

        print('偏心率最低的是', resultlist[0][0])
        return [resultlist[0][0]]

    '''
        1 基于覆盖率的置信算法实现
        思路：
            1 初始化每个点的一阶邻域覆盖率
            2 随机某个点i和它的邻居节点j1，j2，j3。（通过i来影响j）
            3 从i向j1，j2，j3发送消息。消息的定义公式一定要搞下，操。
            再重复2，3直到所有点都更新了。
            4 计算每个点的置信度，将它所收到的所有消息乘积起来。
            最大的就是谣言中心。


    '''



    def belief_algorithm_newworkx(self, infectG, subinfectG, true_source):
            # 初始化所有的点的覆盖率，有初始值。
            node_coverage = defaultdict(int)
            for node_index in list(infectG.nodes()):
                if infectG.node[node_index]['SI'] == 2:
                    neighbour = list(nx.neighbors(infectG, node_index))
                    SI_len = len([x for x in neighbour if infectG.node[x]['SI'] == 2])
                    # if SI_len != len(neighbour):
                    #     print('不是啊啊发士大夫')
                    node_coverage[node_index] = SI_len / len(neighbour)
            print('node_coverage', node_coverage)

            # node_message = defaultdict(list)  # 这个会根据无向图的所有点和度生成一个空的度。
            # 直接有一个矩阵不就好了嘛。
            node_message =dict()
            # new_arrays = np.zeros((infectG.number_of_nodes(), infectG.number_of_nodes()))
            # 变成图版本，
            for edge in  infectG.edges():
                node_message[(edge[0],edge[1])] = 0
                node_message[(edge[1],edge[0])] = 0


            for i in range(0, 50):
                # 对每个点来说，向四周发送消息。消息为
                lists = list(subinfectG.nodes)
                random.shuffle(lists)
                for node in lists:
                    for neighbour_temp in list(nx.neighbors(subinfectG, node)):
                        mutiplue = 0
                        # 制造list，除去邻居neighbor_temp的node其他邻居节点list
                        neighbour_temp_list = list(nx.neighbors(subinfectG, node))
                        neighbour_temp_list.remove(neighbour_temp)
                        for neighbour_two in neighbour_temp_list:
                            mutiplue = mutiplue + node_coverage[neighbour_two]  # 改成了加，效果很好啊。还是需要再修改下，这个公式
                        # 消息更新
                        node_message[(node, neighbour_temp)] = mutiplue + node_coverage[node]# 还是有问题，就是这里应该有加的。
            # 这个矩阵就是所有点相互之间发送的消息了。
            node_belief_dict = defaultdict(int)
            # 现在计算每个点的置信度。
            for node_belief in list(subinfectG.nodes):
                mutiplue_belief = 1
                for neighbour_belief in list(nx.neighbors(subinfectG, node_belief)):
                    mutiplue_belief = mutiplue_belief * node_message[(neighbour_belief,node_belief)]  # 注意这里是反的，并不是正
                node_belief_dict[node_belief] = mutiplue_belief * node_coverage[node_belief]

            node_belief_dict_sort = sorted(node_belief_dict.items(), key=lambda x: x[1], reverse=True)
            print('node_belief_dict', node_belief_dict_sort)
            print('distance', nx.shortest_path_length(infectG, source=node_belief_dict_sort[0][0], target=true_source))
            same_belief_list = []
            same_belief_list.append(node_belief_dict_sort[0][0])
            for index in range(0, len(node_belief_dict_sort) - 1):
                if node_belief_dict_sort[index][1] == node_belief_dict_sort[0][1]:
                    same_belief_list.append(node_belief_dict_sort[index][0])

            for source_index in same_belief_list:
                print(nx.shortest_path_length(infectG, source=source_index, target=true_source))

            jarcenlist = []
            resultlist = []
            for i in same_belief_list:
                jarcenlist.append([i, nx.eccentricity(subinfectG, i)])  # 按照离心率进行排序,最小离心率的就是源点。
                resultlist = sorted(jarcenlist, key=lambda x: x[1])

            print('偏心率最低的是', resultlist[0][0])
            return [resultlist[0][0]]


    '''
      设计本类用来做单源  定位。
    # '''

    def main(self,filename):

        # #拿到图
        initG = commons.get_networkByFile(filename)

        # ecc=nx.eccentricity(initG)
        # sort_ecc=sorted(ecc.items(),key=lambda  x:x[1])
        # product_srouce =sort_ecc[0][0]
        max_sub_graph = commons.judge_data(initG)
        # source_list = product_sourceList(max_sub_graph, 2)
        source_list = commons.product_sourceList(max_sub_graph, 1)
        # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
        infectG,T = commons.propagation1(max_sub_graph,[1000])
        # infectG1, T = commons.propagation1(max_sub_graph, [source_list])
        subinfectG = commons.get_subGraph_true( infectG)  # 只取感染点，为2表示,真实的感染图。
        #将在这里进行单源测试。
        print(sorted(list(subinfectG.nodes())))
        #
        # result_node = self.revsitionAlgorithm_singlueSource(subinfectG)
        # ''' 第二种，就是coverage/distance'''
        # result_node= self.single_source_bydistance_coverage(infectG,subinfectG,source_list[0])
        # '''  第3种，距离中心'''
        # result_node = self.single_source_bydistance( subinfectG)

        #'''  第6种，质量距离中心'''
        # result_node = self.single_source_byQuality_centrality(infectG,subinfectG)


        # #''''第7种，特征向量中心性
        # result_node = self.single_source_bybetweenness_centrality( subinfectG)
        # #''''第8种，反转加t性
        # result_node = self.single_source_get_T_jarden_center( T,subinfectG)

       #第9种，谣言中心性‘’

        result_node = self.rumor_center(infectG,subinfectG,1000)

      #
      # # #’‘ 乔丹中心性
      #   result_node = self.jarden_cente_networkx(infectG,subinfectG,source_list[0])


        # 覆盖率加我们的操作
        # result_node = self.coverage_BFS_single_source(infectG,subinfectG,source_list[0])

        # #多个观察点
        # result_node = self.coverage_BFS_single_source(infectG,subinfectG,source_list[0])

        #基于覆盖率的计算方式

        # result_node = self.belief_algorithm(infectG, subinfectG,1000)
        print('真实源是',source_list[0])
        # print('预测源是',result_node[0])
        distance= nx.shortest_path_length(subinfectG,source=1000, target=result_node[0])
        print('结果他们的距离是', distance)
        return distance



import time

if __name__ == '__main__':
    test = Single_source()
    sum = 0
    # initG = commons.get_networkByFile('../../../data/CA-GrQc.txt')
    # initG = commons.get_networkByFile('../../../data/3regular_tree1000.txt')
    # initG = commons.get_networkByFile('../../data/4_regular_graph_3000_data.txt')
    # initG = commons.get_networkByFile(filename)
    # filname = '../../../data/4_regular_graph_3000_data.txt'
    # initG = commons.get_networkByFile('../../../data/email-Eu-core.txt')
    filname = '../../../data/CA-GrQc.txt'
    # filname = '../../../data/4regular_tree9.txt'
    # filname = '../../../data/random_tree_10000.txt'
    # filname = '../../../data/5regular_tree_10000.txt'


    # method ='distan+ covage'
    # method = 'jardan_center'
    # method ='distance'
    method = '谣言中心性'
    for i in range(0, 20):
        tempresult = test.main(filname)
        sum += tempresult  # 跑实验
        with open('result.txt', "a") as f:
            # f.write("这是个测试！")  # 这句话自带文件关闭功能，不需要再写f.close()
            f.write(str(time.asctime(time.localtime(time.time()))) + '\n')
            f.write('每一步的结果是   '+str(tempresult)+'      数据集'+'方法'+str(method) + str(filname) +   '\n')
    with open('result.txt', "a") as f:
        f.write('数据集' + str(filname)+'方法' +str(method)+ '总结果   ' + str(sum / 20) + '\n')
        f.write('\n')
    print('result', sum / 20)
    print(sum / 20)




