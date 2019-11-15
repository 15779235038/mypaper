import copy
import  commons
import matplotlib.pyplot as plt
import  networkx as nx

class jordan:
    def jordan_centrality_up(self,up_messages, who_infected, parent_node, current_node):
        print('父亲节点', parent_node)
        print('当前节点', current_node)
        print('upmessage改变',up_messages)
        if current_node == parent_node:
            for child_node in who_infected[current_node]:
                up_messages = self.jordan_centrality_up(up_messages, who_infected, current_node, child_node)
                print('从当前节点=父节点的返回up——message',up_messages)
        elif len(who_infected[current_node]) == 1:
            print('当前节点只跟一个点相连，自然就是边界点。',current_node)
            up_messages[parent_node][0] = max(up_messages[parent_node][0], (up_messages[current_node][0] + 1))
            print('更新它的父亲节点id，', parent_node)
            print('更新它的父亲节点，',up_messages[parent_node])
            if len(who_infected[parent_node]) >= 3:
                print('只有parent_node的节点度为3，然后就要加？',parent_node)
                up_messages[parent_node][1] = up_messages[current_node][1] + 1
                print('父亲的度》3，表示父亲的第二项需要加,又变成了',up_messages[parent_node][1])

        # leave
        else:
            print('从当前节点往孩子遍历')
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    up_messages = self.jordan_centrality_up(up_messages, who_infected, current_node, child_node)
                    print('从当前节点往孩子遍历得到的up_messages', up_messages)
                    # up_messages[parent_node][1]=up_messages[parent_node][1]*up_messages[child_node][1]
            up_messages[parent_node][0] = max(up_messages[parent_node][0], (up_messages[current_node][0] + 1))
            if len(who_infected[parent_node]) >= 3:
                print('度大于3表示的是有多个从root的分支，我们的upmessage第一项需要取最大的那个长度，而第二项作用？')
                print('parent_node的度大于3',parent_node)
                up_messages[parent_node][1] = up_messages[current_node][0] + 1
                print('父亲的度》3，表示父亲的第二项需要加,变成了', up_messages[parent_node][1])
            # up_messages[parent_node][1]=up_messages[parent_node][0]*up_messages[parent_node][1]
        print('只有走到底才会回溯',)
        print('父亲节点', parent_node)
        print('当前节点', current_node)
        print('每次返回的upmessage',up_messages)
        return up_messages


    def jordan_centrality_down(self,down_messages, who_infected, parent_node, current_node, centre):

        print('parent_node父亲节点',parent_node)
        print('current_node 当前节点',current_node)
        print('center',centre)

        if current_node == parent_node:
            print('当前节点=父亲节点')
            if (down_messages[parent_node][0] - down_messages[parent_node][1]) > 1:
                print('当前节点的upmessage两个值之差大于1')
                for child_node in who_infected[current_node]:
                    print('那么针对当前节点的孩子来说，都要进行更新，更新什么呢？'
                          '孩子节点的第二项，要变成孩子节点第二项或者父亲节点的第二项+1的较大者')
                    down_messages[child_node][1] = max(down_messages[child_node][1], down_messages[current_node][1] + 1)

                    print ('更新后的孩子节点',child_node)

                    print('更新后的孩子节点', down_messages[child_node][1])
                    print('down_message',down_messages)
                    down_messages, centre = self.jordan_centrality_down(down_messages, who_infected, current_node, child_node,
                                                                   centre)
            else:
                print('差距小于1')
                c = copy.deepcopy(current_node)
                centre = c
                return down_messages, centre
        else:
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    if (down_messages[current_node][0] - down_messages[current_node][1]) > 1:
                        print('如果当前节点的第一项，跟第二项之差大于1，那么当前节点的孩子第二项就需要更新为自己的第二项和父亲节点第二项+1')
                        down_messages[child_node][1] = max(down_messages[child_node][1], down_messages[current_node][1] + 1)

                        print('更新后的孩子节点', child_node)
                        print('更新后的孩子节点', down_messages[child_node][1])
                        print('down_message', down_messages)
                        down_messages, centre = self.jordan_centrality_down(down_messages, who_infected, current_node,
                                                                       child_node, centre)
                    else:
                        print('current_node',current_node)
                        print('如果差距小于等于1')
                        c = copy.deepcopy(current_node)
                        centre = c
                        return down_messages, centre
        return down_messages, centre


    def jordan_centrality(self,who_infected):
        root_node = 5
        up_messages = []
        for i in range(len(who_infected)):
            up_messages.append([0, 0])
        jordan_center = -1
        print('who_infected',who_infected)
        up_message = self.jordan_centrality_up(up_messages, who_infected, root_node, root_node)
        print('返回的最终的up_message',up_messages)
        print('现在需要自顶向下更新所有孩子了。')
        print()
        print()
        down_message, jordan_center = self.jordan_centrality_down(up_message, who_infected, root_node, root_node, root_node)
        print('down_message', down_message)
        print('down_message',down_message[jordan_center])
        return jordan_center





import  plot_main
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

    initG = commons.get_networkByFile('../../../data/2regular_tree9.txt')
    adjacency_temp  = [[] for i in range(initG.number_of_nodes())]
    print('number_ofnodes',initG.number_of_nodes())
    for node_index in list(initG.nodes()):
        neighbor = list(nx.neighbors(initG,node_index))
        adjacency_temp[node_index]= neighbor



    rumor_center_object = jordan()
    rumor_center = rumor_center_object.jordan_centrality(adjacency_temp)
    print('rumor_center',rumor_center)
    G = nx.Graph()
    for index in range(len(adjacency)):
        for j in adjacency[index]:
            G.add_edge(index, j)
    print('number_of_G', G.number_of_nodes())

    # tree=nx.bfs_tree(G,source=0)
    # print(list(nx.all_neighbors(tree, 2)))
    # print('rumor_center', rumor_center)
    # print('center', rumor_center)

    plot_main.plot_G_node_color_simple(initG,[rumor_center])

