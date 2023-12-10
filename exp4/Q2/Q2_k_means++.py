import numpy as np
import matplotlib.pyplot as plt
import time

plt.ion()
# plt中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # font.sans-serif参数来指定"SimHei"字体
plt.rcParams['axes.unicode_minus'] = False  # axes.unicode_minus参数用于显示负号
name = 'K-Means++'

datasetPath = './datasets/flame.txt'


class K_Mean():
    def __init__(self, x):
        self.x = x
        self.nodes_data = 0

    def fit(self, k):
        # 随机选取1个聚类中心
        nodes = self.x[np.random.choice(self.x.shape[0], 1, replace=False)]
        nodes = np.array(nodes, dtype=float)
        # 计算距离
        dis = np.empty(shape=(self.x.shape[0]), dtype=np.float64)
        # 循环选取其余的k均值点：
        for j in range(1, k):
            # 循环每一个样本点，计算它们与初始中心点的距离
            for i in range(self.x.shape[0]):
                result = nodes - self.x[i, :]
                L2 = np.linalg.norm(result, ord=2, axis=1)
                dis[i] = np.min(L2)
            # 计算概率
            p = dis / dis.sum()
            # 依据概率选取下一个聚类中心点
            new_node = self.x[np.random.choice(self.x.shape[0], 1, p=p)]
            nodes = np.insert(nodes, j, new_node, axis=0)

        self.nodes_data = nodes.copy()  # 为了将数据保存到模型中，预测的时候好调用。
        distances = np.empty((self.x.shape[0], self.nodes_data.shape[0]), dtype=np.float64)
        epoch = 0
        while True:  # 循环迭代
            for j, each_k in enumerate(nodes):
                # 求每一个点到不同簇中心的距离, 结果按列保存到distances中
                result = self.x - each_k
                distance = np.linalg.norm(result, ord=2, axis=1).reshape(-1)
                distances[:, j] = distance
            # 计算各点和哪个簇中心最近
            a = np.argmin(distances, axis=1)
            # 对每一个簇重新计算均值点并更新
            for each in range(k):
                mean = np.mean(self.x[a == each], axis=0)
                nodes[each, :] = mean
            plot_figure(self.x, a, self.nodes_data, epoch)
            # 簇中心不再变化, 结束迭代
            if (self.nodes_data == nodes).all():
                break
            else:
                self.nodes_data = nodes.copy()

            epoch += 1
            time.sleep(1)


# 绘图
def plot_figure(x, y, nodes_data, epoch):
    map_color = {0: 'r', 1: 'g', 2: 'b', 3: 'm', 4: 'pink', 5: 'teal', 6: 'yellow', 7: 'plum', 8: 'silver', 9: 'cyan',
                 10: 'olive', 11: 'peru', 12: 'brown', 13: 'gray', 14: 'lightblue', 15: 'mistyrose', 16: 'khaki',
                 17: 'olivedrab', 18: 'palegreen', 19: 'lime', 20: 'black', 21: 'tomato', 22: 'thistle', 23: 'beige',
                 24: 'royalblue', 25: 'cornsilk', 26: 'fuchsia', 27: 'slategray', 28: 'honeydew', 29: 'peachpuff',
                 30: 'bisque'}
    color_initial = [map_color[i] for i in y.squeeze()]
    plt.cla()
    plt.scatter(x[:, 0], x[:, 1], c=color_initial, s=10)
    plt.scatter(nodes_data[:, 0], nodes_data[:, 1], c='gold', s=200, marker='*')
    plt.title(f'{name} 算法第 {epoch} 轮执行后的簇中心', fontsize=14)
    plt.show()


def readfile(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            point = []
            i = 0
            # 由于十个数据集的数据格式不同, 使用遍历来分词
            while i < len(line):
                if line[i] == ' ' or line[i] == '\t':
                    i += 1
                    continue
                else:
                    tmp = ''
                    while line[i] != ' ' and line[i] != '\t':
                        tmp += line[i]
                        i += 1
                        if i == len(line):
                            break
                    tmp = float(tmp)
                    point.append(tmp)
            data.append(point)
    dataset = np.array(data)
    if dataset.shape[-1] > 2:
        data = dataset[:, 0:2]
        labels = dataset[:, 2]
        dataset = data.copy()

    return dataset


if __name__ == '__main__':
    # 读取数据集
    dataset = readfile(datasetPath)
    # 初始化并训练模型
    model = K_Mean(dataset)
    model.fit(3)
