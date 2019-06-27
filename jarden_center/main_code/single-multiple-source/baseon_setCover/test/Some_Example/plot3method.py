import numpy as np
import matplotlib.pyplot as plt


def plotform():
    x = range(1, 6)


    #facebook
    # dynamic_age = [2.3,2.5,4.3,4.7,5.1]
    # K_center = [2.5,2.5,2.4,2.6,3.2]
    # Our_method=[1.4,1.5,1.8,2.3,2.7]

    #GA-Gq
    # # dynamic_age = [2.3,2.5,4.3,4.7,5.1]
    # # K_center = [2.5,2.5,2.4,2.6,3.2]
    Our_method=[1.7,2.0,2.2,1.9,2.2]


    plt.xlim(0, 7)  # 限定横轴的范围
    plt.ylim(0, 6)  # 限定纵轴的范围

    # plt.plot(x, dynamic_age, marker='o', mec='r', mfc='w', label='dynamic_age')
    # plt.plot(x, K_center, marker='*', ms=10, label='K_center')
    plt.plot(x, Our_method, marker='.', ms=10, label='Our_method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of sources')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    # plt.title("GAGA  data(5242 node  28980 edges)")  # 标题
    plt.title("Face-book  data(4039 node  88234 edges)")  # 标题

    plt.savefig('f1.png')
    plt.show()


plotform()