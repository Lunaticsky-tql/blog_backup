---
title: 重新认识HTTP/2
categories: 笔记
tags:
  - 寄网
date: 2023-08-29 14:27:14
---
# 重新认识HTTP/2

可以说，我们浏览网页，下载资源，甚至克隆一个感兴趣的github仓库，都在与HTTP协议打交道。但是，在计算机网络课程和考研中HTTP都不作为重点去讲述，而在面试和实际工作中却经常需要接触。因此更深入的了解HTTP协议显得尤为重要。[上一节](https://lunaticsky-tql.github.io/posts/43947/)从HTTP的起源开始，重点深入探讨了HTTP/1.1新增特性的一些细节。本节将继续深入剖析HTTP/2的重要特性，并结合实践进行分析。

## 总览

HTTP/1.1 链接需要请求以正确的顺序发送，理论上可以用一些并行的链接（尤其是 5 到 8 个），但是带来的成本和复杂性堪忧。比如，HTTP  管线化（pipelining）就成为了 Web 开发的负担。如下图的形式，浏览器同时建立了5个TCP连接，这样确实可以“并行”的获取资源，避免了前面提到的队头阻塞问题，但每一次TCP都要三次握手四次挥手，而且内存要同时为5个链接开辟缓冲区，未免有些太浪费计算和存储资源。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142651995802_532_image-20230828223930304.png" alt="image-20230828223930304" width="67%" height="67%" />

为此，在 2010 年早期，谷歌通过实践了一个实验性的 SPDY  协议。这种在客户端和服务器端交换数据的替代方案引起了在浏览器和服务器上工作的开发人员的兴趣。明确了响应数量的增加和解决复杂的数据传输，SPDY  成为了 HTTP/2 协议的基础。

HTTP/2 在 HTTP/1.1 有几处基本的不同：

- HTTP/2 是二进制协议而不是文本协议。不再可读，也不可无障碍的手动创建，改善的优化技术现在可被实施。
- 这是一个多路复用协议。并行的请求能在同一个链接中处理，移除了 HTTP/1.x 中顺序和阻塞的约束。
- 压缩了标头。因为标头在一系列请求中常常是相似的，其移除了重复和传输重复数据的成本。
- 其允许服务器在客户端缓存中填充数据，通过服务器推送的机制来提前请求。

如果希望详尽的了解HTTP/2的细节，可以参见第一手资料[RFC7540](https://www.rfc-editor.org/rfc/rfc7540#page-4)。同时有[RFC7541](https://www.rfc-editor.org/rfc/rfc7541#page-4)。它主要单独讨论了 HTTP/2 的头部压缩 (HPACK) 问题。

## 实践基础

首先，现在的HTTP/2连接几乎都是 HTTP over TLS (即 HTTPS) 的。关于HTTPS，后面会详细介绍。这意味着，我们无法像HTTP/1.x版本一样，若不启用HTTPS，是可以用wireshark抓到明文包的。

但是，我们也不是没有办法。毕竟我们从浏览器的F12中就能看到HTTP/2的一些信息的，浏览器知道怎么解密这些信息。是的，否则我们也无法看到想看到的页面。

具体来说，Chrome 或者 Firefox 都支持: 如果设置了环境变量 `SSLKEYLOGFILE`, 就把 SSL/TLS 的` pre-master  secret key `写到设置的文件里面去. 之后可以使用这个` pre-master secret key` 文件在 wireshark  里面解密加密的流量。

由于我使用的是mac，这里以mac为例讲解配置方法，Windows和linux同理。

1.设置 `SSLKEYLOGFILE` 环境变量
可以简单在命令行使用 export 命令 (记得之后打开 Chrome 要在这个命令行)

```shell
export SSLKEYLOGFILE=~/ssh_key.log
```

2.在同一个命令行窗口打开 Chrome

```shell
open /Applications/Google\ Chrome.app/
```

3.在 Chrome 随便访问一个 https 的网站, 检查` ~/ssh_key.log` 是不是有内容

4.打开 wireshark 拦截流量或者 使用 tcpdump 有针对性的拦截

```shell
sudo tcpdump host 103.144.218.5 -w mydump.pcap 
```

5.打开 wireshark, 分析这个加密的流量. 
显示设置SSL/TLS 的 `pre-master secret key log` 文件:

菜单: preferences -> Protocols -> TLS

![image-20230828224802757](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142653033344_250_image-20230828224802757.png)

以我自己的电脑为例，在终端输入`ifconfig`，查看wifi对应网卡的ip地址，如下所示：

![image-20230829103603439](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142654100695_258_image-20230829103603439.png)

## HTTP2协商

由于 HTTP不同版本协议之间的交互方式存在差异, 当客户端和服务端通信时, 首先需要确定或称协商出所使用的 HTTP  协议版本, 对于存在多版本的协议的通信双方在握手时几乎都需要有协商 (Negotiation) 环节。

单纯的 HTTP 协议和 HTTP over TLS  (即 https) 协议对于 HTTP/2 的协商方式是不同的。在协议中以 h2 表示 HTTP over TLS, 以 h2c (c 是  clear 的首字母, 代表 clear text, 与 https 的加密报文相区分) 表示单纯的 HTTP 协议。二者的协商方式不同, 我们首先讨论 HTTP 的协商方式。

### HTTP协商

在这种情况下，HTTP/2的协商方式和HTTP/1/1的协商方式是相同的。由于之前没有讲述HTTP/1.1的协商方式，在这里再进行讲解。

在没有任何先验知识的情况下, 客户端若想要和服务端以 HTTP/2 协议进行通信, 那么客户端可以向服务端发送如下形式的 Request:

```http
GET / HTTP/1.1
Host: server.example.com
Connection: Upgrade, HTTP2-Settings
Upgrade: h2c
HTTP2-Settings: <base64url encoding of HTTP/2 SETTINGS payload>
```

客户端通过 `Upgrade` 头部字段列出所希望升级到的协议和版本，多个协议之间用英文逗号和空格（0x2C, 0x20）隔开。这里只有h2c。

如果服务端不同意升级或者不支持 `Upgrade` 所列出的协议，直接忽略即可（当成 HTTP/1.1 请求，以 HTTP/1.1 响应）；如果服务端同意升级，那么需要这样响应：

```http
HTTPHTTP/1.1 101 Switching Protocols
Connection: upgrade
Upgrade: h2c

[... data defined by new protocol ...]
```

可以看到，HTTP Upgrade 响应的状态码是 `101`，并且响应正文可以使用新协议定义的数据格式。

同时注意到，客户端发的头部有一个`HTTP2-Settings`字段。这个与HTTP/1.1有所不同。[RFC 7540](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc7540) 要求进行 HTTP/2 协商的客户端在 Header 中必须包含且仅包含一个 `HTTP2-Settings` 字段, 这个字段的值是  base64 编码的 HTTP/2 SETTINGS frame (将在下面具体讨论), 用于客户端向服务端传递一些配置参数,  若客户端在协商阶段发送的 Request 的 Header 中没有包含这个字段或多于一个该字段, 则服务端不能 (MUST NOT) 升级为  HTTP/2 协议。

### HTTPS协商

由于 TLS 的拓展字段支持 ALPN (Application-Layer Protocol Negotiation, 应用层协议协商), 即在进行 TLS 握手的同时本身可以通过 ALPN 知晓对方使用的应用层协议是什么，因此通过 ALPN 拓展字段已经协商好了双方使用的应用层协议, 因此当 TLS 握手完成后便可以进行 HTTP/2 的通信交互了。

这一点怎么验证呢？ALPN拓展是在TLS的Say Hello阶段的。我们找到它：

![image-20230829105143660](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142655503186_353_image-20230829105143660.png)

最后一行就是。

然后点开`Transmission Control Protocol`即TLS，然后找到`Handshake Protocol:Client Hello`，点开就可以看到一堆拓展。然后我们就能看到ALPN了。

![image-20230829105347601](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142656507459_485_image-20230829105347601.png)

分析得知，浏览器在进行SSL连接，第一次发送Client Hello包时，在扩展字段里携带浏览器支持的版本，其中 h2 代表浏览器支持http2协议。

相应的，服务器在返回Server Hello包时，如果服务器支持http 2，则会返回h2，如果不支持，则从客户端支持的协议列表中选取一个它支持的协议，一般为http/1.1。

![image-20230829105644589](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142657588930_231_image-20230829105644589.png)



在 HTTP/2 协议中, 客户端和服务端都需要发送 Connection Preface ，以便最终确认双方使用 HTTP/2 协议进行交互,  并且在 Connection Preface 中可以对协议参数做一些初始化的工作。对于客户端来说, 当收到服务端 101 状态码的响应 (通过 HTTP Upgrade 进行协议协商) 或 TLS 握手成功 (通过 TLS ALPN 进行协议协商) 后,  便立即开始发送 Connection Preface。

Connection Preface 的开头是一个固定的字节序列(可以认为这是一个魔数, 一般在设计网络协议时都会设置一个魔数以过滤掉不支持的数据), 这个值用字符串表示为 `PRI *  HTTP/2.0\r\n\r\nSM\r\n\r\n`, 在此序列后跟随发送一个可选的 SETTINGS frame,  其中可以设置一些协议参数(将在下面讨论), 服务端的 Connection Preface 不需要魔数, 但同样需要包含一个可选的  SETTINGS frame 用于设置服务端的协议参数, 无论是客户端还是服务端, 当收到不合法的 Connection Preface  都需要报告连接错误。

![image-20230829110305712](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142658796661_863_image-20230829110305712.png)

## HTTP/2 Stream

流(Stream) 是 HTTP/2 协议的核心, 因为在 HTTP/1.x 中, 所有的请求都是在单个 TCP 连接上顺序发送的, HTTP/2  引入了 Stream 的概念, Stream 实际上是一个逻辑概念, 是虚拟的, 并非真实存在的对象。

 一个 TCP 连接上可以同时存在多个 Stream, 这些 Stream 可以并发地传输数据这些数据被称作帧(frame)。因此实际上, HTTP/2 Stream 是对 TCP 连接的多路复用  (Multiplexing)。

在 frame 的结构中我们看到,  frame header 中有 Stream Identifier 字段, 用于指示该 frame 所属的 Stream 序号, 当一个  Stream Identifier 为 N 的 frame 在 TCP 链路上传输时, 我们就可以认为它是在 Stream N 上传输.  Stream 需要由一方主动创建, [RFC 7540](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc6455) 要求**由客户端初始化的 Stream, 其编号 (即 Identifier) 必须是奇数, 而由服务端初始化的 Stream,  其编号必须是偶数**。特别地, 编号为 0 的 Stream 是用来传输整个 (TCP) 连接的控制消息的。

![image-20230829112913643](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142659977825_226_image-20230829112913643.png)

在 HTTP/2 中, 每一个新创建的 Stream 的编号必须比已有的所有的 Stream 的编号都大, 当使用新编号的 Stream 时,  所有低于该编号的并且处于空闲 (Idle) 状态的 Stream 都会被隐式的关闭, 在一个 TCP 链接中, 流编号不能重复使用, 即新创建的 Stream 编号不能是之前用过的编号(即便是之前用过的编号并且已关闭也不允许再使用), 在 frame 中, 由于流编号只有 31 位,  因此对于一个 TCP 长连接来说, 存在流编号被用光的情形, 当流编号用尽时, 如果需要再创建一个新的 Stream, 对于客户端来说,  可以创建一个新的 TCP 连接, 对于服务端来说, 可以向客户端发送一个 GOAWAY frame, 强制客户端打开新的一个 TCP 连接。

### 流的生命周期

Flags 字段可以用来控制帧的状态。下图展示了一个流的生命周期。

![image-20230829115727462](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142701018586_639_image-20230829115727462.png)

其中`PUSH_PROMISE`帧是一种特殊类型的帧，用于服务器推送资源给客户端。**HTTP/2的推送机制**允许服务器在响应一个客户端请求时，主动推送其他相关的资源给客户端，从而提前加载可能需要的资源，以改善页面加载性能和用户体验。

图中Reserved状态表示，在流上发送PUSH_PROMISE帧会将这个流留存供以后使用。具体的说当服务器向客户端发送PUSH_PROMISE帧，通知客户端它将会推送一个新的关联流（promised stream），这个新流会被标记为`reserved (local)`状态。在接收到客户端的同意（或拒绝）之前，服务器会保留对该流的控制权。相应的，当客户端收到这个帧时候对于客户端来说这个新流就是`reserved (remote)`状态。

### 流控制

#### 流量控制

HTTP/2 在单个 TCP 连接上虚拟出多个 Stream, 多个 Stream 实现对一个  TCP 连接的多路复用, 为了合理地利用传输链路, 实现在有限资源内达到传输性能的最优化, 必须对 Stream 做一定的控制, HTTP/2  本身只在逻辑层面规定了流控制的语义, 具体的实现算法由协议的实现者自行决定, 类似于定义了一组抽象接口, 具体的实现交由程序员去完成,  HTTP/2 的流量控制有如下几个特点：

- HTTP/2 的流控制与 TCP 的流量控制有些类似, 但不完全相同, 双方发送 WINDOW_UPDATE frame 以字节为单位来指示自身所接受的窗口大小, 双方都必须遵守对方设置的窗口大小, [RFC 7540](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc6455) 规定的初始化窗口大小为 65535 个字节
- 只有 DATA frame 受流控制的约束, 对于其它类型的 frame 不受该规则限制, 从而确保控制类的 frame  不会因流控约束而无法(及时)发送, 并且 HTTP/2 的流控制双方都必须严格遵守, 流控制在 HTTP/2 中不能被关闭 (disable), 当发送方不需要进行流控制时可以发送 WINDOW_UPDATE frame 将窗口的值设置为最大值 ,  但它仍然需要遵守对方设置的窗口限制。

#### 优先级

由于在一个 TCP 上存在多个 Stream, 而底层的传输层连接只有一个,  为了更好地利用有限的资源, HTTP/2 对流引入了优先级的概念, 引入优先级一方面向对方表达自身希望对方为该流分配资源的权重, 另一方面,  对自身来说, 当资源有限时, 流的优先级可以用于决策优先发送哪个流上的 frame, 可以通过标记一个流依赖于另一个流的完成来表征它的优先级,  并且为依赖关系分配一个相对的权重, 举例来说, 若流 A 依赖于流 B, 则称流 A 是流 B 的从属流 (dependent stream), 流 B 是流 A 的父级流 (parent stream), 一个流可以被任意个其它流所依赖, 例如流 B, C 可以同时依赖于流 A,  它们都是流 A 的从属流, 可以用如下所示的图示来表示:

```text
   A                 A
  / \      ==>      /|\
 B   C             B D C
```

可以在创建流的时候通过 HEADERS frame (将在下面讨论) 指示该流所依赖的流, 当流创建完成以后也可以通过 PRIORITY frame  来改变流的优先级, 在设置流的依赖关系时, 可以在 frame header 中设置 exclusive flag 来指示该流的排他性,  在上面的例子中, 我们看到流 B C 同时依赖于 A, 若不设置 exclusive flag 我们可以继续创建流 D 使其与流 B C  一样都在同一级依赖于流 A, 而若设置了 exclusive flag, 那么流的层级依赖关系将如下所示:

```text
                     A
   A                 |
  / \      ==>       D
 B   C              / \
                   B   C
```

在这里例子中, 原先 B C 都依赖于流 A, 而创建流 D 时, 在 frame 中设置了 exclusive flag, 这样以来只有流 D 直接依赖于流 A, 而原先的流 B C 的父级流都将更改为流 D。

依赖的权重 (Weight) 用于决定流所能分配的资源(这个资源可能是多维度的, 如为该流分配的内存等), 在 HTTP/2 中,  流的权重是一个 1~256 的整数, 权重越大, 分配到的资源便越多, 举例来说, 假设流 B 和流 C 同时依赖于流 A, 流 B  的依赖权重为 4, 流 C 的依赖权重为 12, 当流 A 的操作都完成以后或流 A 处于阻塞状态暂时无法继续进行更多的操作, 在理想情况下, 流 B 分配到的资源应是流 C 分配到的资源总量的 $\frac{1}{3}$。

当然, 流的权重和优先级在 HTTP/2 中只是建议, 通信双方应该 (SHOULD) 尽可能遵守这些规则, 但并不强制,  通信的任何一方都不能强制要求对方必须按照流的优先级对流进行处理或严格按照权重比例进行资源分配, 任何流都有依赖的流,  没有显示指明依赖流的流都依赖于编号为 0x0 的流。

比如，下面请求CDN上相关js和css文件。

![image-20230829141914005](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142702230552_298_image-20230829141914005.png)

第一份javascript文件不指明依赖流，权重最高。

![image-20230829142038049](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142705943679_812_image-20230829142038049.png)

后面几个流依次依赖前面的流。

![image-20230829142143613](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142707262834_965_image-20230829142143613.png)

CSS文件流是js文件流的从属流，权重较低。

## HTTP/2 frame

我们在计网课上学过，HTTP/2是使用二进制分帧传输的。在这里便对帧涉及到的细节进行讲述。

在 HTTP/2 中, frame 是客户端和服务端数据传输的最小单元, 当 HTTP/2  Connection Preface 都发送校验完毕之后, 双方就可以正式开始以 frame 的形式进行数据交换, frame 由 Header 和 Payload 两部分构成, 其中 Header (注意区分 frame 的 Header 和 HTTP 协议本身的 Header)  的长度固定为 9 字节, Payload 的长度是可变的, frame 的结构[如下所示](https://datatracker.ietf.org/doc/html/rfc7540#page-12):

![image-20230829110616241](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142708629121_799_image-20230829110616241.png)

- Length 字段长度为 3 字节, 以字节为单位指示 frame 的 Payload 的长度(即该字段指示的长度不包含 9 字节的 frame header)
- Type 字段长度为 1 字节, 指示 frame 的类型
- Flags 字段长度为 1 字节, Flags 字段与 frame 的类型有关, 以 bit 位来表征特定类型 frame 的特定设置
- R 字段长度为 1 比特, 它是 Reserve 的首字母, 即该字段是保留字段, 目前必须设置为 0
- Stream Identifier 是 31 位的无符号整数, 它的值代表流编号, 当该字段非 0 时, 表示当前帧属于某个特定的 Stream , 当其为 0 时, 代表该帧是属于整个 TCP 连接的

因为 Length 字段的长度为 3 字节, 所以在 HTTP/2 中, 一个 frame 的最大长度为 $2^{24}$ 字节的 Payload + 9 字节的 header, 在实际交互中, 客户端和服务端任何一方都可以通过 SETTINGS frame 来设置自己所接受的 frame  payload 的最大长度, 这个长度的范围可以取$2^{14}$  到 $2^{24}-1$ (以字节为单位) 的区间内任意一个值,  当设置了该最大值时, 若在以后的通信中接收到的 frame 的 payload 超过之前的设定, 则接收方应发送  FRAME_SIZE_ERROR 错误, 尽管在 HTTP/2 中, frame payload 最大可以设置为 $2^{24}-1$  个字节的大小, 但对于时延敏感的 frame (如 RST_STREAM, 类似于 TCP 的 rst, 用于复位连接) 当 frame  数据过大时传输效率低下, 将会影响整体的性能。

以下面这个`SETTING`帧为例。这是一个没有载荷的SETTING帧，是客户端向服务器发ACK。

![image-20230829111247968](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142709689208_586_image-20230829111247968.png)

### DATA frame

![image-20230829123200882](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142710882929_634_image-20230829123200882.png)

我们看到第一个字段是`Pad Length`。它是干什么的呢？frame 可以选择性的传输 padding, padding 用于隐藏实际的 payload 长度，以便达到**隐私保护**的目的。观察者可能通过观察数据包大小来推测出某些请求的内容。通过在帧中添加填充数据，可以使所有请求的数据包大小相似，从而增强用户数据的隐私保护。

当需要使用 padding 时, 需要在 frame header 中设置标志, padding 的标志值为 `0x8`, 在设置标识时可以将所有标识位按位或, 写到标识位对应的  offset 上, 它的标志值为` 0x8` 代表需要将标识字段的第四位二进制位设置成 1。

当设置了 padding 标识后, `Pad  length` 字段指示 padding 的长度, 而 Padding 字段便是相应长度的数据, 这里的数据是没有任何语义的, 需要都设置为 0, 接收方若收到设置了 padding 标识的 DATA frame, 并且它的 padding 字段非 0 可以返回 `Connection Error`。若 Pad length 指示的长度与实际的 Padding 长度不匹配, 则接收方应立即报告 `Connection Error`。

以下面这个博客css文件的DATA帧为例，就没有padding。

![image-20230829123341595](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142711803565_423_image-20230829123341595.png)

前面讲到了流的生命周期，DATA frame 只能在状态为 open 或 half-closed (remote) 状态的 Stream 上发送, 当接收方收到不属于这两种状态的 Stream 的 DATA frame 时, 应立即报告 `STREAM_CLOSED` 的 `Stream Error`

### HEADERS frame

HEADERS frame 用来初始化一个新的 Stream 或传输 HTTP/2 Header Block (将在下面讨论), Header frame 的 frame type 为 0x1, 它的 Payload 结构[如下所示](https://datatracker.ietf.org/doc/html/rfc7540#page-32):

![image-20230829114341902](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86HTTP2/20230829142713340881_806_image-20230829114341902.png)

`Pad Length`前面已经讲述过，不再赘述。

`E`, 长度为 1 比特, 作为一个放在 Payload 中的标志位, 用来指示是否开启 exclusive flag 。当且仅当在 frame 的 header 中设置了 PRIORITY flag 时, 该字段有效。

`Stream Dependency`, 长度为 31 比特, 用来指示该流所依赖的流 。

`Weight`, 长度为 1 字节, 用于设置依赖的权重。值的有效范围为 1 ~ 256, 当且仅当在 frame 的 header 中设置了 PRIORITY flag 时, 该字段有效。

`Header Block  Fragment`是指头部块片段，它是用于在头部压缩上下文中传输HTTP头部信息的一部分。HTTP/2使用了HPACK压缩算法来减少头部信息的传输大小，从而提高传输效率。在头部信息较大时，可以将头部分成多个片段，每个片段被称为"Header Block Fragment"。头部压缩技术的细节还是有些复杂的，后面会专门拎出来讲。

简单的说，HTTP/2的头部压缩使用了静态表（Static Table）和动态表（Dynamic  Table）来存储已经发送或接收的头部字段，以便更有效地传输这些字段。当发送或接收头部信息时，可以参考这些表来减少重复传输。如果头部信息太大，就可以将其分割成多个片段，在传输过程中逐个发送。

## 总结

综上，这一部分的内容对HTTP/2的流机制和分帧传输方式进行了非常详尽的介绍。在其中也简单的介绍了服务器推送相关的内容。可以通过[这个网站](https://http2.akamai.com/demot)体会HTTP/1.1和HTTP/2的性能差距，当然也可以对此进行抓包分析。这一部分尚未介绍的是头压缩机制。后面将会展开讲述。