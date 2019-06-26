import numpy as np
import matplotlib.pyplot as plt


def plotform():
    x = range(1, 6)
    dynamic_age = [2.3,2.5,4.3,4.7,5.1]
    K_center = [2.5,2.5,2.4,2.6,3.2]
    Our_method=[1.4,1.0,1.5,1.5,1.8]
    # plt.plot(x, y, 'ro-')
    # plt.plot(x, y1, 'bo-')
    plt.xlim(0, 7)  # 限定横轴的范围
    plt.ylim(0, 6)  # 限定纵轴的范围

    plt.plot(x, dynamic_age, marker='o', mec='r', mfc='w', label='dynamic_age')
    plt.plot(x, K_center, marker='*', ms=10, label='K_center')
    plt.plot(x, Our_method, marker='.', ms=10, label='Our_method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of sources')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    plt.title("FaceBook  data")  # 标题
    plt.savefig('f1.png')
    plt.show()


plotform()