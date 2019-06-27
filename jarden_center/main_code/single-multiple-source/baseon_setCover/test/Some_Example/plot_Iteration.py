import numpy as np
import matplotlib.pyplot as plt


def plotform():
    x = [5,10,20]
    SI_probability = [1.8,1.5,1.3]

    # plt.plot(x, y, 'ro-')
    # plt.plot(x, y1, 'bo-')W
    plt.xlim(1, 25)  # 限定横轴的范围
    plt.ylim(0, 4)  # 限定纵轴的范围

    plt.plot(x, SI_probability, marker='o', mec='r', mfc='w', label='our_method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('iterations ')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    plt.title("Jaya algorithm at  FaceBook  data")  # 标题
    plt.savefig('f1.png')
    plt.show()


plotform()