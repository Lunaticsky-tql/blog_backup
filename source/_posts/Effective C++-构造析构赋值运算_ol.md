---
title: Effective C++-构造/析构/赋值运算
categories: 笔记
tags:
  - C++
abbrlink: 42906
date: 2023-09-18 22:42:54
---
# Effective C++-构造/析构/赋值运算

### 总览

这一模块的内容是在完整阅读《Effective C++》的基础上，参考了[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的[一篇文章学完 Effective C++：条款 & 实践](https://zhuanlan.zhihu.com/p/613356779)进行总结。虽然[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的文章将最重要的部分总结的非常到位，但在此结合自己的理解和编程实践对其进行补充，并订正一些错误，以方便自己后续总结回顾，同时在尽可能保持简洁的前提下提高可读性。虽然原书有些地方写的比较拖沓，但作为经典的C++参考书，想要了解更多的细节，还是值得仔细去阅读的。

同时，假定阅读文章时对C++已经具有本科高级语言程序设计课程内容的理解水平。大部分情况下，除非它很重要，不会对C++基础的语法特性进行介绍。

本部分是第二章内容，对**条款5-12**进行介绍。

构造/析构/赋值运算是C++面向对象编程中最常打交道的内容，必须要良好的定义它们。

### 条款 5：了解 C++ 默默编写并调用哪些函数

C++ 中的空类并不是真正意义上的空类，编译器会为它预留以下内容：

```cpp
class Empty {
public:
    Empty() { ... }                           // 默认构造函数（没有任何构造函数时）
    Empty(const Empty&) { ... }               // 拷贝构造函数
    Empty(Empty&&) { ... }                    // 移动构造函数 (since C++11)
    ~Empty() { ... }                          // 析构函数
    
    Empty& operator=(const Empty&) { ... }    // 拷贝赋值运算符
    Empty& operator=(Empty&&) { ... }         // 移动赋值运算符 (since C++11)
};
```

唯有当这些函数被调用时，它们才会真正被编译器创建出来，下面代码将造成上述每一个函数被创建：

```cpp
Empty e1;                   // 默认构造函数 & 析构函数
Empty e2(e1);               // 拷贝构造函数
Empty e3 = std::move(e2);   // 移动构造函数 (since C++11)
e2 = e1;                    // 拷贝赋值运算符
e3 = std::move(e1);         // 移动赋值运算符 (since C++11)
```

需要注意的是，拷贝赋值运算符只有在允许存在时才会自动创建，比如以下情况：

```cpp
class NamedObject {
private:
    std::string& nameValue;
};
```

在该类中，我们有一个string引用类型，然而引用无法指向不同对象，因此编译器会拒绝为该类创建一个默认的拷贝赋值运算符。

除此之外，以下情形也会导致拷贝赋值运算符不会自动创建：

1. 类中含有const成员。
2. 基类中含有private的拷贝赋值运算符。

> 关于这一点，别忘了在高级语言程序设计中早已学过的：如果一个对象内有指针存储的数据成员，拷贝时一定要再new一个，否则可能会出现多次delete同一块内存的情况。条款 10讲了怎么在复制时保证异常安全。

### 条款 6：若不想使用编译器自动生成的函数，就该明确拒绝

原书中使用的做法是将不想使用的函数声明为private，或者更进一步的，专门定义一个`Uncopyable`对象，它的copy构造函数和copy assignment操作符是private的，让不想被拷贝的对象继承它。

但在 C++11 后我们有了更好的做法：

```cpp
class Uncopyable {
public:
    Uncopyable(const Uncopyable&) = delete;
    Uncopyable& operator=(const Uncopyable&) = delete;
};
```

### 条款 7：为多态基类声明虚析构函数

当派生类对象经由一个基类指针被删除，而该**基类指针带着一个非虚析构函数**，其结果是未定义的，可能会**无法完全销毁派生类的成员，造成内存泄漏**  (因为调用的是基类的析构函数）。消除这个问题的方法就是对基类使用虚析构函数：

```cpp
class Base {
public:
    Base();
    virtual ~Base();
};
```

如果你不想让一个类成为基类，那么在类中声明虚函数是是一个坏主意，因为额外存储的虚表指针会使类的体积变大。

> 并非所有base classes的设计目的都是为了多态用途。例如标准string和STL 容器都不被设计作为base classes使用，更别提多态了。它们都没有虚析构函数，所以**不要继承它们**。
>
> 某些classes的设计目的是作为base classes使用，但不是为了多态用途。它们也不需要虚析构函数。

虚析构函数的运作方式是，最深层派生的那个类的析构函数最先被调用，然后是其上的基类的析构函数被依次调用。

如果你想将基类作为抽象类使用，但手头上又没有别的虚函数，那么将它的析构函数设为纯虚函数是一个不错的想法。考虑以下情形：

```cpp
class Base {
public:
    virtual ~Base() = 0;
};
```

但若此时从该基类中派生出新的类，会发生报错，这是因为编译器无法找到基类的析构函数的实现。因此，即使是纯虚析构函数，也需要一个函数体：

```cpp
Base::~Base() {}
```

或者以下写法也被允许：

```cpp
class Base {
public:
    virtual ~Base() = 0 {}
};
```

### 条款 8：别让异常逃离析构函数

在析构函数中吐出异常并不被禁止，但为了程序的可靠性，应当极力避免这种行为。

为了实现 RAII，我们通常会将对象的销毁方法封装在析构函数中，如下例子：

```cpp
class DBConn {
public:
    ...
    ~DBConn() {
        db.close();    // 该函数可能会抛出异常
    }

private:
    DBConnection db;
};
```

但这样我们就需要在析构函数中完成对异常的处理，以下是几种常见的做法：

第一种：杀死程序：

```cpp
DBConn::~DBConn() {
    try { db.close(); }
    catch (...) {
        // 记录运行日志，以便调试
        std::abort();
    }
}
```

第二种：直接吞下异常不做处理，但这种做法不被建议。

第三种：重新设计接口，将异常的处理交给客户端完成：

```cpp
class DBConn {
public:
    ...
    void close() {
        db.close();
        closed = true;
    }

    ~DBConn() {
        if (!closed) {
            try {
                db.close();
            }
            catch(...) {
                // 处理异常
            }
        }
    }

private:
    DBConnection db;
    bool closed;
};
```

在这个新设计的接口中，我们提供了`close`函数供客户手动调用，这样客户也可以根据自己的意愿处理异常；若客户忘记手动调用，析构函数才会自动调用`close`函数。

当一个操作可能会抛出需要客户处理的异常时，将其暴露在普通函数而非析构函数中是一个更好的选择。

### 条款 9：绝不在构造和析构过程中调用虚函数

在创建派生类对象时，基类的构造函数永远会早于派生类的构造函数被调用，而基类的析构函数永远会晚于派生类的析构函数被调用。

在派生类对象的基类构造和析构期间，对象的类型是基类而非派生类，因此**此时调用虚函数会被编译器解析至基类的虚函数版本**，通常不会得到我们想要的结果。

```cpp
class Transaction {
public:
    Transaction(); //所有交易的base class
    virtual void logTransaction() const = 0; //做出一份因类型不同而不同 //的日志记录(log entry)
    ...
};

Transaction::Transaction() {
    ...
    // Call to pure virtual member function 'logTransaction' has undefined behavior; 
    // overrides of 'logTransaction' in subclasses are not available 
    // in the constructor of 'Transaction'
    logTransaction();
}

class BuyTransaction : public Transaction {  //derived class
public:
    virtual void logTransaction() const; //志记(1og)此型交易
    ...
};

class SellTransaction : public Transaction { //derived class
public:
    virtual void logTransaction() const; //志记(1og)此型交易
    ...
};
```

```cpp
BuyTransaction b; //被调用的logTransaction是Transaction内的版本
```

上面的错误或许一眼能看出来，而且运行时也会报错，因为在`Transaction`中`logTransaction`是纯虚函数，一般会因为没有提供实现而无法链接。

但是，间接调用虚函数是一个比较难以发现的危险行为，需要尽量避免：

```cpp
class Transaction {
public:
    Transaction() { Init(); }
    virtual void LogTransaction() const = 0;

private:
    void Init(){
        ...
        LogTransaction();      // 此处间接调用了虚函数！
    }
};
```

如果想要基类在构造时就得知派生类的构造信息，推荐的做法是在派生类的构造函数中将必要的信息向上传递给基类的构造函数：

```cpp
class Transaction {
public:
    explicit Transaction(const std::string& logInfo);
    void LogTransaction(const std::string& logInfo) const;
    ...
};

Transaction::Transaction(const std::string& logInfo) {
    LogTransaction(logInfo); // 更改为了非虚函数调用
}

class BuyTransaction : public Transaction {
public:
    BuyTransaction(...):Transaction(CreateLogString(...)) { ... }    // 将信息传递给基类构造函数
    ...

private:
    static std::string CreateLogString(...);
}
```

注意此处的`CreateLogString`是一个静态成员函数，这是很重要的，因为静态成员函数可以确保不会使用未完成初始化的成员变量。

### 条款 10：令 operator= 返回一个指向 *this 的引用

虽然并不强制执行此条款，但为了实现**连锁赋值**，大部分时候应该这样做：

```cpp
class Widget {
public:
    Widget& operator+=(const Widget& rhs) {    // 这个条款适用于
        ...                                    // +=, -=, *= 等等运算符
        return *this;
    }
    Widget& operator=(int rhs) {               // 即使参数类型不是 Widget& 也适用
        ...
        return *this;
    }
};
```

### 条款 11：在 operator= 中处理“自我赋值”

自我赋值是合法的操作，但在一些情况下可能会导致意外的错误，例如在复制堆上的资源时：

```cpp
Widget& operator+=(const Widget& rhs) {
    delete pRes;                          // 删除当前持有的资源
    pRes = new Resource(*rhs.pRes);       // 复制传入的资源
    return *this;
}
```

但若`rhs`和`*this`指向的是相同的对象，就会导致访问到已删除的数据。

最简单的解决方法是在执行后续语句前先进行**证同测试（Identity test）**：

```cpp
Widget& operator=(const Widget& rhs) {
    if (this == &rhs) return *this;        // 若是自我赋值，则不做任何事

    delete pRes;
    pRes = new Resource(*rhs.pRes);
    return *this;
}
```

另一个常见的做法是只关注异常安全性，而不关注是否自我赋值：

```cpp
Widget& operator=(const Widget& rhs) {
    Resource* pOrigin = pRes;             // 先记住原来的pRes指针
    pRes = new Resource(*rhs.pRes);       // 复制传入的资源
    delete pOrigin;                       // 删除原来的资源
    return *this;
}
```

仅仅是适当安排语句的顺序，就可以做到使整个过程具有异常安全性。

> 注：这种情况下如果是自我赋值，仅仅是销毁又重新分配了一次空间。这是非常符合常理的办法，虽然有一些性能损耗。
>
> 同时，下面两种方法本质上与此等价。

还有一种取巧的做法是使用 copy and swap 技术，这种技术聪明地利用了栈空间会自动释放的特性，这样就可以通过析构函数来实现资源的释放：

```cpp
Widget& operator=(const Widget& rhs) {
    Widget temp(rhs);
    std::swap(*this, temp);
    return *this;
}
```

上述做法还可以写得更加巧妙，就是利用按值传参，自动调用构造函数：

```cpp
Widget& operator=(Widget rhs) {
    std::swap(*this, rhs);
    return *this;
}
```

### 条款 12：复制对象时勿忘其每一个成分

这个条款正如其字面意思，当你决定手动实现拷贝构造函数或拷贝赋值运算符时，忘记复制任何一个成员都可能会导致意外的错误。

1. 如果在编码过程中为类新增了成员变量，必须同时修改 **copying函数**。（当然也需要修改类的所有**构造函数**，以及任何非标准形式的**operator=**)。如果你忘记，编译器不太可能提醒你。

2. 当使用继承时，继承自基类的成员往往容易忘记在派生类中完成复制，如果你的**基类拥有拷贝构造函数和拷贝赋值运算符，应该记得调用它们**：

   ```cpp
   class PriorityCustomer : public Customer {
   public:
       PriorityCustomer(const PriorityCustomer& rhs);
       PriorityCustomer& operator=(const PriorityCustomer& rhs);
       ...
   
   private:
       int priority;
   }
   
   PriorityCustomer::PriorityCustomer(const PriorityCustomer& rhs)
       : Customer(rhs),                // 调用基类的拷贝构造函数
         priority(rhs.priority) {
       ...
   }
   
   PriorityCustomer::PriorityCustomer& operator=(const PriorityCustomer& rhs) {
       Customer::operator=(rhs);       // 调用基类的拷贝赋值运算符
       priority = rhs.priority;
       return *this;
   }
   ```


注意，不要尝试在拷贝构造函数中调用拷贝赋值运算符，或在拷贝赋值运算符的实现中调用拷贝构造函数，一个在初始化时，一个在初始化后，它们的功用是不同的。

再次强调：`Copying`函数应该确保复制“**对象内的所有成员变量**”及“**所有base class成分**”。