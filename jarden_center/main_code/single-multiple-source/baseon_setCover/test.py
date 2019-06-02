# encoding=utf-8
from matplotlib import pyplot
import matplotlib.pyplot as plt

names = range(8, 21)
names = [str(x) for x in list(names)]
print (names)
x = range(len(names))
y_train = [0.840, 0.839, 0.834, 0.832, 0.824, 0.831, 0.823, 0.817, 0.814, 0.812, 0.812, 0.807, 0.805]
y_test = [0.838, 0.840, 0.840, 0.834, 0.828, 0.814, 0.812, 0.822, 0.818, 0.815, 0.807, 0.801, 0.796]
# plt.plot(x, y, 'ro-')
# plt.plot(x, y1, 'bo-')
# pl.xlim(-1, 11)  # 限定横轴的范围
# pl.ylim(-1, 110)  # 限定纵轴的范围


plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='uniprot90_train')
plt.plot(x, y_test, marker='*', ms=10, label='uniprot90_test')
plt.legend()  # 让图例生效
plt.xticks(x, names, rotation=1)

plt.margins(0)
plt.subplots_adjust(bottom=0.10)
plt.xlabel('the length')  # X轴标签
plt.ylabel("f1")  # Y轴标签
pyplot.yticks([0.750, 0.800, 0.850])
# plt.title("A simple plot") #标题
plt.savefig('f1.png')
plt.show()
