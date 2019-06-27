
import   networkx as  nx
G = nx.path_graph(3)
list(nx.bfs_edges(G, 0))

print (list(nx.bfs_edges(G, source=0, depth_limit=1)))