
import  networkx as nx
G = nx.path_graph(3)
print(dict(nx.bfs_successors(G,0)))

H = nx.Graph()
H.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
print(dict(nx.bfs_successors(H, 0)))

# G = nx.Graph()
# nx.add_path(G, [0, 1, 2, 3, 4, 5, 6])
# nx.add_path(G, [2, 7, 8, 9, 10])
# print(dict(nx.bfs_successors(G, source=1, depth_limit=3)))