---
title: Effective C++ - Item1-4 - 让自己习惯C++ 
categories: 笔记
tags:
  - EffectiveC++
abbrlink: 53266
date: 2023-09-18 22:22:08
---
# Effective C++ - Item1-4 - 让自己习惯 C++ 

### 总览

这一模块的内容是在完整阅读《Effective C++》的基础上，参考了[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的[一篇文章学完 Effective C++：条款 & 实践](https://zhuanlan.zhihu.com/p/613356779)进行总结。虽然[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的文章将最重要的部分总结的非常到位，但在此结合自己的理解和编程实践对其进行补充，并订正一些错误，以方便自己后续总结回顾，同时在尽可能保持简洁的前提下提高可读性。虽然原书有些地方写的比较拖沓，但作为经典的C++参考书，想要了解更多的细节，还是值得仔细去阅读的。

同时，假定阅读文章时对C++已经具有本科高级语言程序设计课程内容的理解水平。大部分情况下，除非它很重要，不会对C++基础的语法特性进行介绍。

本部分是第一章内容，对**条款1-4**进行介绍。

### 条款 1：视 C++ 为一个语言联邦

C++ 拥有多种不同的编程范式，而这些范式集成在一个语言中，使得 C++ 是一门即灵活又复杂的语言：

1. 传统的面向过程 C：区块，语句，预处理器，内置数据类型，数组，指针。
2. 面向对象的 C with Classes：类，封装，继承，多态，动态绑定。
3. 模板编程 Template C++ 和堪称黑魔法的模板元编程（TMP）。
4. C++ 标准库 STL。

C++ 高效编程守则视情况而变化，程序设计没有银弹。

### 条款 2：尽量以 const, enum, inline 替换 #define

在原书写成时 C++11 中的`constexpr`还未诞生，现在一般认为应当用`constexpr`定义编译期常量来替代大部分的`#define`宏常量定义：

```cpp
#define ASPECT_RATIO 1.653
```

替代为：

```cpp
constexpr auto aspect_ratio = 1.653;
```

我们也可以将编译期常量定义为类的静态成员：

```cpp
class GamePlayer {
public:
    static constexpr auto numTurns = 5;
};
```

`enum`可以用于替代整型的常量，并且在模板元编程中应用广泛（见条款 48）：

```cpp
class GamePlayer {
public:
    enum { numTurns = 5 };
};
```

大部分`#define`宏常量应当用内联模板函数替代：

```cpp
#define CALL_WITH_MAX(a, b) f((a) > (b) ? (a) : (b))
```

> 或许你认为加了括号就能避免误用。并不是。
>
> ```cpp
> int a =5,b 0;
> 
> CALL WITH MAX (++a,b);   //a被累加二次 
> 
> CALL WITH MAX (++a,b+10);   //a被累加一次
> 
> ```

上面的宏可以用内联模版替代为：

```cpp
template<typename T>
inline void CallWithMax(const T& a, const T& b) {
    f(a > b ? a : b);
}
```

需要注意的是，宏和函数的行为本身并不完全一致，**宏只是简单的替换**，并不涉及传参和复制。

### 条款 3：尽可能使用 const

若你想让一个常量只读，那你应该明确说出它是const常量，对于指针来说，更是如此：

```cpp
char greeting[] = "Hello";
char* p = greeting;                // 指针可修改，数据可修改
const char* p = greeting;          // 指针可修改，数据不可修改
char const* p = greeting;          // 指针可修改，数据不可修改
char* const p = greeting;          // 指针不可修改，数据可修改
const char* const p = greeting;    // 指针不可修改，数据不可修改
```

> 常量指针：指向常量的指针；指针常量：指针是常量。上面第三种写法较为少见，但也是合法的。

对于 STL 迭代器，分清使用`const`还是`const_iterator`：

```cpp
const std::vector<int>::iterator iter = vec.begin();    // 迭代器不可修改，数据可修改
std::vector<int>::const_iterator iter = vec.begin();    // 迭代器可修改，数据不可修改
```

面对函数声明时，如果你不想让一个函数的结果被无意义地当作左值，请使用const返回值：

```cpp
const Rational operator*(const Rational& lhs, const Rational& rhs);
```

> `if (a*b=c)... //喔欧,其实是想做一个比较(comparison)动作!`

**const成员函数：**

const成员函数允许我们操控const对象，这在传递常引用时显得尤为重要：

```cpp
class TextBlock {
public:
    const char& operator[](std::size_t position) const {    // const对象使用的重载
        return text[position];
    }

    char& operator[](std::size_t position) {                // non-const对象使用的重载
        return text[position];
    }

private:
    std::string text;
};
```

这样，const和non-const对象都有其各自的重载版本：

```cpp
void Print(const Textblock& ctb) {
    std::cout << ctb[0];            // 调用 const     TextBlock::operator[]
}
```

编译器对待`const`对象的态度通常是 `bitwise constness`，而我们在编写程序时通常采用 `logical constness`。

> `bitwise constness`是指，成员函数不改变任何成员变量，这也是C++编译器对常量性的定义。
>
> `logical constness`是指从对象功能上看，`const`成员函数可以修改它所处对象的一些bits，但对象本身它对外不应该表现出可变性。
>
> 两者不等同。如下例：
>
> ```cpp
> class CTextBlock{
> public:
>     ...
>     char& operator[](std::size t position) const{
>        return pText[position];
>     }//bitwise const声明,但其实不适当.
> private:
>     char* pText;
> }；
> ```
>
> 显然`operator[]`实现代码并不更改`pText`，但在外部可以经由`pText`改变对象内数组的内容。这是`bitwise constness`的但不是`logical constness`。

这就意味着，在确保客户端不会察觉的情况下，我们认为`const`对象中的某些成员变量应当是允许被改变的，使用关键字`mutable`来标记这些成员变量：

```cpp
class CTextBlock {
public:
    std::size_t Length() const;

private:
    char* pText;
    mutable std::size_t textLength;
    mutable bool lengthIsValid;
};

std::size_t CTextBlock::Length() const {
    if (!lengthIsValid) {
        textLength = std::strlen(pText);    // 可以修改mutable成员变量
        lengthIsValid = true;               // 可以修改mutable成员变量
    }
    return textLength;
}
```

在重载`const`和`non-const`成员函数时，需要尽可能避免书写重复的内容，这促使我们去进行常量性转除。在大部分情况下，我们应当避免转型的出现，但在此处为了减少重复代码，转型是适当的：

```cpp
class TextBlock {
public:
    const char& operator[](std::size_t position) const {

        // 假设这里有非常多的代码

        return text[position];
    }

    char& operator[](std::size_t position) {
        return const_cast<char&>(static_cast<const TextBlock&>(*this)[position]);
    }

private:
    std::string text;
};
```

> 需要注意的是，反向做法：令`const`版本调用`non-const`版本以避免重复——并不被建议，一般而言`const`版本的限制比`non-const`版本的限制更多，因此这样做会带来风险。

### 条款 4：确定对象在使用前已被初始化

无初值对象在 C/C++ 中广泛存在，因此这一条款就尤为重要。在定义完一个对象后需要尽快为它赋初值：

```cpp
int x = 0;
const char* text = "A C-style string";

double d;
std::cin >> d;
```

对于类中的成员变量而言，我们有两种建议的方法完成初始化工作，一种是直接在定义处赋初值（since C++11）：

```cpp
class CTextBlock {
private:
    std::size_t textLength{ 0 };
    bool lengthIsValid{ false };
};
```

另一种是使用构造函数成员初始化列表：

```cpp
ABEntry::ABEntry(const std::string& name, const std::string& address,
                 const std::list<PhoneNumber>& phones)
    : theName(name),
      theAddress(address),
      thePhones(phones),
      numTimesConsulted(0) {}
```

成员初始化列表也可以留空用来执行默认构造函数：

```cpp
ABEntry::ABEntry()
    : theName(),
      theAddress(),
      thePhones(),
      numTimesConsulted(0) {}
```

需要注意的是，类中成员的初始化具有次序性，而这次序与成员变量的声明次序一致，与成员初始化列表的次序无关。

>  类中成员的初始化是可选的，但是引用类型必须初始化。

**静态对象的初始化：**

C++ 对于定义于不同编译单元内的全局静态对象的初始化相对次序并无明确定义，因此，以下代码可能会出现使用未初始化静态对象的情况：

```cpp
// File 1 ：你作为作者，写了一个FileSystem工具库供其他人使用
class FileSystem{
public:
		std:size_t numDisks() const;
    ...
}；
extern FileSystem tfs; //预先定义一个对象tfs(the file system)方便客户使用

// File 2：客户建立一个Deirectory用来处理文件系统中的目录：
class Directory {
public:
    Directory() {
        std::size_t disk = tfs.numDisks();
    }
  ...
};

Directory tempDir;
```

在上面这个例子中，你无法确保位于不同编译单元内的`tfs`一定在`tempDir`之前初始化完成。

这个问题的一个有效解决方案是采用 **Meyers' singleton**，将全局静态对象转化为局部静态对象：

> Meyers就是这本书的作者。这是它首创的(笑

```cpp
// File 1
class FileSystem{ ... }   //和前面一样

FileSystem& tfs() {
    static FileSystem fs;
    return fs;
}//这个函数用来替换tfs对象;它在 FileSystem class中可能是个static, 定义并初始化一个local static对象, 返回一个reference指向上述对象。

//File 2
class Directory(){
	Directory(){
    std::size_t disks=tfs().numDisks();
  }
  ...
    
}
Directory& tempDir() {
    static Directory td;
    return td;
}//相应的，后面需要使用单例对象只需要调用tempDir()即可。
```

这个手法的基础在于：C++ 保证，函数内的局部静态对象会在**该函数被调用期间**，**首次遇上该对象之定义式**时被初始化，也就是说顺便还实现了懒加载。也即不用这个函数，它之中的局部静态对象便不会被初始化。

> 根据[这篇文章](https://laristra.github.io/flecsi/src/developer-guide/patterns/meyers_singleton.html)，我们还可以对这种单例进行一下封装。
>
> ```cpp
> class Singleton {
> public:
>     static Singleton& getInstance() {
>         static Singleton instance; // 静态局部变量，在首次访问时初始化
>         return instance;
>     }
> 
>     // 其他成员函数
> 
> private:
>     Singleton() {} // 私有构造函数，防止外部直接实例化
>     Singleton(const Singleton&) = delete; // 禁用拷贝构造函数(详见条款6)
>     Singleton& operator=(const Singleton&) = delete; // 禁用赋值运算符
> };
> ```

当然，这种做法对于多线程来说会有不确定性，最好还是在单线程启动阶段手动调用函数完成初始化。

> 对于多线程的情形，原文是说不敢保证。事实上C++11已经可以保证了。在C++11标准中，要求局部静态变量初始化具有线程安全性。[这篇文章](https://blog.csdn.net/imred/article/details/89069750)十分有深度，对这个问题进行了更细致的分析。因此在实际上我们可以使用Meyers' singleton方法创建线程安全的静态单例。
>
> 这一点可由下面的程序验证：
>
> 摘录一下标准关于局部静态变量初始化的要求：
>
> 1. 变量在代码第一次执行到变量声明的地方时初始化。
>
> 2. 初始化过程中发生异常的话视为未完成初始化，未完成初始化的话，需要下次有代码执行到相同位置时再次初始化。
>
> 3. 在当前线程执行到需要初始化变量的地方时，如果有其他线程正在初始化该变量，则阻塞当前线程，直到初始化完成为止。
>
> 4. 如果初始化过程中发生了对初始化的递归调用，则视为未定义行为。
>
> 关于第四点，怎么会有人写这样的代码。。
>
> ```cpp
> class Bar
> {
> public:
>     static Bar *getInstance()
>     {
>         static Bar s_instance;
>         return &s_instance;
>     }
> private:
>     Bar()
>     {
>         getInstance();
>     }
> };
> ```