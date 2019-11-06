#画图工具，帮助直观看各种图。
import  commons
import matplotlib.pyplot as plt
import  networkx as nx
def   plot_G(G):
    nx.draw_networkx(G, pos=nx.spring_layout(G),node_size=20,node_color='red')
    plt.show()
    plt.savefig('test.png')
    plt.close()
    pass

import Partion_graph
import single_Source_detection

def plot_G_node_color(infectG,subinfectG,nodelist,two_source_list):
    # initG = commons.get_networkByFile('../../../data/2regular_tree.txt')
    # nx.draw_networkx(G, node_size=0.1)
    plt.figure(figsize=(20,20))
    pos = nx.spring_layout(infectG)  # positions for all nodes
    nodelist_all_graph =[]  #图的总节点数目

    for node in list(infectG.nodes()):
        nodelist_all_graph.append(node)

    node_subinfetG =[]
    for k in list(subinfectG.nodes()):
        node_subinfetG.append(k)


    for m in node_subinfetG:
        if m in nodelist_all_graph:
            nodelist_all_graph.remove(m)

    for i in nodelist:
        if i in nodelist_all_graph:
            nodelist_all_graph.remove(i)


    for j in two_source_list:
        if j in nodelist_all_graph:
            nodelist_all_graph.remove(j)

    edge_list =[]
    for edge in list(infectG.edges()):
        edge_list.append(edge)

    nx.draw_networkx_nodes(infectG, pos, nodelist=nodelist_all_graph, node_size=20, node_color='b')  #所有点的
    nx.draw_networkx_nodes(infectG, pos, nodelist=node_subinfetG, node_size=50, node_color='G')  #传播子图的

    nx.draw_networkx_nodes(infectG, pos, nodelist=two_source_list, node_size=300, node_color='Y')  #两个源的
    nx.draw_networkx_nodes(infectG, pos, nodelist=nodelist, node_size=300, node_color='R') #边界点的

    nx.draw_networkx_edges(infectG, pos, edgelist=edge_list, alpha=0.4)

    plt.axis('off')

    plt.savefig('test.png')
    plt.show()
    plt.close()
    pass




def plot_G_node_color_PPT(infectG,subinfectG,two_source_list,result_source_list):
    # initG = commons.get_networkByFile('../../../data/2regular_tree.txt')
    # nx.draw_networkx(G, node_size=0.1)
    plt.figure(figsize=(20,20))
    pos = nx.kamada_kawai_layout(infectG)  # positions for all nodes
    # pos = nx.spring_layout(infectG,center=two_source_list)  # positions for all nodes

    nodelist_all_graph =[]  #图的总节点数目

    for node in list(infectG.nodes()):
        nodelist_all_graph.append(node)

    node_subinfetG =[]
    for k in list(subinfectG.nodes()):
        node_subinfetG.append(k)


    for m in node_subinfetG:
        if m in nodelist_all_graph:
            nodelist_all_graph.remove(m)

    for i in result_source_list:
        if i in nodelist_all_graph:
            nodelist_all_graph.remove(i)


    for j in two_source_list:
        if j in nodelist_all_graph:
            nodelist_all_graph.remove(j)

    edge_list =[]
    for edge in list(infectG.edges()):
        edge_list.append(edge)

    nx.draw_networkx_nodes(infectG, pos, nodelist=nodelist_all_graph, node_size=20, node_color='b')  #所有点的
    nx.draw_networkx_nodes(infectG, pos, nodelist=node_subinfetG, node_size=50, node_color='G')  #传播子图的
    #
    nx.draw_networkx_nodes(infectG, pos, nodelist=two_source_list, node_size=300, node_color='R')  #两个源的
    nx.draw_networkx_nodes(infectG, pos, nodelist=result_source_list, node_size=100, node_color='Y') #边界点的

    nx.draw_networkx_edges(infectG, pos, edgelist=edge_list, alpha=0.4)

    plt.axis('off')

    plt.savefig('test.png')
    plt.show()
    plt.close()
    pass









initG =  commons.get_networkByFile('../../../data/2regular_tree.txt')
max_sub_graph = commons.judge_data(initG)
# source_list = product_sourceList(max_sub_graph, 2)
source_list = commons.product_sourceList(max_sub_graph, 1)
# print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
infectG,trueT = commons.propagation1(max_sub_graph, source_list)
subinfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。

# '''''''# 2 分区，分区的太多了，我们看看那种好。'''
#
# '''2.1   k-center方法'''
# partion_graph_object = Partion_graph.Partion_graph()
# result = partion_graph_object.other_k_center(infectG, subinfectG, source_list, source_number=2)
#
# single_Source_detection_object = single_Source_detection.Single_source()
# print('result', result)
# # 对每一个感染的点建图，用真实的建成一个传播子图
# result_source_list = []
#
# '''
#
#     3  针对2传回来的多个区域，开始定位源点。
#  '''
# for community in result:
#     subsubinfectG = nx.Graph()
#     for edge in list(subinfectG.edges()):
#         if edge[0] in community and (edge[1] in community):
#             subsubinfectG.add_edge(edge[0], edge[1])
#     # 看下图连通吗。
#     # maxsubsubinfectG = self.judge_data(subsubinfectG)
#     # 开始单源定位了。
#     '''jar center'''
#     # # source_node = single_Source_detection_object.revsitionAlgorithm_singlueSource(maxsubsubinfectG)
#     source_node = single_Source_detection_object.single_source_bydistance_coverage(infectG, subsubinfectG,
#                                                                                    source_list)
#     #
#     # source_node = single_Source_detection_object.single_source_bydistance(maxsubsubinfectG)
#
#     result_source_list.append(source_node[0])
#
#
#
#
single_Source_detection_object = single_Source_detection.Single_source()
source_node = single_Source_detection_object.revsitionAlgorithm_singlueSource(subinfectG)

# source_node = single_Source_detection_object.single_source_bydistance_coverage(infectG,subinfectG,source_list)

result_source_list =[]
result_source_list.append(source_node[0])


#需要画3种点，一个是源点，一个是传播点。一个是未传播点。


plot_G_node_color_PPT(initG,subinfectG,source_list,result_source_list)



# plot_G(initG)
#
# plot_G_node_color(initG,[1])