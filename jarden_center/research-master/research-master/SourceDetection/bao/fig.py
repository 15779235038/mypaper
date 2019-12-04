# coding=utf-8
"""
A part of Source Detection.
Author: Biao Chang, changb110@gmail.com, from University of Science and Technology of China
created at 2017/1/9.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


class Fig:
    """drawing figs according to the experiment results."""
    # colors = {'RC': '#00008f', 'DC': '#0070ff', 'JC': '#00dfff', 'RI': '#bfff40', 'DI': '#ffcf00',
    #           'DMP': '#ff6000', 'GSBA-JC': '#ef0000', 'BFSA-JC': '#800000', 'GSBA-U': '#696969', 'GSBA-RC': '#9aad74',
    #           'GSBA-DC': '#31591F', 'GSBA-RI': '#bfff40', 'GSBA-DMP': '#ff6000'}
    colors = {'RC': '#4065BB', 'DC': '#FE7E00', 'JC': '#00B200', 'RI': '#D70000', 'DI': '#9E38C3',
              'DMP': '#8B5446', 'GSBA-JC': '#EB4AC3', 'BFSA-JC': '#7E7E7E', 'GSBA-RC': '#AFCE00',
              'GSBA-DC': '#24BED4', r'GSBA$^-$':'#000000'}
    markers = {'RC': '.', 'DC': '*', 'JC': 'o', 'RI': 'p', 'DI': '+',
               'DMP': 'x', 'GSBA-JC': 's', 'BFSA-JC': '^', 'GSBA-U': '>', 'GSBA-RC': '.', 'GSBA-DC': '*',
               'GSBA-RI': 'p', 'GSBA-DMP': 'x','GSBA$^-$':'x'}
    # hatchs = {'GSBA-RC':'','GSBA-DC','GSBA-JC'}
    debug = False

    def wang_result_recall(self):
        x = ['Cora','Citeseer']
        methods = ['Attri', 'Node2vec', 'LINE', 'Node2vec+Attri', 'LINE+Attri', 'TADW', 'UPP-SNE', 'AANE-N','AANE-A','AANE']
        #colors = ['#0000FF','#1700E8','#2E00D1','#4600B9','#5D00A2','#74008B','#8B0074','#A2005D','#B90046','#696969','#E80017','#FF0000']
        colors = ['#00008f','#0070ff','#00dfff','#bfff40','#31591F','#ffcf00','#ff6000','#ef0000','#B90046','#800000']

        m = len(methods)
        xlabel = 'Data'
        y = [[0.4088,0.6308 ,0.5916 ,0.6516 ,0.6283 ,0.5612 ,0.6116 ,0.7201 ,0.7393 ,0.7443 ],
             [0.5116 ,0.6402 ,0.6252 ,0.6639 ,0.7135 ,0.7313 ,0.7570 ,0.821 ,0.8402 ,0.8422 ]]
        ylabel = 'Recall@5'
        path = base_path + 'recall5.pdf'

        legend = methods[0:m]
        n = len(legend)
        width = 0.4  # the width of the bars
        index = np.arange(len(x))
        fig, ax = plt.subplots(figsize=(11, 8))
        for i in np.arange(0, n):
            print y[0][i],y[1][i]
            ax.bar(index + i * width * 2 / n + 0.1, [y[0][i],y[1][i]], width * 2 / n, label=legend[i],
                       color=colors[i])
        #plt.xlabel(xlabel, fontsize=38)
        plt.ylabel(ylabel, fontsize=38)
        # plt.title('Scores by group and Category')

        plt.xticks(index + width + 0.1, x, fontsize=38)
        plt.yticks(fontsize=38)  # change the num axis size
        # plt.xlim(0, 50)  # The ceil
        y_min = np.min(y)
        y_max = np.max(y)
        plt.ylim(0.8 * y_min, 1.15 * y_max)  # The ceil
        plt.legend(loc=1, ncol=n / 2, mode="expand", borderaxespad=0., fontsize=26)
        plt.tight_layout()
        if path is not None:
            fig.savefig(path)
        plt.show()
        plt.close()

    def wang_parameter_lines(self):
        # x = [0,0.2,0.4,0.6,0.8,1]
        # dataset = ['Cora','Citeseer','DBLP']
        # colors = ['#0070ff','#31591F','#B90046']
        # marker = ['*','o','d']
        # xlabel = r'$\lambda$'
        # y = [[0.82,0.83 ,0.84 ,0.85 ,0.85 ,0.83 ],
        #     [0.73 ,0.72 ,0.72 ,0.73 ,0.74 ,0.72 ],
        #     [0.82 ,0.82 ,0.84 ,0.84 ,0.84 ,0.82]]
        # ylabel = 'Micro-F1'
        # path = base_path + 'micro-f1-lambda.pdf'
        #
        # legend = dataset
        # n = len(legend)
        # width = 5
        # fig, ax = plt.subplots(figsize=(11, 8))
        # for i in np.arange(0, n):
        #     ax.plot(x, y[i], '-D', label=legend[i], color=colors[i], linewidth=width,
        #             markersize=22, marker=marker[i], markeredgewidth=2)
        # plt.xlabel(xlabel, fontsize=38)
        # plt.ylabel(ylabel, fontsize=38)
        # # plt.title('Scores by group and Category')
        #
        # plt.xticks(fontsize=38)
        # plt.yticks(fontsize=38)  # change the num axis size
        # # plt.xlim(0, 50)  # The ceil
        # y_min = np.min(y)
        # y_max = np.max(y)
        # x_max = np.max(x)
        # x_min = np.min(x)
        # plt.xlim(-0.01, x_max*1.01)
        # if y_min<0.1:
        #     plt.ylim(y_min-0.04, 1.05 * y_max)  # The ceil
        # else:
        #     plt.ylim(y_min*0.97, 1.05 * y_max)  # The ceil
        # plt.legend(loc=1, ncol=3, mode="expand", borderaxespad=0., fontsize=28)
        # plt.tight_layout()
        # plt.show()
        # if path is not None:
        #     fig.savefig(path)
        # plt.close()


        x = [50,100,150,200,250,300]
        dataset = ['Cora','Citeseer','DBLP']
        colors = ['#0070ff','#31591F','#B90046']
        marker = ['*','o','d']
        xlabel = 'Embedding Dimension, d'
        y = [[0.84 ,0.85 ,0.85 ,0.85 ,0.85 ,0.85],
            [0.73 ,0.74 ,0.73 ,0.73 ,0.73 ,0.73 ],
            [0.83 ,0.83 ,0.83 ,0.84 ,0.84, 0.83 ]]
        ylabel = 'Micro-F1'
        path = base_path + 'micro-f1-Embedding-Dimension.pdf'

        legend = dataset
        n = len(legend)
        width = 5
        fig, ax = plt.subplots(figsize=(11, 8))
        for i in np.arange(0, n):
            ax.plot(x, y[i], '-D', label=legend[i], color=colors[i], linewidth=width,
                    markersize=22, marker=marker[i], markeredgewidth=2)
        plt.xlabel(xlabel, fontsize=38)
        plt.ylabel(ylabel, fontsize=38)
        # plt.title('Scores by group and Category')

        plt.xticks(fontsize=38)
        plt.yticks(fontsize=38)  # change the num axis size
        # plt.xlim(0, 50)  # The ceil
        y_min = np.min(y)
        y_max = np.max(y)
        x_max = np.max(x)
        x_min = np.min(x)
        plt.xlim(x_min-2, x_max*1.01)
        if y_min<0.1:
            plt.ylim(y_min-0.04, 1.05 * y_max)  # The ceil
        else:
            plt.ylim(y_min*0.97, 1.05 * y_max)  # The ceil
        plt.legend(loc=1, ncol=3, mode="expand", borderaxespad=0., fontsize=28)
        plt.tight_layout()
        plt.show()
        if path is not None:
            fig.savefig(path)
        plt.close()

    def bars(self, x, y, legend, xlabel, ylabel, title='', path=None):
        n = len(legend)
        width = 0.4  # the width of the bars
        index = np.arange(len(x))
        fig, ax = plt.subplots(figsize=(11, 8))
        for i in np.arange(0, n):
            if legend[i].startswith('GSBA'):
                ax.bar(index + i * width * 2 / n + 0.1, y[i], width * 2 / n,
                       label=legend[i], color=self.colors[legend[i]], hatch='')
            else:
                ax.bar(index + i * width * 2 / n + 0.1, y[i], width * 2 / n, label=legend[i],
                       color=self.colors[legend[i]])
        plt.xlabel(xlabel, fontsize=38)
        plt.ylabel(ylabel, fontsize=38)
        # plt.title('Scores by group and Category')

        plt.xticks(index + width + 0.1, x, fontsize=38)
        plt.yticks(fontsize=38)  # change the num axis size
        # plt.xlim(0, 50)  # The ceil
        y_min = np.min(y)
        y_min = 0
        y_max = np.max(y)
        plt.ylim(0.8 * y_min, 1.28 * y_max)  # The ceil
        plt.legend(loc=1, ncol=n / 2, mode="expand", borderaxespad=0., fontsize=26)
        plt.tight_layout()
        if path is not None:
            fig.savefig(path)
        if self.debug:
            plt.show()
        plt.close()

    def lines(self, x, y, legend, xlabel, ylabel, title='', path=None):
        n = len(legend)
        width = 5
        fig, ax = plt.subplots(figsize=(11, 8))
        for i in np.arange(0, n):
            ax.plot(x, y[i], '-D', label=legend[i], color=self.colors[legend[i]], linewidth=width,
                    markersize=22, marker=self.markers[legend[i]], markeredgewidth=2)
        plt.xlabel(xlabel, fontsize=38)
        plt.ylabel(ylabel, fontsize=38)
        # plt.title('Scores by group and Category')

        plt.xticks(fontsize=38)
        plt.yticks(fontsize=38)  # change the num axis size
        # plt.xlim(0, 50)  # The ceil
        y_min = np.min(y)
        y_max = np.max(y)
        x_max = np.max(x)
        x_min = np.min(x)
        plt.xlim(x_min*0.99, x_max*1.01)
        # if y_min<0.1:
        #     plt.ylim(y_min-0.04, 1.3 * y_max)  # The ceil
        # else:
        #     plt.ylim(y_min*0.9, 1.3 * y_max)  # The ceil
        plt.ylim(0, 1.3 * y_max)  # The ceil
        plt.legend(loc=1, ncol=n / 2, mode="expand", borderaxespad=0., fontsize=28)
        plt.tight_layout()
        if self.debug:
            plt.show()
        if path is not None:
            fig.savefig(path)
        plt.close()

    def test(self, base_path):
        x = np.arange(20, 46, 5)
        methods = ['RC', 'DC', 'JC', 'GSBA-RC', 'GSBA-DC', 'GSBA-JC']
        m = len(methods)
        xlable = 'Number of  infected nodes, N'
        y = [[0.092086622, 0.075288403, 0.069216758, 0.063145112, 0.047763611, 0.043108682],
             [0.087634082, 0.069823922, 0.060716454, 0.052823315, 0.044930176, 0.042096742],
             [0.113337381, 0.087634082, 0.075490791, 0.07124064, 0.062133171, 0.049989881],
             [0.156243675, 0.126087836, 0.114754098, 0.107468124, 0.087634082, 0.081562437],
             [0.17911354, 0.148755313, 0.132564258, 0.118801862, 0.101801255, 0.094312892],
             [0.182756527, 0.150779194, 0.133171423, 0.119409027, 0.102003643, 0.093300951], ]
        ylabel = 'Detection Rate'
        path = base_path + 'wiki-vote-prior-full-rate.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

    def results_on_scale_free(self, base_path):
        x = np.arange(5, 11, 1)
        methods = ['RC', 'DC', 'JC', 'RI', 'DI', 'DMP', 'GSBA-JC', 'BFSA-JC']
        m = len(methods)
        xlable = 'Number of  infected nodes, N'
        y = [[0.35,0.27,0.26,0.27,0.17,0.17],[
0.36,0.32,0.26,0.26,0.15,0.16],[
0.29,0.28,0.27,0.23,0.29,0.29],[
0.35,0.28,0.27,0.25,0.16,0.15],[
0.25,0.23,0.24,0.22,0.14,0.18],[
0.57,0.61,0.62,0.51,0.63,0.53],[
0.53,0.46,0.55,0.53,0.52,0.37],[
0.6,0.58,0.67,0.59,0.65,0.51]]
        ylabel = 'Detection Rate'
        path = base_path + 'scale-free-random-rate.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.7,0.82,0.8,0.84,0.98,1.04],[
0.69,0.76,0.8,0.82,1.01,1.03],[
0.78,0.8,0.8,0.91,0.87,0.93],[
0.72,0.83,0.82,0.85,1.02,1.14],[
0.81,0.89,0.87,0.9,1.06,1.13],[
0.49,0.43,0.51,0.62,0.52,0.61],[
0.53,0.63,0.63,0.59,0.76,0.9],[
0.46,0.49,0.44,0.48,0.51,0.69]]
        ylabel = 'Detection Error'
        path = base_path + 'scale-free-random-error.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.462,0.446666667,0.418571429,0.36375,0.378888889,0.385],[
0.452,0.396666667,0.388571429,0.3925,0.397777778,0.431],[
0.48,0.421666667,0.4,0.37,0.375555556,0.406],[
0.436,0.423333333,0.377142857,0.3775,0.39,0.417],[
0.532,0.518333333,0.511428571,0.49625,0.511111111,0.495],[
0.372,0.371666667,0.281428571,0.335,0.288888889,0.332],[
0.336,0.293333333,0.254285714,0.2525,0.242222222,0.249],[
0.31,0.248333333,0.221428571,0.21,0.182222222,0.189]]
        ylabel = 'Detection Ranking'
        path = base_path + 'scale-free-random-ranking.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.326,0.288,0.256,0.228,0.218,0.216],[
0.328,0.288,0.248,0.214,0.22,0.196],[
0.318,0.294,0.318,0.29,0.322,0.306],[
0.328,0.288,0.244,0.202,0.212,0.194],[
0.31,0.252,0.216,0.204,0.17,0.16],[
0.622,0.596,0.596,0.596,0.586,0.544],[
0.56,0.514,0.474,0.458,0.476,0.392],[
0.644,0.612,0.582,0.61,0.62,0.568]]
        ylabel = 'Detection Rate'
        path = base_path + 'scale-free-full-rate.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.712,0.796,0.832,0.886,0.908,0.98],[
0.718,0.792,0.846,0.894,0.926,0.994],[
0.74,0.792,0.792,0.856,0.822,0.884],[
0.718,0.804,0.874,0.934,0.964,1.022],[
0.752,0.86,0.904,0.962,1.024,1.106],[
0.438,0.474,0.51,0.52,0.532,0.608],[
0.518,0.634,0.688,0.752,0.744,0.886],[
0.42,0.484,0.538,0.524,0.506,0.594]]
        ylabel = 'Detection Error'
        path = base_path + 'scale-free-full-error.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.4576,0.44,0.409714286,0.3875,0.357777778,0.3606],[
0.4444,0.415,0.406857143,0.388,0.368222222,0.3764],[
0.4472,0.420666667,0.394,0.371,0.348222222,0.3458],[
0.4404,0.410666667,0.399142857,0.38125,0.355333333,0.3688],[
0.5232,0.523333333,0.511714286,0.499,0.498666667,0.5014],[
0.36,0.348666667,0.324857143,0.30775,0.309333333,0.312],[
0.3236,0.297,0.279714286,0.25375,0.232,0.245],[
0.296,0.260666667,0.232571429,0.20325,0.183555556,0.1804]]
        ylabel = 'Detection Ranking'
        path = base_path + 'scale-free-full-ranking.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

    def results_on_power_grid(self, base_path):
        x = np.arange(20, 46, 5)
        methods = ['RC', 'DC', 'JC', 'RI', 'DI', 'GSBA-JC']
        m = len(methods)
        xlable = 'Number of  infected nodes, N'
        y = [[0.08, 0.11, 0.05, 0.15, 0.07, 0.03], [
            0.08, 0.06, 0.06, 0.09, 0.03, 0.02], [
                 0.03, 0.08, 0.11, 0.12, 0.07, 0.07], [
                 0.1, 0.05, 0.05, 0.07, 0.05, 0.02], [
                 0.03, 0.03, 0.02, 0.03, 0.02, 0.01], [
                 0.19, 0.11, 0.15, 0.14, 0.14, 0.1]]
        ylabel = 'Detection Rate'
        path = base_path + 'power-grid-random-rate.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[1.98, 1.78, 2.25, 2.26, 2.48, 2.76], [
            1.97, 1.83, 2.26, 2.48, 2.42, 2.78], [
                 2.05, 1.95, 2.29, 2.38, 2.43, 2.81], [
                 2, 1.94, 2.3, 2.65, 2.54, 2.87], [
                 2.47, 2.25, 2.81, 3.02, 3.25, 3.6], [
                 1.54, 1.88, 2.18, 2.15, 2.1, 2.52]]
        ylabel = 'Detection Error'
        path = base_path + 'power-grid-random-error.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.4835, 0.3956, 0.441666667, 0.407142857, 0.41275, 0.472222222], [
            0.448, 0.4336, 0.406666667, 0.437142857, 0.398, 0.472666667], [
                 0.4215, 0.4268, 0.372666667, 0.400571429, 0.378, 0.446666667], [
                 0.434, 0.4156, 0.422666667, 0.416857143, 0.38425, 0.449555556], [
                 0.615, 0.4828, 0.561, 0.566285714, 0.579, 0.586], [
                 0.2475, 0.2472, 0.247333333, 0.239428571, 0.22675, 0.269333333]]
        ylabel = 'Detection Ranking'
        path = base_path + 'power-grid-random-ranking.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.092086622, 0.075288403, 0.069216758, 0.063145112, 0.047763611, 0.043108682], [
            0.087634082, 0.069823922, 0.060716454, 0.052823315, 0.044930176, 0.042096742], [
                 0.113337381, 0.087634082, 0.075490791, 0.07124064, 0.062133171, 0.049989881], [
                 0.086622141, 0.066990488, 0.056263914, 0.052823315, 0.043108682, 0.041894353], [
                 0.05565675, 0.043108682, 0.034608379, 0.027727181, 0.021453147, 0.019024489], [
                 0.182756527, 0.150779194, 0.133171423, 0.119409027, 0.102003643, 0.093300951]]
        ylabel = 'Detection Rate'
        path = base_path + 'power-grid-full-rate.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[1.859542603, 2.085205424, 2.253187614, 2.37259664, 2.522363894, 2.649868448], [
            1.865614248, 2.082169601, 2.252985226, 2.370977535, 2.505768063, 2.611009917], [
                 1.878567092, 2.082169601, 2.263711799, 2.388990083, 2.520340012, 2.654523376], [
                 1.92430682, 2.165958308, 2.346286177, 2.471969237, 2.603926331, 2.709775349], [
                 2.326047359, 2.580854078, 2.822100789, 3.019024489, 3.189435337, 3.344059907], [
                 1.652499494, 1.866828577, 2.030965392, 2.158065169, 2.360858126, 2.44161101]]
        ylabel = 'Detection Error'
        path = base_path + 'power-grid-full-error.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.437543007, 0.43623558, 0.439141874, 0.431555209, 0.434036632, 0.434774787], [
            0.42157458, 0.41896782, 0.42340282, 0.417411166, 0.418594414, 0.416177562], [
                 0.408490184, 0.402558187, 0.402158807, 0.395877064, 0.393336369, 0.392444175], [
                 0.418002429, 0.414628618, 0.416137084, 0.409321421, 0.407564258, 0.405896242], [
                 0.557761587, 0.559417122, 0.563866964, 0.56359904, 0.564232949, 0.567716836], [
                 0.264480874, 0.258708763, 0.256068272, 0.249197675, 0.248709775, 0.245330455]]

        ylabel = 'Detection Ranking'
        path = base_path + 'power-grid-full-ranking.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

    def results_on_wiki_vote(self, base_path):
        x = np.arange(20, 46, 5)
        methods = ['RC', 'DC', 'JC', 'RI', 'DI', 'GSBA-JC']
        m = len(methods)
        xlable = 'Number of  infected nodes, N'
        y = [[0.36, 0.37, 0.31, 0.31, 0.36, 0.22], [
            0.13, 0.2, 0.06, 0.07, 0.04, 0.02], [
                 0.22, 0.27, 0.21, 0.21, 0.13, 0.14], [
                 0.15, 0.1, 0.02, 0.03, 0.07, 0.01], [
                 0.28, 0.35, 0.26, 0.23, 0.19, 0.16], [
                 0.57, 0.45, 0.45, 0.46, 0.47, 0.46]]
        ylabel = 'Detection Rate'
        path = base_path + 'wiki-vote-random-rate.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.67, 0.65, 0.74, 0.73, 0.67, 0.87], [
            1.17, 1.13, 1.3, 1.35, 1.5, 1.46], [
                 0.94, 0.88, 0.95, 0.95, 1.04, 1.1], [
                 1.26, 1.46, 1.55, 1.63, 1.62, 1.68], [
                 0.81, 0.72, 0.85, 0.8, 0.85, 0.96], [
                 0.59, 0.75, 0.85, 0.77, 0.83, 0.87]]
        ylabel = 'Detection Error'
        path = base_path + 'wiki-vote-random-error.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.2595, 0.2208, 0.234333333, 0.197714286, 0.17375, 0.173333333], [
            0.5125, 0.522, 0.585333333, 0.579428571, 0.63125, 0.605333333], [
                 0.386, 0.4328, 0.433666667, 0.437428571, 0.50025, 0.453111111], [
                 0.4725, 0.5744, 0.546, 0.598571429, 0.56775, 0.557111111], [
                 0.534, 0.4952, 0.566, 0.530285714, 0.578, 0.594], [
                 0.102, 0.1012, 0.085333333, 0.104857143, 0.07625, 0.088222222]]
        ylabel = 'Detection Ranking'
        path = base_path + 'wiki-vote-random-ranking.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.333427682, 0.321398245, 0.313331446, 0.297339372, 0.285168412, 0.287149731], [
            0.147325219, 0.104585338, 0.074157939, 0.052646476, 0.036795924, 0.025191056], [
                 0.269176337, 0.230257571, 0.204924993, 0.183272007, 0.155250495, 0.146900651], [
                 0.088876309, 0.04825927, 0.037220492, 0.027879989, 0.026323238, 0.021228418], [
                 0.296348712, 0.267195018, 0.240730258, 0.220775545, 0.199830173, 0.181432211], [
                 0.523634305, 0.490659496, 0.466034532, 0.443532409, 0.418341353, 0.4105576]]
        ylabel = 'Detection Rate'
        path = base_path + 'wiki-vote-full-rate.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.69615058, 0.713699406, 0.728700821, 0.758562129, 0.78304557, 0.795075007], [
            1.120718936, 1.244126804, 1.346447778, 1.433908859, 1.515992075, 1.576139258], [
                 0.831021795, 0.901641664, 0.956835551, 1.015001415, 1.083215398, 1.136569488], [
                 1.342202095, 1.542881404, 1.593405038, 1.630484008, 1.673082366, 1.688932918], [
                 0.751627512, 0.790829324, 0.833286159, 0.870648174, 0.913812624, 0.961081234], [
                 0.678318709, 0.742994622, 0.802717237, 0.856495896, 0.913529578, 0.946079819]]
        ylabel = 'Detection Error'
        path = base_path + 'wiki-vote-full-error.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.25394141, 0.234203227, 0.212062459, 0.199057863, 0.190192471, 0.182432305], [
            0.516593547, 0.550240589, 0.574474007, 0.602054102, 0.622151854, 0.643060666], [
                 0.389088593, 0.40931786, 0.431389754, 0.451255509, 0.476461223, 0.496059377], [
                 0.506941693, 0.587042174, 0.584904236, 0.581052121, 0.574823097, 0.574104475], [
                 0.523690914, 0.539416926, 0.552103972, 0.563535644, 0.575258279, 0.583080165], [
                 0.108831022, 0.099433909, 0.093301255, 0.091063847, 0.086944523, 0.084960845]]

        ylabel = 'Detection Ranking'
        path = base_path + 'wiki-vote-full-ranking.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

    def results_on_ca_astroph(self, base_path):
        x = np.arange(20, 46, 5)
        methods = ['RC', 'DC', 'JC', 'RI', 'DI', 'GSBA-RC', 'GSBA-DC', 'GSBA-JC']
        m = len(methods)
        xlable = 'Number of  infected nodes, N'
        y = [[0.256,0.2315,0.2335,0.205,0.202,0.1945],[
0.1305,0.114,0.1055,0.0885,0.0595,0.064],[
0.211,0.1915,0.1795,0.1515,0.136,0.1325],[
0.089,0.064,0.0685,0.0505,0.042,0.0415],[
0.275,0.2465,0.2065,0.1765,0.1535,0.1245],[
0.334,0.27,0.2645,0.262,0.2405,0.213],[
0.24,0.1955,0.184,0.1905,0.1855,0.15],[
0.256,0.1975,0.186,0.19,0.1835,0.152]]
        ylabel = 'Detection Rate'
        path = base_path + 'ca-astroph-random-rate.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y =[[0.8345,0.887,0.8915,0.952,0.9725,1.001],[
1.045,1.1245,1.1565,1.219,1.2885,1.3295],[
0.9385,1.011,1.029,1.099,1.1615,1.1945],[
1.22,1.3835,1.393,1.4875,1.5455,1.558],[
0.8705,0.94,0.998,1.077,1.14,1.19],[
0.784,0.9,0.9265,0.9275,0.9965,1.0655],[
0.9775,1.099,1.126,1.1235,1.1925,1.283],[
0.9625,1.0995,1.1295,1.1285,1.199,1.288]]
        ylabel = 'Detection Error'
        path = base_path + 'ca-astroph-random-error.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.33645,0.33494,0.298733333,0.307085714,0.301375,0.292022222],[
0.4881,0.4711,0.465433333,0.466785714,0.4821625,0.474577778],[
0.40625,0.3882,0.380516667,0.374671429,0.384525,0.371411111],[
0.4585,0.4892,0.491866667,0.475742857,0.4834,0.492344444],[
0.404675,0.42152,0.423483333,0.446085714,0.4680375,0.471077778],[
0.188525,0.19358,0.176933333,0.181971429,0.1692,0.172111111],[
0.221375,0.222,0.205783333,0.205828571,0.19255,0.197311111],[
0.21655,0.2191,0.204566667,0.2048,0.191225,0.196211111]]
        ylabel = 'Detection Ranking'
        path = base_path + 'ca-astroph-random-ranking.pdf'
        self.bars(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

    def effect_of_different_priors(self, base_path):
        x = np.arange(20, 46, 5)
        methods = ['RC', 'DC', 'JC', 'GSBA-RC', 'GSBA-DC', 'GSBA-JC']
        m = len(methods)
        xlable = 'Number of  infected nodes, N'
        y = [[0.092086622, 0.075288403, 0.069216758, 0.063145112, 0.047763611, 0.043108682],
             [0.087634082, 0.069823922, 0.060716454, 0.052823315, 0.044930176, 0.042096742],
             [0.113337381, 0.087634082, 0.075490791, 0.07124064, 0.062133171, 0.049989881],
             [0.156243675, 0.126087836, 0.114754098, 0.107468124, 0.087634082, 0.081562437],
             [0.17911354, 0.148755313, 0.132564258, 0.118801862, 0.101801255, 0.094312892],
             [0.182756527, 0.150779194, 0.133171423, 0.119409027, 0.102003643, 0.093300951], ]
        ylabel = 'Detection Rate'
        path = base_path + 'power-grid-prior-full-rate.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[1.859542603, 2.085205424, 2.253187614, 2.37259664, 2.522363894, 2.649868448],
             [1.865614248, 2.082169601, 2.252985226, 2.370977535, 2.505768063, 2.611009917],
             [1.878567092, 2.082169601, 2.263711799, 2.388990083, 2.520340012, 2.654523376],
             [1.57842542, 1.793159279, 1.939688322, 2.077109897, 2.247723133, 2.346893341],
             [1.659380692, 1.864197531, 2.03339405, 2.160089051, 2.359036632, 2.439587128],
             [1.652499494, 1.866828577, 2.030965392, 2.158065169, 2.360858126, 2.44161101], ]
        ylabel = 'Detection Error'
        path = base_path + 'power-grid-prior-full-error.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.437543007, 0.43623558, 0.439141874, 0.431555209, 0.434036632, 0.434774787],
             [0.42157458, 0.41896782, 0.42340282, 0.417411166, 0.418594414, 0.416177562],
             [0.408490184, 0.402558187, 0.402158807, 0.395877064, 0.393336369, 0.392444175],
             [0.306274034, 0.301420765, 0.301369493, 0.294463238, 0.294960534, 0.292608334],
             [0.267364906, 0.2608136, 0.25804493, 0.251001821, 0.250875329, 0.246765162],
             [0.264480874, 0.258708763, 0.256068272, 0.249197675, 0.248709775, 0.245330455], ]
        ylabel = 'Detection Ranking'
        path = base_path + 'power-grid-prior-full-ranking.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        """++++++++++++++++++++++++++++++++++++++++++++++++++"""
        x = np.arange(5, 11, 1)
        y = [[0.33, 0.304, 0.27, 0.256, 0.212, 0.182],
             [0.332, 0.302, 0.266, 0.244, 0.22, 0.18],
             [0.324, 0.33, 0.286, 0.304, 0.312, 0.292],
             [0.584, 0.546, 0.514, 0.508, 0.488, 0.426],
             [0.568, 0.496, 0.498, 0.442, 0.45, 0.404],
             [0.572, 0.5, 0.514, 0.468, 0.468, 0.408], ]
        ylabel = 'Detection Rate'
        path = base_path + 'scale-free-prior-full-rate.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.71, 0.76, 0.802, 0.882, 0.918, 1.032],
             [0.706, 0.77, 0.806, 0.912, 0.902, 1.016],
             [0.74, 0.744, 0.792, 0.83, 0.84, 0.914],
             [0.458, 0.518, 0.542, 0.584, 0.616, 0.696],
             [0.532, 0.63, 0.684, 0.784, 0.762, 0.864],
             [0.514, 0.632, 0.656, 0.742, 0.74, 0.87], ]
        ylabel = 'Detection Error'
        path = base_path + 'scale-free-prior-full-error.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.4648, 0.427, 0.408857143, 0.38525, 0.362, 0.3656],
             [0.4464, 0.406333333, 0.400857143, 0.38825, 0.372, 0.3814],
             [0.4528, 0.405666667, 0.388285714, 0.37275, 0.348444444, 0.3522],
             [0.316, 0.282, 0.261428571, 0.245, 0.219555556, 0.2232],
             [0.3224, 0.298333333, 0.273714286, 0.26325, 0.236222222, 0.24],
             [0.3204, 0.297333333, 0.271428571, 0.25825, 0.233111111, 0.2356], ]
        ylabel = 'Detection Ranking'
        path = base_path + 'scale-free-prior-full-ranking.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        """++++++++++++++++++++++++++++++++++++++++++++++++++"""
        x = np.arange(20, 46, 5)
        y = [[0.335692046,0.318426267,0.307529012,0.301585055,0.294084348,0.286725163],[
0.144070195,0.102037928,0.076280781,0.050523634,0.039060289,0.027030852],[
0.269883951,0.231672799,0.20223606,0.180866119,0.161902066,0.142230399],[
0.67478064,0.643928673,0.619728276,0.578828191,0.553212567,0.521936032],[
0.523775828,0.493489952,0.466883668,0.435890178,0.417916785,0.405038211],[
0.518681008,0.490942542,0.463628644,0.433342768,0.41664308,0.404189074]]
        ylabel = 'Detection Rate'
        path = base_path + 'wiki-vote-prior-full-rate.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.691480328,0.718652703,0.735918483,0.753608831,0.773988112,0.794791962],[
1.113218228,1.239173507,1.34602321,1.440418907,1.521369941,1.580526465],[
0.821964336,0.895980753,0.960939711,1.018681008,1.077271441,1.139824512],[
0.464902349,0.514435324,0.557741296,0.632040759,0.670534956,0.714973111],[
0.674356071,0.740447212,0.799179168,0.869799038,0.909425417,0.961788848],[
0.678177187,0.742994622,0.801443532,0.870223606,0.910699123,0.957118596]]
        ylabel = 'Detection Error'
        path = base_path + 'wiki-vote-prior-full-error.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.25546278,0.233908859,0.214808001,0.200731875,0.19072672,0.183105324],[
0.515319841,0.548406453,0.576889329,0.601261575,0.623782904,0.644969651],[
0.387432777,0.406476083,0.429427304,0.455270713,0.474288848,0.495971318],[
0.086187376,0.077565808,0.071662421,0.069819255,0.069264789,0.068015851],[
0.108986697,0.099790546,0.092428531,0.089773968,0.087768893,0.083995345],[
0.109786301,0.100475517,0.092777621,0.090000404,0.087751203,0.083923012]]
        ylabel = 'Detection Ranking'
        path = base_path + 'wiki-vote-prior-full-ranking.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        """++++++++++++++++++++++++++++++++++++++++++++++++++"""
        x = np.arange(20, 46, 5)
        y = [[0.256,0.2315,0.2335,0.205,0.202,0.1945],
[0.1305,0.114,0.1055,0.0885,0.0595,0.064],
[0.211,0.1915,0.1795,0.1515,0.136,0.1325],
[0.334,0.27,0.2645,0.262,0.2405,0.213],
[0.24,0.1955,0.184,0.1905,0.1855,0.15],
[0.256,0.1975,0.186,0.19,0.1835,0.152]]
        ylabel = 'Detection Rate'
        path = base_path + 'ca_astroph-prior-random-rate.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.39861657,0.403285756,0.385807738,0.409250785,0.406263404,0.403712213],
[0.429067749,0.438988907,0.429218909,0.442128488,0.453498177,0.447967744],
[0.394796191,0.399104237,0.392371735,0.405251857,0.415963359,0.401769667],
[0.362171149,0.393264568,0.385535622,0.376849979,0.398106747,0.410303798],
[0.443243015,0.462444605,0.457480636,0.452293884,0.468731617,0.487141657],
[0.442764189,0.468590322,0.466599798,0.459260383,0.478125604,0.496472922]]
        ylabel = 'Detection Error'
        path = base_path + 'ca_astroph-prior-random-error.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)

        y = [[0.33645,0.33494,0.298733333,0.307085714,0.301375,0.292022222],
[0.4881,0.4711,0.465433333,0.466785714,0.4821625,0.474577778],
[0.40625,0.3882,0.380516667,0.374671429,0.384525,0.371411111],
[0.188525,0.19358,0.176933333,0.181971429,0.1692,0.172111111],
[0.221375,0.222,0.205783333,0.205828571,0.19255,0.197311111],
[0.21655,0.2191,0.204566667,0.2048,0.191225,0.196211111]]
        ylabel = 'Detection Ranking'
        path = base_path + 'ca_astroph-prior-random-ranking.pdf'
        self.lines(x, y[0:m], methods[0:m], xlable, ylabel, path=path)


    def graph(self):
        g = nx.read_weighted_edgelist("../data/test.txt", comments='#')
        nx.draw(g)
        nx.draw_networkx_edge_labels(g, pos=nx.spring_layout(g))
        plt.show()

    def running_time_scale_free(self, base_path):
        d = 0

    def f(self, t):
        return np.exp(-t) * np.cos(2 * np.pi * t)

    def test_subplot(self,base_path):
        # t1 = np.arange(0, 5, 0.1)
        # t2 = np.arange(0, 5, 0.02)
        #
        # plt.figure(12)
        # plt.subplot(331)
        # plt.plot(t1, self.f(t1), 'bo', t2, self.f(t2), 'r--')
        #
        # plt.subplot(332)
        # plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')
        #
        # plt.subplot(333)
        # plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')
        #
        # plt.subplot(312)
        # plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        #
        # plt.subplot(313)
        # plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        #
        # plt.show()

        x = np.arange(5, 11, 1)
        methods = ['RC', 'DC', 'JC', 'RI', 'DI', 'DMP', 'GSBA-JC', 'BFSA-JC']
        m = len(methods)
        xlabel = 'Number of  infected nodes, N'
        y = [[0.35, 0.27, 0.26, 0.27, 0.17, 0.17], [
            0.36, 0.32, 0.26, 0.26, 0.15, 0.16], [
                 0.29, 0.28, 0.27, 0.23, 0.29, 0.29], [
                 0.35, 0.28, 0.27, 0.25, 0.16, 0.15], [
                 0.25, 0.23, 0.24, 0.22, 0.14, 0.18], [
                 0.57, 0.61, 0.62, 0.51, 0.63, 0.53], [
                 0.53, 0.46, 0.55, 0.53, 0.52, 0.37], [
                 0.6, 0.58, 0.67, 0.59, 0.65, 0.51]]
        ylabel = 'Detection Rate'
        path = base_path + '111scale-free-random-rate.pdf'

        y = y[0:m]
        legend = methods[0:m]
        n = len(legend)
        width = 5
        fig,ax = plt.subplots(1,3, figsize=(20,6)) #
        axis = ax[0]
        for i in np.arange(0, n):
            axis.plot(x, y[i], '-D', label=legend[i], color=self.colors[legend[i]], linewidth=width,
                    markersize=22, marker=self.markers[legend[i]], markeredgewidth=2)
        axis.set_xlabel(xlabel, fontsize=30)
        axis.set_ylabel(ylabel, fontsize=30)
        # ax[0].set_xticklabels(fontdict={'fontsize':38})
        # ax[0].set_yticklabels(fontdict={'fontsize':38})  # change the num axis size
        # plt.xlim(0, 50)  # The ceil
        y_min = np.min(y)
        y_max = np.max(y)
        x_max = np.max(x)
        x_min = np.min(x)
        axis.set_xlim(x_min*0.99, x_max*1.01)
        axis.set_ylim(0, 1.3 * y_max)  # The ceil
        for tick in axis.xaxis.get_major_ticks():
            tick.label1.set_fontsize(30)
        for tick in axis.yaxis.get_major_ticks():
            tick.label1.set_fontsize(30)



        axis = ax[1]
        for i in np.arange(0, n):
            axis.plot(x, y[i], '-D', label=legend[i], color=self.colors[legend[i]], linewidth=width,
                    markersize=22, marker=self.markers[legend[i]], markeredgewidth=2)
        axis.set_xlabel(xlabel, fontsize=30)
        axis.set_ylabel(ylabel, fontsize=30)
        # ax[0].set_xticklabels(fontdict={'fontsize':38})
        # ax[0].set_yticklabels(fontdict={'fontsize':38})  # change the num axis size
        # plt.xlim(0, 50)  # The ceil
        y_min = np.min(y)
        y_max = np.max(y)
        x_max = np.max(x)
        x_min = np.min(x)
        axis.set_xlim(x_min*0.99, x_max*1.01)
        axis.set_ylim(0, 1.3 * y_max)  # The ceil
        for tick in axis.xaxis.get_major_ticks():
            tick.label1.set_fontsize(30)
        for tick in axis.yaxis.get_major_ticks():
            tick.label1.set_fontsize(30)

        my_legends = ()

        axis = ax[2]
        for i in np.arange(0, n):
            l = axis.plot(x, y[i], '-D', label=legend[i], color=self.colors[legend[i]], linewidth=width,
                      markersize=22, marker=self.markers[legend[i]], markeredgewidth=2)
            my_legends.(my_legends)
        axis.set_xlabel(xlabel, fontsize=30)
        axis.set_ylabel(ylabel, fontsize=30)
        # ax[0].set_xticklabels(fontdict={'fontsize':38})
        # ax[0].set_yticklabels(fontdict={'fontsize':38})  # change the num axis size
        # plt.xlim(0, 50)  # The ceil
        y_min = np.min(y)
        y_max = np.max(y)
        x_max = np.max(x)
        x_min = np.min(x)
        axis.set_xlim(x_min * 0.99, x_max * 1.01)
        axis.set_ylim(0, 1.3 * y_max)  # The ceil
        for tick in axis.xaxis.get_major_ticks():
            tick.label1.set_fontsize(30)
        for tick in axis.yaxis.get_major_ticks():
            tick.label1.set_fontsize(30)

        print tuple(legend)
        fig.legend(my_legends,tuple(legend),fontsize=28)

        plt.tight_layout()  # tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        plt.show()
        if path is not None:
            plt.savefig(path)
            fig.savefig(path)
        plt.close()

if __name__ == '__main__':
    base_path = '../data/fig1204/'
    fig = Fig()
    fig.debug = False
    fig.test_subplot(base_path)

    # if fig.debug == 1:
    #     fig.test(base_path)
    # fig.effect_of_different_priors(base_path)
    # fig.results_on_scale_free(base_path)
    # fig.results_on_power_grid(base_path)
    # fig.results_on_wiki_vote(base_path)
    # fig.results_on_ca_astroph(base_path)

    # fig.wang_result_recall()
    # fig.wang_parameter_lines()