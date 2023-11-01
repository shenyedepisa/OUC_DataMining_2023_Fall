import time

min_support = 0.05
fileName = 'TDB1.dat'


def apriori(database):
    size = len(database)
    # 找出所有单项集及其支持度
    originalItems = {}
    for transaction in database:
        for item in transaction:
            if tuple([item]) not in originalItems:
                originalItems[tuple([item])] = 1
            else:
                originalItems[tuple([item])] += 1

    # 删除不满足最小支持度的单项集
    minNum = size * min_support
    newItems = {}
    for item, value in originalItems.items():
        if value >= minNum:
            newItems[item] = value

    # 找出所有频繁项集及其支持度
    frequent_itemSets = newItems
    lastItems = newItems
    alternative = {key: 0 for key, _ in newItems.items()}
    num = 1
    if len(frequent_itemSets) != 0:
        print('频繁 {} 项集:'.format(num))
        for key, support in frequent_itemSets.items():
            print('frequent item: {}\t\t support: {:.7f}'.format(key, support / size))
    while True:
        num += 1
        searchSpace = {}  # 搜索空间 剪枝
        newItems = {}  # 频繁n项集
        for i, _ in alternative.items():
            for item in lastItems.keys():
                newFlag = 0
                tempKey = [key for key in item]
                it = [key for key in i]
                if it[0] not in tempKey:
                    tempKey.append(it[0])
                    tempKey = tuple(sorted(list(tempKey)))
                    if tempKey in searchSpace.keys():
                        continue
                    searchSpace[tempKey] = 1
                    for transaction in database:
                        if set(tempKey).issubset(transaction):
                            newFlag = 1
                            try:
                                newItems[tempKey] += 1
                            except KeyError:
                                newItems[tempKey] = 1
                # 删除小于最小支持度的项
                if newFlag == 1:
                    if newItems[tempKey] >= minNum:
                        alternative[tuple(it)] += 1
                    else:
                        newItems.pop(tempKey)

        for key, value in newItems.items():
            frequent_itemSets[key] = value
        temp = {key: 0 for key, value in alternative.items() if value != 0}
        alternative = temp
        lastItems = newItems
        if len(alternative) != 0:
            print('频繁 {} 项集:'.format(num))
            for key, support in newItems.items():
                print('frequent item: {}\t\t support: {:.7f}'.format(key, support / size))
        else:
            break

    print('The number of frequent items: {}'.format(len(frequent_itemSets)))

    return frequent_itemSets


def readfile(path):
    database = []
    with open(path, 'r') as file:
        line = file.readline()
        while line:
            database.append(line[:-2].split(' '))
            line = file.readline()
    return database


if __name__ == "__main__":
    T1 = time.process_time()
    data = readfile(fileName)
    frequent = apriori(data)
    T2 = time.process_time()
    print('Time used: {}s'.format(T2 - T1))
