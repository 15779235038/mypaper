import copy

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
        up_message = self.jordan_centrality_up(up_messages, who_infected, root_node, root_node)
        down_message, jordan_center = self.jordan_centrality_down(up_message, who_infected, root_node, root_node, root_node)
        return jordan_center