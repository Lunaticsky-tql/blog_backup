---
title: Go 刷题快速入门
categories: 笔记
date: 2023-08-23 10:00:00
tags:
  - Go
abbrlink: 41936
---
# Go 刷题快速入门

这篇文章讲述使用Golang刷题时遇到的关于输入输出和数据结构的常见问题，并在必要时进行相关知识点的讲解，方便刚入门Go进行刷题实践时进行查阅和学习理解。

## 输入输出

如果是在力扣这类核心代码模式的平台，就和写其他语言一样，不需要去关心输入输出的模式。但当下大部分公司的笔试算法题都是采用的ACM模式。因此若希望在笔试中展现自己的Golang编程能力，还是需要熟悉常见的输入输出格式。

### 读整数

这里我们以`a+b`为例说明。

#### 每行数字固定

> 输入描述:
> 输入包括两个正整数 a,b(1 <= a, b <= 1000),输入数据包括多组。
>
> 输出描述:
> 输出a+b的结果
>
> 输入例子1:
> 1 5
> 10 20
>
> 输出例子1:
> 6
> 30

最简单的情况。`fmt.Scan`返回成功读取的item数以及`err`。这里由于仅仅是算法示例题目，为了方便忽略了错误处理。当然用`fmt.Scanln`也是可以的。

Scan 从标准输入扫描文本，读取由空白符分隔的值保存到传递给本函数的参数中，换行符视为空白符。本函数返回成功扫描的数据个数和遇到的任何错误。如果读取的数据个数比提供的参数少，会返回一个错误报告原因。

而Scanln遇到换行才停止扫描。最后一个数据后面必须有换行或者到达结束位置。返回值和Scan含义一样。

下面给出示例代码：

```go
package main

import (
    "fmt"
)

func main() {
    a := 0
    b := 0
    for {
        n, _ := fmt.Scan(&a, &b)
        if n == 0 {
            break
        } else {
            fmt.Printf("%d\n", a + b)
        }
    }
}
```

#### 每行数字不固定，但知道数量

> 输入描述:
> 输入数据有多组, 每行表示一组输入数据。
> 每行的第一个整数为整数的个数n(1 <= n <= 100)。
> 接下来n个正整数, 即需要求和的每个正整数。
>
> 输出描述:
> 每组数据输出求和的结果
>
> 输入例子1:
> 4 1 2 3 4
> 5 1 2 3 4 5
>
> 输出例子1:
> 10
> 15

同样的道理，不赘述。

```go
package main

import(
    "fmt"
)

func main(){
    var t,crr,sum int
    for {
        n,_ := fmt.Scan(&t)
        if n == 0{
            break
        }else{
            sum = 0
            for i:=0;i<t;i++{
                fmt.Scan(&crr)
                sum += crr
            }
            fmt.Println(sum)
        }
    }
    
}
```

#### 每行数字不固定，也不知道数量

这个时候我们需要一整行一整行地读，这时需要用到bufio包，还是需要格外记忆一下。

```go
package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
)

func main() {
    inputs := bufio.NewScanner(os.Stdin)
    for inputs.Scan() {  //每次读入一行
        data := strings.Split(inputs.Text(), " ")  //通过空格将他们分割，并存入一个字符串切片
        var sum int
        for i := range data {
            num, _ := strconv.Atoi(data[i])   //将字符串转换为int
            sum += num
        }
        fmt.Println(sum)
    }
}
```

补充一个C++的实现，用到了`stringstream`。

另外需要提醒的是，`stringstream`构造函数会特别消耗内存，似乎不打算主动释放内存(或许是为了提高效率)，但如果你要在程序中用同一个流，反复读写大量的数据，将会造成大量的内存消耗，因些这时候，需要适时地清除一下缓冲 (用 stream.str("") ，需要注意clear()仅仅清空标志位，并没有释放内存)

```C++
#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::string line;
    while (std::getline(std::cin, line)) {
        std::istringstream iss(line);
        int sum = 0;
        int num;

        while (iss >> num) {
            sum += num;
        }
        std::cout << sum << std::endl;
    }

    return 0;
}
```

