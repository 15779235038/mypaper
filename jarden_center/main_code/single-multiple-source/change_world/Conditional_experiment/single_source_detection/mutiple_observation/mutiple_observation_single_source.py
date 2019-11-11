import math
import sys
sys.setrecursionlimit(100000)  # 例如这里设置为十万
import  commons
import matplotlib.pyplot as plt
import  networkx as nx

class rumor_center:
    def __init__(self):
        print('谣言中心构建开始...')

    def rumor_centrality_up(self, up_messages, who_infected, parent_node, current_node,inter_set,union_set):
        # message_passing_up(up_messages, adjacency, root_node, root_node)
        print('往上传播')
        print('up_message',up_messages )
        print('who_infected',who_infected)
        print('parent_node',parent_node)
        print('current_node',current_node)
        print()
        if current_node == parent_node:
            for child_node in who_infected[1][current_node]:   #只走共同的点
                print('如果当前节点是源点，往下找孩子节点发消息')
                up_messages = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node,inter_set,union_set)
                print('往上发的消息up_message', up_messages)
        elif len(who_infected[1][current_node]) == 1:
            print('这个点只跟某一个点相连的话，就是叶子节点。',current_node)

            up_messages[parent_node][0][0] += 1
            print('up_message改变',up_messages)
            up_messages[parent_node][1][0] = up_messages[parent_node][1][0] * up_messages[current_node][1][0]
            print('up_message改变', up_messages)
        # leave
        else:
            print('对于其实都是递归往上走的')
            for child_node in who_infected[1][current_node]:
                if child_node != parent_node:
                    up_messages = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node,inter_set,union_set)
                    up_messages[current_node][2][0] = up_messages[current_node][2][0] * up_messages[child_node][2][0]

            up_messages[parent_node][0][0] += up_messages[current_node][0][0]
            print('往上传的消息改变。就是父节点', up_messages)
            up_messages[current_node][1] = up_messages[current_node][0][0] * up_messages[current_node][2][0]
            print('往上传的消息改变当前节点收到孩子', up_messages)
        return up_messages





    def rumor_centrality_down(self, down_messages, up_messages, who_infected, parent_node, current_node):
        print()
        print('往下传播')
        print('down_messages', down_messages)
        print('up_messages', up_messages)
        print('who_infected', who_infected)
        print('parent_node', parent_node)
        print('current_node', current_node)
        print()
        if current_node == parent_node:
            down_messages[current_node] = math.log(math.factorial(len(who_infected))) - math.log((len(who_infected)))
            print('down_message改变',down_messages)

            for child_node in who_infected[current_node]:
                down_messages[current_node] = down_messages[current_node] - math.log((up_messages[child_node][1]))
            print('down_message改变,这一步减去了每个孩子的分量', down_messages)
            for child_node in who_infected[current_node]:
                down_messages = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                           child_node)
            print('down_message改变', down_messages)
        else:
            down_messages[current_node] = (down_messages[parent_node] + math.log(up_messages[current_node][0])) - (
                math.log((len(who_infected) - up_messages[current_node][0])))
            print('非根节点的改变', down_messages)
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    down_messages = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                               child_node)

            print('down_message改变,这一步减去了每个孩子的分量', down_messages)
        return down_messages

    def rumor_centrality(self, who_infected):
        print('who_infected',who_infected)
        root_node = 2
        rumor_center = -1
        up_messages = []
        A_set = [x for x in range(len(who_infected[0]))]
        B_set = [x for x in range(len(who_infected[1]))]
        print(A_set)
        print(B_set)
        max_len=max(len(A_set),len(B_set))
        print('max_len',max_len)

        intertion_set = set(A_set) & set(B_set)
        print('intertion_set',intertion_set)
        union_set = set(A_set) |  set(B_set)
        print('union_set',union_set)

        for i in range(max_len):
            up_messages.append([[1, 1], [1, 0], [1]])

        down_messages = [1] * max_len
        print('down_messages', down_messages)
        up_message = self.rumor_centrality_up(up_messages, who_infected, root_node, root_node,intertion_set,union_set)
        down_message = self.rumor_centrality_down(down_messages, up_message, who_infected, root_node, root_node)
        center = max(down_message)
        for i in range(len(down_messages)):
            if down_messages[i] == center:
                rumor_center = i
        return rumor_center, center





if __name__ == '__main__':
    # creating a toy graph (tree)
    adjacency1 = [[] for i in range(7)]
    adjacency1[0] = [1, 2]
    adjacency1[1] = [0, 3, 4]
    adjacency1[2] = [0, 5]
    adjacency1[3] = [1]
    adjacency1[4] = [1]
    adjacency1[5] = [2, 6]
    # adjacency[6] = [2,5]
    adjacency1[6] = [5]

    #多一个传播图，




    adjacency2 = [[] for i in range(8)]
    adjacency2[0] = [1, 2]
    adjacency2[1] = [0, 3, 4]
    adjacency2[2] = [0, 5]
    adjacency2[3] = [1]
    adjacency2[4] = [1]
    adjacency2[5] = [2, 6]
    # adjacency[6] = [2,5]
    adjacency2[6] = [5,7]
    adjacency2[7] = [6]

    # print(__name__)
    #这肯定是一个树，不然处理不了。构建成一颗树，然后处理吧。然后画图，然后再理解思路。
    G = nx.Graph()
    for index in range(len(adjacency2)):
        for j  in adjacency2[index]:
            G.add_edge(index, j)
    print('number_of_G', G.number_of_nodes())
    nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=20, node_color='red')
    plt.savefig('test.png')
    # plt.show()
    plt.close()


    adjacency_list = []

    adjacency_list.append(adjacency1)
    adjacency_list.append(adjacency2)
    rumor_center_object = rumor_center()
    rumor_center, center = rumor_center_object.rumor_centrality(adjacency_list)
    print(rumor_center, center )