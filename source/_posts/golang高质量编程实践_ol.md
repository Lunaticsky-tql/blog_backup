---
title: Go 高质量编程实践
categories: 笔记
tags:
  - Go
abbrlink: 2118
---
# Go编码规范

最近正在阅读`Effective C++`和`Effective Modern C++`，其中的很多条款都值得反复阅读并牢记，理解其中的原理对用好C++这把瑞士军刀受益匪浅。相应的，最近也发现了[`Effective go`](https://go.dev/doc/effective_go)，就如何编写清晰、地道的 Go 代码提供了一些技巧。它是对 [语言规范](https://go-zh.org/ref/spec)、 [Go 语言之旅](https://tour.golang.org/) 以及 [如何使用 Go 编程](https://go-zh.org/doc/code.html) 的补充说明。得益于Go的简洁，其编程规范比C++要简洁清晰很多。结合Go的官方指导以及实践，对高质量编程的一些方面进行了总结。

## 高质量编程简介

实现同样的功能，可能大到编程范式，小到实现细节，有很多种编码的风格和方式供我们选择。编写的代码能够达到正确可靠、简洁清晰的目标需要我们不断的在实践中修炼。不管是面试还是在实际的项目开发中，都需要我们对高质量的代码有所追求。

在课件中提到的三个主要的判断维度：

- 各种边界条件是否考虑完备
- 异常情况处理，稳定性保证
- 易读易维护

编程原则：

- 简单性
- 可读性
- 团队生产力

前面两点原则容易理解，关于最后一点，因为我们编程其实更重要的是一个团队合作的一个过程，团队的整体工作效率也是非常重要的。比如字节内部采用Go语言，其实最有特点的一点就是，Go语言的简洁性对于降低新成员上手项目代码成本很有帮助。

在实际的工程项目当中，如果有一些复杂的一些程序逻辑，其他人基本上就不太敢动，尤其是有一些历史的一些逻辑的话，写得比较复杂，可能又难以理解，新接手的人就没办法明确的知道我们这些调整会造成的影响的一些范围，可能会产生什么样的问题。这样的话就会让代码变得难以维护。这些难以维护的这些逻辑在排查问题的时候也会带来不少麻烦。而如果我们的代码比较清晰的话，那么就算出现了一些问题，我们也能通过现象，或者代码逻辑，快速分析排查定位到这些问题。能够提升整体的整个项目开发环节的效率。所以说在写代码时考虑对于团队生产力带来的影响，也是高质量编程原则给我们带来的好的习惯。

## 编码规范

如何编写高质量 Go 代码

### 代码格式

格式化问题总是充满了争议，但却始终没有形成统一的定论。虽说人们可以适应不同的编码风格，但抛弃这种适应过程岂不更好？**若所有人都遵循相同的编码风格，在这类问题上浪费的时间将会更少**。问题就在于如何实现这种设想，而无需冗长的语言风格规范。

在 Go 中我们另辟蹊径，**让机器来处理大部分的格式化问题**。`gofmt` 程序（也可用 `go fmt`，它以包为处理对象而非源文件）将 Go 程序按照标准风格缩进、 对齐，保留注释并在需要时重新格式化。

### 注释

```go
Good code has lots of comments, bad code requires lots of comments
好的代码有很多注释，坏代码需要很多注释 
         ---Dave Thomas and Andrew Hunt
```

- 注释需要解释代码实现的原因。

  适合解释代码的外部因素

  提供额外上下文

  ```go
  switch resp.StatusCode {
  // ...
  case 307, 308:
  redirectMethod = reqMethod
   shouldRedirect = true
   includeBody = true
   if ireq.GetBody == nil && ireq.outgoingLength() != 0 {
    // We had a request body, and 307/308 require
    // re-sending it, but GetBody is not defined. So just
    // return this response to the user instead of an
    // error, like we did in Go 1.7 and earlier.
    shouldRedirect = false
   }
  }
  ```

- **注释应该解释代码什么情况会出错**
  
  在调用方在使用这个方法的时候，可能它不需要实际的去特别细究里面的代码，d但是注释有必要提供需要注意的点，在用户或者自己使用的时候，如果是注意到相关这些点的话，它就能够更正确的来处理相关的一些结果。
  
- 公共符号始终要注释。对于公共符号都需要有注释说明

- 注释最好是**完整的句子**，这样它才能适应各种自动化的展示。

  第一句应当以**被声明的东西开头**，并且是**单句的摘要**。

  ```go
  // Compile parses a regular expression and returns, if successful,
  // a Regexp that can be used to match against text.
  func Compile(str string) (*Regexp, error) {
  ```

  若注释总是以名称开头，`go doc` 命令的输出就能通过 **grep** 变得更加有用。假如你记不住 Compile 这个名称，而又在找正则表达式的解析函数（”解析”意味着关键词为 parse），那就可以运行

  ```shell
  $ go doc -all regexp | grep -i parse
  ```

  快速查找。

### 命名

#### 变量

Go约定使用驼峰命名，而不是下划线。其他一些通用的命名原则：

- 简洁胜于冗长
- 缩略词全大写，但当其位于变量开头且不需要导出时，使用全小写
  - 例如使用 `ServeHTTP` 而不是 `ServeHttp`
  - 使用 `XMLHTTPRequest` 或者 `xmlHTTPRequest`
- 变量距离其被使用的地方越远，则需要携带越多的上下文信息。全局变量在其名字中需要更多的上下文信息，使得在不同地方可以轻易辨认出其含义

#### 接口

按照约定，**只包含一个方法的接口**应当以该方法的名称加上 `-er` 后缀来命名，如 `Reader`、`Writer`、`Formatter`、`CloseNotifier` 等。

诸如此类的命名有很多，遵循它们及其代表的函数名会让事情变得简单。Read、Write、Close、Flush、 String  等都具有典型的签名和意义。为避免冲突，请不要用这些名称为你的方法命名，除非你明确知道它们的签名和意义相同。反之，若你的类型实现了的方法，**与一个众所周知的类型的方法拥有相同的含义，那就使用相同的命名**。请将字符串转换方法命名为 `String` 而非 `ToString`。

#### 函数

- 函数名不携带包名的上下文信息，因为包名和函数名总是成对出现的
- 函数名尽量简短
- 当名为 foo 的包某个函数返回类型 Foo 时，可以省略类型信息而不导致歧义
- 当名为 foo 的包某个函数返回类型 T 时（T 并不是 Foo），可以在函数名中加入类型信息

#### 包名

- 只由小写字母组成。不包含大写字母和下划线等字符
- 简短并包含一定的上下文信息。例如 schema、task 等
- 不要与标准库同名。例如不要使用 sync 或者 strings

一个约定就是**包名应为其源码目录的基本名称**。在 `src/pkg/encoding/base64` 中的包应作为 `"encoding/base64"` 导入，其包名应为 `base64`，而非 `encoding_base64` 或 `encodingBase64`。

包的导入者可通过包名来引用其内容，因此包中的可导出名称可以此来避免冲突。（请勿使用 `import .` 记法，它可以简化必须在被测试包外运行的测试，除此之外应尽量避免使用。这个原则在其他语言中也是通用的。）例如，`bufio` 包中的缓存读取器类型叫做 `Reader` 而非 `BufReader`，因为用户将它看做 `bufio.Reader`，这是个清楚而简洁的名称。此外，由于被导入的项总是通过它们的包名来确定，因此 `bufio.Reader` 不会与 `io.Reader` 发生冲突。同样，用于创建 `ring.Ring` 的新实例的函数（这就是 Go 中的构造函数）一般会称之为 `NewRing`，但由于 Ring 是该包所导出的唯一类型，且该包也叫 ring，因此它可以只叫做 `New`，它跟在包的后面，就像 `ring.New`。使用包结构可以帮助你选择好的名称。

另一个简短的例子是 `once.Do`，`once.Do(setup)` 表述足够清晰，使用 `once.DoOrWaitUntilDone(setup)` 完全就是画蛇添足。**长命名并不会使其更具可读性。一份有用的说明文档通常比额外的长名更有价值**。

### 控制流程

关于控制流程，和其他语言类似，避免嵌套，保持正常流程清晰。遵循线性原理，处理逻辑尽量走直线， 避免复杂的嵌套分支。正常流程代码沿着屏幕向下移动先处理异常情况并return掉是个好习惯，可以减少嵌套的同时提高对异常处理的意识，后续产生可能出现的新的异常时也便于修改。

### 错误与异常处理

在工程实践中，错误和异常处理大概是最重要的部分。Go语言的异常处理和其他主流编程语言风格相差较大，既有`defer`这种优雅的压栈处理回调行为，以便正确管理资源的支持，也有喜闻乐见的`if err!=nil`。下面对Golang的错误处理进行更深入的认识。

#### 简单错误

简单错误指仅出现一次的错误，且在其他地方不需要捕获该错误

优先使用 errors.New 创建匿名变量来直接表示简单错误

如果有格式化的需求，使用` fmt.Error`

```go
func defaultCheckRedirect(req *Request, via []*Request) error {
	if len(via) >= 10 {
		return errors.New("stopped after 10 redirects")
	}
	return nil
}
```

#### 错误的 Wrap 和 Unwrap

将一个 error 嵌套进另一个 error 中，从而生成一个 error 的跟踪链

从 Go1.13 后，可以在 `fmt.Errorf` 中使用 `%w` 关键字来将一个错误 wrap 至其错误链中

```go
list, _, err := c.GetBytes(cache.Subkey(a.actionID, "srcfiles"))
if err != nil {
	return fmt.Errorf("reading srcfiles list: %w", err)
}
```

#### 错误判定

- 使用 `errors.Is` 可以判定错误链上的所有错误是否含有特定的错误

```go
data, err = lockedfile.Read(targ)
if errors.Is(err, fs.ErrNotExist) {
// Treat non-existent as empty, to bootstrap the "latest" file
// the first time we connect to a given database.
return []byte{}, nil
}
```

- 在错误链上获取特定种类的错误，使用 `errors.As`

```go
  if _, err := os.Open("non-existing"); err != nil {
  		var pathError *fs.PathError
  		if errors.As(err, &pathError) {
  			fmt.Println("Failed at path:", pathError.Path)
  		} else {
  			fmt.Println(err)
  		}
  	}
```

#### panic

- 不建议在业务代码中使用 panic，若问题可以被屏蔽或解决，最好就是让程序继续运行而不是终止整个程序。
- 如果当前 goroutine 中所有 deferred 函数都不包含 recover 就会造成整个程序崩溃
- 当程序启动阶段发生不可逆转的错误时，可以在 init 或 main 函数中使用 panic

#### recover

- recover 只能在被 defer 的函数中使用，嵌套无法生效，只在当前 goroutine 生效
- 如果需要更多的上下文信息，可以 recover 后在 log 中记录当前的调用栈。

### 总结

上述内容仅是个人结合最近的学习内容和Effective Go总结出的自己认为较重要的部分记录，以便回顾和提醒。深入掌握一门语言还是要靠阅读第一手材料和动手实践。
