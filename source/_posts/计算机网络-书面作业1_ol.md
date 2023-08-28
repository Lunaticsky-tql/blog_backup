---
title: 计算机网络-书面作业1
categories: 笔记
date: 2022-12-20 23:00:00
tags:
  - 寄网
abbrlink: 54831
---
# 计算机网络-书面作业1

2013599_田佳业

### 第一章问题

网络结构如下图所示，主机A与主机B之间通过两段链路和一台转发设备R进行连接，每条链路的长度和传输速率已经在图中标出，R采用存储转发机制。主机A向主机B发送一个长度为10000字节的报文，请回答以下问题（设电磁波传播速度为2*108米/秒）

(1)   如果采用报文交换，请计算端到端的最小时延，即从主机A传输报文的第一位开始，到主机B接收到报文的最后一位为止所用的时间。

(2)   如果将报文分成5个报文分组传输，请计算完成报文传输的最小端到端时延（忽略报文分组的封装开销）。

在统计多路复用机制中，端到端的时延具有不确定性，请简要分析影响端到端时延的主要因素。



![img](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211058424432_805_20221120095815944612_600_clip_image002.png)

1.

![image-20221228093807403](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211059236518_851_20221228103350003675_727_image-20221228093807403.png)

![image-20221228095021089](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211100678849_931_20221228103353392389_877_image-20221228095021089.png)
$$
\mathrm{Latency_1 = PROP + TRANSP}=\frac{(4+2)\times 10^3}{2 \times 10^{8}}+\frac{10^{4} \times 8}{100\times 10^6}+\frac{10^{4} \times 8}{10\times 10^6}\\
=3\times 10^{-5}+8\times 10^{-4}+8\times 10^{-3}=8.83\times 10^{-3}\text{s}
$$
可以看到传播速率主要取决于链路2的传输速度。

2.



$$
\mathrm{Latency_2} =\mathrm{Latency_1}-\frac{4}{5}\frac{10^{4} \times 8}{100\times 10^6}=8.19\times 10^{-3}\text{s}
$$
为什么可以这么算?

![image-20221228101441745](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211102220231_387_20221228103355518362_356_image-20221228101441745.png)

同时也可以看出，在这个问题中，节省的时间仅取决于第一个链路的时延。因为第二条链路比较慢，所以总体上来说并没有节省太多时间。

（3）主要因素包括：

+ 核心：存储转发设备中的排队时延

+ 路由器中的处理时间：路由决策、差错检验、分片等操作

+ 报文分组大小和分组数量，数据流的个数，数据流占带宽的频率，都会影响时延。 

+ 链路的传输速率，链路长度 

排队时延是导致“不确定性“的最主要因素。

### 第二章问题

###### 1.

通过使用Windows命令行模式提供的nslookup命令查询www.baidu.com的IP地址，给出结果截图，并对返回的结果进行解释。同时，利用Wireshark捕获查询的交互过程，给出结果截图，并进行简要说明。

1)

nslookup命令用于**查询DNS的记录，查看域名解析是否正常，在网络故障的时候用来诊断网络问题**

![image-20221115205303473](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211105692753_410_20221120095816836309_574_image-20221115205303473.png)

服务器为本机DNS服务器信息，Address表示的是 DNS 服务器地址。

非权威应答表示，非从域名的权威服务器获得结果，而是从本地DNS缓存中获取的结果

www.a.shifen.com是百度域名曾经的一个别名，`shifen.com`和`baidu.com`两台域服务器其实是同一台服务器。

下面的Address便是百度域名对应的ip地址。以第一个为例，搜索一下看看:

![image-20221115210510064](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211106734346_212_20221120095817744460_340_image-20221115210510064.png)

2)

![image-20221115211104602](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211107709615_845_20221120095840824680_626_image-20221115211104602.png)

输入dns进行过滤，可以看到解析百度时的报文发送和应答，对应左边灰色的箭头。

可以看出 ，DNS 为应用层协议 ，下层传输层采用 UDP ，再下层网络层是 IPV4 协议 。 

下面结合DNS报文格式进行分析:

