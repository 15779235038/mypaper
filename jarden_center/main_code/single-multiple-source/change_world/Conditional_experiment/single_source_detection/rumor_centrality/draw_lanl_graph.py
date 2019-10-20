import matplotlib.pyplot as plt
import networkx as nx
try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or pydot")
class draw_lanl_graph:
    def lanl_graph(file_path):
        """ Return the lanl internet view graph from lanl.edges
        """
        try:
            fh = open(file_path, 'r')
        except IOError:
            print("lanl.edges not found")
            raise

        G = nx.Graph()

        time = {}
        time[0] = 0  # assign 0 to center node
        for line in fh.readlines():
            (head, tail, rtt) = line.split()
            G.add_edge(int(head), int(tail))
            time[int(head)] = float(rtt)

        # get largest component and assign ping times to G0time dictionary
        G0 = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
        G0.rtt = {}
        for n in G0:
            G0.rtt[n] = time[n]
        return G0

    def draw_lanl_graph(G):
        print("graph has %d nodes with %d edges"
              % (nx.number_of_nodes(G), nx.number_of_edges(G)))
        print(nx.number_connected_components(G), "connected components")

        plt.figure(figsize=(8, 8))
        # use graphviz to find radial layout
        pos = graphviz_layout(G, prog="twopi", root=0)
        # draw nodes, coloring by rtt ping time
        nx.draw(G, pos,
                node_color=[G.rtt[v] for v in G],
                with_labels=False,
                alpha=0.5,
                node_size=15)
        # adjust the plot limits
        xmax = 1.02 * max(xx for xx, yy in pos.values())
        ymax = 1.02 * max(yy for xx, yy in pos.values())
        plt.xlim(0, xmax)
        plt.ylim(0, ymax)
        plt.show()
        return G


# if __name__ == '__main__':
#
#     G = draw_lanl_graph.lanl_graph(file_path='lanl_routes.txt')

