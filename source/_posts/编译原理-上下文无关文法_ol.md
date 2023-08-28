---
title: 编译原理-上下文无关文法
categories: 笔记
date: 2022-11-19 10:00:00
tags:
  - 编译原理
abbrlink: 44201
---
# 编译原理-上下文无关文法

## CFG基本概念

<font color='Apricot'>符号串集合！</font>

CFG可以表示所有正则表达式的所能表达文法集合，反过来不成立

### CFG设计

可以结合正则表达式设计，思路类似。

- 最基本的一个例子：$L=\{abb^{2n}|n≥0\}$

  S→b|aSbb

- 设计接受语言${\{a^ib^ja^kb^l| i+j=k+l, i, j, k, l>=0\}}$的上下文无关文法。

  S→aSb | A | B | M

  A→aAa | M

  B→bBb | M

  M→bMa | e

   思路：两边对称，先构造中间，再对称的加a或b。特别注意，A，B只涵盖了“一边的情况，所以”S→aSb“是必须的。

- 设计接受C++数组声明语句的上下文无关文法，其中数组元素类型限定为int、char及它们的指针，数组维数可以是任意维。

  D→T id M ;

  T→int | char | T*

  M→M [num] | [num]

  注意：指针也可以套任意个

- 形如xy(x≠y)的01串

  $S \rightarrow A B \mid B A$
  $A \rightarrow X A X \mid 0$ ( $A$ 是奇数长度, 中间为 0 的串)
  $B \rightarrow X B X \mid 1$ ( $B$ 是奇数长度, 中间为 1 的串)
  $X \rightarrow 0 \mid 1$
  
- 接受语言 $\left\{a^i b^j a^k \mid j=i+k, i>=0, k>=0\right\}$ 的上下文无关文法。 答:
$$
\begin{aligned}
&\mathbf{S} \rightarrow \mathbf{A B} \\
&\mathbf{A} \rightarrow \mathbf{a A b} \mid \varepsilon \\
&\mathbf{B} \rightarrow \mathbf{b B a} \mid \varepsilon
\end{aligned}
$$

练习：

1. $\quad\left\{0^i 1^j 0^k \mid j=2 i+k\right\}$

   仿照最后一个题容易得到答案

2. 无法写成 $x x$ 形式的 01 串

   仿照倒数第二个题，$S \rightarrow A B \mid B A \mid A \mid B \mid \varepsilon$

### NFA和CFG转换

一一对应即可，非常简单

![image-20221115092857560](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205642582509_675_20221201120121396547_551_image-20221115092857560.png)

注意别忘了终态的规则(替换空串)

![image-20221115093159798](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205643806820_805_20221201120122982777_294_image-20221115093159798.png)

“不包含子串011的01串，3显然不需要包含进CFG”

## CFG修改

### 消除二义性

消除二义性没有固定的套路，建立在对文法理解的基础上。

![image-20221201134248289](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205645038077_709_image-20221201134248289.png)

### 消除左递归

消除直接左递归很简单，在龙书第二章有所讲述。下面一个消除间接左递归的例子：

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205646564550_859_20221201120126538302_916_image-20221115094108795.png" alt="image-20221115094108795" width="67%" height="67%" />

### 消除空字

消除空字需要注意的一点时一定要替换“干净”，即所有与含有空字的非终结符文法定义相关的条目都要考虑并替换

![image-20221115094610591](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205648003494_548_20221201120128030368_860_image-20221115094610591.png)

![image-20221115094838176](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205649177202_905_20221201120129388514_865_image-20221115094838176.png)

### 消除回路

![image-20221115095219937](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205650398355_928_20221201120130871049_366_image-20221115095219937.png)

### 左公因子提取

$A \rightarrow \alpha \beta_1 \mid \alpha \beta_2$
改写为：
$\mathrm{A} \rightarrow \alpha \mathrm{A}^{\prime}$
$A^{\prime} \rightarrow \beta_1 \mid \beta_2$

例子：

$\mathrm{S} \rightarrow \mathrm{iEtS}|\mathrm{iEtSeS}| \mathrm{a}$
$\mathrm{E} \rightarrow \mathrm{b}$
i $\rightarrow$ if, t$ \rightarrow$ then, e $\rightarrow$ else, E $\rightarrow$ 表达式, S $\rightarrow$ 语句
改写为:
$\mathrm{S} \rightarrow \mathrm{iEtSS}$ ' | a
$\mathrm{S}^{\prime} \rightarrow \mathrm{eS} \mid \varepsilon$
$\mathrm{E} \rightarrow \mathrm{b}$

## CFG无法描述的语言结构

(重在理解)

例1: $\mathrm{L}_1=\left\{\mathrm{wcw} \mid \mathrm{w} \in(\mathrm{a} \mid \mathrm{b})^*\right\}$

