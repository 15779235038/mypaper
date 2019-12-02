# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import numpy as np
import networkx as nx
import scipy as sp
import math

import data
from time import clock

a = np.random.rand(2,2)
b = np.random.rand(2,2)
print a*b, a[0,0], np.ones([5,5])
a = np.mat(a)
b = np.mat(b)
print a, b
print a*b
print a[0,0]*b[0,0]+a[0,1]*b[1,0]
print np.log(a).diagonal()

d = data.Graph("../data/test.txt", weighted=1)
a = nx.adjacency_matrix(d.graph).todense()  # adjacent matrix
aa = nx.adjacency_matrix(d.graph, weight=None).todense()  # adjacent matrix

mu = np.zeros(d.graph.number_of_nodes())  # recover probability
d = np.ones([5,5])
print a
print aa
print np.dot(a,aa)
print d[0], a.diagonal()

print np.tile(1,5)

x = np.asarray([[1,2],[3,4]])
y = np.asarray([[2.0,2.0],[2.0,2.0]])
print x[0][0], x[0,1]

print math.factorial(1000)
print np.arange(0,10)

import collections
d = collections.OrderedDict()
d['a'] = 20
d['b'] = 10
d['c'] = 30
print collections.OrderedDict(sorted(d.items(), key=lambda t: t[1]))

g = nx.barabasi_albert_graph(4000, 10)
print g.number_of_nodes(), g.number_of_edges()
a= nx.adjacency_matrix(g, weight='weight')
x = 0
start = clock()
for i in np.arange(100000):
    x += a[0,2]
end = clock()
print x, end-start

b= a.todense()
start = clock()
for i in np.arange(100000):
    x += b[0,2]
end = clock()
print x, end-start

b= b.tolist()
start = clock()
for i in np.arange(100000):
    x += b[0][2]
end = clock()
print x, end-start
