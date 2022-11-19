---
title: 寄网-传输层
categories: 笔记
tags:
  - 寄网
abbrlink: 6389
---
# 寄网-传输层

## UDP

### 特点

![image-20221019101254797](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112829451012_857_image-20221019101254797.png)

![image-20221019102904831](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112833830874_553_image-20221019102904831.png)

> D

### 复用分用

<div class="note note-info">如何理解复用和分用？</div>


复用就是多个应用层进程汇聚成一个传输层进程（八车道变一车道）

分用就是反过来，传输层的多个进程相应的通向多个应用层进程（单车道变八车道）

通常复用针对发送，分用针对接收。

![image-20221019101337529](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112836012813_910_image-20221019101337529.png)

![image-20221019104559718](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112841055514_461_image-20221019104559718.png)
> B

### 报文结构和校验

![image-20221019102648654](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112842251316_209_image-20221019102648654.png)

<font color='Apricot'>算校验和的时候别忘了进位</font>

![image-20221019101834126](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112844925605_254_image-20221019101834126.png)

![image-20221019102038599](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112847899571_967_image-20221019102038599.png)

![image-20221019101153691](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112851148719_202_image-20221019101153691.png)

> B：长度包含头部，但不包含伪首部

最重要的“为什么”部分：

![image-20221019102522221](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112852360163_657_image-20221019102522221.png)

### 应用

![image-20221019103901732](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112854071267_984_image-20221019103901732.png)

## 可靠数据传输

### 目标

左边是希望对上层达到的抽象，右边是实际的情况。![image-20221019161257579](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112856140137_289_image-20221019161257579.png)

### 设计思路

![image-20221019162323429](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112857352548_948_image-20221019162323429.png)

#### rdt1.0

考虑最简单的情况，即底层信道是完全可靠的：

![image-20221019162337067](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112900136029_437_image-20221019162337067.png)

发送端：打包数据，直接调用底层信道进行传输；

接收端：拆包，将数据交给上层应用

#### rdt2.0

下层通道可能造成某些位出现错误（如:1变0，0变1)

![image-20221019163254576](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112902564743_320_image-20221019163254576.png)

<p class="note note-secondary">缩写：ACKnowledge character；Not AcKnowledge  character 肯定确认和否定确认。
同时为简便直白，对于package的翻译，用包代替分组</p>


##### 发送端：

仅当接收到ACK并离开该状态时才能发生rdt_send()事件。因此，在发送方确信接收方已正确接收当前分组之前肯定不会发送新数据。由于这种行为，rdt2.0这样的协议被称为停等 (stop-and-wait)协议。

##### 接收端：

上面表示如果packet受损发送NAK，下面表示如果package正确向上层传送数据并发送ACK

##### 存在的问题：

![image-20221019164147811](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112906743219_237_image-20221019164147811.png)

#### rdt2.1

![image-20221019165240189](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112909502820_948_image-20221019165240189.png)

答案是只需要1bit。因为如果发送端交替发送01包，接收端只需要知道收到的包是最近收到的(序号没变)还是新的(序号变了)。

按照这样的思路状态机如下：

发送端就是每当收到正确且是ACK的包的时候就准备发下一个，否则收到的是受损包或NAK就重发。

![image-20221019170813474](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112911602268_247_image-20221019170813474.png)

接收端：等待接受状态上面部分是发现包受损发NAK且等待，发现和上一次收到的包重复就发ACK(以让发送端发下一个包)，然后等待，也是什么也不做，不向下层传输信息(丢数据)

![image-20221019171058350](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112913795898_163_image-20221019171058350.png)

还有，接受端收到受损包其实不需要发NAK，再发一次上一次正确接收的ACK，发送端发现收到了对同一个包的两个ACK就知道接收端没正确接收这个包。

这其实就是rdt2.2

#### rdt2.2

![image-20221019171614203](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112917959019_890_image-20221019171614203.png)

在前面的基础上，看懂这种情况下的状态机就不再困难了。

![image-20221019183702448](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112919789535_361_image-20221019183702448.png)

接收端的主要变化是：在ACk中添加最后收到的包的序列和号，对应`make_pkt`第二个参数。

![image-20221019184436444](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112923670147_103_image-20221019184436444.png)

#### rdt3.0

##### 方案：

解决的问题：

![image-20221019185155113](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112929819897_715_image-20221019185155113.png)

添加了计时器的发送端：

![image-20221019185225064](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112931855615_706_image-20221019185225064.png)

接收端不需要改变。因为在2.3中已经实现了判断重复并丢弃了。

##### 实例

![image-20221019185429262](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112933551292_417_image-20221019185429262.png)

![image-20221019185440433](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112937343229_422_image-20221019185440433.png)

<p class="note note-primary">失序问题(二义性)是不能解决的，如下图所示</p>

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112939258493_256_image-20221026092203952.png" alt="image-20221026092203952" width="67%" height="67%" />

如果是上述情况，接收端不能辨别是重传的pkt1还是想要的pkt1.

<p class="note note-primary">怎么解决？
wifi用的是停等协议(和rdt3.0一样)，加入标志位表明是否是重传的包。如果接收端发现是接受过的，丢弃。但对于tcp性能优化后，就需要增加序号字段宽度</p>

### 流水线可靠数据传输

#### 停等协议的性能问题

![image-20221019185844985](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112941284045_123_image-20221019185844985.png)

发送时间相比传输时间是极短的

![image-20221019185852269](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112942732666_577_image-20221019185852269.png)

![image-20221019185917983](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112946369564_281_image-20221019185917983.png)

#### 流水线协议

##### Go-Back-N(GBN)

