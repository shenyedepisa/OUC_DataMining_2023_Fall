from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
import ijson
import warnings
import math
import csv

warnings.filterwarnings('ignore', category=DeprecationWarning)
# AI:14363, CV: 4928
num = 4928
minNum = 100
secondNum = 20
themeName = 'CV'


def readfile(path):
    data, id_name = [], {}
    with open(path, 'r', encoding='utf-8') as file:
        objects = ijson.items(file, 'item')
        for obj in objects:
            temp = []
            for i in range(len(obj['authors'])):
                if obj['authors'][i]['id'] != '':
                    temp.append(obj['authors'][i]['id'])
                    id_name[obj['authors'][i]['id']] = obj['authors'][i]['name']
            data.append(temp)
    return id_name, data


def getYear(path, idList):
    years = []
    yearsCount = {}
    idSet = set(idList)
    with open(path, 'r', encoding='utf-8') as file:
        objects = ijson.items(file, 'item')
        for obj in objects:
            temp = set([obj['authors'][i]['id'] for i in range(len(obj['authors'])) if obj['authors'][i]['id'] != ''])
            if idSet & temp == idSet:
                years.append(obj['year'])
    years.sort()
    for i in range(len(years)):
        try:
            yearsCount[years[i]] += 1
        except KeyError:
            yearsCount[years[i]] = 1

    return yearsCount


def writeCsv(data):
    header = ['Author A', 'Author B', 'S(A and B)', 'S(A)', 'S(B)', 'A => B confidence', 'B => A confidence', 'Jaccard',
              'Cosine',
              'Kulc', 'IR', 'years']
    with open(f'{themeName}_measures.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def miningAndMeasures(idDic, dataset):
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # 使用fpgrowth找到频繁项集, 生成关联规则
    frequent_itemsets = fpgrowth(df, min_support=20 / num, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)

    print(f"{'Author A':30s}{'Author B':30s}{'S(A ∪ B)':15s}{'S(A)':10s}{'S(B)':10s}"
          f"{'A => B 置信度':15s}{'B => A 置信度':15s}{'Jaccard':10s}{'Cosine':10s}{'Kulc':10s}{'IR':10s}{'years':15s}")

    data = []
    for index, row in rules.iterrows():
        if len(row['antecedents']) == 1 and len(row['consequents']) == 1:
            name_A = idDic[list(row['antecedents'])[0]]
            name_B = idDic[list(row['consequents'])[0]]
            S_a_b = round(row['support'] * num)
            S_a = round(row['antecedent support'] * num)
            S_b = round(row['consequent support'] * num)
            conf_a_b = S_a_b / S_a
            conf_b_a = S_a_b / S_b
            Jaccard = S_a_b / (S_a + S_b - S_a_b)
            Cosine = S_a_b / math.sqrt(S_a * S_b)
            kulc = 0.5 * ((S_a_b / S_a) + (S_a_b / S_b))
            ir = abs(S_a - S_b) / (S_a + S_b - S_a_b)
            years = getYear(f'{themeName}_namelist2013-2022_{minNum}_{secondNum}.json', [list(row['antecedents'])[0], list(row['consequents'])[0]])
            data.append([name_A, name_B, S_a_b, S_a, S_b, conf_a_b, conf_b_a, Jaccard, Cosine, kulc, ir, years])
            print(f"{name_A:30s}{name_B:30s}{S_a_b:d}{S_a:15d}{S_b:10d}{conf_a_b:15.4f}{conf_b_a:17.4f}{'':6s}"
                  f"{Jaccard:10.4f}{Cosine:10.4f}{kulc:10.4f}{ir:10.4f}{'':5s}{years}")
    writeCsv(data)


if __name__ == "__main__":
    dic, dataset = readfile(f'{themeName}_namelist2013-2022_{minNum}_{secondNum}.json')
    miningAndMeasures(dic, dataset)
