---
title: 信息检索_系统评价
categories: 笔记
date: 2022-11-11 10:00:00
tags:
  - 信息检索
abbrlink: 23422
---
# 信息检索_系统评价

## 总思路

![image-20221102140305383](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B3%BB%E7%BB%9F%E8%AF%84%E4%BB%B7/20230828210413749537_765_20221102181425241957_651_image-20221102140305383.png)

## 单查询

### 无序检索结果集合的评价


<details>
<summary>回顾</summary>

查准率 (Precision) : $P=\frac{T P}{T P+F P}$ 。预测正确的正例数据占预测为正例数据的比例。

召回率 (Recall) : $R=\frac{TP }{TP+FN}$ 。预测为正例的数据占实际为正例数据的比例。

F1值 (F1 score) :
$$
F1=\frac{2}{\frac{1}{P}+\frac{1}{R}}=\frac{2 * P * R}{P+R}\nonumber
$$
</details>

### 有序检索结果集合的评价

#### P-R曲线的例子

![image-20221102141151261](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B3%BB%E7%BB%9F%E8%AF%84%E4%BB%B7/20230828210415422791_840_20221102181427482098_652_image-20221102141151261.png)

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B3%BB%E7%BB%9F%E8%AF%84%E4%BB%B7/20230828210416775229_758_20221102181431710114_302_image-20221102141322869.png" alt="image-20221102141322869" width="50%" height="50%" />

![image-20221102142019252](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B3%BB%E7%BB%9F%E8%AF%84%E4%BB%B7/20230828210417972832_913_20221102181432975281_362_image-20221102142019252.png)

#### 平均正确率AP

![image-20221102142247895](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B3%BB%E7%BB%9F%E8%AF%84%E4%BB%B7/20230828210419282313_192_20221102181435795246_414_image-20221102142247895.png)

#### Precision@N

Precision@N：在第N个位置上的正确率，对于搜索引擎，大量统计数据表明，大部分搜索引擎用户只关注前一、两页的结果，因此， P@10，P@20对大规模搜索引擎来说是很好的评价指标

![image-20221102142715051](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B3%BB%E7%BB%9F%E8%AF%84%E4%BB%B7/20230828210420576008_695_20221102181437971719_189_image-20221102142715051.png)

