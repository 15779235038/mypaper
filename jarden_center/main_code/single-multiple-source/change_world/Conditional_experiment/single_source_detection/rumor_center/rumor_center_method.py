import math
import sys
sys.setrecursionlimit(100000) #例如这里设置为十万

def rumor_centrality_up(up_messages, who_infected, parent_node, current_node):
    # message_passing_up(up_messages, adjacency, root_node, root_node)
    if current_node == parent_node:
        for child_node in who_infected[current_node]:
            up_messages = rumor_centrality_up(up_messages, who_infected, current_node, child_node)
    elif len(who_infected[current_node]) == 1:
        up_messages[parent_node][0] += 1
        up_messages[parent_node][1] = up_messages[parent_node][1] * up_messages[current_node][1]
    # leave
    else:
        for child_node in who_infected[current_node]:
            if child_node != parent_node:
                up_messages = rumor_centrality_up(up_messages, who_infected, current_node, child_node)
                up_messages[current_node][1] = up_messages[current_node][1] * up_messages[child_node][1]
        up_messages[parent_node][0] += up_messages[current_node][0]
        up_messages[current_node][1] = up_messages[current_node][0] * up_messages[current_node][1]
    return up_messages


def rumor_centrality_down(down_messages, up_messages, who_infected, parent_node, current_node):
    if current_node == parent_node:
        down_messages[current_node] = math.log(math.factorial(len(who_infected))) - math.log((len(who_infected)))
        for child_node in who_infected[current_node]:
            down_messages[current_node] = down_messages[current_node] - math.log((up_messages[child_node][1]))
        for child_node in who_infected[current_node]:
            down_messages = rumor_centrality_down(down_messages, up_messages, who_infected, current_node, child_node)
    else:
        down_messages[current_node] = (down_messages[parent_node] + math.log(up_messages[current_node][0])) - (
            math.log((len(who_infected) - up_messages[current_node][0])))
        for child_node in who_infected[current_node]:
            if child_node != parent_node:
                down_messages = rumor_centrality_down(down_messages, up_messages, who_infected, current_node,
                                                      child_node)
    return down_messages


def rumor_centrality(who_infected):
    root_node = 2
    rumor_center = -1
    up_messages = []
    for i in range(len(who_infected)):
        up_messages.append([1, 1])
    down_messages = [1] * len(who_infected)
    up_message = rumor_centrality_up(up_messages, who_infected, root_node, root_node)
    down_message = rumor_centrality_down(down_messages, up_message, who_infected, root_node, root_node)
    center = max(down_message)
    for i in range(len(down_messages)):
        if down_messages[i] == center:
            rumor_center = i

    return rumor_center,center


# creating a toy graph (tree)
adjacency = [ [] for i in range(11)]
# adjacency[0] = []
adjacency[10] = [6, 7, 8]
adjacency[1] = [2, 3, 7]
adjacency[2] = [1, 3, 4]
adjacency[9] = [5, 6, 7]
adjacency[3] = [1, 2, 5]
adjacency[4] = [2, 5]
adjacency[5] = [3, 9]
adjacency[6] = [8, 9, 10]
adjacency[7] = [1, 9, 10]
adjacency[8] = [6, 10]
adjacency[9] = [5, 6, 7]

root_node = 2 # can use any arbitrary index for the root node

print(rumor_centrality(adjacency))
