from pyclbr import Class

import networkx as nx  # 导入networkx包
import matplotlib.pyplot as plt
from read_net import readNet

class draw_general_graph:
    def general_graph(file_path):
        try:
            fh = open(file_path, 'r')
        except IOError:
            print("lanl.edges not found")
            raise

        G = nx.Graph()

        for line in fh.readlines():
            (head, tail) = line.split()
            G.add_edge(int(head), int(tail))
        return G
    def draw_general_graph(G):

        nx.draw(G,
                with_labels=True,
                alpha=0.5,
                node_size=15)
        plt.show()


