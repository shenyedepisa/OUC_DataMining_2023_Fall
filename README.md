# OUC-DeepLearning-2023-Fall

中国海洋大学数据挖掘秋季课程

**仅供参考, 请勿抄袭**

理论上会在DDL之后一天更新

(咕咕)

### exp1 频繁项挖掘

实现了Apriori算法和Eclat算法

两种算法的实现细节在效率和空间上都没有达到最优

请尽情优化

### exp2 频繁项挖掘

DBLP合作关系挖掘

数据源: [AMiner](https://www.aminer.cn/citation), 下载数据集: [DBLP-Citation-network V14](https://originalfileserver.aminer.cn/misc/dblp_v14.tar.gz)

分析结果保存在 measures.csv

### exp3 频繁序列挖掘

PrefixSpan算法的实现

数据集下载: [SPMF](http://www.philippe-fournier-viger.com/spmf/index.php?link=datasets.php)

数据集很大的时候, PrefixSpan的第一遍扫描开销很大

### exp4 K-Means & K-Means++

实现了两个很经典的聚类算法

但其实本次实验给的十个数据集大部分都是用来测试密度聚类算法的

有兴趣的话建议用 [DBSCAN](https://www.naftaliharris.com/blog/visualizing-dbscan-clustering/) 跑一下