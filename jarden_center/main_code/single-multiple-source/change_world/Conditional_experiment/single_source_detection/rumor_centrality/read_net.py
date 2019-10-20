# -*- coding: utf-8 -*-
import networkx as nx

class readNet:
    # 抽取txt中的数据
    def read_txt(data):
        print('hello!',data)
        g = nx.read_edgelist(data, create_using=nx.DiGraph())
        print(g.edges())
        return g.edges()

    # 抽取gml中的数据
    # networkx可以直接通过函数从gml文件中读出数据
    def read_gml(data):
        H = nx.read_gml(data)
        print(H.edges())


# if __name__ == '__main__':
#     # read_txt('dolphins/dolphins.txt') 无数据
#     print('---------------gml------------------')
#     read_gml('dolphins/dolphins.gml')
