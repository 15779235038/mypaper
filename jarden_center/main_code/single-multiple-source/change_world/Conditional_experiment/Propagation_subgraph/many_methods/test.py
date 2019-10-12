# from igraph import *
# g = Graph.Famous("petersen")
# summary(g)
# plot(g)
#
#
# #networkx画图
#
# import networkx as nx
#
#
# G = nx.Graph()#创建空的网络图
# lists = [[('a','b',5.0),('b','c',3.0),('a','c',1.0)]]
# G.add_edge(1,2)
# import matplotlib.pyplot as plt
#
# nx.draw(G)
# plt.show()
#
#
#
#

# Author: Aric Hagberg (hagberg@lanl.gov)
import matplotlib.pyplot as plt
import networkx as nx

G = nx.cubical_graph()
pos = nx.spring_layout(G)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos,
                       nodelist=[0, 1, 2, 3],
                       node_color='r',
                       node_size=500,
                       alpha=0.8)



nx.draw_networkx_nodes(G, pos,
                       nodelist=[4, 5, 6, 7],
                       node_color='b',
                       node_size=500,
                       alpha=0.8)




# edges
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
nx.draw_networkx_edges(G, pos,
                       edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
                       width=8, alpha=0.5, edge_color='r')
nx.draw_networkx_edges(G, pos,
                       edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
                       width=8, alpha=0.5, edge_color='b')


# some math labels
labels = {}
labels[0] = r'$a$'
labels[1] = r'$b$'
labels[2] = r'$c$'
labels[3] = r'$d$'
labels[4] = r'$\alpha$'
labels[5] = r'$\beta$'
labels[6] = r'$\gamma$'
labels[7] = r'$\delta$'
nx.draw_networkx_labels(G, pos, labels, font_size=16)

plt.axis('off')
plt.show()












def plot_graph(porgration_node_list,porgration_edge_list):
    '''
    :param porgration_list:  #只需要传播节点以及边的list就可以了
    :return:
    '''

    G = nx.cubical_graph()
    pos = nx.spring_layout(G)  # positions for all nodes
    '''
    1 首先生成颜色表，需要几种颜色根据图来的。
    
    
    '''

    #根据node_list长度确定时间t。
        #
    for t in range(len(porgration_node_list)):




    # nodes
    nx.draw_networkx_nodes(G, pos,
                           nodelist=[0, 1, 2, 3],
                           node_color='r',
                           node_size=500,
                           alpha=0.8)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=[4, 5, 6, 7],
                           node_color='b',
                           node_size=500,
                           alpha=0.8)

    # edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(G, pos,
                           edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
                           width=8, alpha=0.5, edge_color='r')
    nx.draw_networkx_edges(G, pos,
                           edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
                           width=8, alpha=0.5, edge_color='b')

    # some math labels
    labels = {}
    labels[0] = r'$a$'
    labels[1] = r'$b$'
    labels[2] = r'$c$'
    labels[3] = r'$d$'
    labels[4] = r'$\alpha$'
    labels[5] = r'$\beta$'
    labels[6] = r'$\gamma$'
    labels[7] = r'$\delta$'
    nx.draw_networkx_labels(G, pos, labels, font_size=16)

    plt.axis('off')
    plt.show()








