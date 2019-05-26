import   matplotlib.pyplot  as plt
import   networkx  as nx
G = nx.path_graph(4)
pos = nx.kamada_kawai_layout(G)
print (pos)
plt.savefig("ba.png")  # 输出方式1: 将图像存为一个png格式的图片文件
plt.show()