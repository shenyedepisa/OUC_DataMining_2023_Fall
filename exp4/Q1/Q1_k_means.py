import numpy as np
import matplotlib.pyplot as plt

plt.ion()
# plt中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # font.sans-serif参数来指定"SimHei"字体
plt.rcParams['axes.unicode_minus'] = False  # axes.unicode_minus参数用于显示负号
name = 'K-Means'


class K_Mean():
    def __init__(self, x):
        self.x = x
        self.nodes_data = 0

    def fit(self, k):  # k 簇中心数量
        nodes = np.array([[2, 10], [5, 8], [1, 2]], dtype=float)
        self.nodes_data = nodes.copy()
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


# 绘图
def plot_figure(x, y, nodes_data, epoch):
    map_color = {0: 'r', 1: 'g', 2: 'b', 4: 'pink', 5: 'teal', 6: 'yellow', 7: 'plum', 8: 'silver', 9: 'cyan'}
    color_initial = [map_color[i] for i in y.squeeze()]
    plt.cla()
    plt.scatter(x[:, 0], x[:, 1], c=color_initial)
    plt.scatter(nodes_data[:, 0], nodes_data[:, 1], c='gold', s=200, marker='*')
    plt.title(f'{name} 算法第 {epoch} 轮执行后的簇中心', fontsize=14)
    plt.show()


if __name__ == '__main__':
    # 数据集
    data = np.array([[2, 10], [2, 5], [8, 4], [5, 8], [7, 5], [6, 4], [1, 2], [4, 9]])
    # 初始化并训练模型
    model = K_Mean(data)
    model.fit(3)
