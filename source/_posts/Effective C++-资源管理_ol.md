---
title: Effective C++-资源管理
categories: 笔记
tags:
  - C++
date: 2023-09-19 10:46:30
---
# Effective C++-资源管理

### 总览

这一模块的内容是在完整阅读《Effective C++》的基础上，参考了[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的[一篇文章学完 Effective C++：条款 & 实践](https://zhuanlan.zhihu.com/p/613356779)进行总结。虽然[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的文章将最重要的部分总结的非常到位，但在此结合自己的理解和编程实践对其进行补充，并订正一些错误，以方便自己后续总结回顾，同时在尽可能保持简洁的前提下提高可读性。虽然原书有些地方写的比较拖沓，但作为经典的C++参考书，想要了解更多的细节，还是值得仔细去阅读的。

同时，假定阅读文章时对C++已经具有本科高级语言程序设计课程内容的理解水平。大部分情况下，除非它很重要，不会对C++基础的语法特性进行介绍。

本部分是第二章内容，对**条款13-17**进行介绍。

资源管理是编写C++代码相比编写其他高级语言代码时所需要更加留心的。C++有强大的操纵资源的能力和性能的同时，也留给我们更多的心智负担去思考如何管理资源。这是我们享受性能裨益的同时要担负的责任。

很多新兴语言如Rust正尝试通过更明确的语言级别限制来尽可能容易的写出安全的代码，但理解了在C++下如何防止资源泄漏，并具有良好的防范意识，是一通百通的。本部分主要的核心内容是**基于对象的资源管理**，从现代C++的视角看其实现便是**智能指针**。经验显示，经过训练后严守这些做法，可以几乎消除资源管理问题。

### 条款 13：以对象管理资源

对于传统的堆资源管理，我们需要使用成对的`new`和`delete`，这样若忘记`delete`就会造成内存泄漏。

> 比如，在delete之前过早的return掉函数。

因此，我们应尽可能以对象管理资源，并采用RAII（Resource Acquisition Is Initialization，资源取得时机便是初始化时机），让**析构函数负责资源的释放**。

原书此处关于智能指针的内容已经过时，在 C++11 中，通过专一所有权来管理RAII对象可以使用`std::unique_ptr`，通过引用计数来管理RAII对象可以使用`std::shared_ptr`。

> 引用计数型能指针 (reference--counting smart pointer RCSP)

```cpp
// Investment* CreateInvestment();

std::unique_ptr<Investment> pUniqueInv1(CreateInvestment());
std::unique_ptr<Investment> pUniqueInv2(std::move(pUniqueInv1));    // 转移资源所有权

std::shared_ptr<Investment> pSharedInv1(CreateInvestment());
std::shared_ptr<Investment> pSharedInv2(pSharedInv1);               // 引用计数+1
```

智能指针默认会自动delete所持有的对象，我们也可以为智能指针指定所管理对象的释放方式（删除器deleter）：

```cpp
void GetRidOfInvestment(Investment*) { std::cout<<"Clean up";}

std::unique_ptr<Investment, decltype(GetRidOfInvestment)*> pUniqueInv(CreateInvestment(), GetRidOfInvestment);
std::shared_ptr<Investment> pSharedInv(CreateInvestment(), GetRidOfInvestment);
```

### 条款 14：在资源管理类中小心拷贝行为

我们应该永远保持这样的思考：当一个RAII对象被复制，会发生什么事？

> 比如，我们将C API的互斥锁包装成RAII对象，它显然不应该被复制。

**选择一：禁止复制**

许多时候允许RAII对象被复制并不合理，如果确是如此，那么就该明确禁止复制行为，条款 6 已经阐述了怎么做这件事。

> 拷贝构造函数和拷贝复值运算符声明为private或者=delete

**选择二：对底层资源祭出“引用计数法”**

正如`std::shared_ptr`所做的那样，每一次复制对象就使引用计数+1，每一个对象离开定义域就调用析构函数使引用计数-1，直到引用计数为0就彻底销毁资源。

**选择三：复制底层资源**

在复制对象的同时复制底层资源的行为又被称作**深拷贝（Deep copying）**，例如在一个对象中有一个指针，那么在复制这个对象时就不能只复制指针，也要复制指针所指向的数据。

**选择四：转移底层资源的所有权**

和`std::unique_ptr`的行为类似，永远保持只有一个对象拥有对资源的管理权，当需要复制对象时转移资源的管理权。

### 条款 15：在资源管理类中提供对原始资源的访问

和所有的智能指针一样，STL 中的智能指针也提供了对原始资源的隐式访问和显式访问：

```cpp
Investment* pRaw = pSharedInv.get();    // 显式访问原始资源
Investment raw = *pSharedInv;           // 隐式访问原始资源
```

> 智能指针针重载了指针取值操作符(operator->和operator*)，它们允许使用指针的方式操作资源，也可以隐式转换至底部原始指针。

当我们在设计自己的资源管理类时，也要考虑在提供对原始资源的访问时，是使用显式访问还是隐式访问的方法，还是两者皆可。

> 下面的例子是将字体包装成RAII对象，同时考虑C API的兼容性，考虑转换为原始资源`FontHandle`的需求，

```cpp
class Font {
public:
    FontHandle Get() const { return handle; }       // 显式转换函数
    operator FontHandle() const { return handle; }  // 隐式转换函数

private:
    FontHandle handle;
};
```

> 注：这里是重载了强制类型转换的括号运算符。

一般而言显式转换比较安全，但隐式转换对客户比较方便。

> 就像多数设计良好的classes一样，它隐藏了客户不需要看的部分，但备妥客户需要的所有东西。

### 条款 16：成对使用 new 和 delete 时要采用相同形式

使用`new`来分配单一对象，使用`new[]`来分配对象数组，必须明确它们的行为并不一致，分配对象数组时会额外在内存中记录“数组大小”，而使用`delete[]`会根据记录的数组大小多次调用析构函数，使用`delete`则仅仅只会调用一次析构函数。对于单一对象使用`delete[]`其结果也是未定义的，程序可能会读取若干内存并将其错误地解释为数组大小。

```cpp
int* array = new int[10];
int* object = new int;

delete[] array;
delete object;
```

需要注意的是，使用`typedef`定义数组类型会带来额外的风险：

```cpp
typedef std::string AddressLines[4];

std::string* pal = new AddressLines;    // pal 是一个对象数组，而非单一对象
//用户后续可能忘记它是个数组
delete pal;                             // 行为未定义
delete[] pal;                           // 正确
```

### 条款 17：以独立语句将 newed 对象置入智能指针

现在更好的做法是使用`std::make_unique`和`std::make_shared`：

```cpp
auto pUniqueInv = std::make_unique<Investment>();    // since C++14
auto pSharedInv = std::make_shared<Investment>();    // since C++11
```

> 原文中举了这样的例子：
>
> ```cpp
> processwidget(std::shared_ptr<Widget>(new Widget),priority());
> ```
>
> 认为`priority()`的执行异常可能导致`Widget`未被置于智能指针中，从而引发资源泄漏。
>
> 函数入参的表达式计算顺序本身就是未定义的，不同编译器的执行结果可能是不同的：
>
> 如：
>
> ```cpp
> #include <iostream>
> using namespace std;
> void dis(int a, int b,int c)
> {
>  cout<<a<<' '<<b<<' '<<c;
> }
> int main() {
>  int x = 0;
>  dis(x++, x++,x);
>  return 0;
> }
> ```
>
> clang-tidy会报：
> ```
> Multiple unsequenced modifications to ’x'
> ```
>
> **因此，不要这么写。**

