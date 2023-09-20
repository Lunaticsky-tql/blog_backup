---
title: Effective C++ - Item41-47 - 模版与泛型编程
categories: 笔记
tags:
  - C++
abbrlink: 4565
date: 2023-09-19 21:54:11
---
# Effective C++ - Item41-47 - 模版与泛型编程

### 总览

这一模块的内容是在完整阅读《Effective C++》的基础上，参考了[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的[一篇文章学完 Effective C++：条款 & 实践](https://zhuanlan.zhihu.com/p/613356779)进行总结。虽然[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的文章将最重要的部分总结的非常到位，但在此结合自己的理解和编程实践对其进行补充，并订正一些错误，以方便自己后续总结回顾，同时在尽可能保持简洁的前提下提高可读性。虽然原书有些地方写的比较拖沓，但作为经典的C++参考书，想要了解更多的细节，还是值得仔细去阅读的。

同时，假定阅读文章时对C++已经具有本科高级语言程序设计课程内容的理解水平。大部分情况下，除非它很重要，不会对C++基础的语法特性进行介绍。

本部分是第七章内容，对**条款41-47**进行介绍。

或许前面的内容只是对早已熟悉的内容进行的强调，而这一部分内容在学校的课程中难以涉及，内容也较为晦涩。

但模版和泛型编程不仅在适当的时候能减少代码的冗余，而且还是STL(Standard Template Library)和Boost的基石，为C++保持运行效率的同时提高易用性作出了巨大贡献。掌握这一部分内容，至少可以称得上是“比较好”的template程序员，对C++的认识也能更进一步。

### 条款 41：了解隐式接口和编译期多态

> 泛型编程本身的核心思想是**编写可以在不同数据类型上工作的通用代码**。但C++的模版不局限于此。

类与模板都支持接口和多态。

对于类而言接口是显式的，以函数签名为中心，多态则是通过虚函数发生于运行期；

而对模板参数而言，接口是隐式的，奠基于有效表达式，多态则是通过**模板具现化和函数重载解析（function overloading resolution）**，发生于编译期。

考虑以下例子：

```cpp
template<typename T>
void DoProcessing(T& w) {
    if (w.size() > 10 && w != someNastyWidget) {
    ...
```

以上代码中，`T`类型的隐式接口要求：

1. 提供一个名为`size`的成员函数，该函数的返回值可与`int`（10 的类型）执行`operator>`，或**经过隐式转换后可执行`operator>`**。
2. 必须支持一个`operator!=`函数，接受`T`类型和`someNastyWidget`的类型，或其隐式转换后得到的类型。

>  同样的道理，`operator&&`也可被重载。即所谓的函数重载解析。

加诸于模板参数身上的隐式接口，就像加诸于类对象身上的显式接口“一样真实”，两者都在编译期完成检查，你无法在模板中使用“不支持模板所要求之隐式接口”的对象（代码无法通过编译）。

> 相比C++，Java实现泛型的原理和C++[大有不同](https://nirvana1997.github.io/c-%E6%B3%9B%E5%9E%8B%E5%92%8Cjava%E6%B3%9B%E5%9E%8B%E7%9A%84%E5%AE%9E%E7%8E%B0/)。
>
> Java 在编译时，它会去执行类型检查和类型推断，然后生成普通的不带泛型的字节码，这种字节码可以被一般的 Java 虚拟机接收并执行，这种技术被称为擦除 (erasure)。
>
> Java 编译后不同类型的模板类编译出的是同一份代码。然后在使用时编译器会帮助进行类型转换。
>
> 这么做是为了保持与Java早期版本的向后兼容性。
>
> ```java
> Pair<String> pair = new Pair<>("", "");
>     pair.setFirst("Generic");
>     pair.setSecond("Programming");
>     String first = pair.getFirst();
>     String second = pair.getSecond();
> ```
>
> 反编译后为:  
>
> ```Java
> Pair pair = new Pair("", "");
>     pair.setFirst("Generic");
>     pair.setSecond("Programming");
>     String first = (String)pair.getFirst();
>     String second = (String)pair.getSecond();
> ```
>
> 所以 java 泛型的实现是在运行时去进行判断和类型转换的，这样会对运行时的效率有一定影响，但编译出来的泛型类的代码只需要一份。

### 条款 42：了解 typename 的双重含义

在模板声明式中，使用`class`和`typename`关键字并没有什么不同，但在模板内部，`typename`拥有更多的一重含义。

为了方便解释，我们首先需要引入一个模板相关的概念：模板内出现的名称如果相依于某个模板参数，我们称之为**从属名称（dependent names）**；如果从属名称在类内呈嵌套状，我们称之为**嵌套从属名称（nested dependent name）**；如果一个名称并不倚赖任何模板参数的名称，我们称之为**非从属名称（non-dependent names）**。

考虑以下模板代码：

```cpp
template<typename C>
void Print2nd(const C& container) {
    //打印容器内的第二元素，注意这不是有效的C++代码
    if (container.size() >= 2) {
        C::const_iterator iter(container.begin());
        ++iter;
        int value = *iter;
        std::cout << value;
    }
}
```

这段代码看起来没有任何问题，但实际编译时却会报错，这一切的罪魁祸首便是`C::const_iterator`。此处的`C::const_iterator`是一个指向某类型的**嵌套从属类型名称（nested dependent type name）**。

> 看完上面的抽象概念，你可能已经有点头大了，现在咱们来重新理一理：
>
> template内出现的名称如果相依于某个template参数,称之为**从属名称(dependent names)**。比如上面的`const C& container`中的`C`
>
> 如果从属名称在class内呈嵌套状，我们称它为**嵌套从属名称(nested dependent name)** 。`C::const iterator`就是这样一个名称。
>
> 实际上它是个**嵌套从属类型名称(nested dependent type name)**,也就是个嵌套从属名称并且指涉某类型。

而嵌套从属名称可能会导致解析困难，因为在编译器知道`C`是什么之前，没有任何办法知道`C::const_iterator`是否为一个类型，这就导致出现了歧义状态，而 C++ **默认假设嵌套从属名称不是类型名称**。

> 这句话是什么意思呢？对于`A::b`这种情况，只是说明在命名空间`A`中有名称`b`，`b`可能是个`typedef`，这种情况就像上面所预想的一样，是嵌套从属类型名称，但也可能是变量名称。这时候如果上面的例子换成这样：`C::const_iterator* x;`,那如果`const_iterator`是变量，我们将`*`理解成乘号便是理所当然的，而且也是**默认的情况**。这就造成了二义性。

这时我们应当显式指明嵌套从属**类型**名称，方法就是将`typename`关键字作为其前缀词：

```cpp
typename C::const_iterator iter(container.begin());
```

同样地，若嵌套从属名称出现在模板函数声明部分，也需要显式地指明是否为类型名称：

```cpp
template<typename C>
void Print2nd(const C& container, const typename C::iterator iter);
```

> 而且`typename`只被用来验明嵌套从属类型名称；或者说只是用来打这个补丁。其他名称不该有它存在。比如在`const C&`前面加`typename`就是画蛇添足了。

这一规则的例外是，`typename`不可以出现在基类列表内的嵌套从属类型名称之前，也不可以在成员初始化列表中作为基类的修饰符：

```cpp
template<typename T>
class Derived : public Base<T>::Nested {    // 基类列表中不允许使用 typename
public:
    explicit Derived(int x)
        : Base<T>::Nested(x) {                 // 成员初始化列表中不允许使用 typename
        typename Base<T>::Nested temp;
        ...
    }
    ...
};
```

捎带提及，在类型名称过于复杂时，可以使用`using`或`typedef`来进行简化。下面给出一个应用实例：

> 假设我们正在撰写一个function template，它接受一个迭代器，而我们打算为该迭代器指涉的对象做一份local副本temp。我们可以这么写：
>
> ```cpp
> template<typename IterT>
> void workWithIterator(IterT iter)
> {
> 	typename std::iterator_traits<IterT>::value_type temp(*iter);
>   ...
> }
> ```
>
> 看着有点复杂。这个语句声明一个local变量(`temp`)，使用`IterT`对象所指物的相同类型，并将`temp`初始化为`iter`所指物。
>
> `std::iterator_traits`是一个模版元编程工具，如其名它能获取迭代器类型的特性信息。`value_type`获取迭代器的值类型。
>
> 比如，如果`IterT`是`vector<int>::iterator`， `temp`的类型就是`int`。如果`IterT`是`list<string>::iterator`，`temp`的类型就是 `string`。由于`std::iterator_traits<IterT>::value_type`是个嵌套从属类型名称(`value type`被嵌套于`iterator_traits<IterT>`之内而`IterT`是个`template `参数)，所以我们必须在它之前放置typename。
>
> 可以这样写：
>
> ```cpp
> template<typename IterT>
> void workWithIterator(IterT iter)
> {
> 	typedef typename std:iterator_traits<IterT>:value_type temp(*iter);
>   // 或using value_type = typename std::iterator_traits<IterT>::value_type;
>   value_type temp(*iter);
>   ...
> }
> ```

### 条款 43：学习处理模板化基类内的名称

在模板编程中，模板类的继承并不像普通类那么自然。

考虑以下情形：

>  有若干公司有发送信息的需求，我们需要写一个`MsgSender`接口，用来对不同公司的信息进行传送。
>
>  ```cpp
>  class CompanyA{
>  public:
>  	void sendcleartext (const std::string &msg);
>  	void sendEncrypted (const std::string &msg);
>  }；
>  
>  class CompanyB{
>  public:
>      void sendCleartext (const std::string&msg);
>  		void sendEncrypted(const std:string&msg);
>  }；
>  ```
>
>  如果编译期间我们有足够信息来决定哪一个信息传至哪一家公司，就可以采用基于template的解法：
>
>  ```cpp
>  class MsgInfo { ... }; //MsgInfo决定我们需要发送的信息
>  
>  template<typename Company>
>  class MsgSender {
>  public:
>      void SendClear(const MsgInfo& info) {
>        std:string msg； 
>        //在这儿，根据info产生信息：
>  			Company c;
>  			c.sendcleartext (msg);
>      }
>      ...
>  };
>  
>  template<typename Company>
>  class LoggingMsgSender : public MsgSender<Company> {
>  public:
>      void SendClearMsg(const MsgInfo& info) {
>        //传送前记录一下日志...
>          SendClear(info);        // 调用基类函数，这段代码无法通过编译
>        //传送后记录一下日志...
>      }
>      ...
>  };
>  ```

很明显，由于直到模板类被真正实例化之前，编译器并不知道模版派生类所继承的基类（如上例`MsgSender<Company>`）具体长什么样，有可能它是一个**全特化**的版本。

> 什么叫全特化？如上例，有一个公司只希望他的信息被加密通信：
>
> ```cpp
> template<> //一个全特化的MsgSender；它和一般template相同， 
> class MsgSender<CompanyZ> { 
> public： 
>   //差别只在于它删掉了sendclear。
>   void sendSecret (const MsgInfo&info){
>     ···
>   }
> }；
> ```
>
> C++ 模板全特化（total template specialization）是 C++ 模板特化的一种形式，它允许你为特定的模板参数提供完全定制的实现，以针对特定类型进行特殊处理。

而在这个版本中可能不满足派生类所假定基类有的隐式接口（比如不存在`SendClear`函数）。由于 C++ 的设计策略是宁愿较早进行诊断，所以编译器会拒绝承认在基类中存在一个`SendClear`函数。

为了解决这个问题，我们需要令 C++“进入模板基类观察”的行为生效，有三种办法达成这个目标：

第一种：在对基类函数的调用动作之前加上`this->`：

```cpp
this->SendClear(info);
```

第二种：使用`using`声明式：

> 如条款33所述，这将基类被遮掩的名称带入派生类中。

```cpp
using MsgSender<Company>::SendClear; //告诉编译器，请它假设sendClear位于base class内.
SendClear(info);
```

第三种：明白指出被调用的函数位于基类内：

```cpp
MsgSender<Company>::SendClear(info);
```

第三种做法是最不令人满意的，如果被调用的是虚函数，上述的明确资格修饰（explicit qualification）会使“虚函数绑定行为”失效。

> 总结一下，这一部分说的是在派生模版类调用基类方法时，怎样解决编译器默认不去寻找继承来的名称的问题，以及编译器这样做的原因。如果你偏偏就要去特化基类，那派生模版类假设基类有这个方法，在传入这个特化基类名作为模版占位符名称，理所当然的会报错。比如：
>
> ```cpp
> LoggingMsgSender<CompanyZ> zMsgSender;
> MsgInfo msgData;
> //在msgData内放置信息。
> zMsgSender.sendClearMsg(msgData); //错误!无法通过编译.
> ```
>
> 那这时就只能继续考虑对派生模板类进行特化。

### 条款 44：将与参数无关的代码抽离模板

模板可以节省时间和避免代码重复，编译器会为填入的每个不同模板参数具现化出一份对应的代码，但长此以外，可能会造成代码膨胀（code bloat），生成浮夸的二进制目标码。

基于**共性和变性分析（commonality and variability analysis）** 的方法，我们需要分析模板中重复使用的部分，将其抽离出模板，以减轻模板具现化带来的代码量。

-  因非类型模板参数而造成的代码膨胀，往往可以消除，做法是以函数参数或类成员变量替换模板参数。

-  因类型模板参数而造成的代码膨胀，往往可以降低，做法是让带有完全相同二进制表述的具现类型共享实现代码。

参考以下矩阵类的例子：

```cpp
template<typename T, std::size_t n>
class SquareMatrix {
public:
    void Invert();
    ...
private:
    std::array<T, n * n> data;
};
```

> 这种情况下
>
> ```cpp
> SquareMatrix<double,5>sml;
> sml.invert() //调用SquareMatrix<double,5>::invert
> SquareMatrix<double,10>sm2;
> sm2.invert() //调用SquareMatrix<double,l0>::invert
> ```
>
> 会具现化两份invert，而这两份invert除了尺寸不一样，操作逻辑都是完全相同的。

修改为：

```cpp
template<typename T>
class SquareMatrixBase {
protected:
    void Invert(std::size_t matrixSize);
    ...
private:
    std::array<T, n * n> data;
};

template<typename T, std::size_t n>
class SquareMatrix : private SquareMatrixBase<T> {  // private 继承实现，见条款 39
    using SquareMatrixBase<T>::Invert;              // 避免掩盖基类函数，见条款 33

public:
    void Invert() { this->Invert(n); }              // 调用模板基类函数，见条款 43
    ...
};
```

`Invert`并不是我们唯一要使用的矩阵操作函数，而且每次都往基类传递矩阵尺寸显得太过繁琐，我们可以考虑将数据放在派生类中，在基类中储存指针和矩阵尺寸。修改代码如下：

```cpp
template<typename T>
class SquareMatrixBase {
protected:
    SquareMatrixBase(std::size_t n, T* pMem)
        : size(n), pData(pMem) {}
    void SetDataPtr(T* ptr) { pData = ptr; }
    ...
private:
    std::size_t size;
    T* pData;
};

template<typename T, std::size_t n>
class SquareMatrix : private SquareMatrixBase<T> {
public:
    SquareMatrix() : SquareMatrixBase<T>(n, data.data()) {}
    ...
private:
    std::array<T, n * n> data;
};
```

然而这种做法并非永远能取得优势，硬是绑着矩阵尺寸的那个版本（最初的版本），有可能生成比共享版本更佳的代码。

例如在尺寸专属版中，尺寸是个编译期常量，因此可以在编译期藉由常量的广传达到最优化；而在共享版本中，不同大小的矩阵只拥有单一版本的函数，可减少可执行文件大小，也就因此降低程序的 working set（在“虚内存环境”下执行的进程所使用的一组内存页），并强化指令高速缓存区内的引用集中化（locality of  reference），这些都可能使程序执行得更快速。究竟哪个版本更佳，只能经由具体的测试后决定。

同样地，上面的代码也使用到了牺牲封装性的`protected`，可能会导致资源管理上的混乱和复杂，考虑到这些，也许一点点模板代码的重复并非不可接受。

总结一下，在使用模版编程编写库时，要有代码膨胀的潜在意识，并站在使用的角度选择合适的处理方法，以平衡性能和二进制大小。

### 条款 45：运用成员函数模板接受所有兼容类型

从某种意义上说，**面向对象设计和模版设计是正交的**。

同一个template的不同具现体*(instantiations)*之间并不存在什么固有关系：如果以带有继承关系的`B`，`D`两类型分别具现化某个`template`，产生出来的两个具现体并不带有继承关系。

> 具体一点，下面的代码无法通过编译：
> ```cpp
> class B {..}
> class D:public B {..}
> 
> template<typename T>
> class SmartPtr{
> public:
> 	explicit SmartPtr(T* realptr);
>   ...
> }
> SmartPtr<B> pt1=SmartPtr<D>(new D); //模版具现体不保留继承关系
> SmartPtr<const B> pt2=pt1; //模版具现体也不保留non-const到const的隐式转换
> ```
> 

C++ 视模板类的不同具现体为完全不同的的类型，但在**泛型编程**中，我们可能需要一个模板类的不同具现体能够相互类型转换。

那考虑设计一个智能指针模版类，而智能指针需要支持不同类型指针之间的隐式转换（如果可以的话），以及普通指针到智能指针的显式转换。

这时我们需要的是模版成员函数*(member function templates)*，比如下面的模版构造函数和模板拷贝构造函数：

```cpp
template<typename T>
class SmartPtr {
public:
    template<typename U>
    SmartPtr(const SmartPtr<U>& other)
        : heldPtr(other.get()) { ... }

    template<typename U>
    explicit SmartPtr(U* p)
        : heldPtr(p) { ... }

    T* get() const { return heldPtr; }
    ...
private:
    T* heldPtr;
};
```

这里使用成员初值列*(member initialization list)*来初始化`SmartPtr<T>`之内类型为`T*`的成员变量，并以类型为`U*`的指针（由`SmartPtr<U>`持有）作为初值。

这个行为只有当“存在某个隐式转换可将一个`U*`指针转为一个`T*`指针”时才能通过编译，而那正是我们想要的。最终效益是`SmartPtr<T>`现在有了一个泛化copy构造函数，这个构造函数只在其所获得的实参隶属适当（兼容）类型时才通过编译。

使用`get`获取原始指针，并将在原始指针之间进行类型转换本身提供了一种保障，如果原始指针之间不能隐式转换，那么其对应的智能指针之间的隐式转换会造成编译错误。

模板构造函数并不会阻止编译器暗自生成默认的构造函数，所以如果你想要控制拷贝构造的方方面面，你必须同时声明泛化拷贝构造函数和普通拷贝构造函数，相同规则也适用于赋值运算符：

```cpp
template<typename T>
class shared_ptr {
public:
    shared_ptr(shared_ptr const& r);                // 拷贝构造函数

    template<typename Y>
    shared_ptr(shared_ptr<Y> const& r);             // 泛化拷贝构造函数

    shared_ptr& operator=(shared_ptr const& r);     // 拷贝赋值运算符

    template<typename Y>
    shared_ptr& operator=(shared_ptr<Y> const& r);  // 泛化拷贝赋值运算符

    ...
};
```

### 条款 46：需要类型转换时请为模板定义非成员函数

该条款与条款 24 一脉相承，还是使用原先的例子：

```cpp
template<typename T>
class Rational {
public:
    Rational(const T& numerator = 0, const T& denominator = 1);

    const T& Numerator() const;
    const T& Denominator() const;

    ...
};

template<typename T>
const Rational<T> operator*(const Rational<T>& lhs, const Rational<T>& rhs) {
   return Rational<T>(lhs.Numerator() * rhs.Numerator(), lhs.Denominator() * rhs.Denominator());
}


Rational<int> oneHalf(1, 2);
Rational<int> result = oneHalf * 2;     // 无法通过编译！
```

上述失败启示我们：模板实参在推导过程中，从不将隐式类型转换纳入考虑。虽然以`oneHalf`推导出`Rational<int>`类型是可行的，但是试图将`int`类型隐式转换为`Rational<T>`是绝对会失败的。

由于模板类并不依赖模板实参推导，所以编译器总能够在`Rational<T>`具现化时得知`T`，因此我们可以使用友元声明式在模板类内指涉特定函数：

```cpp
template<typename T>
class Rational {
public:
    ...
    friend const Rational<T> operator*(const Rational<T>& lhs, const Rational<T>& rhs);
    ...
};
```

在模板类内，模板名称可被用来作为“模板及其参数”的简略表达形式，因此下面的写法也是一样的：

```cpp
template<typename T>
class Rational {
public:
    ...
    friend const Rational operator*(const Rational& lhs, const Rational& rhs);
    ...
};
```

当对象`oneHalf`被声明为一个`Rational<int>`时，`Rational<int>`类于是被具现化出来，而作为过程的一部分，友元函数`operator*`也就被自动声明出来，其为一个普通函数而非模板函数，因此在接受参数时可以正常执行隐式转换。

为了使程序能正常链接，我们需要为其提供对应的定义式，最简单有效的方法就是直接合并至声明式处：

```cpp
friend const Rational operator*(const Rational& lhs, const Rational& rhs) {
    return Rational(lhs.Numerator() * rhs.Numerator(), lhs.Denominator() * rhs.Denominator());
}
```

由于定义在类内的函数都会暗自成为内联函数，为了降低内联带来的冲击，可以使`operator*`调用类外的辅助模板函数：

```cpp
template<typename T> class Rational;

template<typename T>
const Rational<T> DoMultiply(const Rational<T>& lhs, const Rational<T>& rhs) {
    return Rational<T>(lhs.Numerator() * rhs.Numerator(), lhs.Denominator() * rhs.Denominator());
}

template<typename T>
class Rational {
public:
    ...
    friend const Rational operator*(const Rational& lhs, const Rational& rhs) {
        return DoMultiply(lhs, rhs);
    }
    ...
};
```

### 条款 47：请使用 traits classes 表现类型信息

traits classes 可以使我们在编译期就能获取某些类型信息，它被广泛运用于 C++ 标准库中。traits 并不是 C++  关键字或一个预先定义好的构件：它们是一种技术，也是 C++ 程序员所共同遵守的协议，并要求对用户自定义类型和内置类型表现得一样好。

设计并实现一个 trait class 的步骤如下：

1. 确认若干你希望将来可取得的类型相关信息。
2. 为该类型选择一个名称。
3. 提供一个模板和一组特化版本，内含你希望支持的类型相关信息。

以迭代器为例，标准库中拥有多种不同的迭代器种类，它们各自拥有不同的功用和限制：

1. `input_iterator_tag`：单向输入迭代器，只能向前移动，一次一步，客户只可读取它所指的东西。
2. `output_iterator_tag`：单向输出迭代器，只能向前移动，一次一步，客户只可写入它所指的东西。
3. `forward_iterator_tag`：单向访问迭代器，只能向前移动，一次一步，读写均允许。
4. `bidirectional_iterator_tag`：双向访问迭代器，去除了只能向前移动的限制。
5. `random_access_iterator_tag`：随机访问迭代器，没有一次一步的限制，允许随意移动，可以执行“迭代器算术”。

标准库为这些迭代器种类提供的标签结构体（tag struct）的继承关系如下：

```cpp
struct input_iterator_tag {};

struct output_iterator_tag {};

struct forward_iterator_tag : input_iterator_tag {};

struct bidirectional_iterator_tag : forward_iterator_tag {};

struct random_access_iterator_tag : bidirectional_iterator_tag {};
```

将`iterator_category`作为迭代器种类的名称，嵌入容器的迭代器中，并且确认使用适当的标签结构体：

```cpp
template< ... > //省略一些 template参数
class deque {
public:
    class iterator {
    public:
        using iterator_category = random_access_iterator;
        ...
    }
    ...
}

template< ... >
class list {
public:
    class iterator {
    public:
        using iterator_category = bidirectional_iterator;
        ...
    }
    ...
}
```

为了做到类型的 traits 信息可以在类型自身之外获得，标准技术是把它放进一个模板及其一个或多个特化版本中。这样的模板在标准库中有若干个，其中针对迭代器的是`iterator_traits`：

```cpp
template<class IterT>
struct iterator_traits {
  	typedef typename IterT::iterator_category iterator_category;
    // 或者 using iterator_category = IterT::iterator_category; 见条款42
    ...
};
```

为了支持指针迭代器，`iterator_traits`特别针对指针类型提供一个**偏特化版本**，而指针的类型和随机访问迭代器类似，所以可以写出如下代码：

```cpp
template<class IterT>
struct iterator_traits<IterT*> {
  		typedef typename iterator_category = random_access_iterator_tag;
     // using iterator_category = random_access_iterator_tag;
    ...
};
```

当我们需要为不同的迭代器种类应用不同的代码时，traits classes 就派上用场了。

或许我们朴素的想法是这样：

```cpp
template<typename IterT, typename DisT>
void advance(IterT& iter, DisT d) {
    if (typeid(std::iterator_traits<IterT>::iterator_category)
        == typeid(std::random_access_iterator_tag)) {
        iter +d;
    }
}
```

但这样类型测试便发生于运行期而非编译期。而我们希望类型的判断能在编译期完成。

> 不仅如此，这样的实现也会造成编译期问题。
>
> ```cpp
> std::list<int>::iterator iter;
> advance(iter,10); //移动1ter向前走10个元素:
> //上述实现无法通过编译。
> ```
>
> 为什么呢？我们不妨模拟一下编译器的模板实参推导：
>
> ```cpp
> void advance(std::list<int>::iterator& iter,int d){
>   if(typeid(std:iterator_traits<std:list<int>:iterator>::iterator_category)==typeid(std:random_access_iterator_tag)){ 
>     iter +=d; //错误!
> }
> else{
> 	if (d >=0) {while (d--)++iter;}
>   else {while (d++)--iter;}
> }
> ```
>
> 虽然我嫩运行时绝不会执行+=那一行，但编译器必须确保所有源码都有效。编译器觉得只有random access迭代器才支持`+=`，而`std::list<int>::iterator`不支持`+=`，因此会报错。

`iterator_category`是在编译期决定的，然而`if`却是在运行期运作的，无法达成我们的目标。

在 C++17 之前，解决这个问题的主流做法是利用函数重载（也是原书中介绍的做法）：

> 编译器匹配**最**适合的重载函数，何尝不是一种if？

```cpp
template<typename IterT, typename DisT>
void doAdvance(IterT& iter, DisT d, std::random_access_iterator_tag) {
    iter +=d;
}   


template<typename IterT, typename DisT>
void doAdvance(IterT& iter, DisT d, std::bidirectional_iterator_tag) {
    if(d>=0) { while(d--) ++iter; } 
    else { while (d++) --iter; }
}

template<typename IterT, typename DisT>
void doAdvance(IterT& iter, DisT d, std::input_iterator_tag) {
  // input 迭代器和 forward 迭代器都适用
    if (d < 0) {
        throw std::out_of_range("Negative distance");       // 单向迭代器不允许负距离
    }
    while (d--)++iter;
}

template<typename IterT, typename DisT>
void advance(IterT& iter, DisT d) {
    doAdvance(iter, d, std::iterator_traits<IterT>::iterator_category());
}
```

在 C++17 之后，我们有了更简单有效的做法——使用`if constexpr`：

```cpp
template<typename IterT, typename DisT>
void Advance(IterT& iter, DisT d) {
    if (constexpr (typeid(std::iterator_traits<IterT>::iterator_category)
        == typeid(std::random_access_iterator_tag)) {
        ...
    }
}
```

### 条款 48：认识模板元编程

模板元编程（Template metaprogramming，TMP）是编写基于模板的 C++ 程序并执行于编译期的过程，它并不是刻意被设计出来的，而是当初 C++  引入模板带来的副产品，事实证明模板元编程具有强大的作用，并且现在已经成为 C++ 标准的一部分。实际上，在条款 47 中编写 traits  classes 时，我们就已经在进行模板元编程了。

由于模板元程序执行于 C++ 编译期，因此可以将一些工作从运行期转移至编译期，这可以帮助我们在编译期时发现一些原本要在运行期时才能察觉的错误，以及得到较小的可执行文件、较短的运行期、较少的内存需求。当然，副作用就是会使编译时间变长。

模板元编程已被证明是“图灵完备”的，并且以“函数式语言”的形式发挥作用，因此在模板元编程中没有真正意义上的循环，所有循环效果只能藉由递归实现，而递归在模板元编程中是由 **“递归模板具现化（recursive template instantiation）”** 实现的。

常用于引入模板元编程的例子是在编译期计算阶乘：

```cpp
template<unsigned n>            // Factorial<n> = n * Factorial<n-1>
struct Factorial {
    enum { value = n * Factorial<n-1>::value }; //enum hack，见条款2
};

template<> //特殊情况，使用全特化实现
struct Factorial<0> {           // 处理特殊情况：Factorial<0> = 1
    enum { value = 1 };
};
//怎么用
std::cout << Factorial<5>::value;
```

模板元编程很酷，**但对其进行调试可能是灾难性的**，因此在实际应用中并不常见。

作者提出，我们可能会在下面几种情形中见到它的出场：

1. 确保量度单位正确，用于早期错误侦测。

   > 我们知道，越早发现错误越好。

2. 优化矩阵计算。

   > 不过，并行计算才是正道。

3. 可以进行代码生成。

   > 除了基础库以外暂时还没见过实例，可能是眼界太狭隘了。

