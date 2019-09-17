#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/15 8:09 下午

# @Author  : baozhiqiang

# @File    : test.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************

from munkres import  *
m = Munkres()

import  numpy as np

cost = np.array([[4, 5, 5] ,[3,3,4] ,[4, 2, 5]])
from scipy.optimize import linear_sum_assignment
row_ind, col_ind = linear_sum_assignment(cost)

print(cost[row_ind, col_ind].sum())

import  numpy
from munkres import  print_matrix,Munkres
def calcuCost( matrix_partim):
    m = Munkres()
    indexes = m.compute(matrix_partim)
    print_matrix(matrix_partim, msg='Lowest cost through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix_partim[row][column]
        total += value
        print(row, column, total)
    print(total)
    return total


calcuCost(np.array([[4, 5, 5] ,[3,3,4] ,[4, 2, 5]]))

