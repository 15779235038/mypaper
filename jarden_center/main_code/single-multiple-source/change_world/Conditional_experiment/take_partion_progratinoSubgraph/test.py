
import  networkx as nx


# G = nx.Graph()
# nx.add_path(G, [0, 1, 2])
# nx.add_path(G, [0, 10, 2])
# print([p for p in nx.all_shortest_paths(G, source=0, target=2)])


# a = [1,2,3,4]
# b = set([1,7])
# print(b.issubset(a))
#
G = nx.path_graph(4)  # or DiGraph, etc
G.remove_edge(1, 2)
G.remove_edge(1, 0)
print(G.number_of_nodes())