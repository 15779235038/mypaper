import  networkx as nx
from networkx.algorithms.community import k_clique_communities
G = nx.complete_graph(5)
K5 = nx.convert_node_labels_to_integers(G,first_label=2)
G.add_edges_from(K5.edges())

print (G.nodes)
print (G.edges)
c = list(k_clique_communities(G, 5))
print (list(c[0]))

print (list(k_clique_communities(G, 6)))