---
title: 寄网-应用层
categories: 笔记
tags:
  - 寄网
abbrlink: 31769
---
## 第一章

### 一些基本概念

![image-20220921102100658](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090215966691_917_image-20220921102100658.png)
$$
\frac{640*480*3}{1024}=900\text{KB}
$$



### Internet边缘与核心

#### 电路交换

##### 时分和频分多路复用

![image-20220921091644435](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090217080225_394_image-20220921091644435.png)

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090219745396_605_image-20220914113833784.png" alt="image-20220914113833784" width="50%" height="50%" />

##### 报文分组交换

![image-20220921090426643](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090222052725_480_image-20220921090426643.png)

”谁来用谁,满了就丢“（当然刚满的时候有临时缓存）

<p class="note note-secondary">由于成本问题，广域网带宽往往比局域网小得多。</p>

问题：因为有排队现象，延迟大

![image-20220921091804148](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090236334011_832_image-20220921091804148.png)

![image-20220921092457252](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090239402715_311_image-20220921092457252.png)

![image-20220921102342289](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090242065298_766_image-20220921102342289.png)

![image-20220921102115526](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090244516116_167_image-20220921102115526.png)

题中是Mb不是MB。别忘了字节和bit的转换，正确答案是C。

#### 传输时延

<font color='Apricot'>别忘了RTP的定义</font>

![image-20221012101652816](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090246765227_486_image-20221012101652816.png)

![image-20221115202145242](/Users/tianjiaye/Library/Application Support/typora-user-images/image-20221115202145242.png)

### Web服务器访问示例

网络体系结构概览，理解。

![image-20220921135514064](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090248226957_689_image-20220921135514064.png)

## 第二章

### 应用层协议和进程通信模型

#### 进程通信模型

<p class="note note-primary">进程之间如何通信？

1.管道
2.共享内存
3.消息队列</p>

![image-20220928093225868](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090249957055_679_image-20220928093225868.png)

<p class="note note-info">C/S模型的缺陷：如果访问量大的时候，会影响服务质量，甚至会导致中心服务器瘫痪
P2P模型缺陷：不便于管理</p>

![image-20221012092450719](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090255703101_824_image-20221012092450719.png)

D。客户机面向用户。其实主要注意C是对的

![image-20221012112533931](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090257212133_865_image-20221012112533931.png)

![image-20221012112556726](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090258905463_489_image-20221012112556726.png)

![image-20220928094631013](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090300525887_688_image-20220928094631013.png)

#### 进程地址标识

![image-20220928101653200](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090302563658_334_image-20220928101653200.png)

#### 应用层协议定义的内容

![image-20220928103019165](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090304286709_112_image-20220928103019165.png)

#### 传输层

作用：保证端到端服务的可靠性

![image-20220928103725740](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090306529509_443_image-20220928103725740.png)

UCP服务的不可靠是相对的，只是级别比较低。

UCP的优势：建立连接快，占用资源少，实现简单，不容易被监控

<p class="note note-info">无论TCP还是UDP都没有提供任何加密机制，这就是说发送进程传进其套接字的数据，与经网络传送到目的进程的数据相同。因此，举例来说如果某发送进程以明文方式（即没有加密）发送了一个口令进入它的套接字，该明文口令将经过发送方与接收方之间的所有链路传送，这就可能在任何中间链路被嗅探和发现。因为隐私和其他安全问题对许多应用而言已经成为至关重要的问题，所以因特网界已经研制了TCP的加强版本，称为安全套接字层(Secure Sockets Layer，SSL)。用SSL加强后的TCP不仅能够做传统的TCP所能做的一切，而且提供了关键的进程到进程的安全性服务，包括加密、数据完整性和端点鉴别。</p>

TCP/IP协议通常在操作系统的内核中实现

#### socket

![image-20220928111844557](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090312331202_111_image-20220928111844557.png)

TCP/UDP协议感性认识

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090313969554_614_image-20220928135917798.png" alt="image-20220928135917798" width="50%" height="50%" />

#### socket编程

![image-20221005095507884](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090321048624_770_image-20221005095507884.png)

PowerPC采用大端序，其他CPU大多使用小端序。网络编程使用大端序。

### 文件传输协议

FTP基于TCP的可靠服务

![image-20221012093347724](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090322840513_285_image-20221012093347724.png)

对应的，邮件传输是带内控制。

> FTP客户首先连接服务器的21号端口，建立控制连接（控制连接在整个会话期间一直保持打开)，然后建立数据连接，在数据传送完毕后，数据连接最先释放，控制连接最后释放。

![image-20221012095753630](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090326097608_519_image-20221012095753630.png)

![image-20221012095828837](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090328651614_685_image-20221012095828837.png)

D

<p class="note note-info">为什么FTP不适合共享读写文件？
因为FTP使用了一个分离的控制连接，所以也称FTP的控制信息是带外(Out-of-band)传送的？使用FTP时，若要修改服务器上的文件，则需要先将此文件传送到本地主机，然后再将修改后的文件副本传送到原服务器，来回传送耗费很多时间。网络文件系统(NFS)采用另一种思路，它允许进程打开一个远程文件，并能在该文件的某个特定位置开始读写数据。这样，NFS可使用户复制一个大文件中的一个很小的片段，而不需要复制整个大文件。</p>

> 针对文件传输FTP，系统管理员建立了一个特殊的用户ID，名为anonymous，即匿名用户。Internet上的任何人在任何地方都可以使用该用户ID，只是在要求提供用户ID时必须输入 anonymous，该用户ID的密码可以是任何字符串。

<p class="note note-info">为什么FTP要采用两个独立的连接？
在FTP的实现中，客户与服务器之间采用了两条传输连接，其中控制连接用于传输各种FTP命令，而数据连接用于文件的传送。之所以这样设计，是因为使用两条独立的连接可使FTP变得更加简单、更容易实现、更有效率。同时在文件传输过程中，还可以利用控制连接控制传输过程，如客户可以请求终止、暂停传输等。</p>

### Web服务和HTTP协议

#### 最新最热HTTP2.0

##### 二进制分帧传输

![image-20221012105830716](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090330394790_595_image-20221012105830716.png)

##### TCP连接复用

虽然想法很朴素，但确解决了为追求简单和仅适应文本传输的历史遗留问题

![image-20221012110140184](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090332798519_644_image-20221012110140184.png)

![image-20221012110329212](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090334780017_529_image-20221012110329212.png)

##### 服务器推送和HTTP头压缩

当然服务器推送也增加了服务器的压力，因为之前服务器并不需要关注传输的是什么内容

![image-20221012110625529](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090336747509_846_image-20221012110625529.png)

![image-20221012111205235](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090338868210_673_image-20221012111205235.png)

#### CDN

#### DASH

![image-20221019092551081](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090340524655_762_image-20221019092551081.png)

![image-20221019092718918](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090342143506_385_image-20221019092718918.png)

![image-20221019092804145](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E5%BA%94%E7%94%A8%E5%B1%82/20221026090343857447_572_image-20221019092804145.png)
