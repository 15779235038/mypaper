import numpy as np
import matplotlib.pyplot as plt


def plotform():
    x = range(1, 6)
    SI_probability = [2.3,2.5,4.3,4.7,5.1]

    # plt.plot(x, y, 'ro-')
    # plt.plot(x, y1, 'bo-')
    plt.xlim(0, 7)  # 限定横轴的范围
    plt.ylim(0, 6)  # 限定纵轴的范围

    plt.plot(x, SI_probability, marker='o', mec='r', mfc='w', label='our_method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('SI_probability')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    plt.title("FaceBook  data")  # 标题
    plt.savefig('f1.png')
    plt.show()


plotform()