![image-20221019190539995](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112949459658_238_image-20221019190539995.png)

![image-20221019190656995](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112952032314_240_image-20221019190656995.png)

![image-20221019190714367](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102112956234191_425_image-20221019190714367.png)

![image-20221019190525409](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113000887288_715_image-20221019190525409.png)

GBN  协议看起来很浪费，因为它会丢弃一个正确接收（但失序）的包。但这样做是有道理的。因为数据必须按序交付。接收方可能缓存包 n + 1，但是，根据 GBN  重传规则，如果包 n 丢失，则这个包及第n + 1及之后的包迟早会再重传，所以，接收方只需要直接丢弃第n + 1个包即可。

这种方法的优点是**接收方不需要缓存任何失序分组**，**唯一需要维护的信息就是下一个按序接收的分组的序号**。缺点就是**随后对该分组的重传也许会丢失或出错，进而引发更多的重传。**

##### SR

与GBN的主要区别：

- 发送端：

  - 每个分组必须拥有其自己的逻辑定时器，因为超时发生后只能发送一个包。

  - 记录收到的ACK(因为不再重复发送)，但仅当收到的ACK的序号等于基序号`base`时窗口才会移动，移动到最小的未确认分组处(接收到的最大ACK+1)

- 接收端

  - 收到没收到过的包，在窗口口内，缓存并发ACK这个包的序号。(没收到的包在窗口外那肯定是接收端缓存放不下了)

  - 收到已经收到过的包，也发这个包的ACK。

<p class="note note-primary">第二种情况是什么情景？
收到已经收到过的包，那么只有一种情况，那就是接收端的ACK丢失，发送端不知道接收端这个包已经接受了，认为是中途丢了，就会再发一次。
为什么要返回 ACK？
加入按照上图中所示的发送方和接收方的序号空间，如果分组 send_base 的 ACK 没有从接收方传播回发送方，则发送方最终将重传分组 send_base，即使显然接收方已经收了该分组。如果接收方不确认该分组，则发送方窗口将永远不能向前滑动。</p>

![image-20221026102125865](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113003951000_939_image-20221026102125865.png)

然而，SR还是没解决类似的失序问题(虽然产生原因不一样，但导致的后果是一样的，即二义性)

![image-20221026102907586](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113005960023_920_image-20221026102907586.png)

我们能够直观的感觉到，只要**序号空间应大于等于窗口大小的2倍**，就能“错开”潜在的二义性区间。

### TCP

#### 段格式

![image-20221028201125789](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113010320175_456_image-20221028201125789.png)

<p class="note note-info">报头长度为20~60B，其中固定部分为20B。由于数据偏移字段的单位是4B，也就是说当偏移取最大时TCP首部长度为15×4=60B。</p>

#### 连接管理

![image-20221028202938399](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113012417879_161_image-20221028202938399.png)

> B

关于连接的建立和释放(三次握手，四次挥手)等内容，在实验作业中有详细的阐述。

---

Wireshark分析交互过程
https://lunaticsky-tql.github.io/posts/13596/

---

#### 传输过程

![image-20221028202640029](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113015046715_418_image-20221028202640029.png)

对于某一端来说，seq表示发送的报文段中数据部分的第一个字节在其发送缓存区中的编号，<font color='Apricot'>ack表示它期望收到的下一个报文段的数据部分的第一个字节在另一端的发送缓存区中的编号</font>。

![image-20221028202202650](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113021254308_149_image-20221028202202650.png)

> 同一个TCP报文中的seq和ack的值是没有联系。在B发给A的报文（捎带确认） 中，seq值应和A发向B的报文中的ack值相同，即201：ack值表示B期望下次收到A发出的报文段的第一个字节的编号，应是200+2=202。

![image-20221028203537641](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113022900814_335_image-20221028203537641.png)

> D

#### 重传场景

##### 超时重传

![image-20221102090515967](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113025521130_952_image-20221102090515967.png)

###### RTO设置重要性

RTO设置过大，对于丢失的报文段重传等待的时间过长，对于应用来说会引入较大的时延

RTO设置过小，可能会提前超时，引入不必要的重传，浪费带宽资源

###### 算法思路

最新样本赋予的权值大于老样本的权值（老化算法）

越新的样本越能更好地反映网络的当前状况

不仅如此，在实际情况中，网络拥塞情况会对网络时延有很大影响(体现在下面的DevRTT中)

启发式算法：

![image-20221102090928397](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113027424562_662_image-20221102090928397.png)

##### 快速重传

“事不过三”。如果收到重复ACK，至少说明客户端接收到的包失序了。如果一两个，可能只是包跑的不一样快，但多了就认为很有可能是丢了。

![image-20221102091321589](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113029523742_128_image-20221102091321589.png)

#### 流量控制

##### 滑动窗口

![image-20221102102355905](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113031785988_286_image-20221102102355905.png)

<p class="note note-primary">如果上图中黄×所在的ACK没收到咋办？会出现什么情况？如何解决？</p>

服务器不知道

> TCP使用滑动窗口机制来进行流量控制，其窗口尺寸的设置很重要，如果滑动窗口值设置得太小，那么会产生过多的ACK(因为窗口大可以累积确认，因此会有更少的ACK)，影响网络吞吐率；如果设置得太大，那么又会由于传送的数据过多而使路由器变得拥挤，浪费主机的存储资源，导致主机可能丢失分组。

##### 性能问题![image-20221102100002266](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/%E5%AF%84%E7%BD%91-%E4%BC%A0%E8%BE%93%E5%B1%82/20221102113034340991_595_image-20221102100002266.png)