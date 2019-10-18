
import  networkx as nx

####功能：将list对象N等分
def div_list(ls, n):
    if not isinstance(ls, list) or not isinstance(n, int):
        return []
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len // n
        k = ls_len % n
        ### j,j,j,...(前面有n-1个j),j+k
        # 步长j,次数n-1
        ls_return = []
        for i in range(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
        # 算上末尾的j+k
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


#获取根据中介性分层的点。
def  get_layer_node_between(G):
    sort_dict = nx.betweenness_centrality(G)
    print(sort_dict)
    sort_list = sorted(sort_dict.items(), key=lambda x: x[1], reverse=True)
    # 先均匀分成10份，然后传回去。
    sort_result = div_list(sort_list,10)
    return sort_result
    # pass


#获取根据中介性分层的边。
def get_layer_edge_between(G):
    sort_dict = nx.edge_betweenness_centrality(G)
    print(sort_dict)
    sort_list = sorted(sort_dict.items(), key=lambda x: x[1], reverse=True)
    # print(sort_list)
    # print(len(sort_list))


    #先均匀分成10份，然后传回去。
    # sort_result = div_list(sort_list,10)

    print('sort_list[0][0',sort_list[0][0])
    return sort_list


