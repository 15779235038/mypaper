import numpy as np
import matplotlib.pyplot as plt


def plotform():
    x = range(2, 6)


    #facebook
    # dynamic_age = [2.3,2.5,4.3,4.7,5.1]
    # K_center = [2.5,2.5,2.4,2.6,3.2]
    # Our_method=[1.4,1.5,1.8,2.3,2.7]

    #GA-Gq
    dynamic_age = [1.6,2.7,2.9,3.1,3.7]
    K_center = [2.0,2.7,2.7,2.9,3.1]
    Our_method=[1.7,2.0,2.2,1.9,2.2]


    #email-core
    # dynamic_age = [2.1,2.9,2.6,2.6,3.2]
    # K_center = [1.4,1.5,1.6,1.7,1.4]
    # Our_method = [1.6,1.8,1.2,1.6,1.7]



    #P2p
    # dynamic_age = [2.1,3.3,3.7,3.9,4.2]
    # K_center = [1.9,3.6,3.6,3.7,4.1]
    differ_time=[1.914,2.141,2.235,2.650]
    Our_method = [1.484,1.595,1.679,2.040]


    plt.xlim(1,6)  # 限定横轴的范围
    plt.ylim(1, 3)  # 限定纵轴的范围

    # plt.plot(x, dynamic_age, marker='o', mec='r', mfc='w', label='dynamic_age')
    plt.plot(x, differ_time, marker='*', ms=10, label='differ_time')
    plt.plot(x, Our_method, marker='.', ms=10, label='Our_method')
    plt.legend()  # 让图例生效

    plt.margins(0)
    plt.subplots_adjust(bottom=0.10)
    plt.xlabel('Number of sources')  # X轴标签
    plt.ylabel("Average error  (in hops)")  # Y轴标签
    # plt.title("GAGA  data(5242 node  28980 edges)")  # 标题
    plt.title("P2P")  # 标题

    plt.savefig('f1.png')
    plt.show()


plotform()