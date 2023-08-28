---
title: 编译原理-词法分析
categories: 笔记
date: 2022-11-20 10:00:00
tags:
  - 编译原理
abbrlink: 6004
---
# 编译原理-词法分析

## 正则表达式

注意课上没提到的正则写法，仅作为了解

`\w` 用于查找字母、数字和下划线

`\W` 匹配除字母、数字和下划线之外的字符

`\d` 仅用来匹配数字

`\D `用来匹配数字之外的所有字符

`\s` 仅匹配空白字符

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210524206495_377_20221107081612860400_768_image-20221105204422750.png" alt="image-20221105204422750" width="50%" height="50%" />

首尾符号不同的a、b串

```c++
(a(a*b)+) | (b(b*a)+)
或(a(a|b)*b) | (b(a|b)*a)
```

首尾符号相同的a、b串	**包括只有a或b的情况**

```c++
(a(b*a)*)|(b(a*b)*)
```

## NFA设计

不包含字串011的01串

![image-20221105211752301](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210525349884_991_20221107081614097039_483_image-20221105211752301.png)

偶数个0，偶数个1的0/1串

![image-20221105212835393](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210526567412_869_20221107081615829280_894_image-20221105212835393.png)

能被3整除的二进制串

![image-20221105213415355](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210527886997_545_20221107081617166099_636_image-20221105213415355.png)

## 正则-NFA

`Thomson 构造法`。基本思想是递归：

1. 对于基本的 re，直接构造

2. 对于复合的 re，递归构造

具体构造方式比较简单，在此略去

以(0 | 1)\*110(0 | 1)\*为例：



![image-20221106093147221](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210529135341_633_20221107081618854779_247_image-20221106093147221.png)

### NFA-DFA

`子集构造法`

#### 算法理解：

递推的思想

最简单的符号串ε：NFA状态集合←→DFA 状态

长度为1的串a=εa，在自动机中可达的状态为：从c对应的状态经过标记为a的边可达的状态

长度为2的串...

#### 算法需要注意的地方：

1. DFA新的状态对应NFA状态集消耗一个字符，能够走到的状态集。所以很明显，这里要消耗，所以不能是 ε，并且只能消耗一个。

2. 得到步骤 1 中的状态集之后，还需要考虑，这里面的所有节点，通过 ε 能走到的所有状态。注意，这里的每个状态，只要可以通过 ε 走，就必须一直走下去，也就是所谓的 `ε-闭包`。这一步得到状态集的就是最后的结果。

3. 第二步需要格外注意的是别忘了检查克林顿闭包中往回返的边。

4. 只要包含了NFA中的终态，在DFA中就作为终态出现。

5. 直到检查某一个状态的ε-闭包不再产生新状态的时候，算法停止。

#### 实例


上面的图进行一遍子集构造的过程(往年的期末考题，推导过程要比课上讲的例子长一些，小心出错)

![image-20221106093147221](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210529135341_633_20221107081618854779_247_image-20221106093147221.png)

先考虑空串：

ε_closure({0})={0, 1, 2, 4, 7}=A

![image-20221106113307803](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210532194577_427_20221107081622072895_220_image-20221106113307803.png)

在DFA里加入开始状态A。

由于只有2有能够消耗0的边，因此下一步从这个状态指向的3开始考虑：

![image-20221106113154787](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210534447618_828_20221107081623719225_876_image-20221106113154787.png)

ε\_closure(δ(A, 0))=ε\_closure({3})={3, 6, 7, 1, 2, 4}={1, 2, 3, 4, 6, 7}=B

同理。不过这一次在A中4和7都能提供消耗1的边，因此要从5和8开始拓展两次ε_closure：

![image-20221106113520151](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210535648426_872_20221107081625192588_768_image-20221106113520151.png)

ε_closure(δ(A, 1))=ε\_closure({5,8})={5, 6, 7, 1, 2, 4, 8}={1, 2, 4, 5, 6, 7, 8}=C

考虑了所有消耗一个字符的情况后，我们的DFA应当是这个样子：

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210536903027_990_20221107081626891613_879_image-20221106095750761.png" alt="image-20221106095750761" width="67%" height="67%" />

B状态消耗0的状态是{3}。而{3}的ε闭包我们已经求过，它就是B：

![image-20221106094657352](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210538031576_380_20221107081627912947_486_image-20221106094657352.png)

ε_closure(δ(B, 0))=ε\_closure({3})=B

同样的，B消耗1后为{5,8}，它的ε闭包我们也是知道的，是C。

ε_closure(δ(B, 1))=ε\_closure({5,8})=C

那么有：

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210539258340_309_20221107081629295837_152_image-20221106113947097.png" alt="image-20221106113947097" width="67%" height="67%" />

