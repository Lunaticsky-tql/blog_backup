---
title: 人工智能导论
categories: 笔记
date: 2022-9-10 10:00:00
tags:
  - 机器学习
abbrlink: 46759
---
人工智能导论

逻辑推理

<p align="center"><img alt="image-20220831205211237" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210025711643_258_20220916221103884501_923_image-20220831205211237.png" width="50%"/></p>
<p align="center"><img alt="image-20220831205344502" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210026938592_641_20220916221111633086_904_image-20220831205344502.png" width="50%"/></p>
<p align="center"><img alt="image-20220831205448441" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210028062306_917_20220916221120315099_386_image-20220831205448441.png" width="50%"/></p>

任意对析取，存在对合取都是蕴含关系，分开的条件强于合起来的（举个例子就明白了）

![image-20220831210345470](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210029114569_463_20220916221127063207_401_image-20220831210345470.png)

<p align="center"><img alt="image-20220831210404798" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210030208844_354_20220916221128281126_946_image-20220831210404798.png" width="50%"/></p>

只与新加入的直接相关

<p align="center"><img alt="image-20220831211022710" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210031412961_436_20220916221129758335_145_image-20220831211022710.png" width="50%"/></p>
<p align="center"><img alt="image-20220831211029655" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210033180741_738_20220916221130984768_647_image-20220831211029655.png" width="50%"/></p>
<p align="center"><img alt="image-20220831211350521" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210034293828_443_20220916221132416550_481_image-20220831211350521.png" width="50%"/></p>

因果分析三层次：关联，介入，反事实

因果图三种形式：链，分连，汇连（chain，fork，collider)

![image-20220831212134887](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210035573692_180_20220916221134366409_448_image-20220831212134887.png)

做法：联合概率分布由每个节点与其父节点之间的条件概率得出。根节点是外生变量，其他的是内生

---



<p align="center"><img alt="image-20220831212713182" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210036929707_670_20220916221135899101_136_image-20220831212713182.png" width="50%"/></p>

深搜可能会陷入无限循环

<p align="center"><img alt="image-20220831213452142" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210038002300_969_20220916221137133557_194_image-20220831213452142.png" width="50%"/></p>
<p align="center"><img alt="image-20220831213527818" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210039846813_917_20220916221139012135_477_image-20220831213527818.png" width="50%"/></p>
<p align="center"><img alt="image-20220831213624058" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210041129476_223_20220916221140593318_530_image-20220831213624058.png" width="50%"/></p>

有环路的图会使贪婪最佳优先算法不完备。

判断：启发函数满足可容性则一定能保证算法最优性x

树搜索是这样法，图不一定

判断：启发函数恒为0一定满足可容性x

启发函数不一定要是正数。

满足一致性可保证A*搜索算法最优

启发函数不会过高估计从当前节点到目标结点之间的实际代价。x

满足可容性的启发函数才有这样的性质。



MinMax的适用条件：两人博弈，信息透明，零和博弈

<p align="center"><img alt="image-20220831215141822" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210042520064_342_20220916221142369023_436_image-20220831215141822.png" width="50%"/></p>

注意，没有规定必须要公平。D违反了零和博弈

<p align="center"><img alt="image-20220831220640110" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210044088962_452_20220916221144124086_686_image-20220831220640110.png" width="50%"/></p>

![image-20220831220659274](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210047629658_923_20220916221145565187_669_image-20220831220659274.png)

这个做法是不对的，根据课本上的过程，A*算法会考虑所有可达的评价函数，每次从边缘集合拓展的节点并非总是当前节点的后继节点。fn评价函数是唯一标准如果发现有更小的，会倒回去。

<p align="center"><img alt="image-20220831220818630" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210048841987_713_20220916221146871853_388_image-20220831220818630.png" width="50%"/></p>

而且贪婪最佳优先搜索也是启发式算法，优先选择启发函数最小的后继节点拓展。

