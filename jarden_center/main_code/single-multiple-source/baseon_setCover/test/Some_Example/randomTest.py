import numpy as np 

#读取excel表的sheet



import xlrd

from datetime import date,datetime

file = '数据.xlsx'

def read_excel():

	wb = xlrd.open_workbook(filename=file)#打开文件

	print(wb.sheet_names())#获取所有表格名字

	sheet1 = wb.sheet_by_index(0)#通过索引获取表格

	print(sheet1)
	print(sheet1.name,sheet1.nrows,sheet1.ncols)
	rowfangcha=[]
	for  i  in range(sheet1.nrows):
		rows=sheet1.row_values(i)
		arr_var = np.var(rows)
		rowfangcha.append(arr_var)
	print ('每一行的方差'+str(rowfangcha))

	rowfangcha.clear()
	for  j  in range(sheet1.ncols):
		cols=sheet1.col_values(j)
		arr_var = np.var(cols)
		rowfangcha.append(arr_var)
	print ('每一列的方差'+str(rowfangcha))
	# rows = sheet1.row_values(2)#获取行内容
	# cols = sheet1.col_values(3)#获取列内容
	# print(rows)
	#
	# print(cols)
	#
	# print(sheet1.cell(1,0).value)#获取表格里的内容，三种方式
	#
	# print(sheet1.cell_value(1,0))
	#
	# print(sheet1.row(1)[0].value)







read_excel()

# arr = [1,2,3,4,5,6]
# #求均值
# arr_mean = np.mean(arr)
# #求方差
# arr_var = np.var(arr)
# #求标准差
# arr_std = np.std(arr,ddof=1)
# print("平均值为：%f" % arr_mean)
# print("方差为：%f" % arr_var)
# print("标准差为:%f" % arr_std)
