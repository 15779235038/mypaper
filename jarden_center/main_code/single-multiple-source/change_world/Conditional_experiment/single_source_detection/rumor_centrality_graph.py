import math
import sys
sys.setrecursionlimit(100000)  # 例如这里设置为十万
import  commons
import matplotlib.pyplot as plt
import  networkx as nx

class rumor_center:
    def __init__(self):
        print('谣言中心构建开始...')

    def rumor_centrality_up(self, up_messages, who_infected, parent_node, current_node):
        # message_passing_up(up_messages, adjacency, root_node, root_node)
        # print('往上传播')
        # print('up_message',up_messages )
        # print('who_infected',who_infected)
        # print('parent_node',parent_node)
        # print('current_node',current_node)
        # print()
        if current_node == parent_node:
            for child_node in who_infected[current_node]:
                # print('如果当前节点是源点，往下找孩子节点发消息')
                up_messages = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node)
                # print('往上发的消息up_message', up_messages)
        elif len(who_infected[current_node]) == 1:
            # print('这个点只跟某一个点相连的话，就是叶子节点。',current_node)

            up_messages[parent_node][0] += 1
            # print('up_message改变',up_messages)
            up_messages[parent_node][1] = up_messages[parent_node][1] * up_messages[current_node][1]
            # print('up_message改变', up_messages)
        # leave
        else:
            # print('对于其实都是递归往上走的')
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    up_messages = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node)
                    up_messages[current_node][1] = up_messages[current_node][1] * up_messages[child_node][1]

            up_messages[parent_node][0] += up_messages[current_node][0]
            # print('往上传的消息改变。就是父节点', up_messages)
            up_messages[current_node][1] = up_messages[current_node][0] * up_messages[current_node][1]
            # print('往上传的消息改变当前节点收到孩子', up_messages)
        return up_messages





    def rumor_centrality_down(self, down_messages, up_messages, who_infected, parent_node, current_node):
        # print()
        # print('往下传播')
        # print('down_messages', down_messages)
        # print('up_messages', up_messages)
        # print('who_infected', who_infected)
        # print('parent_node', parent_node)
        # print('current_node', current_node)
        # print()
        if current_node == parent_node:
            down_messages[current_node] = math.log(math.factorial(len(who_infected))) - math.log((len(who_infected)))
            # print('down_message改变',down_messages)

            for child_node in who_infected[current_node]:
                down_messages[current_node] = down_messages[current_node] - math.log((up_messages[child_node][1]))
            # print('down_message改变,这一步减去了每个孩子的分量', down_messages)
            for child_node in who_infected[current_node]:
                down_messages = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                           child_node)
            # print('down_message改变', down_messages)
        else:
            down_messages[current_node] = (down_messages[parent_node] + math.log(up_messages[current_node][0])) - (
                math.log((len(who_infected) - up_messages[current_node][0])))
            # print('非根节点的改变', down_messages)
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    down_messages = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                               child_node)

            # print('down_message改变,这一步减去了每个孩子的分量', down_messages)
        return down_messages

    def rumor_centrality(self, who_infected):

        # print('who_infected',who_infected)
        root_node = 99
        rumor_center = -1
        up_messages = []
        for i in range(len(who_infected)):
            up_messages.append([1, 1])
        down_messages = [1] * len(who_infected)
        # print('down_messages', down_messages)
        up_message = self.rumor_centrality_up(up_messages, who_infected, root_node, root_node)
        print('up_message',up_messages)
        #up_message的第一项是它作为子树的节点个数，第二项是子树上所有节点的子树个数的乘积。
        down_message = self.rumor_centrality_down(down_messages, up_message, who_infected, root_node, root_node)
        print('down_message',down_messages)
        #down_messag是下发给孩子节点的所有孩子。
        center = max(down_message)
        for i in range(len(down_messages)):
            if down_messages[i] == center:
                rumor_center = i
        return rumor_center, center



import  random

if __name__ == '__main__':
    # #拿到图
    initG = commons.get_networkByFile('../../../data/3regular_tree9.txt')
    max_sub_graph = commons.judge_data(initG)
    # source_list = product_sourceList(max_sub_graph, 2)
    source_list = commons.product_sourceList(max_sub_graph, 1)
    # print('两个节点的距离', nx.shortest_path_length(max_sub_graph, source=source_list[0], target=source_list[1]))
    infectG, T = commons.propagation1(max_sub_graph, source_list)
    # infectG1, T = commons.propagation1(max_sub_graph, [source_list])
    subInfectG = commons.get_subGraph_true(infectG)  # 只取感染点，为2表示,真实的感染图。


    # result_node = rumor_center(infectG, subinfectG, source_list[0])



    # 将图构造成两个list，一个是感染点list，一个是感染和它的邻居点构造成的list
    infect_node = []
    infect_neighbour_list = []
    print(infectG.number_of_nodes())
    random_node = random.choice(list(subInfectG.nodes()))
    subinfectG_temp = nx.bfs_tree(subInfectG, source=source_list[0])

    subinfectG = subinfectG_temp.to_undirected()
    # who_infected =  [[] for i in range(infectG.number_of_nodes())]
    # 找出最大的id数目。
    maxs = 0
    for node_index in list(infectG.nodes):
        if node_index > maxs:
            maxs = node_index
    print('maxs', maxs)
    for node in list(subinfectG.nodes()):
        infect_node.append(node)
    who_infected = [[] for i in range(maxs + 1)]

    i = 0
    for node_temp in infect_node:
        neighbour_list = list(nx.all_neighbors(subinfectG, node_temp))
        neighbour_list_index = []
        for neighbour in neighbour_list:
            neighbour_list_index.append(infect_node.index(neighbour))
        who_infected[i] = neighbour_list_index
        i += 1

    print('infect_node', infect_node)
    print('who_infected', who_infected)
    rumor_center_object = rumor_center()

    rumor_center, center = rumor_center_object.rumor_centrality(who_infected)

    print('rumor_center', rumor_center)
    print('center', center)
    print('[infect_node[rumor_center]]', [infect_node[rumor_center]])

    print('真实源是', source_list[0])
    # print('预测源是', result_node[0])
    distance = nx.shortest_path_length(subinfectG, source=source_list[0], target=[infect_node[rumor_center]][0])
    print('结果他们的距离是', distance)



