import   networkx as nx
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



# G=nx.random_tree(3000)
#生成1000个节点树图
G=nx.full_rary_tree(3,100)
# G= nx.balanced_tree(2,13)

print (len(list(G.nodes)))
print (len(list(G.edges)))


for  edge  in list(G.edges):
    listToTxt(edge,'2regular_tree.txt')
#
# #读取生成图
# G=nx.Graph()
# Ginit=ContractDict('3regular_tree1000.txt',G)
# print (list(Ginit.edges))
#
#










