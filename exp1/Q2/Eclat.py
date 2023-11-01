import numpy as np
import time

min_support = 0.05
fileName = "TDB2.dat"


# 读取数据集
def readfile(path):
    dataset = []
    with open(path, "r") as file:
        line = file.readline()
        while line:
            dataset.append(line[:-2].split(" "))
            line = file.readline()
    return dataset


# eclat算法
def eclat(transactions, min_support):
    items_vert = {}
    minNum = len(transactions) * min_support
    n = 0
    for transaction in transactions:  # 找出频繁一项集候选集
        n += 1
        goods = list(np.unique(transaction))
        for combo in goods:
            if tuple([combo]) not in items_vert:
                items_vert[tuple([combo])] = {n}
            else:
                items_vert[tuple([combo])].add(n)
    res = {}
    for key in items_vert:  # 删除小于最小支持度的项
        if len(items_vert[key]) >= minNum:
            res[key] = items_vert[key]
    items_vert = res.copy()
    k_1 = [key for key in items_vert.keys()]
    k = 1
    if len(items_vert) != 0:
        print('频繁 {} 项集:'.format(k))
        for key, support in items_vert.items():
            print("frequent item: {}\t\t support: {:.7f}".format(key, len(support) / len(transactions)))
    while True:
        k += 1
        candidate = {}
        len_k_1 = len(k_1)  # k-1项集的长度
        for i in range(len_k_1):
            for j in range(i + 1, len_k_1):
                k1 = tuple(sorted(list(k_1[i])))
                k2 = tuple(sorted(list(k_1[j])))
                if k1[: k - 2] == k2[: k - 2]:  # 如果前k减2个元素相等 , 就将两几何求并
                    value = items_vert[k1] & items_vert[k2]
                    key = tuple(sorted(list(set(k1) | (set(k2)))))
                    candidate[key] = value  # set union
        temp = {}
        for key in candidate:
            if len(candidate[key]) >= minNum:
                temp[key] = candidate[key]
        candidate = temp.copy()
        if len(candidate) != 0:
            k_1 = [key for key in candidate.keys()]
            print('频繁 {} 项集:'.format(k))
            for key, support in candidate.items():
                print("frequent item: {}\t\t support: {:.7f}".format(key, len(support) / len(transactions)))
                items_vert[key] = support
        else:
            break

    print("The number of frequent items: {}".format(len(items_vert)))


if __name__ == "__main__":
    T1 = time.process_time()
    data = readfile(fileName)
    eclat(data, min_support)
    T2 = time.process_time()
    print("Time used: {}s".format(T2 - T1))