<p align="center"><img alt="image-20220831222502968" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210052161521_136_20220916221148285550_794_image-20220831222502968.png" width="50%"/></p>
<p align="center"><img alt="image-20220831222848019" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210053407331_533_20220916221149618933_986_image-20220831222848019.png" width="50%"/></p>

![image-20220831223950629](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210055914678_403_20220916221152879301_392_image-20220831223950629.png)

![image-20220831223959591](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210100629197_676_20220916221155537145_635_image-20220831223959591.png)

记住蒙特卡洛树UCB的公式，明白反向传播的过程。
$$
U C B=\bar{X}_j+C \times \sqrt{\frac{2 \ln n}{n_j}}
$$
**上限置信区间** **(Upper Confidence Bound, UCB)**

---

监督学习中经验风险和期望风险的概念

![image-20220831224734326](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210104619307_128_20220916221157700882_480_image-20220831224734326.png)

<p align="center"><img alt="image-20220831224903093" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210105955603_361_20220916221159350035_550_image-20220831224903093.png" width="50%"/></p>

![image-20220831224941130](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210107235144_810_20220916221201393460_662_image-20220831224941130.png)<p align="center"><img alt="image-20220831224941224" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210107235144_810_20220916221201393460_662_image-20220831224941130.png" width="50%"/></p>

​    常用的正则项方法包括L1正则项和L2正则项：其中L1使权重稀疏，L2使权重平滑。一句话总结就是：L1会趋向于产生少量的特征，而其他的特征都是0，而L2会选择更多的特征，这些特征都会接近于0。

怎么记：1比2小，生成的特征少

<p align="center"><img alt="image-20220831225522763" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210111062631_540_20220916221204366868_381_image-20220831225522763.png" width="50%"/></p>
<p align="center"><img alt="image-20220831225535198" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210112552099_228_20220916221206081717_192_image-20220831225535198.png" width="50%"/></p>

考法：判断哪些算法是判别模型，哪些是生成模型。大部分典型机器学习算法都是判别模型。贝叶斯方法，隐马科代夫链式生成模型



<p align="center"><img alt="image-20220831230142515" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210115820984_167_20220916221207951204_832_image-20220831230142515.png" width="50%"/></p>

信息熵小，信息稳定，单一，纯度高；信息熵大，信息不稳定，纯度低。

<p align="center"><img alt="image-20220831230645025" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210117454363_880_20220916221209692239_698_image-20220831230645025.png" width="50%"/></p>

决策树是在干什么呢？选择最佳属性对样本进行划分，得到最大的“纯度”

同时注意决策树是有监督学习。

**线性区别分析** **(**linear discriminant analysis, LDA**)**

线性判别分析的核心：类内方差小，类间间隔大。“君子和而不同，小人同而不和”，是一种降为方法

#请判断下面说法是否正确： 线性判别分析是在最大化类间方差和类内方差的比值(√)

#在一个监督学习任务中，每个数据样本有 4个属性和一个类别标签，每种属性分别有3、
2、2和2种可能的取值，类别标签有3种不同的取值。请问可能有多少种不同的样本？（注意，并不是在某个数据集中最多有多少种不同的样本，而是考虑所有可能的样本)()

乘起来就可以。72

![image-20220831232017771](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210118757882_389_20220916221224036219_753_image-20220831232017771.png)

记住就可以

重点：

<p align="center"><img alt="image-20220831231843333" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210120139847_342_20220916221225672479_673_image-20220831231843333.png" width="50%"/></p>
<p align="center"><img alt="image-20220831232347725" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210123240274_952_20220916221227106679_945_image-20220831232347725.png" width="50%"/></p>
<p align="center"><img alt="image-20220831233241581" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210124487664_976_20220916221229085668_716_image-20220831233241581.png" width="50%"/></p>



