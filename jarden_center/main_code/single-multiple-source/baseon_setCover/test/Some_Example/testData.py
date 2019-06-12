import  networkx as nx
def read_gml(data):
    H = nx.read_gml(data,label ='id')
    print (len(H.edges()))



print('---------------gml------------------')

read_gml('../../../data/powergrid/power.gml')

