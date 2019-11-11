import copy
import  commons
import matplotlib.pyplot as plt
import  networkx as nx

class jordan:
    def jordan_centrality_up(self,up_messages, who_infected, parent_node, current_node):
        if current_node == parent_node:
            for child_node in who_infected[current_node]:
                up_messages = self.jordan_centrality_up(up_messages, who_infected, current_node, child_node)
        elif len(who_infected[current_node]) == 1:
            up_messages[parent_node][0] = max(up_messages[parent_node][0], (up_messages[current_node][0] + 1))
            if len(who_infected[parent_node]) >= 3:
                up_messages[parent_node][1] = up_messages[current_node][1] + 1
        # leave
        else:
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    up_messages = self.jordan_centrality_up(up_messages, who_infected, current_node, child_node)
                    # up_messages[parent_node][1]=up_messages[parent_node][1]*up_messages[child_node][1]
            up_messages[parent_node][0] = max(up_messages[parent_node][0], (up_messages[current_node][0] + 1))
            if len(who_infected[parent_node]) >= 3:
                up_messages[parent_node][1] = up_messages[current_node][0] + 1
            # up_messages[parent_node][1]=up_messages[parent_node][0]*up_messages[parent_node][1]
        return up_messages


    def jordan_centrality_down(self,down_messages, who_infected, parent_node, current_node, centre):
        if current_node == parent_node:
            if (down_messages[parent_node][0] - down_messages[parent_node][1]) > 1:
                for child_node in who_infected[current_node]:
                    down_messages[child_node][1] = max(down_messages[child_node][1], down_messages[current_node][1] + 1)
                    down_messages, centre = self.jordan_centrality_down(down_messages, who_infected, current_node, child_node,
                                                                   centre)
            else:
                c = copy.deepcopy(current_node)
                centre = c
                return down_messages, centre
        else:
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    if (down_messages[current_node][0] - down_messages[current_node][1]) > 1:
                        down_messages[child_node][1] = max(down_messages[child_node][1], down_messages[current_node][1] + 1)
                        down_messages, centre = self.jordan_centrality_down(down_messages, who_infected, current_node,
                                                                       child_node, centre)
                    else:
                        c = copy.deepcopy(current_node)
                        centre = c
                        return down_messages, centre
        return down_messages, centre


    def jordan_centrality(self,who_infected):
        root_node = 3
        up_messages = []
        for i in range(len(who_infected)):
            up_messages.append([0, 0])
        jordan_center = -1
        print('who_infected',who_infected)
        up_message = self.jordan_centrality_up(up_messages, who_infected, root_node, root_node)
        print('up_message',up_messages)

        down_message, jordan_center = self.jordan_centrality_down(up_message, who_infected, root_node, root_node, root_node)
        print('down_message', down_message)
        return jordan_center


    def jorden_centrality_upmessage(self,root_node_temp,who_infected):
        root_node = root_node_temp
        up_messages = []
        for i in range(len(who_infected)):
            up_messages.append([0, 0])
        jordan_center = -1
        print('who_infected', who_infected)
        up_message = self.jordan_centrality_up(up_messages, who_infected, root_node, root_node)
        print('up_message', up_messages)

        down_message, jordan_center = self.jordan_centrality_down(up_message, who_infected, root_node, root_node,
                                                                  root_node)
        # print('down_message', down_message)
        # return jordan_center

        print('jordan_center,',jordan_center)

        return down_message




if __name__ == '__main__':
    # creating a toy graph (tree)
    adjacency = [[] for i in range(7)]
    adjacency[0] = [1, 2]
    adjacency[1] = [0, 3, 4]
    adjacency[2] = [0, 5]
    adjacency[3] = [1]
    adjacency[4] = [1]
    adjacency[5] = [2, 6]
    # adjacency[6] = [2]
    adjacency[6] = [5]
    # print(__name__)
    #这肯定是一个树，不然处理不了。构建成一颗树，然后处理吧。然后画图，然后再理解思路。


    rumor_center_object = jordan()
    rumor_center = rumor_center_object.jordan_centrality(adjacency)
    print('rumor_center',rumor_center)
    G = nx.Graph()
    for index in range(len(adjacency)):
        for j in adjacency[index]:
            G.add_edge(index, j)
    print('number_of_G', G.number_of_nodes())

    tree=nx.bfs_tree(G,source=0)
    print(list(nx.all_neighbors(tree, 2)))
    print('00000000000000')

    nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=20, node_color='red')
    plt.savefig('test.png')
    plt.show()
    plt.close()