---
title: 计算机组成原理习题讲解部分勘误
categories: 笔记
date: 2022-9-10 10:00:00
updated: 2022-9-10 10:00:00
tags:
  - 计组
abbrlink: 23086
---
4.12

![image-20220822231146713](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%84%E6%88%90%E5%8E%9F%E7%90%86%E4%B9%A0%E9%A2%98%E8%AE%B2%E8%A7%A3%E9%83%A8%E5%88%86%E5%8B%98%E8%AF%AF/20230828210843270855_989_20221013150014727108_816_image-20220822231146713.png)

流水线周期取决于耗时最长的阶段。此处忘记了IF的时钟周期仍为150ps。

5.6

![image-20220821230253484](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%84%E6%88%90%E5%8E%9F%E7%90%86%E4%B9%A0%E9%A2%98%E8%AE%B2%E8%A7%A3%E9%83%A8%E5%88%86%E5%8B%98%E8%AF%AF/20230828210844556701_290_20221013150016592317_276_image-20220821230253484.png)

![image-20220821230543233](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%84%E6%88%90%E5%8E%9F%E7%90%86%E4%B9%A0%E9%A2%98%E8%AE%B2%E8%A7%A3%E9%83%A8%E5%88%86%E5%8B%98%E8%AF%AF/20230828210846005959_170_20221013150018066044_526_image-20220821230543233.png)

第三问的讲解如上图所示。此处p1和p2的CPI计算有误。原因是未考虑指令缺失造成的代价。
$$
CPI=1+平均每条指令阻塞始终周期数\\
=1+指令缺失阻塞时钟周期数+数据缺失阻塞时钟周期数
$$

$$
指令缺失阻塞时钟周期数=\texttt{cache}缺失率*指令缺失代价\\
指令缺失代价=\frac{访存时间}{\texttt{cache}命中时间}
$$

$$
数据缺失阻塞时钟周期数=\texttt{cache}缺失率*访存指令占比*数据缺失代价\\
指令缺失代价=\frac{访存时间}{\texttt{cache}命中时间}
$$

得到两个CPI分别约为12.54和7.35

5.12

![image-20220822230445847](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%84%E6%88%90%E5%8E%9F%E7%90%86%E4%B9%A0%E9%A2%98%E8%AE%B2%E8%A7%A3%E9%83%A8%E5%88%86%E5%8B%98%E8%AF%AF/20230828210848319381_189_20221013150019552299_178_image-20220822230445847.png)

第三小问关于反置页表。

![image-20220822231114457](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%84%E6%88%90%E5%8E%9F%E7%90%86%E4%B9%A0%E9%A2%98%E8%AE%B2%E8%A7%A3%E9%83%A8%E5%88%86%E5%8B%98%E8%AF%AF/20230828210849511576_828_20221013150020954753_868_image-20220822231114457.png)

在反置页表中是为每一个物理块设置一个页表项的，视频中也有所阐述,但在计算时依旧是使用的虚拟地址。此处应为
$$
PTE= \text{Number of pages in physical memory}\\

\begin{aligned}
&=\frac{\text { Size of physical memory }}{\text { Page size }}\\
&=\frac{16 \mathrm{GiB}}{4 \mathrm{KiB}} \\
&=\frac{2^{34}}{2^{12}} \\
&=2^{22}
\end{aligned}
$$
