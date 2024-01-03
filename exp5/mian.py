import time
import pandas as pd
from plotTree import PlotTree
import random
from decisionTreeCART import DecisionTreeCART


def test_decision_treeCART(Y_test, tree):
    Y_test["Predict classification"] = None
    nums = Y_test.shape[0]
    for i in range(nums):
        row = Y_test.loc[i].copy()
        find_categoryCART(row, tree)
        Y_test.loc[i, "Predict classification"] = row["Predict classification"]
    print(" ")


def find_categoryCART(row, treeNode):
    childNodes = treeNode.children
    if treeNode.feature is None:
        row["Predict classification"] = treeNode.category
        return
    else:
        node = childNodes.get(row[treeNode.feature])
        if node is None:
            node = childNodes.get(list(childNodes.keys())[1])
        find_categoryCART(row, node)
        return


if __name__ == "__main__":
    # 数据预处理
    t1 = time.time()
    splitToken = ","  # statlog是' ', 其余是','
    keyWord = "iris"  # iris, statlog, page-blocks
    txtOutputPath = f"./output/benchmark/{keyWord}_CART.txt"
    csvOutputPath = f"./output/data/{keyWord}_CART.csv"
    pntOutputPath = f"./output/images/{keyWord}_CART.png"
    namePath = f"./data/{keyWord}/{keyWord}.names"
    dataPath = f"./data/{keyWord}/{keyWord}.data"
    namelist = []
    with open(namePath, "r") as f:
        lines = f.readline()
        for line in f:
            namelist.append(line.split(" : ")[0])
    namelist.append("classification")
    datalist = []
    with open(dataPath, "r") as f:
        for line in f:
            line = line.strip("\n")
            datalist.append(line.split(splitToken))
    index = list(range(len(datalist)))
    random.shuffle(index)
    test_index = index[: int(0.2 * len(index))]
    train_index = index[int(0.2 * len(index)) :]
    trainDataList = [datalist[i] for i in train_index]
    testDataList = [datalist[i] for i in test_index]
    data_train = pd.DataFrame(columns=namelist, data=trainDataList)
    data_test = pd.DataFrame(columns=namelist, data=testDataList)

    Y_data_train = data_train["classification"]
    X_data_train = data_train.drop("classification", axis=1)

    # CART算法
    tree = DecisionTreeCART(X_data_train, Y_data_train).root_node

    # 测试集
    Y_data_test = data_test["classification"]
    test_decision_treeCART(data_test, tree)
    Y_data_predict = data_test["Predict classification"]
    count = 0
    measure = {}
    for i in range(len(Y_data_test)):
        y = Y_data_test.loc[i]
        predict = Y_data_predict.loc[i]
        try:
            _ = measure[y]
        except:
            measure[y] = {"TP": 0, "FN": 0, "FP": 0, "TN": 0}
        try:
            _ = measure[predict]
        except:
            measure[predict] = {"TP": 0, "FN": 0, "FP": 0, "TN": 0}

    for i in range(len(Y_data_test)):
        y = Y_data_test.loc[i]
        predict = Y_data_predict.loc[i]
        if y == predict:
            measure[y]["TP"] += 1
        else:
            measure[y]["FN"] += 1
            measure[predict]["FP"] += 1
        for key in measure.keys():
            if key != y:
                measure[key]["TN"] += 1
    allTP, allFN, allFP, allTN = 0, 0, 0, 0
    with open(txtOutputPath, "w") as f:
        for key in measure.keys():
            TP = measure[key]["TP"]
            FN = measure[key]["FN"]
            FP = measure[key]["FP"]
            TN = measure[key]["TN"]
            recall = TP / (TP + FN)
            precision = TP / (TP + FP)
            acc = (TP + TN) / (TP + FN + FP + TN)
            F1 = 2 * (precision * recall) / (precision + recall)
            allTP += TP
            allFN += FN
            allFP += FP
            allTN += TN
            f.write(
                f"{key}:\n"
                f"\tAccuracy: {acc:.3f}"
                f"    Precision: {precision:.3f}"
                f"    Recall: {recall:.3f}"
                f"    F1-measure: {F1:.3f}"
                f"    sample size: {TP + FN}\n"
            )
            print(
                f"{key}:\n"
                f"\tAccuracy: {acc:.3f}"
                f"    Precision: {precision:.3f}"
                f"    Recall: {recall:.3f}"
                f"    F1-measure: {F1:.3f}"
                f"    sample size: {TP + FN}\n"
            )
        recall = allTP / (allTP + allFN)
        precision = allTP / (allTP + allFP)
        acc = (allTP + allTN) / (allTP + allFN + allFP + allTN)
        F1 = 2 * (precision * recall) / (precision + recall)
        f.write(
            f"\nAverage:\n"
            f"\tAccuracy: {acc:.3f}"
            f"    Precision: {precision:.3f}"
            f"    Recall: {recall:.3f}"
            f"    F1-measure: {F1:.3f}"
            f"    testData size: {allTP + allFN}\n"
        )
        print(
            f"\nAverage:\n"
            f"\tAccuracy: {acc:.3f}"
            f"    Precision: {precision:.3f}"
            f"    Recall: {recall:.3f}"
            f"    F1-measure: {F1:.3f}"
            f"    testData size: {allTP + allFN}\n"
        )

    # 保存预测结果
    data_test.to_csv(csvOutputPath, index=False)
    t2 = time.time()
    # print(f"\nused time : {t2-t1:.3f}s\n\nPlotting...")
    pt = PlotTree()
    pt.createPlot(tree, pntOutputPath)
    t3 = time.time()
    # print(f"\nPlotting time : {t3-t2:.3f}s")
