---
title: 寄网第一二章
categories: 笔记
tags:
  - web
  - 寄网
abbrlink: 47623
---
## 寄网

### 第一章

#### 一些基本概念

![image-20220921102100658](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140244969763_823_image-20220921102100658.png)
$$
\frac{640*480*3}{1024}=900\text{KB}
$$



#### Internet边缘与核心

时分和频分多路复用

![image-20220921091644435](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140246164281_313_image-20220921091644435.png)

<p align="center"><img alt="image-20220914113833784" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140247918940_123_image-20220914113833784.png" width="50%"/></p>

![image-20220921090426643](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140249637000_165_image-20220921090426643.png)

”谁来用谁,满了就丢“（当然刚满的时候有临时缓存）

<p class="note note-secondary">由于成本问题，广域网带宽往往比局域网小得多。</p>

问题：因为有排队现象，延迟大

![image-20220921091804148](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140251667625_745_image-20220921091804148.png)

![image-20220921092457252](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140254211234_437_image-20220921092457252.png)

![image-20220921102342289](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140256515520_955_image-20220921102342289.png)

![image-20220921102115526](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140258270940_747_image-20220921102115526.png)

别忘了字节和bit的转换

#### Web服务器访问示例

网络体系结构概览，理解。

![image-20220921135514064](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140259958997_827_image-20220921135514064.png)

### 第二章

#### 应用层协议和进程通信模型

##### 进程通信

<p class="note note-primary">进程之间如何通信？

1.管道
2.共享内存
3.消息队列</p>



![image-20220928093225868](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140301954282_880_image-20220928093225868.png)

<p class="note note-info">C/S模型的缺陷：如果访问量大的时候，会影响服务质量，甚至会导致中心服务器瘫痪
P2P模型缺陷：不便于管理</p>

![image-20220928094631013](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140304191029_856_image-20220928094631013.png)

##### 进程地址标识

![image-20220928101653200](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140306050316_256_image-20220928101653200.png)

##### 应用层协议定义的内容

![image-20220928103019165](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140307775494_627_image-20220928103019165.png)

#### 传输层

作用：保证端到端服务的可靠性

![image-20220928103725740](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140309649551_638_image-20220928103725740.png)

UCP服务的不可靠是相对的，只是级别比较低。

UCP的优势：建立连接快，占用资源少，实现简单，不容易被监控

<p class="note note-info">无论TCP还是UDP都没有提供任何加密机制，这就是说发送进程传进其套接字的数据，与经网络传送到目的进程的数据相同。因此，举例来说如果某发送进程以明文方式（即没有加密）发送了一个口令进入它的套接字，该明文口令将经过发送方与接收方之间的所有链路传送，这就可能在任何中间链路被嗅探和发现。因为隐私和其他安全问题对许多应用而言已经成为至关重要的问题，所以因特网界已经研制了TCP的加强版本，称为安全套接字层(Secure Sockets Layer，SSL)。用SSL加强后的TCP不仅能够做传统的TCP所能做的一切，而且提供了关键的进程到进程的安全性服务，包括加密、数据完整性和端点鉴别。</p>

TCP/IP协议通常在操作系统的内核中实现

##### socket

![image-20220928111844557](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140312104068_654_image-20220928111844557.png)

TCP/UDP协议感性认识

<p align="center"><img alt="image-20220928135917798" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E5%AF%84%E7%BD%91/20220928140313787528_278_image-20220928135917798.png" width="50%"/></p>