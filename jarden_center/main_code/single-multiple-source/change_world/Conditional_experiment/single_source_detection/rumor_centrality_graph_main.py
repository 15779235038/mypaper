import math
import sys
sys.setrecursionlimit(100000)  # 例如这里设置为十万
from  collections import  defaultdict

import  networkx as nx
import matplotlib.pyplot as plt
class rumor_center:
    def __init__(self):
        print('谣言中心构建开始...')

    def rumor_centrality_up(self, up_messages, who_infected, parent_node, current_node,infectG,upmessage_dict):
        # message_passing_up(up_messages, adjacency, root_node, root_node)
        print('往上传播')
        print('up_message',up_messages )
        print('up_message_dict',upmessage_dict)
        print('who_infected',who_infected)
        print('parent_node',parent_node)
        print('current_node',current_node)
        # print()
        if current_node == parent_node:
            print('current_node',current_node)
            neighbour_list = list(nx.neighbors(infectG,current_node))  #取curren的邻居节点。
            print('neighobr',neighbour_list)
            for child_node in neighbour_list:
                # print('如果当前节点是源点，往下找孩子节点发消息')
                up_messages,upmessage_dict = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node,infectG,upmessage_dict)

                print('往上发的消息up_message', up_messages)
        # elif len(who_infected[current_node]) == 1:
        elif infectG.degree[current_node] ==1:
            print('这个点只跟某一个点相连的话，就是叶子节点。',current_node)
            up_messages[parent_node][0] += 1
            upmessage_dict[parent_node][0] += 1


            print('up_message改变',[parent_node][0])
            print('up_meesge——dict改变', upmessage_dict[parent_node][0])
            up_messages[parent_node][1] = up_messages[parent_node][1] * up_messages[current_node][1]
            upmessage_dict[parent_node][1] = upmessage_dict[parent_node][1] * upmessage_dict[current_node][1]

            print('up_message改变', up_messages)
        # leave
        else:
            print('对于其实都是递归往上走的')
            neighbour_list = list(nx.neighbors(infectG, current_node))  # 取curren的邻居节点。
            # for child_node in who_infected[current_node]:
            for child_node in neighbour_list:
                if child_node != parent_node:
                    up_messages,upmessage_dict = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node,infectG,upmessage_dict)
                    up_messages[current_node][1] = up_messages[current_node][1] * up_messages[child_node][1]
                    upmessage_dict[current_node][1] = upmessage_dict[current_node][1] * upmessage_dict[child_node][1]


            up_messages[parent_node][0] += up_messages[current_node][0]
            upmessage_dict[parent_node][0] += upmessage_dict[current_node][0]
            print('往上传的消息改变。就是父节点', up_messages)
            up_messages[current_node][1] = up_messages[current_node][0] * up_messages[current_node][1]
            upmessage_dict[current_node][1] = upmessage_dict[current_node][0] * upmessage_dict[current_node][1]
            print('往上传的消息改变当前节点收到孩子', up_messages)
        return up_messages,upmessage_dict





    def rumor_centrality_down(self, down_messages, up_messages, who_infected, parent_node, current_node,infectG,down_messages_dict):
        # print()
        # print('往下传播')
        # print('down_messages', down_messages)
        # print('up_messages', up_messages)
        # print('who_infected', who_infected)
        # print('parent_node', parent_node)
        # print('current_node', current_node)
        # print()
        node_sum = infectG.number_of_nodes()
        if current_node == parent_node:
            down_messages[current_node] = math.log(math.factorial(node_sum)) - math.log((node_sum))
            # print('down_message改变',down_messages)
            down_messages_dict[current_node] = math.log(math.factorial(node_sum)) - math.log((node_sum))
            neighbour_list = list(nx.neighbors(infectG, current_node))  # 取curren的邻居节点。
            for child_node in neighbour_list:
                down_messages[current_node] = down_messages[current_node] - math.log((up_messages[child_node][1]))
                down_messages_dict[current_node] = down_messages_dict[current_node] - math.log((up_messages[child_node][1]))

            # print('down_message改变,这一步减去了每个孩子的分量', down_messages)
            for child_node in neighbour_list:
                down_messages,down_messages_dict = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                           child_node,infectG,down_messages_dict)
            # print('down_message改变', down_messages)
        else:
            neighbour_list = list(nx.neighbors(infectG, current_node))  # 取curren的邻居节点。
            down_messages[current_node] = (down_messages[parent_node] + math.log(up_messages[current_node][0])) - (
                math.log((len(who_infected) - up_messages[current_node][0])))

            down_messages_dict[current_node] = (down_messages_dict[parent_node] + math.log(up_messages[current_node][0])) - (
                math.log((len(who_infected) - up_messages[current_node][0])))
            # print('非根节点的改变', down_messages)
            for child_node in neighbour_list:
                if child_node != parent_node:
                    down_messages,down_messages_dict = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                               child_node,infectG,down_messages_dict)

            # print('down_message改变,这一步减去了每个孩子的分量', down_messages)
        return down_messages,down_messages_dict

    def rumor_centrality(self, who_infected,infectG):

        # print('who_infected',who_infected)
        root_node = 3
        rumor_center = -1
        up_messages = []
        for i in range(len(who_infected)):
            up_messages.append([1, 1])


        #up_message改成键值对形式，键为图id，值为list，第一项是它作为子树的节点个数，第二项是子树上所有节点的子树个数的乘积。
        # down_message改成键值对形式，键为图id，值就是简单的值。
        upmessage_dict = defaultdict(list)
        down_messages_dict =defaultdict(int)
        for node_index in list(infectG.nodes()):
            upmessage_dict[node_index] = [1,1]
            down_messages_dict[node_index] =1
        print('upmessge_dict',upmessage_dict)
        down_messages = [1] * len(who_infected)
        # print('down_messages', down_messages)

        up_message,upmessage_dict_temp = self.rumor_centrality_up(up_messages, who_infected, root_node, root_node,infectG,upmessage_dict)
        print('up_message',up_message)
        print('up_message_temp',upmessage_dict_temp)
        #up_message的第一项是它作为子树的节点个数，第二项是子树上所有节点的子树个数的乘积。
        '''
        注意这里的upmessage——dict——temp参数已经变了。
        '''
        down_message,down_messages_dict_temp = self.rumor_centrality_down(down_messages, upmessage_dict_temp, who_infected, root_node, root_node,infectG,down_messages_dict)
        print('down_message',down_messages)
        print('down_message_dict_temp',down_messages_dict_temp)
        #down_messag是下发给孩子节点的所有孩子。
        center = max(down_message)
        for i in range(len(down_messages)):
            if down_messages[i] == center:
                rumor_center = i
        return rumor_center, center





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
    G = nx.Graph()
    for index in range(len(adjacency)):
        for j in adjacency[index]:
            G.add_edge(index, j)
    print('number_of_G', G.number_of_nodes())
    print('number_edge——',G.number_of_edges())
    rumor_center_object = rumor_center()
    rumor_center, center = rumor_center_object.rumor_centrality(adjacency,G)
    print(rumor_center, center )

    nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=20, node_color='red')
    plt.show()

    plt.close()
