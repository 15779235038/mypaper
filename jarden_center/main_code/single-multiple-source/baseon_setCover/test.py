# encoding=utf-8
from matplotlib import pyplot
import matplotlib.pyplot as plt


x = range(1, 6)
y_train = [0.840, 0.839, 0.834, 0.832, 0.824]
y_test = [0.838, 0.840, 0.840, 0.834, 0.8281]
# plt.plot(x, y, 'ro-')
# plt.plot(x, y1, 'bo-')
# pl.xlim(-1, 11)  # 限定横轴的范围
# pl.ylim(-1, 110)  # 限定纵轴的范围

plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='our algorithm')
plt.plot(x, y_test, marker='*', ms=10, label='uniprot90_test')
plt.legend()  # 让图例生效

plt.margins(0)
plt.subplots_adjust(bottom=0.10)
plt.xlabel('Number of sources')  # X轴标签
plt.ylabel("Average error  (in hops)")  # Y轴标签
plt.title("Wiki-Vote  data")  # 标题
plt.savefig('f1.png')
plt.show()

