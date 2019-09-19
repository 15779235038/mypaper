
#!/usr/bin/python3

# -*-coding:utf-8 -*-

#Reference:**********************************************

# @Time    : 2019/9/18 8:50 下午

# @Author  : baozhiqiang

# @File    : test.py

# @User    : bao

# @Software: PyCharm

#Reference:**********************************************



def  csv(dir):
        import csv

        import pandas as pd
        df = pd.read_csv(dir, index_col=0)

        final_list = df.tolist()
        print(final_list)






dir = './data_center/CA-GrQc.csv'
csv(dir)