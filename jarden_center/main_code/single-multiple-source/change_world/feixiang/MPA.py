import networkx as nx
# 抽取txt中的数据
from read_net import readNet
from draw_lanl_graph import draw_lanl_graph
from random import choice
import numpy

from collections import defaultdict

#根据最短路径求节点u所在层数
def hierarchy(G,root,u):
    #tree = nx.bfs_tree(G,root)#从源位置开始的宽度优先搜索构造的定向树
    return nx.shortest_path(G,root,u)

#孩子（list）node_child
def get_t_up(G,node_child):
    sum = 0
    for u in node_child:
        sum = sum + get_traverse_len(G,u) #从孩子节点开始BFS，计算子树节点数目
    return sum

#返回BFS的节点数目
def get_traverse_len(G,root):
    traverse_edges = nx.bfs_edges(G, root)
    traverse_nodes = [root] + [v for u, v in traverse_edges]
    return len(traverse_nodes)

#孩子（list）node_child
def get_p_up(G,node_child):
    sum = 0
    for u in node_child:
        child_parent,child_child = get_child_and_parent(G,node_child,u)
        si = 0 #孩子的孩子的个数
        for i in child_child:
            si = si + get_traverse_len(G,i)
        sum = sum * si
    return sum

def get_child_and_parent(G,root,u):
    neighbor = nx.neighbors(G,u)#返回邻居节点的list
    print('父亲、孩子（list）节点为：')
    h1 = nx.shortest_path(G, root, u)  # u节点的层数
    parent = root
    child = []#孩子有多个
    for n in neighbor:
        h2 = nx.shortest_path(G, root, u)  # 邻居节点n的层数
        if h1 > h2:
            parent = n #n为u的父亲
        else:
            child.append(n) #n为u的孩子
    print(parent,child)
    return parent,child

#随机获取一个叶子节点
def get_start_node(G):
    while True:
        choice_u = choice(G)
        u = sorted(choice_u._atlas.keys())[0]
        if G.degree(u) == 1:
            break
    print('开始节点为:',u)
    return u

if __name__=="__main__":
    # dict = defaultdict(list)
    # dict['t'].append('t')
    #
    # print(dict)
    file_path = 'graphDataSet/lanl_routes.txt'
   # data = readNet.read_txt(file_path)
    G = draw_lanl_graph.lanl_graph(file_path)#生成传播图
   # print(data)
    print("G:")
    print(nx.edges(G))
    choice_v = choice(G)
    v = sorted(choice_v._atlas.keys())[0]#随机获取一个传播源
    #print(keys)
    print('传播源为：',v)
    degree_v = G.degree(v)#节点v的度
    #print(degree_v)

    #随机选一叶子节点开始遍历
    u = get_start_node(G)

    #从u开始遍历的路径
    root = u
    traverse_edges = nx.bfs_edges(G,root)
    traverse_nodes = [root] + [v for u,v in traverse_edges]
    print('遍历过程为：',traverse_nodes)

    N = len(traverse_nodes)
    print(len(traverse_nodes))
    t_up = [1] * N
    p_up = [1] * N
    r_down = [1] * N
    print('------计算开始------')
    get_child_and_parent(G, root, traverse_nodes[3])
    for node in traverse_nodes:
        if G.degree(node) == 1:
            t_up[node] = 1
            p_up[node] = 1
        else:
            node_parent, node_child = get_child_and_parent(G, root, node)
            if(node==v):
                r_down[v] = numpy.math.factorial(N-1)/get_p_up(G,node_child)#公式
            else:
                t_up[node] = get_t_up(G,node_child) + 1 #求和公式
                p_up[node] = t_up[node] * get_p_up(G,node_child) #新公式
                r_down[node] = r_down[node_parent]*(t_up[node]/(N-t_up[node]))
        print('遍历一层完成...r_down:',r_down)
    print('预测传播源为：',max(r_down))
