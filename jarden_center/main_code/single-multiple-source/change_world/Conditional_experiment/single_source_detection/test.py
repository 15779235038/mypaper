import networkx as nx
G = nx.DiGraph()
# print(list(nx.bfs_tree(G ,1).edges()))
# [(1, 0), (1, 2)]
# H = nx.Graph()
# nx.add_path(H, [0, 1, 2, 3, 4, 5, 6])
# nx.add_path(H, [2, 7, 8, 9, 10])
# print(sorted(list(nx.bfs_tree(H, source=3, depth_limit=3).edges())))
# # [(1, 0), (2, 1), (2, 7), (3, 2), (3, 4), (4, 5), (5, 6), (7, 8)]
#
#
#
#
#i
#
#
#
#
#
#
#
#
# print('isTree,', nx.is_tree(H))
# subinfectG = nx.bfs_tree(H, source=4)
# print('isTree,', nx.is_tree(subinfectG))
# print(sorted(list(nx.bfs_tree(H, source=3).edges())))
#


G.add_edges_from([(1, 2)], weight=3)
G.add_edges_from([(2, 1)], weight=6)
print(G[2][1]['weight'])
print(G[1][2]['weight'])