import   networkx as nx
import matplotlib.pyplot as plt
def listToTxt(listTo, dir):
    fileObject = open(dir, 'a')
    fileObject.write(str(listTo).replace('(','').replace(')','').replace(',',' '))
    fileObject.write('\n')
    fileObject.close()

def ContractDict(dir, G):
    with open(dir, 'a') as f:
        for line in f:
            line1 = line.split()
            G.add_edge(int(line1[0]), int(line1[1]))
    for edge in G.edges:
        G.add_edge(edge[0], edge[1], weight=1)
        # G.add_edge(edge[0],edge[1],weight=effectDistance(randomnum))
    print(len(list(G.nodes)))
    # G.remove_node(0)
    print(len(list(G.nodes)))
    return G




# G=nx.full_rary_tree(4,10000)   #生成规定节点数目的常规树


# G= nx.watts_strogatz_graph(5000,7,0.5)  #小世界图
# G = nx.scale_free_graph(5000)        #无标度图

G=nx.general_random_intersection_graph(5000,)


print('IS_TREE',nx.is_tree(G))
# nx.draw(G,with_labels=True)
# plt.show()
print (len(list(G.nodes)))
print (len(list(G.edges)))


for  edge  in list(G.edges):
    listToTxt(edge,'intersection_graph5000.txt')
#
# #读取生成图
# G=nx.Graph()
# Ginit=ContractDict('3regular_tree1000.txt',G)
# print (list(Ginit.edges))
#
#










