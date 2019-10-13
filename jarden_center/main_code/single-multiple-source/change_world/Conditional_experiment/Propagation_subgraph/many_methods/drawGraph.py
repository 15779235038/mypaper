import networkx as nx             #导入networkx包
import matplotlib.pyplot as plt

G = nx.Graph()

# result=[]
# with open('node_list.txt','r') as f:
#     for line in f:
#         l = line.replace('[','').replace(']','').replace(',','')
#         ll = l.split()
#         #print(ll)
#         n = []
#         for i in ll:
#             j = int(i)
#             n.append(j)
#         for m in n:
#             s = str(m)
#             G.add_node(s)


result=[]
with open('edge_list.txt','r') as f:
    for line in f:
        l = line.replace('[','').replace(']','').replace(',','').replace('(','').replace(')','')

        ll = l.split()
        n = []
        for i in ll:
            j = int(i)
            n.append(j)
        #print(n)
        for i in range(0,len(n),2):
            s1 = n[i]
            s2 = n[i+1]
            G.add_edge(s1, s2)
nx.draw(G,node_size=2, edge_color = 'r')
plt.show()

