import numpy as np
import matplotlib.pyplot as plt


def plotform():
    x = range(1, 6)
    y_train = [1.0, 1.4, 1.1 , 1.225,1.44]
    y_test = [0,1.75, 2.67, 3.2, 3.4]
    # plt.plot(x, y, 'ro-')
    # plt.plot(x, y1, 'bo-')
    plt.xlim(0, 7)  # 限定横轴的范围
    plt.ylim(0, 5)  # 限定纵轴的范围

    plt.plot(x, y_train, marker='o', mec='r', mfc='w', label='our method')
    plt.plot(x, y_test, marker='*', ms=10, label='k-center method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of sources')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    plt.title("Wiki-Vote  data")  # 标题
    plt.savefig('f1.png')
    plt.show()


plotform()