### 读字符串

> 输入描述:
> 多个测试用例，每个测试用例一行。
>
> 每行通过空格隔开，有n个字符，n＜100
>
> 输出描述:
> 对于每组测试用例，输出一行排序过的字符串，每个字符串通过空格隔开
>
> 输入例子1:
> a c bb
> f dddd
> nowcoder
>
> 输出例子1:
> a bb c
> dddd f
> nowcoder

排序是我们算法设计中频繁使用的操作，因此在这里也捎带进行讲解和记录。

Go语言的 sort.Sort 函数不会对具体的序列和它的元素做任何假设。相反，它使用了一个接口类型 sort.Interface  来指定通用的排序算法和可能被排序到的序列类型之间的约定。这个接口的实现由序列的具体表示和它希望排序的元素决定，序列的表示经常是一个切片。

根据直觉，排序算法需要知道三个东西：序列的长度，表示两个元素比较的结果，一种交换两个元素的方式。

```go
  package sort
  type Interface interface {
      Len() int            // 获取元素数量
      Less(i, j int) bool // i，j是序列元素的指数。
      Swap(i, j int)        // 交换元素
  }
```

为了对序列进行排序，我们需要定义一个实现了这三个方法的类型，然后对这个类型的一个实例应用 sort.Sort 函数。

我们可以像任何其他语言一样灵活的自定义排序规则。但大部分情况中，只需要对字符串、整型等进行快速排序。根据优化热点行为的原则，Golang对Go语言中提供了一些固定模式的封装以方便开发者迅速对内容进行排序。因此在这个题目中我们可以简单的调用`sort.Strings`按字典序进行排序。同时，像C++一样，我们可以自定义排序函数，使其倒序排列：

```go
sort.Slice(a,func(i,j int)bool{return a[i]>a[j] })
```

`strings.Join`将切片连接成字符串。

```go
package main

import (
    "fmt"
    "bufio"
    "os"
    "strings"
    "sort"
)

func main(){
    input := bufio.NewScanner(os.Stdin)
    for input.Scan(){
        data := strings.Split(input.Text()," ")
        sort.Strings(data)
        fmt.Println(strings.Join(data, " "))
	}
}
```

## 数据结构

### 线性容器

