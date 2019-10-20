import networkx as nx
# 抽取txt中的数据
from read_net import readNet
# from draw_lanl_graph import draw_lanl_graph
# from draw_general_graph import draw_general_graph
from random import choice
import numpy
import  commons
from collections import defaultdict

#孩子（list）node_child 首先建树，
def get_t_up(G,root,node_child):
    #print('t_up start!')
    sum = 0
    tree = nx.bfs_tree(G,root)# tree为树图
    # print('传播源：',root)
    # print('node_child',node_child)
    for u in node_child:
        sum = sum + get_traverse_len(tree,u) #从孩子节点开始BFS，计算子树节点数目
    return sum

#返回BFS的节点数目 子树大小 但是不包括根
def get_traverse_len(G,root):
    #print('gettraverselen:',root,'子树')
    traverse_edges = nx.bfs_edges(G, root)
    # print(root,'TTTT',list(traverse_edges))
    # print(list(nx.neighbors(G,root)))
    traverse_nodes = [v for u, v in traverse_edges]
    #print(traverse_nodes)
    return len(traverse_nodes)

#孩子（list）node_child
def get_p_up(G,root,node_child):
    print('p_up start!')
    sum = 1
    tree = nx.bfs_tree(G, root)
    for u in node_child:
        child_parent,child_child = get_child_and_parent(G,root,u)
        si = 0 #孩子的孩子的个数
        for i in child_child:
            si = si + get_traverse_len(tree,i)
        sum = sum * si # 乘改为+
    return sum

def get_child_and_parent(G,root,u):
    neighbor = nx.neighbors(G,u)#返回邻居节点的list
    #print('父亲、孩子（list）节点为：')
    h1 = nx.shortest_path(G, root, u)  # u节点的层数
    parent = root
    child = []#孩子有多个
    for n in neighbor:
        h2 = nx.shortest_path(G, root, u)  # 邻居节点n的层数
        if h1 > h2:
            parent = n #n为u的父亲
        # else:
        #     child.append(n)  # n为u的孩子     直接这样 兄弟之间的孩子会有重复
    tree = nx.bfs_tree(G, root) #使用定向树求孩子 定向树的邻居就是孩子
    child = nx.neighbors(tree,u)
    return parent,child

#随机获取一个叶子节点
def get_start_node(G):
    # while True:
    choice_u = choice(G)
    u = sorted(choice_u._atlas.keys())[0]
        # if G.degree(u) == 1:
        #     break
    return u

# if __name__=="__main__":
    # dict = defaultdict(list)
    # dict['t'].append('t')
    #
    # print(dict)
def MPA(file_path,n=2): #3为带有权重或者时间标志的三元组图，2为一般图 默认值
    #file_path = 'graphDataSet/3_regular_tree_200_data.txt' #3_regular_tree_25_data.txt
    #data = readNet.read_txt(file_path)
    if n==3:
        # G = draw_lanl_graph.lanl_graph(file_path)
        # draw_lanl_graph.draw_lanl_graph(G)
        pass
    else:
        G = commons.get_networkByFile('../../../../data/3regular_tree1000.txt')

        # G = draw_general_graph.general_graph(file_path)#生成传播图
        # draw_general_graph.draw_general_graph(G) #画图
   # print(data)
   #  print("G:")
    print(nx.edges(G))
    v= get_start_node(G)#随机获取一个传播源
    print('传播源为：',v)
    #degree_v = G.degree(v)#节点v的度
    #print(degree_v)

    #随机选一节点开始遍历
    u = get_start_node(G)
    print('开始节点为:',u)

    #从u开始遍历的路径
    root = u
    traverse_edges = nx.bfs_edges(G,root)
    traverse_nodes = [root] + [v for u,v in traverse_edges]
    print('遍历过程为：',traverse_nodes)

    N = len(traverse_nodes)
    #print(len(traverse_nodes))
    t_up = [1] * N
    p_up = [1] * N
    r_down = [1] * N
    print('------计算开始------')
    # parent,child = get_child_and_parent(G, v, traverse_nodes[6])
    # print('孩子传递给父亲的t_up:',get_t_up(G,v,child),'p_up:',get_p_up(G,v,child))
    for node in traverse_nodes:
        if G.degree(node) == 1:
            t_up[node] = 1
            p_up[node] = 1
        else:
            node_parent, node_child = get_child_and_parent(G, v, node)
            node_gradpa, node_brother = get_child_and_parent(G, root, node_parent)  # 向上一步，求所有的孩子
            if(node==v):
                for n in node_child:
                    r_down[n] = numpy.sum(N)/N * get_p_up(G,v,node_child)#公式
            else:
                t_up[node_parent] = get_t_up(G,v,node_brother) + 1 #t_up
                p_up[node_parent] = t_up[node_parent] * get_p_up(G,v,node_brother) #p_up
                for n in node_child:
                    r_down[n] = r_down[node_parent]*(t_up[node_parent]/(N-t_up[node_parent]))
        print('遍历一层完成...r_down:',r_down)
        # print('t_up',t_up)
        # print('p_up',p_up)
        print(' ')
    for i in range(0,N):
        if r_down[i] == max(r_down):
            print('预测传播源为：', i)
            print('距离为',nx.shortest_path_length(G,source=i,target=v))
            print('真实传播源为',v)
            print(list(nx.neighbors(G, v)))
            print(list(nx.neighbors(G,i)))
    return G



MPA('../../../../data/treenetwork3000.txt',n=2)