再来考察C：

![image-20221106100409568](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210540531607_259_20221107081630470656_164_image-20221106100409568.png)

ε_closure(δ(C, 0))=ε\_closure({3})=B

ε_closure(δ(C, 1))=ε\_closure({5,8,9})={5, 6, 7, 1, 2, 4, 8, 9}={1, 2, 4, 5, 6, 7, 8, 9}=D

![image-20221106100750517](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210541717135_769_20221107081632830316_747_image-20221106100750517.png)

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210543144145_212_20221107081635290017_116_image-20221106114421614.png" alt="image-20221106114421614" width="67%" height="67%" />

考察新状态D：

![image-20221106101039674](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210544300675_259_20221107081636596912_786_image-20221106101039674.png)

ε\_closure(δ(D, 0))=ε_closure({3,10})={3, 6, 7, 1, 2, 4, 10, 11, 12, 14, 17}={1, 2, 3, 4, 6, 7, 10, 11, 12, 14, 17}=E

这一次覆盖的状态包含了终态17.因此在DFG中E就要加一个圈，表示终态。

![image-20221106101722642](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210545455540_648_20221107081638049390_665_image-20221106101722642.png)

ε\_closure(δ(D, 1))=ε_closure({4,7,8})=D

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210546517685_226_20221107081639688157_503_image-20221106114710326.png" alt="image-20221106114710326" width="67%" height="67%" />

![image-20221106101722642](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210545455540_648_20221107081638049390_665_image-20221106101722642.png)

ε\_closure(δ(E, 0))=ε\_closure({3,13})={1, 2, 3, 4, 6, 7, 11, 12, 13, 14, 16, 17}=F

![image-20221106164356951](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210549141377_330_20221107081642146138_964_image-20221106164356951.png)

ε\_closure(δ(E, 1))=ε\_closure({5,8,15})={ 1, 2, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 17}=G

![image-20221106164315789](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210550434003_492_20221107081643785412_875_image-20221106164315789.png)

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210551952501_856_20221107081645146555_627_image-20221106164515007.png" alt="image-20221106164515007" width="67%" height="67%" />

![image-20221106164356951](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210549141377_330_20221107081642146138_964_image-20221106164356951.png)

ε\_closure(δ(F, 0))=ε\_closure({3,13})=F

ε\_closure(δ(F, 1))=ε\_closure({5,8,15})=G

![image-20221106164315789](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210550434003_492_20221107081643785412_875_image-20221106164315789.png)

ε\_closure(δ(G, 0))=ε\_closure({3,13})=F

ε\_closure(δ(G, 1))= ε\_closure({5,8,9,15})={ 1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17}=H

![image-20221106164831871](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210555562961_855_20221107081649213700_939_image-20221106164831871.png)

ε\_closure(δ(H, 0))=ε\_closure({3,10,13})={1, 2, 3, 4, 6, 7, 10, 11, 12, 13, 14, 16, 17}=I

![image-20221106165419438](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210557006457_224_20221107081650544945_592_image-20221106165419438.png)

ε\_closure(δ(H, 1))=H

ε\_closure(δ(I, 0))=F

ε\_closure(δ(I, 1))=G

发现I不再产生新的状态了，长舒一口气，终于可以结束了。

最终的DFA如下所示：

![image-20221106114818599](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210558147478_146_20221107081651688510_197_image-20221106114818599.png)

做题技巧：做到后面可以连同记下求过的ε\_closure。A⊆B则ε\_closure(A)⊆ε\_closure(B)

识别0111010过程：A →B →C →D →D →E →G →F

## DFA优化

#### 优化思想

具有非ε的输出边的状态显然是NFA中的重要状态

δ(s，a)不空，当且仅当s是重要状态→ 决定了ε\_closure(δ(T，a))的计算→子集构造法的核心

两个子集若具有相同的重要状态，且同时包含或同时不包含终态，则可看作等价

#### 算法理解

下面这一篇文章对正则到DFA和DFA最小化的思想和具体实现剖析的比较透彻。其中正则到DFA并非重点考察内容，但对理解DFA优化的思想有比较大的帮助。

---

词法分析-正则表达式到DFA
https://wangwangok.github.io/2019/10/28/compiler_regular2dfa/

---

#### 实例

最小化上面求得的DFA：

![image-20221106114818599](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210558147478_146_20221107081651688510_197_image-20221106114818599.png)

初始非终态{A, B, C, D}，终态{E, F, G, H, I}，

终态内部自己打转儿，不可再分

0将前者分裂为{A, B, C}和{D}，1将前者分裂为{A, B}和{C}，至此不可再分

![image-20221106175951220](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86-%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90/20230828210600746159_100_20221107081655357057_638_image-20221106175951220.png)