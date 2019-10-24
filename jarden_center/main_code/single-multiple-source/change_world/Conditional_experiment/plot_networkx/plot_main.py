#画图工具，帮助直观看各种图。
import  commons
import matplotlib.pyplot as plt
import  networkx as nx
def   plot_G(G):
    nx.draw_networkx(G, node_size=0.1,node_color='red')
    plt.show()
    plt.savefig('test.png')
    plt.close()
    pass



def plot_G_node_color(infectG,subinfectG,nodelist,two_source_list):
    # initG = commons.get_networkByFile('../../../data/2regular_tree9.txt')
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







# initG = commons.get_networkByFile('../../../data/2regular_tree9.txt')
# plot_G(initG)
#
# plot_G_node_color(initG,[1])