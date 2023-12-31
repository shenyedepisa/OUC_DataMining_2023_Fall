import pandas as pd
import numpy as np


class TreeNode:
    def __init__(self, parent, children, feature, category, X_data, Y_data):
        self.parent = parent
        self.children = children
        self.feature = feature
        self.category = category
        self.X_data = X_data
        self.Y_data = Y_data

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children


class DecisionTreeCART:
    def __init__(self, X, Y):
        self.X_train = X
        self.Y_train = Y
        self.root_node = TreeNode(None, None, None, None, self.X_train, self.Y_train)
        self.features = self.get_features(self.X_train)
        self.tree_generate(self.root_node)

    def get_features(self, X_train_data):
        features = dict()
        for i in range(len(X_train_data.columns)):
            feature = X_train_data.columns[i]
            features[feature] = list(X_train_data[feature].value_counts().keys())

        return features

    def tree_generate(self, tree_node):
        X_data = tree_node.X_data.copy()
        Y_data = tree_node.Y_data.copy()
        features = list(X_data.columns)

        # 如果Y_data中的实例属于同一类，则置为单结点，并将该类作为该结点的类
        if len(list(Y_data.value_counts())) == 1:
            tree_node.category = Y_data.iloc[0]
            tree_node.children = None
            return

        # 如果特征集为空，则置为单结点，并将Y_data中最大的类作为该结点的类
        elif len(features) == 0:
            tree_node.category = Y_data.value_counts(ascending=False).keys()[0]
            tree_node.children = None
            return

        # 否则，计算各特征的基尼指数，选择基尼指数最小的特征
        else:
            # gini_d = self.compute_gini(Y_data)
            XY_data = pd.concat([X_data, Y_data], axis=1)
            d_nums = XY_data.shape[0]
            min_gini_index = 1
            feature = None
            feature_value = None

            for i in range(len(features)):
                # 当前特征有哪些取值
                v = XY_data[features[i]].value_counts().keys()
                # 当前特征的取值只有一种
                if len(v) <= 1:
                    continue
                # 当前特征的每一个取值分为是和不是两类
                for j in v:
                    Gini_index = 0
                    dv = XY_data[XY_data[features[i]] == j]
                    dv_nums = dv.shape[0]
                    dv_not = XY_data[XY_data[features[i]] != j]
                    dv_not_nums = dv_not.shape[0]
                    gini_dv = self.compute_gini(dv[dv.columns[-1]])
                    gini_dv_not = self.compute_gini(dv_not[dv_not.columns[-1]])
                    if d_nums == 0:
                        continue
                    Gini_index += (
                        dv_nums / d_nums * gini_dv + dv_not_nums / d_nums * gini_dv_not
                    )

                    if Gini_index < min_gini_index:
                        min_gini_index = Gini_index
                        feature = features[i]
                        feature_value = j

            if feature is None:
                tree_node.category = Y_data.value_counts(ascending=False).keys()[0]
                tree_node.children = None
                return
            tree_node.feature = feature

            # 否则，对当前特征的最小基尼指数取值，将Y_data分成两类子集，构建子结点
            tree_node.children = dict()
            for i in range(2):
                # 左分支，左分支为是的分支
                if i == 0:
                    X_data = XY_data[XY_data[feature] == feature_value].copy()
                    X_data.drop(feature, axis=1, inplace=True)
                    child_name = feature_value
                # 右分支，右分支为否的分支
                else:
                    X_data = XY_data[XY_data[feature] != feature_value].copy()
                    child_name = "!" + str(feature_value)

                Y_data = X_data[X_data.columns[-1]]
                X_data.drop(X_data.columns[-1], axis=1, inplace=True)
                childNode = TreeNode(tree_node, None, None, None, X_data, Y_data)
                tree_node.children[child_name] = childNode
                self.tree_generate(childNode)

            return

    def compute_gini(self, Y):
        gini = 1
        for cate in Y.value_counts(1):
            gini -= cate * cate
        return gini
