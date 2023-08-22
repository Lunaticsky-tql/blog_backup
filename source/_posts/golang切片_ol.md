---
title: Go 语言入门指南：slice使用解析
categories: 笔记
tags:
  - Go
abbrlink: 29701
---
# Go 语言入门指南：slice使用解析

在讲slice使用之前，先来看一下切片的结构, 理解slice的底层存储对得心应手的使用slice来说是必须的。切片的数据结构是一个结构体, 结构体内有三个参数, pointer指向底层数组中的某个元素, length表示长度, cap表示最大容量。

```go
type slice struct {
    array unsafe.Pointer  //底层数组
    len   int   //长度
    cap   int   //容量
}
```

此部分源码位于[`src/runtime/slice.go`](https://go.dev/src/runtime/slice.go)。

### 空切片和nil切片

在开发中我们会经常遇到这种情况, 我们想返回长度为零的切片时, 有时返回的是nil, 有时返回的是空切片, 这两者有什么区别呢, 我们到底应该使用哪一种呢。

```go
func main() {
    // 定义nil切片
    var s1 []string
    //定义空切片
    s2 := make([]string, 0)
    s3 := []string{}
    fmt.Printf("%#v,Len:%d,cap:%d,ptr:%p,nil=%t\n", s1, len(s1), cap(s1), s1, nil == s1)
    fmt.Printf("%#v,Len:%d,cap:%d,ptr:%p,nil=%t\n", s2, len(s2), cap(s2), s2, nil == s2)
    fmt.Printf("%#v,Len:%d,cap:%d,ptr:%p,nil=%t\n", s3, len(s3), cap(s3), s3, nil == s3)
}
```

打印结果：

```go
[]string(nil),Len:0,cap:0,ptr:0x0,nil=true
[]string{},Len:0,cap:0,ptr:0x10438c108,nil=false
[]string{},Len:0,cap:0,ptr:0x10438c108,nil=false
```

 现在分别打印这三个切片, 可以发现长度容量相同且都为零, 那两者有什么不同呢。

第一点切片的指针指向不同。`nil`切片通过`var`关键词定义, 仅声明未初始化`pointer`指针为`nil`空指针, 空切片通过`make`关键词定义声明并初始化了空间, 由于初始化的长度为零, `pointer`指针指向了空结构体的地址, 还未指向底层数组。

第二点是否等于`nil`。这个是显然的。但这也说明判断一个切片是否为空时, 我们应该通过长度是否为零来判断, 而不是通过是否为nil而来判断。

第三点, 转码`json`后不同。对切片进行`json`编码, `nil`切片会被编码成当空, 切片会被编码成空数组。这一点在前后端交互时值得注意。

`make`参数第一个是数据类型，第二个是 len ，第三个是 cap 。如果不传入第三个参数，则 `cap=len`。

### slice传递

下面看一段代码：

```go
func main() {
	var s []int
	for i := 0; i < 3; i++ {
		s = append(s, i)
	}
	modifySlice(s)
	fmt.Println(s)
}
```

一眼就能看出来，肯定是打印[1024,1,2,2048]吧。其实不是，运行这段代码后只会打印出 [1024,1,2]。原因就是slice 是按值传递的，这里传递的是s底层的数组的指针。

但是仅仅是共享了slice底层的数组，slice底层的`len`和`cap`都是被复制了一份，所以在`modifySlice`里面的`len+1`在外层是看不到的。外层的`len`还是3。

更进一步，如果我们再append一条数据会怎么样呢？

```go
func modifySlice(s []int) {
	s = append(s, 2048)
	s = append(s, 4096)
	s[0] = 1024
}
```

我们可以看到外层打印的slice变成了 **[0,1,2]**。因为modifySlice函数内的slice底层的数组发生了扩容，变成了另一个扩容后的结构体，但是外层的slice还是引用的老的结构体。

由此我们得出： slice 还有array 都按值传递的 (传递的时候会复制内存)，golang里所有数据都是按值传递的，指针也是值的一种

如果没有发生扩容，修改在原来的底层数组内存中

如果发生了扩容，修改会在新的内存中

显然，这会发生我们意料之外的行为。因此我们应当使用指针传递作为函数的参数，这与C语言类似。

```go
func modifySlice2(s *[]int) {
	*s = append(*s, 2048)
	(*s)[0] = 1024
}
```

相应的，调用方式为`modifySlice(&s)`。

### 扩容策略

当一次向slice中添加大于原slice容量两倍的元素时，直接将新长度作为容量。否则，

1.当cap < 256 的时候 slice 每次扩容 * 2。

2.当cap >= 256 的时候， slice每次扩容 * 1.25。

我们可以查看[源码](https://go.dev/src/runtime/slice.go)中`growslice`的实现具体分析，这里摘录其核心部分：

```go
	//num = number of elements being added
	//newLen = current length (= oldLen + num)
	oldLen := newLen - num	
	newcap := oldCap
	doublecap := newcap + newcap
	if newLen > doublecap {
		newcap = newLen
	} else {
		const threshold = 256
		if oldCap < threshold {
			newcap = doublecap
		} else {
			// Check 0 < newcap to detect overflow
			// and prevent an infinite loop.
			for 0 < newcap && newcap < newLen {
				// Transition from growing 2x for small slices
				// to growing 1.25x for large slices. This formula
				// gives a smooth-ish transition between the two.
				newcap += (newcap + 3*threshold) / 4
			}
			// Set newcap to the requested cap when
			// the newcap calculation overflowed.
			if newcap <= 0 {
				newcap = newLen
			}
		}
	}
```

在`make`slice时预先分配内存可以提升性能，避免重复的扩容导致性能损失。

### 切片操作

#### 原理

切片操作并不复制切片指向的元素，创建一个新的切片会复用原来切片的底层数组，因此切片操作是非常高效的。

看下面的例子：

```go
nums := make([]int, 0, 8)
nums = append(nums, 1, 2, 3, 4, 5)
nums2 := nums[2:4]
printLenCap(nums)  // len: 5, cap: 8 [1 2 3 4 5]
printLenCap(nums2) // len: 2, cap: 6 [3 4]

nums2 = append(nums2, 50, 60)
printLenCap(nums)  // len: 5, cap: 8 [1 2 3 4 50]
printLenCap(nums2) // len: 4, cap: 6 [3 4 50 60]
```

![slice](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/golang%E5%88%87%E7%89%87/20230821221521427663_524_slice.jpg)

- nums2 执行了一个切片操作 `[2, 4)`，此时 nums 和 nums2 指向的是同一个数组。
- nums2 增加 2 个元素 50 和 60 后，将底层数组下标 [4] 的值改为了 50，下标[5] 的值置为 60。
- 因为 nums 和 nums2 指向的是同一个数组，因此 nums 被修改为 [1, 2, 3, 4, 50]。

#### 性能陷阱

切片的底层是数组，因此在某处插入元素或删除元素意味着后面的元素需要逐个向后或向前移位。每次删除的复杂度为 O(N)，因此切片不合适大量随机删除的场景，这种场景下适合使用链表。

另外在`slice传递`一节中提到，在已有切片的基础上进行切片，不会创建新的底层数组。因为原来的底层数组没有发生变化，内存会一直占用，直到没有变量引用该数组。因此很可能出现这么一种情况，原切片由大量的元素构成，但是我们在原切片的基础上切片，虽然只使用了很小一段，但底层数组在内存中仍然占据了大量空间，得不到释放。比较推荐的做法是使用 `copy` 替代 `re-slice`。

```go
func lastNumsBySlice(origin []int) []int {
	return origin[len(origin)-2:]
}

func lastNumsByCopy(origin []int) []int {
	result := make([]int, 2)
	copy(result, origin[len(origin)-2:])
	return result
}
```

### 总结

相比C++和Java中的线性容器，golang的切片使用起来更加灵活，但使用时也有更多需要注意的地方。同时，很多常见的数据结构需要我们自己去定义封装，而不像其他语言一样语法层面或标准库层面做了很多实现和封装。关于这一方面的知识会在后续的文章中继续分享。