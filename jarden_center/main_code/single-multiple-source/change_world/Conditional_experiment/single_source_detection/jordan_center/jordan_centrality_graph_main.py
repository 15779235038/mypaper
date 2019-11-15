import copy
import commons
import matplotlib.pyplot as plt
import networkx as nx
import random
import commons
from collections import defaultdict

import  plot_main
class jordan:
    def jordan_centrality_up(self, parent_node, current_node, infectG, upmessage_dict):


        # print('父亲节点',parent_node)
        # print('当前节点',current_node)
        if current_node == parent_node:
            nehibour_list = list(nx.neighbors(infectG, current_node))
            # print('从谁的孩子一直遍历所有子节点，类似DFS',current_node)
            # print('neighbour', nehibour_list)
            for child_node in nehibour_list:
                upmessage_dict = self.jordan_centrality_up(current_node, child_node, infectG, upmessage_dict)

        elif infectG.degree[current_node] == 1:
            # print('当前节点只跟一个点相连，自然就是边界点。',current_node)
            # up_messages[parent_node][0] = max(up_messages[parent_node][0], (up_messages[current_node][0] + 1))
            upmessage_dict[parent_node][0] = max(upmessage_dict[parent_node][0], (upmessage_dict[current_node][0] + 1))

            # print('更新它的父亲节点，',up_messages[parent_node])

            if infectG.degree[parent_node] >= 3:
                upmessage_dict[parent_node][1] = upmessage_dict[current_node][1] + 1
                # print('只有1的节点度为3，然后就要加1？')
        # leave
        else:
            nehibour_list = list(nx.neighbors(infectG, current_node))
            for child_node in nehibour_list:
                if child_node != parent_node:
                    # up_messages = self.jordan_centrality_up( current_node, child_node,infectG,upmessage_dict)
                    upmessage_dict = self.jordan_centrality_up(current_node, child_node, infectG, upmessage_dict)

                    # up_messages[parent_node][1]=up_messages[parent_node][1]*up_messages[child_node][1]
            # up_messages[parent_node][0] = max(up_messages[parent_node][0], (up_messages[current_node][0] + 1))
            upmessage_dict[parent_node][0] = max(upmessage_dict[parent_node][0], (upmessage_dict[current_node][0] + 1))

            if infectG.degree[parent_node] >= 3:
                upmessage_dict[parent_node][1] = upmessage_dict[current_node][0] + 1
            # up_messages[parent_node][1]=up_messages[parent_node][0]*up_messages[parent_node][1]
        return upmessage_dict






    def jordan_centrality_down_first(self,down_messages, who_infected, parent_node, current_node, centre):
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



    def jordan_centrality_down(self,  parent_node, current_node, centre,infectG,downmessage_dict):
        print('parent_node父亲节点', parent_node)
        print('current_node 当前节点', current_node)
        print('center', centre)

        if current_node == parent_node:

            if (downmessage_dict[parent_node][0] - downmessage_dict[parent_node][1]) > 1:
                nehibour_list = list(nx.neighbors(infectG, current_node))
                for child_node in nehibour_list:
                    downmessage_dict[child_node][1] = max(downmessage_dict[child_node][1], downmessage_dict[current_node][1] + 1)
                    downmessage_dict, centre = self.jordan_centrality_down(current_node,
                                                                        child_node,
                                                                        centre,infectG,downmessage_dict)
            else:
                c = copy.deepcopy(current_node)
                centre = c
                return downmessage_dict, centre
        else:
            nehibour_list = list(nx.neighbors(infectG, current_node))
            for child_node in nehibour_list:
                if child_node != parent_node:
                    if (downmessage_dict[current_node][0] - downmessage_dict[current_node][1]) > 1:
                        downmessage_dict[child_node][1] = max(downmessage_dict[child_node][1],
                                                           downmessage_dict[current_node][1] + 1)
                        print('更新后的孩子节点', child_node)
                        print('更新后的孩子节点', downmessage_dict[child_node][1])
                        print('down_message', downmessage_dict)
                        downmessage_dict, centre = self.jordan_centrality_down( current_node,
                                                                            child_node, centre,infectG,downmessage_dict)
                    else:
                        c = copy.deepcopy(current_node)
                        centre = c
                        return downmessage_dict, centre
        return downmessage_dict, centre




    def jordan_centrality(self, infectG):

        random_root_node = random.choice(list(infectG.nodes()))
        root_node = random_root_node
        print('root_node', root_node)

        print('随便选了一个节点就是为源点',root_node)
        # up_message改成键值对形式，键为图id，值为list，第一项是它作为子树的节点个数，第二项是子树上所有节点的子树个数的乘积。
        # down_message改成键值对形式，键为图id，值就是简单的值。
        upmessage_dict = defaultdict(list)
        for node_index in list(infectG.nodes()):
            upmessage_dict[node_index] = [0,0]

        # print('upmessge_dict', upmessage_dict)

        upmessage_dict_temps = self.jordan_centrality_up(root_node, root_node, infectG, upmessage_dict)

        print('up_message_temp', upmessage_dict_temps)

        # print('upmessage_dict_temp', upmessage_dict_temps[root_node])

        # up_message的第一项是它作为子树的节点个数，第二项是子树上所有节点的子树个数的乘积。
        '''
        注意这里的upmessage——dict——temp参数已经变了。
        '''
        down_messages_dict_temp,jordan_center = self.jordan_centrality_down(root_node, root_node,
                                                                  root_node,infectG,upmessage_dict_temps)
        print('down_message_dict_temp',down_messages_dict_temp)
        print('down_message_dict_temp',down_messages_dict_temp[jordan_center])
        print(upmessage_dict_temps[jordan_center])
        return jordan_center



if __name__ == '__main__':
    # #拿到图
    initG = commons.get_networkByFile('../../../data/3regular_tree9.txt')
    max_sub_graph = commons.judge_data(initG)
    # source_list = product_sourceList(max_sub_graph, 2)
    source_list = commons.product_sourceList(max_sub_graph, 1)
    # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
    infectG, T = commons.propagation1(max_sub_graph,source_list)
    # infectG1, T = commons.propagation1(max_sub_graph, [source_list])
    subInfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。

    # result_node = rumor_center(infectG, subinfectG, source_list[0])

    # 将图构造成两个list，一个是感染点list，一个是感染和它的邻居点构造成的list
    # infect_node = []
    # infect_neighbour_list = []
    # print(infectG.number_of_nodes())
    # random_node = random.choice(list(subInfectG.nodes()))
    # subinfectG_temp = nx.bfs_tree(subInfectG, source=source_list[0])
    # subinfectG = subinfectG_temp.to_undirected()

    jordan_center_object = jordan()
    center = jordan_center_object.jordan_centrality(subInfectG)

    print('center', center)
    print('真实源是', source_list[0])
    # print('预测源是', result_node[0])
    distance = nx.shortest_path_length(infectG, source=source_list[0], target=center)
    print('结果他们的距离是', distance)

    plot_main.plot_G_node_color_simple(initG,[center])
    # nx.draw(initG,pos=nx.spring_layout(initG))
    # plt.show()



