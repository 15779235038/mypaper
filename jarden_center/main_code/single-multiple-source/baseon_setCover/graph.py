

import  matplotlib.pyplot as plt
x = range(1 ,4)
y_train = [1.3, 1.4, 1.5333333333333332]
y_test = [2.53, 2.31, 2.12]
# plt.plot(x, y, 'ro-')
# plt.plot(x, y1, 'bo-')
plt.xlim(0,4)  # 限定横轴的范围
plt.ylim(0,4)  # 限定纵轴的范围

plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='our method')
plt.plot(x, y_test, marker='*', ms=10, label='exist method')
plt.legend()  # 让图例生效


plt.margins(0)
plt.subplots_adjust(bottom=0.10)
plt.xlabel('Number of sources')  # X轴标签
plt.ylabel("Average error  (in hops)")  # Y轴标签
plt.title("Wiki-Vote  data")  # 标题
plt.savefig('f1.png')
plt.show()