Golang内置的切片以及其方便的操作，可以满足我们使用向量，栈和队列等需求。比如以经典的考察栈的运用的[有效的括号](https://leetcode.cn/problems/valid-parentheses/)为例：

```go
func isValid(s string) bool {
    n := len(s)
    if n % 2 == 1 {
        return false
    }
    pairs := map[byte]byte{
        ')': '(',
        ']': '[',
        '}': '{',
    }
    stack := []byte{}
    for i := 0; i < n; i++ {
        if pairs[s[i]] > 0 {
            if len(stack) == 0 || stack[len(stack)-1] != pairs[s[i]] {
                return false
            }
            stack = stack[:len(stack)-1]
        } else {
            stack = append(stack, s[i])
        }
    }
    return len(stack) == 0
}
```

### 映射

Golang中的`map` 对应于C++中的`unordered_map`。下面主要讲述怎么使用`map`实现`set`和可排序的`map`。

`map`的 key 肯定是唯一的，而这恰好与 set 的特性一致，天然保证 set 中成员的唯一性。而且通过 map 实现 set，在检查是否存在某个元素时可直接使用 `_, ok := m[key] `的语法，效率高。

先来看一个简单的实现，如下：

```go
set := make(map[string]bool) // New empty set
set["Foo"] = true            // Add
for k := range set {         // Loop
    fmt.Println(k)
}
delete(set, "Foo")    // Delete
size := len(set)      // Size
exists := set["Foo"]  // Membership
```

通过创建 `map[string]bool `来存储` string `的集合，比较容易理解。而且判断元素是否存在可以很简单的写成`if set["foo"]`，一般做算法题的时候已经足够了，简单快捷。

但这里还有个问题，`map` 的 `value` 是布尔类型，这会导致 set 多占一定内存空间，而 `set` 不该有这个问题。如果我们对占用空间有要求，可以考虑利用空结构体。

在 Go 中，空结构体不占任何内存。

```go
unsafe.Sizeof(struct{}{}) // 结果为 0
```

因此可以实现如下例所示：

```go
func main() {
	set := map[string]struct{}{
		"pm": {},
		"fe": {},
		"rd": {},
	}
	if v, ok := set["rd"]; ok {
		fmt.Println("exist")
		fmt.Println("size:", unsafe.Sizeof(v))
	} else {
		fmt.Println("not exist")
	}
}
```

### 堆

Go的标准包`Container`中包含了常用的容器类型,包括`conatiner/List`,`container/heap`,`container/ring`。关于双向链表和环形链表，虽然在实际工作中也会经常用到，但在力扣中通常会给出链表的结构体，其他链表的操作和功能需要我们自己去实现；而ACM题目为了方便程序调试常常使用向量模拟链表，鉴于篇幅有限不在此详细讲解，也可以参阅[这篇文章](https://juejin.cn/post/7042729165400834056)进行更深入的了解。在此主要总结一下堆的实现和使用。

首先若是ACM模式，需要导包：

```go
package main

import (
	"container/heap"
	"fmt"
)
```

我们要使用go标准库给我们提供的heap，那么必须自己实现这些接口定义的方法，需要实现的方法如下：

- Len() int
- Less(i, j int) bool
- Swap(i, j int)
- Push(x interface{})
- Pop() interface{}

实现了这五个方法的数据类型才能使用go标准库给我们提供的heap，下面简单示例为定义一个IntHeap类型，并实现上面五个方法。

```go
type IntHeap []int  // 定义一个类型

func (h IntHeap) Len() int { return len(h) }  // 绑定len方法,返回长度
func (h IntHeap) Less(i, j int) bool {  // 绑定less方法
	return h[i] < h[j]  // 如果h[i]<h[j]生成的就是小根堆，如果h[i]>h[j]生成的就是大根堆
}
func (h IntHeap) Swap(i, j int) {  // 绑定swap方法，交换两个元素位置
	h[i], h[j] = h[j], h[i]
}

func (h *IntHeap) Pop() interface{} {  // 绑定pop方法，从最后拿出一个元素并返回
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func (h *IntHeap) Push(x interface{}) {  // 绑定push方法，插入新元素
	*h = append(*h, x.(int))
}
```

我们可以借此通过[前k个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/description)进行练习。当然这道题目更好的方法是采用快速划分的思想。

```go
func topKFrequent(nums []int, k int) []int {
    occ:=map[int]int{}
    for _,num:=range nums{
        occ[num]++
    }
    h:=&IHeap{}
    heap.Init(h)
    for key, value := range occ{
        heap.Push(h, [2]int{key, value})
        if h.Len() > k {
            heap.Pop(h)
        }
    }
    ret := make([]int, k)
    for i := 0; i < k; i++ {
        ret[k - i - 1] = heap.Pop(h).([2]int)[0]
    }
    return ret
}

type IHeap[][2]int
func (h IHeap) Len() int{
    return len(h)
}
func (h IHeap) Less(i,j int) bool{
    return h[i][1]<h[j][1]
}
func (h IHeap) Swap(i, j int){ 
    h[i], h[j] = h[j], h[i] 
}

func (h *IHeap) Push(x interface{}) {
    *h = append(*h, x.([2]int))
}

func (h *IHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}
```

### 总结

这篇文章仅仅是非常浅的总结了Go在算法题目中常用的接口和数据结构，很多地方总结的还不到位，更多知识点还是需要多刷题多实践。当然，从最常用的数据结构和接口中也能体会出很多Go语言的设计思想。尽管有喜闻乐见的手写`max`函数，但作为一门结合了Python的简洁与C++的严谨和性能的语言，还是很值得我们去学习的，也希望能够渐入佳境，成为训练有素的Gopher。
