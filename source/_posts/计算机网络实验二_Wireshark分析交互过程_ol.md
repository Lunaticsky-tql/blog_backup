---
title: 计算机网络实验二_Wireshark分析交互过程
categories: 作业
date: 2022-12-22 10:00:00
tags:
  - 寄网
abbrlink: 13596
---
# 计算机网络实验二_Wireshark分析交互过程

## 实验要求

（1）搭建Web服务器（自由选择系统），并制作简单的Web页面，包含简单文本信息（至少包含专业、学号、姓名）和自己的LOGO。

（2）通过浏览器获取自己编写的Web页面，使用Wireshark捕获浏览器与Web服务器的交互过程，并进行简单的分析说明

- 主要分析的是tcp握手、http请求应答、tcp挥手几个过程和相关问题

## [Wireshark可以做什么](https://zhuanlan.zhihu.com/p/82498482)

- 网络管理员使用Wireshark检测网络问题
- 网安工程师用Wireshark检查信息安全相关问题
- 开发者使用Wireshark为新的通信协议调试
- 普通用户使用Wireshark学习网络协议相关知识
- 憨憨学生使用Wireshark应付TCP/IP课程要求(别骂了)

## 服务器搭建

在本次实验中我使用了本地服务器。我们可以使用Springboot，flask等在localhost上搭建Web服务器。不过最近恰好在研究博客搭建相关内容，这里通过使用Hexo搭建静态博客的比较“自动化”的方式在本机搭建Web服务器。

通过下面命令安装`hexo`环境。(其实还需要安装`npm`环境，不过在此就略去了)。

```shell
sudo npm install -g hexo-cli
```

新建博客目录结构如下：

```shell
my_hexo_test_server
.
├── _config.yml
├── db.json
├── node_modules
		├──...
├── package-lock.json
├── package.json
├── public
├── scaffolds
├── source
│   └── _posts
└── themes
    └── wireshark
        ├── _config.yml
        ├── layout
        │   ├── index.ejs
        │   ├── layout.ejs
        │   └── post.ejs
        └── source
            ├── css
            ├── img
            └── js
```

`_config.yml`中`theme`改为自定义的`wireshark`，在`index.ejs`中写入网页内容：

```html
<!DOCTYPE html>
<html>

<head>
    <title></title>
    <meta charset="utf-8">
</head>

<body>

    <h1>this is layout.ejs</h1>
    <h2> 2013599 田佳业</h2>
    <h3>计算机科学与技术</h3>
    <img src="img/test.png" alt="">


</body>

</html>
```
在终端执行
```shell
(base) ➜  my_hexo_test_server hexo g
(base) ➜  my_hexo_test_server hexo s
```

可以看到生成网页如下所示：

![image-20221026200601767](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210657935762_127_20221028232042709573_203_image-20221026200601767.png)

## Wireshark 分析TCP连接过程

由于服务器在本地，选择`Loopback:lo0`即可。

![image-20221026200751668](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210700374694_433_20221028232044366413_373_image-20221026200751668.png)

首先我们需要尝试找到TCP建立连接三次握手的位置。刷新网页，并输入`http`进行过滤，以隐藏其他无关的数据包。

![image-20221028173616526](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210701652648_872_20221028232045903947_824_image-20221028173616526.png)
找到第一个`GET`数据包。右键选中，`Follow stream`——`TCPstream`，显示握手信息。

![image-20221028174135897](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210702797226_521_20221028232048121868_131_image-20221028174135897.png)

### 三次握手

下面展示了三次握手的过程，并结合握手信息对照报文段进行分析：

![image-20221028175332107](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210704135079_964_20221028232049728449_411_image-20221028175332107.png)



- 第一次握手：建立连接时，客户端发送SYN包（Seq=j）到服务器，并进入SYN_SENT状态，等待服务器确认；SYN：同步序列编号（Synchronize Sequence Numbers）。    

捕获的第一段报文如下所示：

![image-20221028174837176](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210705714512_581_20221028232051494572_180_image-20221028174837176.png)

