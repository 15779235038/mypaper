import math
import sys
sys.setrecursionlimit(100000)  # 例如这里设置为十万

import  networkx as nx

class rumor_center:
    def __init__(self):
        print('谣言中心构建开始...')

    def rumor_centrality_up(self, up_messages, who_infected, parent_node, current_node):
        # message_passing_up(up_messages, adjacency, root_node, root_node)
        if current_node == parent_node:
            for child_node in who_infected[current_node]:
                up_messages = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node)
        elif len(who_infected[current_node]) == 1:
            up_messages[parent_node][0] += 1
            up_messages[parent_node][1] = up_messages[parent_node][1] * up_messages[current_node][1]
        # leave
        else:
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    up_messages = self.rumor_centrality_up(up_messages, who_infected, current_node, child_node)
                    up_messages[current_node][1] = up_messages[current_node][1] * up_messages[child_node][1]
            up_messages[parent_node][0] += up_messages[current_node][0]
            up_messages[current_node][1] = up_messages[current_node][0] * up_messages[current_node][1]
        return up_messages

    def rumor_centrality_down(self, down_messages, up_messages, who_infected, parent_node, current_node):
        if current_node == parent_node:
            down_messages[current_node] = math.log(math.factorial(len(who_infected))) - math.log((len(who_infected)))
            for child_node in who_infected[current_node]:
                down_messages[current_node] = down_messages[current_node] - math.log((up_messages[child_node][1]))
            for child_node in who_infected[current_node]:
                down_messages = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                           child_node)
        else:
            down_messages[current_node] = (down_messages[parent_node] + math.log(up_messages[current_node][0])) - (
                math.log((len(who_infected) - up_messages[current_node][0])))
            for child_node in who_infected[current_node]:
                if child_node != parent_node:
                    down_messages = self.rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                               child_node)
        return down_messages

    def rumor_centrality(self, who_infected):
        root_node = 5
        rumor_center = -1
        up_messages = []
        for i in range(len(who_infected)):
            up_messages.append([1, 1])
        down_messages = [1] * len(who_infected)
        up_message = self.rumor_centrality_up(up_messages, who_infected, root_node, root_node)
        down_message = self.rumor_centrality_down(down_messages, up_message, who_infected, root_node, root_node)
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
    





    rumor_center_object=rumor_center()
    rumor_center, center=rumor_center_object.rumor_centrality(adjacency)
    print(rumor_center,center)