![image-20221115211202585](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211108799252_424_20221120095842598552_479_image-20221115211202585.png)

本机(10.130.93.171是WLAN的IPv4地址)首先向服务器发出查询请求 ， 然后服务器解析 IP 找到主机 ，做出响应 。接着 ，主机向服务器发送查询 www.baidu.com信息的对应请求，服务器接受到请求后作出响应 。并且可以看到回应的报文Answers区域报文包括的内容未必是等长，格式相同的。每一个回答反映一部分需要的信息。



![image-20221115211646689](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211110204046_677_20221120095845117430_948_image-20221115211646689.png)

资源记录结构如下所示:

![image-20221115220024906](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211111256885_875_20221120100009402791_134_image-20221115220024906.png)

比如图中的A对应将名称对应到IPv4的32位地址。

###### 2.

以反复解析为例，说明域名解析的基本工作过程（可以结合图例）。给出内容分发网络（CDN）中DNS重定向的基本方法，说明原始资源记录应该如何修改，并描述重定向过程。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211112307874_994_20221120100010926561_580_image-20221115222340231.png" alt="image-20221115222340231" style="zoom: 67%;" />

1.2.首先查本地缓存，如果没有记录，则以DNS客户的身份向根域名服务器发出解析请求(2)，如果有直接将IP地址返回请求主机(实验操作中的情况，对应图中的8)

3.根域名服务器收到请求后，判断该域名属于.com 域，将对应的TLD(顶级域名服务器，此处为.com)的IP地址返回给本地域名服务器。
4.本地域名服务器再次请求

5.TLD收到请求后，判断该域名属于baidu.com域，因此将对应的授权域名服务器baidu.com 的IP地址返回给本地域名服务器。

6.向百度的顶级域名服务器baidu.com.请求www.baidu.com。

7.返回ip地址

8.本地域名服务器把结果返回客户机并缓存

当然对于百度这个例子，它发现这个www有别名叫www.a.shifen.com。

拿到www.baidu.com的别名www.a.shifen.com的时候，本来要重新到com域查找shifen.com的NS，又因为，两个域在同一台NS上，所以直接向本机(授权域名服务器)发起了shifen.com域的查找请求，把a.shifen.com的IP返回。

###### 3.

在DNS域名系统中，域名解析时使用UDP协议提供的传输层服务（DNS服务器使用UDP的53端口），而UDP提供的是不可靠的传输层服务，请你解释DNS协议应如何保证可靠机制。

首先，查阅了解了为什么DNS使用UDP:其实感性上就可以理解，DNS并不需要TCP所提供的全部可靠性机制，而TCP会相比UDP耗费更多的资源。当然，其实DNS 在设计之初就在区域传输中引入了 TCP 协议的可选项。

关于如何保证可靠性，主要有以下几个方面:

从DNS应用层本身来说，首先报文中问题的数量、回答的数量，就可以可以用来进行一定的校验，同时DNS也是有生存周期的，在生命周期过后会进行重新请求更新以保证数据的正确性。

从可用性上来说，DNS的权威服务器也是冗余支持的。

从安全性上来说，DNS脆弱性主要有两个可能的方面:一是课本中提到的DDoS攻击，当然由于缓存机制的存在很难造成实质性的危害;另外更常见的是针对缓存进行欺骗的所谓投毒攻击，现在也有DNS 安全扩展 ([DNSSEC](https://cloud.google.com/dns/docs/dnssec?hl=zh-cn))对其进行保护。

当然以上几个方面和TCP从协议层面上保证的可靠性肯定不能等同而论，但足以满足实际应用是需求。

> 答案就写了超时重传和差错检测，大概其实是想问如果要实现可靠机制需要增加哪些机制吧。

###### 捎带复习一下域名格式压缩

![image-20221115230206425](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211113362069_658_20221120100012567584_212_image-20221115230206425.png)

"11"指字节的前两位

![image-20221115230406295](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C-%E4%B9%A6%E9%9D%A2%E4%BD%9C%E4%B8%9A1/20230828211114836606_350_20221120100014215164_756_image-20221115230406295.png)