博客示例网页运行在`localhost:4000`，目的端口号匹配。同时可以看到Flag字段值为2，也即第二位SYN字段为1，其余全0。

-  第二次握手：服务器收到SYN包，必须确认客户的SYN（ACK=j+1），同时自己也发送一个SYN包（SYN=k），即SYN+ACK包，此时服务器进入SYN_RECV状态；        

第二段报文如下所示：

![image-20221028175454476](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210707089949_308_20221028232054080895_215_image-20221028175454476.png)

 从端口号可以看出，这是服务器发给客户的。Flag字段为ACK和SYN。这次我们注意一下确认序列号的值。从[Wireshark Wiki](https://wiki.wireshark.org/TCP_Relative_Sequence_Numbers)我们可以了解到，考虑到可读性其在列表中采用了相对序列号。在详细信息中可以看到原始(`raw`)序列号。我们可以看到：

第一次握手客户端`Sequence Number (raw):2932922641`（Seq=j）

第二次握手服务器端`Acknowledgment number (raw):2932922642`（ACK=j+1），与示意图中的握手过程的过程相符。

- 第三次握手：客户端收到服务器的SYN+ACK包，向服务器发送确认包ACK(ack=k+1），此包发送完毕，客户端和服务器进入ESTABLISHED（TCP连接成功）状态，完成三次握手，客户端与服务器开始传送数据。

同样可以验证ACK(ack=k+1）。

![image-20221028180628702](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210708887036_756_20221028232056001837_289_image-20221028180628702.png)

也可对照查看右侧的十六进制报文源码。

#### 过程理解

<p class="note note-primary">为什么是三次握手？</p>

需要以最小的代价验证会话双方的收发功能正常:

- 第一次握手成功：说明客户端的数据可以被服务端收到，说明客户端的发功能可用，说明服务端的收功能可用。但客户端自己不知道数据是否被接收。

- 第二次握手成功：说明服务端的数据可以被客户端收到，说明服务端的发功能可用，说明客户端的收功能可用。同时客户端知道自己的数据已经正确到达服务端，自己的发功能正常。但是服务端自己不知道数据是否被接收。

- 第三次握手成功：说明服务端知道自己的数据已经正确到达客户端端，自己的发功能正常。至此服务成功建立。

<p class="note note-primary">为什么每次连接的序列号都不同？</p>

避免新老连接混淆

#### Syn洪泛攻击

在 TCP 连接的三次握手过程中，我们假设发生以下情况：

一个用户向服务器发送了 Syn报文后突然死机或掉线, 则服务器在发出 SYN 和ACK 应答报文后，客户端无法及时答复，导致服务器无法收到客户端的 ACK 报文( 即第三次握手无法完成) 。

这种情况下服务器端一般会重试并等待一段时间后丢弃这个未完成的连接, 称为**半连接握手状态。**

攻击者只需要向服务端发送大量的TCP请求连接而不进行第三次回应，就会出现大量的这种半握手状态的连接, 在服务器产生很多的请求队列, **由于第一次握手时服务端就已经为客户端开辟了接收缓冲区**，大量的请求最后的结果往往是堆栈溢出崩溃,  服务器也将忙于处理攻击者伪造的TCP连接请求而无暇理睬客户的正常请求, 此时服务器失去了对客户端的响应, 从而达到SynFlood攻击的目的。

[DoS攻击之Syn洪泛攻击原理及防御](https://zhuanlan.zhihu.com/p/457884093)

### 四次挥手

左边的实线连起来的表示同一次会话发生的各个阶段。沿着这条线走到最底端，可以看到四次挥手的过程。

![image-20221028181245513](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210711202693_873_20221028232058311718_623_image-20221028181245513.png)

结合TCP连接关闭的过程，可以看到第81到84个报文是挥手的过程。分析方式与握手类似，在此不再赘述。

![image-20221028181501786](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210712345252_558_20221028232100061679_207_image-20221028181501786.png)

另外，其实两端中的任何一个都可以主动提出关闭连接。只是通常情况下是客户端。

#### 过程理解

<p class="note note-primary">第二次挥手和第三次挥手一定是紧挨着的吗？
</p>

不一定。这时候只是表示A不再发送数据。服务器仍可在这两次挥手中间发送一些数据。
<p class="note note-primary">为什么第四次挥手后A不能立刻释放资源？
</p>
A并不知道B有没有正确的收到了A的ACK。正常情况下什么也不会发生。但如果没收到，B应当重传FIN，A得知道
<p class="note note-primary">为什么要等两倍MSL？
</p>
无论是否正常，A都需要等待，要取这两种情况等待时间的最大值，以应对最坏的情况发生，这个最坏情况是：
去向ACK消息最大存活时间（MSL) + 来向FIN消息的最大存活时间(MSL)。

<p class="note note-primary">一定要四次挥手吗？</p>

![image-20221102103437478](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210713552048_108_20221102112611088782_354_image-20221102103437478.png)

![image-20221102103222135](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210714695223_822_20221102112614834681_752_image-20221102103222135.png)

客户端和服务端的生命周期总结如下：

![image-20221028181827531](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210715568267_759_20221028232101334092_481_image-20221028181827531.png)

![image-20221028181835974](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210717454207_339_20221028232103339683_762_image-20221028181835974.png)

### 传输窗口

#### TCP Window Scale

在 TCP刚被发明的时候，全世界的网络带宽都很小，所以最大接收窗口被定义成 65535字节。随着硬件的革命性进步， 65535字节已经成为性能瓶颈了，怎么样才能扩展呢？ TCP头中只给接收窗口值留了 16 bit，肯定是无法突破 65535 （$2^{16} − 1$）的。 1992年的 RFC 1323中提出了一个解决方案，就是在三次握手时，把自己的 Window Scale信息告知对方。由于 Window Scale放在 TCP头之外的 Options中，所以不需要修改 TCP头的设计。 Window Scale的作用是向对方声明一个 Shift count，我们把它作为 2的指数，再乘以 TCP头中定义的接收窗口，就得到真正的 TCP接收窗口了。

这对应于Wireshark中的Caculated window size，如下图所示。

![image-20221028184429901](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210719179687_261_20221028232105453916_456_image-20221028184429901.png)



## Http传输分析

![image-20221028190921283](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210720298497_440_20221028232107541741_783_image-20221028190921283.png)

以下是前三个HTTP传输报文。

![image-20221028191110711](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210721857050_893_20221028232109214457_454_image-20221028191110711.png)

查看第一次客户端向服务器发送GET请求，含有浏览器请求头以及请求行。GET方法没有请求体。

![image-20221028190632604](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210723036742_240_20221028232111055813_462_image-20221028190632604.png)

从右边解析出的明文可以看出HTTP是采用ASCII码进行传输的。

之后请求成功，返回200状态码及HTML。

![image-20221028191208877](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210725379619_811_20221028232113806376_581_image-20221028191208877.png)

分析文本的十六进制编码：

```
0000   20 20 20 20 3c 68 32 3e 20 32 30 31 33 35 39 39
0010   20 e7 94 b0 e4 bd b3 e4 b8 9a 3c 2f 68 32 3e 0a
```

第一行末尾可以看到是我的学号`2013599`的ASCII码。

中文采用的是Unicode编码。具体方式为：

>
 将需要转码的字符，按指定编码方式（默认使用UTF-8编码）转化为字节流，每个字节按16进制表示，并添加%组成一个percent编码。
> 

给第二行每个字节前加%后用UrlDecode解码，可以还原出我的名字。

![image-20221028193717733](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210728206705_896_20221028232117064239_862_image-20221028193717733.png)

再之后请求图片：

同时我们可以看到图片信息也请求成功。

![image-20221028194251309](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%BA%8C_Wireshark%E5%88%86%E6%9E%90%E4%BA%A4%E4%BA%92%E8%BF%87%E7%A8%8B/20230828210729172278_543_20221028232118651904_458_image-20221028194251309.png)

> 在 `vim` 内调用 `:%!xxd` 命令，其实就是调用系统的 `xxd` 命令，对打开的内容进行16进制转换。