ada boosting



 $Z_m=\sum_{i=1}^N w_{m, i} \mathrm{e}^{-\alpha_m y G_i\left(x_i\right) \text { 。 }}$ 可以把对第 $i$ 个训练样本更新后的分布权重写为如下分段函数形式:
$$
w_{m+1, i}= \begin{cases}\frac{w_{m, i}}{Z_m} \mathrm{e}^{-\alpha_m}, &amp; G_m\left(x_i\right)=y_i \\ \frac{w_{m, i}}{Z_m} \mathrm{e}^{\alpha_m}, &amp; G_m\left(x_i\right) \neq y_i\end{cases}
$$
可见, 如果第 $i$ 个训练样本无法被第 $m$ 个弱分类器 $G_m(x)$ 分类成功, 则需要增大该样本权重, 否则减少该样本权重。这样, 被错误分类样本 会在训练第 $m+1$ 个弱分类器 $G_{m+1}(x)$ 时被 “重点关注”。

在第 $m$ 次迭代中, Ada Boosting 总是趋向于将具有<font color="Apricot">最小误差的学习模型</font>（err最小的）选做本轮次生成的弱分类器 $G_m$, 促使累积误差快速下降。

---

无监督学习

K-means往往找都是一个局部最优

聚类迭代满足如下任意一个条件，则聚类停止：

•已经达到了迭代次数上限

•前后两次迭代中，聚类质心基本保持不变



<p align="center"><img alt="image-20220831234829916" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210125709606_805_20220916221230319204_134_image-20220831234829916.png" width="50%"/></p>
<p align="center"><img alt="image-20220831234856133" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210127172626_838_20220916221232576761_180_image-20220831234856133.png" width="50%"/></p>

应当是尽量“不相关”

•**主成分分析是将𝑛维特征数据映射到𝑙维空间**(**n≫l**)**，去除原始数据之间的冗余性（通过去除相关性手段达到这一目的）。**每一维的样本方差尽可能大



•**特征人脸方法是一种应用主成份分析来实现人脸图像降维的方法，其本质是用一种称为“特征人脸****(eigenface)”****的特征向量（而不是像素）按照线性组合形式来表达每一张原始人脸图像，进而实现人脸识别。**

每一个特征人脸的维数与原始人脸图像的维数一样大x 会变小

特征人脸之间的相关度要尽可能大√

为了使算法更高效采用了奇异值分解的方法

---

<p align="center"><img alt="image-20220901002546496" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210130379164_284_20220916221234267125_288_image-20220901002546496.png" width="50%"/></p>

批量梯度下降算法是在整个训练集上计算损失误差C()。如果数据集较大，则会因内存容量不足而无法完成，同时这一方法收敛速度较慢。随机梯度下降算法是使用训练集中每个训练样本计算所得C()来分别更新参数。虽然，随机梯度下降收敛速度会快一些，但可能出现所优化目标函数震荡不稳定现象。

<p align="center"><img alt="image-20220901004646914" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210132063072_174_20220916221236054772_109_image-20220901004646914.png" width="50%"/></p>
$$
f(x)=\frac{1}{1+\mathrm{e}^{-x}}
$$
选取 sigmoid函数作为激活函数, 因为其具有如下优点: (1) 概率形式输出, sigmoid函数值域为 $(0,1)$, 因此使 sigmoid函数输出可视为概 率值; (2) 单调递增, sigmoid函数对输人 $x$ 取值范围没有限制, 但当 $x$ 大 于一定值后, 函数输出无限趋近于 1 , 而小于一定数值后, 函数输出无限趋近于 0 , 特别地, 当 $x=0$ 时, 函数输出为 $0.5$; (3) 非线性变化, $x$ 取 值在 0 附近时, 函数输出值的变化幅度比较大 (函数值变化陡峭), 意味 着函数在 0 附近容易被激活且是非线性变化, 当 $x$ 取值很大或很小时, 函数输出值几乎不变, 这是基于概率的一种认识与需要。

