database = [
    ['M', 'O', 'N', 'K', 'E', 'Y'],
    ['D', 'O', 'N', 'E', 'K', 'Y'],
    ['M', 'A', 'K', 'E'],
    ['M', 'U', 'C', 'K', 'Y'],
    ['C', 'O', 'K', 'I', 'E']
]
min_support = 0.6
min_confidence = 0.8
SIZE = len(database)


def apriori():
    # 找出所有单项集及其支持度
    originalItems = {}
    for transaction in database:
        for item in transaction:
            if tuple([item]) not in originalItems:
                originalItems[tuple([item])] = 1
            else:
                originalItems[tuple([item])] += 1

    # 删除不满足最小支持度的单项集
    minNum = SIZE * min_support
    newItems = {}
    for item, value in originalItems.items():
        if value >= minNum:
            newItems[item] = value
    frequent_itemSets = newItems
    num = 1
    if len(frequent_itemSets) != 0:
        print('频繁 {} 项集:'.format(num))
        for key, support in frequent_itemSets.items():
            print('frequent item: {}\t\t support: {}'.format(key, support / SIZE))

    # 找出所有频繁项集及其支持度
    lastItems = newItems
    alternative = {key: 0 for key, _ in newItems.items()}
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
                print('frequent item: {}\t\t support: {}'.format(key, support / SIZE))
        else:
            break

    print('The number of frequent items: {}'.format(len(frequent_itemSets)))

    return frequent_itemSets, num


# 找出所有强关联规则
def rule(dataDict, num):
    rules = []
    frequent_itemSets = dataDict
    M = num
    for n in range(2, M):
        pre = [key for key, value in frequent_itemSets.items() if len(key) == n]
        after = [key for key, value in frequent_itemSets.items() if len(key) == n + 1]
        for i in after:
            for j in pre:
                temp = []
                if all(elem in i for elem in j):
                    if frequent_itemSets[i] / frequent_itemSets[j] >= min_confidence:
                        temp.append(j)
                        temp.append(tuple([elem for elem in i if elem not in j]))
                        temp.append(frequent_itemSets[i] / frequent_itemSets[j])
                        rules.append(temp)

    print('\nstrong association rules:')
    for i in rules:
        print('{} => {},\t confidence: {}'.format(i[0], i[1][0], i[2]))

    return rules


if __name__ == "__main__":
    frequent, maxNum = apriori()
    rules = rule(frequent, maxNum)
