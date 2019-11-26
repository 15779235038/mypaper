# import networkx as nx
# G = nx.DiGraph()
# # print(list(nx.bfs_tree(G ,1).edges()))
# # [(1, 0), (1, 2)]
# # H = nx.Graph()
# # nx.add_path(H, [0, 1, 2, 3, 4, 5, 6])
# # nx.add_path(H, [2, 7, 8, 9, 10])
# # print(sorted(list(nx.bfs_tree(H, source=3, depth_limit=3).edges())))
# # # [(1, 0), (2, 1), (2, 7), (3, 2), (3, 4), (4, 5), (5, 6), (7, 8)]
# #
# #
# #
# #
# #i
# #
# #
# #
# #
# #
# #
# #
# #
# # print('isTree,', nx.is_tree(H))
# # subinfectG = nx.bfs_tree(H, source=4)
# # print('isTree,', nx.is_tree(subinfectG))
# # print(sorted(list(nx.bfs_tree(H, source=3).edges())))
# #
#
#
# G.add_edges_from([(1, 2)], weight=3)
# G.add_edges_from([(2, 1)], weight=6)
# print(G[2][1]['weight'])
# print(G[1][2]['weight'])


# _*_ coding: utf-8 _*_
# 作者: yhao
# 博客: http://blog.csdn.net/yhao2014
# 邮箱: yanhao07@sina.com

# 训练集
# 每个样本点有3个分量 (x0,x1,x2)
x = [(1, 0., 3), (1, 1., 3), (1, 2., 3), (1, 3., 2), (1, 4., 4)]
# y[i] 样本点对应的输出
y = [95.364, 97.217205, 75.195834, 60.105519, 49.342380]

# 迭代阀值，当两次迭代损失函数之差小于该阀值时停止迭代
epsilon = 0.0001

# 学习率
alpha = 0.01
diff = [0, 0]
max_itor = 1000
error1 = 0
error0 = 0
cnt = 0
m = len(x)

# 初始化参数
theta0 = 0
theta1 = 0
theta2 = 0

while True:
    cnt += 1

    # 参数迭代计算
    for i in range(m):
        # 拟合函数为 y = theta0 * x[0] + theta1 * x[1] +theta2 * x[2]
        # 计算残差
        diff[0] = (theta0 + theta1 * x[i][1] + theta2 * x[i][2]) - y[i]

        # 梯度 = diff[0] * x[i][j]
        theta0 -= alpha * diff[0] * x[i][0]
        theta1 -= alpha * diff[0] * x[i][1]
        theta2 -= alpha * diff[0] * x[i][2]

    # 计算损失函数
    error1 = 0
    for lp in range(len(x)):
        error1 += (y[lp] - (theta0 + theta1 * x[lp][1] + theta2 * x[lp][2])) ** 2 / 2

    if abs(error1 - error0) < epsilon:
        break
    else:
        error0 = error1

print('nihao',theta0)
print('nihao',theta1)
print('nihao',theta2)