![image-20220901012351440](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210134382419_848_20220916221237401626_567_image-20220901012351440.png)

![image-20220901012412558](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210134382419_848_20220916221237401626_567_image-20220901012351440.png)

![image-20220901012437001](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210137677694_125_20220916221245033698_681_image-20220901012437001.png)

<p align="center"><img alt="image-20220901012512732" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210139040872_789_20220916221246660573_722_image-20220901012512732.png" width="50%"/></p>

![image-20220901012559806](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210140127492_349_20220916221248004240_176_image-20220901012559806.png)

![image-20220901012619080](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210141391762_346_20220916221249466398_422_image-20220901012619080.png)

![image-20220901012639822](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210143541722_397_20220916221251026834_417_image-20220901012639822.png)

---

强化学习的特征

![image-20220901082606079](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210144952030_795_20220916221252634813_271_image-20220901082606079.png)

<p align="center"><img alt="image-20220901082635583" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210146158871_774_20220916221254174712_770_image-20220901082635583.png" width="50%"/></p>

一个随机过程实际上是一列随时间变化的随机变量。当时间是离散 量时, 一个随机过程可以表示为 $\left\{X_t\right\}_{t=0,1,2, \cdots}$, 这里每个 $X_t$ 都是一个随机变量, 这被称为离散随机过程。为了方便分析和求解, 通常要求通过合理的问题定义使得一个随机过程满足马尔可夫性 (Markov property), 即满足如下性质:
$$
P\left(X_{t+1}=x_{t+1} \mid X_0=x_0, X_1=x_1, \cdots, X_t=x_t\right)=P\left(X_{t+1}=x_{t+1} \mid X_t=x_t\right) \text { (式7.1) }
$$
这个公式的直观解释为: 下一刻的状态 $X_{t+1}$ 只由当前状态 $X_t$ 决定 (而与更早的所有状态均无关)。满足马尔可夫性的离散随机过程被称为 马尔可夫链 (Markov chain)。

<p align="center"><img alt="image-20220901083631487" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210147483095_532_20220916221255863567_937_image-20220901083631487.png" width="50%"/></p>

- 动作 $-$ 价值函数 (action-value function): $q: S \times A \mapsto \mathbb{R}$, 其中 $q_\pi(s, a)=\mathbb{E}_\pi\left[G_t \mid S_t=s, A_t=a\right]$, 表示智能体在时刻 $t$ 处于状态 $s$ 时, 选择 了动作 $a$ 后，在 $t$ 时刻后根据策略 $\pi$ 采取行动所获得回报的期望。
价值函数和动作 $-$ 价值函数反映了智能体在某一策略下所对应状态 序列获得回报的期望, 它比回报本身更加准确地刻画了智能体的目标。 注意, 价值函数和动作 $-$ 价值函数的定义之所以能够成立, 离不开决策 过程所具有的马尔可夫性, 即当位于当前状态 $s$ 时, 无论当前时刻 $t$ 的取值是多少, 一个策略回报值的期望是一定的 (当前状态只与前一状态有 关，与时间无关）。（所以不是$q_\pi(s, a,t)$）
至此, 强化学习可以转化为一个策略学习问题, 其定义为: 给定一 个马尔可夫决策过程 $M D P=(S, A, P, R, \gamma)$, 学习一个最优策略 $\pi^*$, 对任 意 $s \in S$ 使得 $V_{\pi^*}(s)$ 值最大。

![image-20220901083736614](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210148664772_929_20220916221257340897_656_image-20220901083736614.png)

![image-20220901083803818](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210149824175_670_20220916221258558310_351_image-20220901083803818.png)

---



<p align="center"><img alt="image-20220901090535698" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210151522208_726_20220916221300893504_791_image-20220901090535698.png" width="50%"/></p>

![image-20220901090816141](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%AF%BC%E8%AE%BA/20230828210153123121_732_20220916221302843487_985_image-20220901090816141.png)