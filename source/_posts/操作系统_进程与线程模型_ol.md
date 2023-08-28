---
title: 操作系统_进程与线程模型
categories: 笔记
date: 2022-11-13 10:00:00
tags:
  - 操作系统
abbrlink: 30463
---
## 操作系统--进程与线程

### 进程概念

#### 从并发开始

串行排队

![image-20220926142304076](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210733845566_917_20221019110755222583_746_image-20220926142304076.png)

分时调用

![image-20220926142216136](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210734963850_163_20221019110756926120_483_image-20220926142216136.png)

“但是并发除了会让脑子更乱以外并不会让事情变得更好”

![image-20220926151301063](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210736115343_796_20221019110758632298_262_image-20220926151301063.png)

尽管如此，并发确实可以提高CPU的利用率。当然可能会带来设备（慢操作）延迟。

![image-20221018192004694](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210737627177_866_20221019110801392732_151_image-20221018192004694.png)

C

**进程就是为了“保存”和“恢复”一个程序的执行过程，以实现并发的目标**

#### 进程和程序的区别

![image-20221016200649356](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210739060065_253_20221019110803473763_292_image-20221016200649356.png)

### 进程和线程的区别

+ 进程作为分配资源的基本单位，线程作为独立运行和独立调度的基本单位(注意：在多线程 OS 中，进程不是一个可执行的实体)

+ 进程拥有一个完整的虚拟地址空间，不依赖于线程而独立存在；反之，线程是进程的一部分，没有自己的地址空间，与进程内的其他线程一起共享分配给该进程的所有资源。



### 进程的数据结构--PCB

![image-20220926152249647](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210740834601_450_20221019110805822552_826_image-20220926152249647.png)

![image-20221018191442452](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210741862299_153_20221019110807671323_383_image-20221018191442452.png)

### 进程的组织

#### 进程状态和切换

<p class="note note-primary">对于某一个进程：
为什么被暂停了？
为什么选它来运行？
为什么选择这个时机进行切换？</p>

![image-20221018191551669](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210744007444_666_20221019110809885582_767_image-20221018191551669.png)

操作系统可以将会触发慢操作的状态记录下来。

<p class="note note-primary">“把printf的汇编代码放到自己的程序中，并且把控制休眠的指令注释掉，会不会能正常运行？”</p>

不能。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210745247267_536_20221019110811863911_528_image-20220926161106287.png" alt="image-20220926161106287" width="50%" height="50%" />

##### 五状态进程模型

![image-20221014152546893](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210746398255_505_20221019110813764309_930_image-20221014152546893.png)

关于进程的创建：

在一个进程被新建时它并非绝对会被调入内存，通常是分两步，首先创建该进程的PCB，并与之关联，但是此时可能面临内存不足或者操作系统限制了最大进程数导致这个进程还无法被调入进程，因此该进程被暂时留在新建态，在这个状态的进程PCB已经创建并且加载进内存，但是进程的代码和数据往往还留在外存中等待加载。

![image-20221018205252597](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210748249617_239_20221019110816170775_715_image-20221018205252597.png)

关于进程的撤销(结束)

![image-20221016192515282](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210749945224_194_20221019110817967015_206_image-20221016192515282.png)

> B。进程有它的生命周期，不会一直存在于系统中，也不一定需要用户显式地撒销。进程在时间片结束时只是就绪，而不是撤销。阻塞和唤醒是进程生存期的中间状态。进程可在完成时撤销， 或在出现内存错误等时撤销。

关于进程的阻塞

![image-20221018192631681](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210750935983_266_20221019110819440912_574_image-20221018192631681.png)

阻塞态完了会进就绪队列

---

关于临界资源及其同步和互斥
https://houbb.github.io/2020/10/04/os-04-sync

---

![image-20221018214846546](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210751921582_106_20221019110821096921_713_image-20221018214846546.png)

> B 可以共享一部分资源，但不共享虚拟地址空间

![image-20221018214339806](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210753335528_479_20221019110822817914_214_image-20221018214339806.png)

> C

##### 添加了挂起状态的进程模型

![image-20220926162706586](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210754362386_519_20221019110824611329_729_image-20220926162706586.png)

![image-20221014151453508](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210755618064_936_20221019110826436181_342_image-20221014151453508.png)

![image-20221018192900616](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210757396249_122_20221019110828695748_821_image-20221018192900616.png)

A

<p class="note note-info">不同操作系统中进程状态设置区别很大。</p>

##### 进程调度方式

![image-20220926162928685](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210758402892_633_20221019110830191623_314_image-20220926162928685.png)

![image-20220926163633315](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210759559721_216_20221019110832168851_702_image-20220926163633315.png)

现在的操作系统都是可抢占系统。

![image-20221018205406513](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210800855757_695_20221019110834324423_859_image-20221018205406513.png)

> A。BC应该将优先级，D时机不合适。
>
> 此部分将在进程调度中详细介绍。

#### 进程通信

共享存储，消息传递，管道通信

![image-20221018211857840](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210802133591_581_20221019110836886804_366_image-20221018211857840.png)

[linux中的管道通信](https://zhuanlan.zhihu.com/p/58489873)

![image-20221018211911941](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210803836196_270_20221019110839761934_452_image-20221018211911941.png)

> A得俩。B容量是一个页的大小(4KB)。管道是一个文件，任何两个不相关的进程当然都可以通过这个管道文件进行通信

#### 进程和线程的设计模型

##### 线程实现方式

![image-20221018194121923](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210805032394_967_20221019110841591537_254_image-20221018194121923.png)

###### ULT(User Level Thread)

需要注意的是在这种模式下调度仍是以进程为单位进行的

优势:

 1.线程切换不需要内核模式特权.

 2.线程调用可以是应用程序级的,根据需要可改变调度算法,但不会影响底层的操作系统调度程序.

 3.ULT管理模式可以在任何操作系统中运行,不需要修改系统内核,线程库是提供应用的实用程序。

劣势:

1.系统调用(慢操作，如输入输出)会引起进程阻塞，而且进程内的所有线程都被阻塞。(内核每次分配给一个进程的仅有一个CPU，因此进程中仅有一个线程能执行)

2.不利于使用多处理器并行

###### KLT

优势：灵活，线程切换快

劣势：需要用户态到内核态的切换，代价高

线程库：

![image-20221018193551401](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210806392125_868_20221019110843340452_876_image-20221018193551401.png)

![image-20221018205754448](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210807734009_103_20221019110847145883_201_image-20221018205754448.png)

> D.其他线程对此不可见

![image-20221018214600427](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210808930696_547_20221019110848853722_394_image-20221018214600427.png)

> B只有在KLT中才会这么做

##### [轻权进程](https://en.wikipedia.org/wiki/Light-weight_process#cite_note-Vah96-1)

类似于一种折衷的方案。但是问题是太复杂

![image-20221018234308117](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F_%E8%BF%9B%E7%A8%8B%E4%B8%8E%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B/20230828210810073059_437_20221019110850808418_676_image-20221018234308117.png)