检查标识符(w)必须在使用之前定义

语义分析阶段才能完成的事情

例2: $\mathrm{L}_2=\left\{a^{\mathrm{n}} b^m c^n d^m \mid n \geqslant 1\right.$ 且 $\left.m \geqslant 1\right\}$

检查函数的形参 (声明) 与实参 (调用)的数目是否匹配

语法定义一般不考虑参数数目

例3: $\mathrm{L}_3=\left\{\mathrm{a}^{\mathrm{n}} b^{\mathrm{n}} \mathrm{c}^{\mathrm{n}} \mid \mathrm{n} \geq 0\right\}$

排版软件, 文本加下划线: $\mathrm{n}$ 个字符, $\mathrm{n}$ 个退格, $\mathrm{n}$ 个下划线

$\mathrm{a}^{\mathrm{n}} b^{\mathrm{n}}$容易描述(S→aSb)

另一种方式: 字符一退格一下划线三元 组序列, $(\mathrm{abc})^*$就可以描述了

**可以描述的类似文法：**

$\mathrm{L}_1{ }^{\prime}=\left\{\mathrm{w} \mathrm{c}\mathrm{w}^{\mathrm{R}} \mathrm{w} \in(\mathrm{a} \mid \mathrm{b})^*, \mathrm{w}^{\mathrm{R}}\right.$ 为$\mathrm{w}$的反转 $\}$

$\mathrm{S} \rightarrow \mathrm{aSa}|\mathrm{bSb}| \mathrm{c}$
$\mathrm{L}_2{ }^{\prime}=\left\{\mathrm{a}^{\mathrm{n}} \mathrm{b}^{\mathrm{m}} \mathrm{c}^{\mathrm{m}} \mathrm{d}^{\mathrm{n}} \mid \mathrm{n} \geqslant 1\right.$ 且 $\left.\mathrm{m} \geqslant 1\right\}$

和考试题类似，中心对称的，先处理中间

$\mathrm{S} \rightarrow \mathrm{aSd}|\mathrm{aAd} \quad \mathrm{A} \rightarrow \mathrm{bAc}| \mathrm{bc}$

$\mathrm{L}_2{ }^{{\prime\prime}}=\left\{\mathrm{a}^{\mathrm{n}} b^{\mathrm{n}} \mathrm{c}^{\mathrm{m}} \mathrm{d}^{\mathrm{m}} \mid \mathrm{n} \geqslant 1\right.$ 且 $\left.m \geqslant 1\right\}$

轴对称的，先处理两边

$\mathrm{S} \rightarrow \mathrm{AB} \quad \mathrm{A} \rightarrow \mathrm{aAb}|\mathrm{ab} \quad \mathrm{B} \rightarrow \mathrm{cBd}| \mathrm{cd}$

$\mathrm{L}_3{ }^{\prime}=\left\{\mathrm{a}^{\mathrm{n}} \mathrm{b}^{\mathrm{n}} \mid \mathrm{n} \geq 1\right\}$

$\mathrm{S} \rightarrow \mathrm{aSb} \mid \mathrm{ab}$


PS：证明$\mathrm{L}_3{ }^{\prime}$不能用正则表达式表示

可以考虑证明它不能使用DFA进行表示。证明的关键就是定义”DF“(确定，有穷):

假定存在DFA D接受 $\mathrm{L}_3{ }^{\prime}$, 其状态数为 $k$(有穷)。 设状态 $\mathrm{s}_0, \mathrm{~s}_1, \ldots, \mathrm{s}_{\mathrm{k}}$ 为读入 $\varepsilon, \mathrm{a}, \mathrm{aa}, \ldots, \mathrm{a}^{\mathrm{k}}$ 后的状态 $\Rightarrow \mathrm{s}_{\mathrm{i}}$ 为读入 $\mathrm{i}$ 个 $\mathrm{a}$ 达到的状态 $(0 \leqslant \mathrm{i} \leqslant \mathrm{k})$
总状态数 $\mathrm{k} \rightarrow \mathrm{s}_0, \mathrm{~s}_1, \ldots, \mathrm{s}_{\mathrm{k}}$ 中至少有两个相同状态, 不妨设为 $s_i 、 s_j ， i<j$

$a^i b^i \in L_3 \rightarrow \Rightarrow s_i\left(s_j\right)$ 到终态路径标记为 $b^i$
$\rightarrow$ 初态 $\rightarrow$ 终态还有标为 $a^i b^i$ 的路径 $\rightarrow D$ 接受 $a^i b^i$, 与”D(确定)“矛盾！

![image-20221115103746485](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E4%B8%8A%E4%B8%8B%E6%96%87%E6%97%A0%E5%85%B3%E6%96%87%E6%B3%95/20230828205651744661_709_20221201120132392020_526_image-20221115103746485.png)