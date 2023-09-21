---
title: Effective C++ - Item49-52 - 定制new和delete
categories: 笔记
tags:
  - EffectiveC++
date: 2023-09-21 12:26:30
---
# Effective C++ - Item49-52 - 定制new和delete

### 总览

这一模块的内容是在完整阅读《Effective C++》的基础上，参考了[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的[一篇文章学完 Effective C++：条款 & 实践](https://zhuanlan.zhihu.com/p/613356779)进行总结。虽然[缪之灵](https://www.zhihu.com/people/96-61-29-67)大佬的文章将最重要的部分总结的非常到位，但在此结合自己的理解和编程实践对其进行补充，并订正一些错误，以方便自己后续总结回顾，同时在尽可能保持简洁的前提下提高可读性。虽然原书有些地方写的比较拖沓，但作为经典的C++参考书，想要了解更多的细节，还是值得仔细去阅读的。

同时，假定阅读文章时对C++已经具有本科高级语言程序设计课程内容的理解水平。大部分情况下，除非它很重要，不会对C++基础的语法特性进行介绍。

本部分是第七章内容，对**条款49-52**进行介绍。

这一部分是对资源管理的延伸。其中条款16提到了成对使用new和delete时要采取相同形式。当我们为了各种目的（条款50）要自定义new和delete时，会发现有更多可能踩的坑，极有可能造成资源泄漏。这也非常考验我们C++的功力。因此虽然只有4个条款，但篇幅并不短。下面便对此进行详细的介绍，并穿插简略介绍现代C++有关内存管理的内容。

### 条款 49：了解 new-handler 的行为

当`operator new`无法满足某一内存分配需求时，会不断调用一个客户指定的错误处理函数，即所谓的 **new-handler**，直到找到足够内存为止，调用声明于`<new>`中的`set_new_handler`可以指定这个函数。`new_handler`和`set_new_handler`的定义如下：

```cpp
namespace std {
    using new_handler = void(*)();
    new_handler set_new_handler(new_handler) throw ();    // 返回值为原来持有的 new-handler
}
```

> 现代C++就不要再用` throw()`了（C++20已移除），用`noexcept`。后面代码也不会再写`throw()`了。

当`operator new`无法满足内存申请时，它会**不断**调用`new-handler`函数，直到找到足够内存。

一个设计良好的 new-handler 函数必须做以下事情之一：

**让更多的内存可被使用：** 可以让程序一开始执行就分配一大块内存，而后当 `new-handler` 第一次被调用，将它们释还给程序使用，造成`operator new`的下一次内存分配动作可能成功。

**设置另一个 new-handler：** 如果目前这个 `new-handler `无法取得更多内存，可以调换为另一个可以完成目标的` new-handler`。

具体的，调用`set_new_handler`，这样下一次调用`new_heandler`就可以做些不同的事。为了达到这个目的，可以让 `new-handler` 修改“会影响 `new-handler` 行为”的静态或全局数据。

**卸除 new-handler：** 将`nullptr`传给`set_new_handler`，这样会使`operator new`在内存分配不成功时抛出异常。

**抛出 bad_alloc（或派生自 bad_alloc）的异常：** 这样的异常不会被`operator new`捕捉，因此会被传播到内存分配处。

**不返回：** 通常调用`std::abort`或`std::exit`。

有的时候我们或许会希望在**为不同的类分配对象时，使用不同的方式处理内存分配失败情况**。这时候使用静态成员是不错的选择：

```cpp
class Widget{
public:
    static std::new_handler set_new_handler(std::new_handler p) noexcept;
    static void* operator new(std::size_t size);
private:
    static std::new_handler currentHandler;
};

// 做和 std::set_new_handler 相同的事情，将它获得的指针存储起来，然后返回先前(在此调用之前)存储的指针
std::new_handler Widget::set_new_handler(std::new_handler p) noexcept {
    std::new_handler oldHandler = currentHandler;
    currentHandler = p;
    return oldHandler; 
}

void* Widget::operator new(std::size_t size) {
    std::new_handler globalHandler = std::set_new_handler(currentHandler);  // 切换至 Widget 的专属 new-handler,暂存原来的供后续恢复
    void* ptr = ::operator new(size);                           // 分配内存或抛出异常
    std::set_new_handler(globalHandler);                        // 切换回全局的 new-handler
    return globalHandler;
}

std::new_handler Widget::currentHandler = nullptr;
```

> 看上去写的有点复杂，再理一下我们要干什么：我们要为`Widget`写一个其专属的`handler`，其行为和标准的`handler`一致，但只对`Widget`生效，而且只对下一次new生效。

`Widget`的客户应该类似这样使用其 new-handling：

```cpp
void OutOfMem(){
  std::cout<<"Custom handler when running out of memory!"
}

Widget::set_new_handler(OutOfMem);
Widget* pw1 = new Widget;              // 若分配失败，则调用 OutOfMem

Widget::set_new_handler(nullptr);
Widget* pw2 = new Widget;              // 若分配失败，则抛出异常
```

实现这一方案的代码并不因类的不同而不同，因此对这些代码加以复用是合理的构想。一个简单的做法是建立起一个“mixin”风格的基类，让其派生类继承它们所需的`set_new_handler`和`operator new`，并且使用模板确保每一个派生类获得一个实体互异的`currentHandler`成员变量：

```cpp
template<typename T>
class NewHandlerSupport {       // “mixin”风格的基类
public:
    static std::new_handler set_new_handler(std::new_handler p) noexcept;
    static void* operator new(std::size_t size);
    ...                         // 其它的 operator new 版本，见条款 52
private:
    static std::new_handler currentHandler;
};

template<typename T>
std::new_handler NewHandlerSupport<T>::set_new_handler(std::new_handler p) noexcept {
    std::new_handler oldHandler = currentHandler;
    currentHandler = p;
    return oldHandler;
}

template<typename T>
void* NewHandlerSupport<T>::operator new(std::size_t size) {
    std::new_handler globalHandler = std::set_new_handler(currentHandler);
    void* ptr = ::operator new(size);
    std::set_new_handler(globalHandler);
    return globalHandler;
}

template<typename T>
std::new_handler NewHandlerSupport<T>::currentHandler = nullptr;

//使用
class Widget : public NewHandlerSupport<Widget> {
public:
    ...                         // 不必再声明 set_new_handler 和 operator new
};
```

注意此处的模板参数`T`并没有真正被当成类型使用，而仅仅是用来区分不同的派生类，**利用模板机制为每个派生类具现化出一份对应的`currentHandler`**。

这个做法用到了所谓的 **CRTP（curious recurring template pattern，奇异递归模板模式）** 。

> C++的模版每具现化一次，都会生成其对应的具现化代码。通过上面的技巧写出的自定义handler代码，在`Widget`（或其他不同于`Widget`任何对象）的客户调用时，依旧可以直接使用`Widget::set_new_handler(OutOfMem);`。

除了在上述设计模式中用到之外，它也被用于实现**静态多态**：

```cpp
template <class Derived> 
struct Base {
    void Interface() {
        static_cast<Derived*>(this)->Implementation();      // 在基类中暴露接口
    }
};

struct Derived : Base<Derived> {
    void Implementation();                                  // 在派生类中提供实现
};
```

除了会调用 new-handler 的`operator new`以外，C++ 还保留了传统的“分配失败便返回空指针”的`operator new`，称为 `nothrow new`，通过`std::nothrow`对象来使用它：

```cpp
Widget* pw1 = new Widget;                   // 如果分配失败，抛出 bad_alloc
if (pw1 == nullptr) ...                     // 这个测试一定失败

Widget* pw2 = new (std::nothrow) Widget;    // 如果分配失败，返回空指针
if (pw2 == nullptr) ...                     // 这个测试可能成功
```

`nothrow new` 对异常的强制保证性并不高，使用它只能保证`operator new`不抛出异常，而无法保证像`new (std::nothrow) Widget`这样的表达式不会导致异常，因此**实际上并没有使用 nothrow new 的需要**。

### 条款 50：了解 new 和 delete 的合理替换时机

以下是常见的替换默认`operator new`和`operator delete`的理由：

**用来检测运用上的错误：** 如果将“new 所得内存”delete 掉却不幸失败，会导致内存泄漏；如果在“new 所得内存”身上多次 delete 则会导致未定义行为。

此外各式各样的编程错误可能导致 **“overruns”（写入点在分配区块尾端之后）** 和 **“underruns”（写入点在分配区块起点之前）**，以额外空间放置特定的 byte pattern 签名，检查签名是否原封不动就可以检测此类错误，下面给出了一个这样的范例：

```cpp
static const int signature = 0xDEADBEEF;              // 调试“魔数”
using Byte = unsigned char;

void* operator new(std::size_t size) {
    using namespace std;
    size_t realSize = size + 2 * sizeof(int);         // 分配额外空间以塞入两个签名

    void* pMem = malloc(realSize);                    // 调用 malloc 取得内存
    if (!pMem) throw bad_alloc();

    // 将签名写入内存的起点和尾端
    *(static_cast<int*>(pMem)) = signature;
    *(reinterpret_cast<int*>(static_cast<Byte*>(pMem) + realSize - sizeof(int))) = signature;

    return static_cast<Byte*>(pMem) + sizeof(int);    // 返回指针指向第一个签名后的内存位置
}
```

实际上这段代码**不能保证内存对齐**，并且有许多地方不遵守 C++ 规范，我们将在条款 51 中进行详细讨论。

> 比如x86平台上int4字节，double8字节。尽管Intel x86 上的doubles可被以任何byte边界对齐，但如果它是8-byte对齐，其访问速度会快许多。这个程序便不能保证。
>
> 所以作者还是认为有必要替换默认new和delete，但建议不要自己造轮子，可以根据需求看看已有的开源或者商业实现。

**为了收集使用上的统计数据：** 定制 new 和 delete 动态内存的相关信息：分配区块的大小分布，寿命分布，FIFO（先进先出）、LIFO（后进先出）或随机次序的倾向性，不同的分配/归还形态，使用的最大动态分配量等等。

**为了增加分配和归还的速度：**  译器所带的`operator new`s和`operator delete`s需要考虑更多通用的因素。当定制的分配器专门针对某特定类型之对象设计时**类专属的分配器可以做到“区块尺寸固定”**，例如 Boost 提供的 Pool  程序库。又例如，编译器所带的内存管理器是线程安全的，但如果你的程序是单线程的，你也可以考虑写一个不线程安全的分配器来提高速度。当然，这需要你对程序进行分析，并确认程序瓶颈的确发生在那些内存函数身上。

**为了降低缺省内存管理器带来的空间额外开销：** 泛用型分配器往往（虽然并非总是）还比定制型分配器使用更多内存，那是因为它们常常在每一个分配区块身上导致某些额外开销。针对小型对象而开发的分配器（例如 Boost 的 Pool 程序库）本质上消除了这样的额外开销。

**为了弥补缺省分配器中的非最佳内存对齐（suboptimal alignment）：**上文例子已经讲过。`std::max_align_t`用来返回当前平台的最大默认内存对齐类型，对于`malloc`分配的内存，其对齐和`max_align_t`类型的对齐大小应当是一致的，但若对`malloc`返回的指针进行偏移，就没有办法保证内存对齐。
> 下面对现代C++中内存对齐的内容进行较深入讨论：
>
> 在 C++11 中，提供了以下内存对齐相关方法：
>
> ```cpp
> // alignas 用于指定栈上数据的内存对齐要求
> struct alignas(8) testStruct { double data; };
> //ps：指定的必须是2的次幂，如果指定的次数大，超过下面提到的max_align_t，不一定能得到保证。这被叫做over-aligned。C++17对其进行了修复。
> 
> // alignof 和 std::alignment_of 用于得到给定类型的内存对齐要求
> std::cout << alignof(std::max_align_t) << std::endl;
> std::cout << std::alignment_of<std::max_align_t>::value << std::endl;
> //通常等于double所占字节数
> 
> // std::align 用于在一大块内存中获取一个符合指定内存要求的地址
> struct Arena {
>   void* ptr = 0;
>   std::size_t size_remain = 0;
>   
>   [[nodiscard]]
>   auto aligned_alloc(std::size_t alignment, std::size_t size) noexcept -> void*
>   {	//参数：期望的对齐方式，每个对齐单元大小，要对齐内存块的起始地址，要对齐内存块的大小；返回：内存块中满足对齐条件的指针，没有返回nullptr
>     void* res = std::align(alignment, size, ptr, size_remain);
>     if (res) {
>         ptr = static_cast<std::byte*>(res) + size;
>         size_remain -= size;
>         return res;
>     }
>     return nullptr;
>   }
> };
> ```
>
> 可以参考[文档](https://en.cppreference.com/w/cpp/memory/align)。上面的案例取自[Align Allocator实现](https://lesleylai.info/zh/std-align/)，实际上现在C++17已经提供了`std::aligned_alloc`实现。
>
> 在 C++17 后，可以使用`std::align_val_t`来重载需求额外内存对齐的`operator new`：
>
> ```cpp
> void* operator new(std::size_t count, std::align_val_t al);
> ```
>
>但是，这样必须同时重载与之配套的operator delete。具体的，需要手动进行对象析构并且选择合适的带有对齐参数的delete。可以参见[这里](https://github.com/MeouSker77/Cpp17/blob/master/markdown/src/ch30.md)

**为了将相关对象成簇集中：**  如果你知道特定的某个数据结构往往被一起使用，而你又希望在处理这些数据时将“内存页错误（page  faults）”的频率降至最低，那么可以考虑为此数据结构创建一个堆，将它们成簇集中在尽可能少的内存页上。一般可以使用 placement new 达成这个目标（见条款 52）。

**为了获得非传统的行为：** 有时候你会希望`operator new`和`operator delete`做编译器版不会做的事情，例如分配和归还共享内存（shared memory），而这些事情只能被 C API 完成，则可以将 C API 封在 C++ 的外壳里，写在定制的 new 和 delete 中。

>  这涉及到linux系统调用。

### 条款 51：编写 new 和 delete 时需固守常规

我们在条款 49 中已经提到过一些`operator new`的规矩，比如内存不足时必须不断调用 new-handler，如果无法供应客户申请的内存，就抛出`std::bad_alloc`异常。C++ 还有一个奇怪的规定，即使客户需求为0字节，`operator new`也得返回一个合法的指针，这种看似诡异的行为其实是为了简化语言其他部分。

根据这些规约，我们可以写出非成员函数版本的`operator new`伪代码：

```cpp
void* operator new(std::size_t size) {
    using namespace std;

    if (size == 0)      // 处理0字节申请
        size = 1;       // 将其视为1字节申请

    while (true) {
        if (分配成功)
            return (一个指针，指向分配得到的内存)

        // 如果分配失败，调用目前的 new-handler
        auto globalHandler = get_new_handler(); // since C++11

        if (globalHandler) (*globalHandler)();
        else throw std::bad_alloc();
    }
}
```

> 在C++11之前，我们没有任何办法可以直接取得new-handling函数指针。只能这样：
>
> ```cpp
> new handler globalHandler set_new_handler(0);
> set_new_handler(globalHandler);
> ```
>
> 这在多线程情况下可能出问题，必须加锁保证事务语义。

上面的伪代码可以看做对条款49的具体遵循。

`operator new`的成员函数版本一般只会分配大小刚好为类的大小的内存空间，但是情况并不总是如此，比如假设我们没有为派生类声明其自己的`operator new`，那么派生类会从基类继承`operator new`，这就导致派生类使用的是基类的 new 分配方式，但派生类和基类的大小很多时候是不同的。

> ```cpp
> class Base{
> public:
>     static void* operator new(std:size t size)throw(std::bad alloc);
> ...
> }
> class Derived:public Base {...};//假设Derived未声明operator new
> 
> Derived* p new Derived; //这里调用的是Base::operator new
> ```
>
> 

处理此情况的最佳做法是将“内存申请量错误”的调用行为改为采用标准的`operator new`：

```cpp
void* Base::operator new(std::size_t size) throw(std::bad_alloc){
    if (size != sizeof(Base))
        return ::operator new(size);    // 转交给标准的 operator new 进行处理
    ...
}
```

注意在`operator new`的成员函数版本中我们也不需要检测分配的大小是否为0了，因为在条款 39 中提到过，非附属对象必须有非零大小，所以`sizeof(Base)`无论如何也不能为0。

如果你打算实现`operator new[]`，即所谓的 array new，那么你唯一要做的一件事就是分配一块未加工的原始内存，因为你无法对 array 之内迄今尚未存在的元素对象做任何事情，实际上你甚至无法计算这个 array 将含有多少元素对象，在多态的情境下更是如此。

> 在More Effective C++ 条款3中提到，绝对不要以多态(polymorphically)方式处理数组。对此情况进行了进一步的解释。

`operator delete`的规约更加简单，你需要记住的唯一一件事情就是 C++ 保证 **“删除空指针永远安全”**：

```cpp
void operator delete(void* rawMemory) noexcept {
  	//如果被删除的是null指针，什么也不用做
    if (rawMemory == 0) return;

    // 归还 rawMemory 所指的内存
}
```

`operator delete`的成员函数版本要多做的唯一一件事就是将大小有误的删除行为转交给标准的`operator delete`：

```cpp
void Base::operator delete(void* rawMemory, std::size_t size) noexcept {
    if (rawMemory == 0) return;
    if (size != sizeof(Base)) {
        ::operator delete(rawMemory);    // 转交给标准的 operator delete 进行处理
        return;
    }

    // 归还 rawMemory 所指的内存
}
```

**如果即将被删除的对象派生自某个基类而后者缺少虚析构函数，那么 C++ 传给`operator delete`的`size`大小可能不正确**，这或许是“为多态基类声明虚析构函数”的一个足够的理由，能作为对条款 7 的补充。

### 条款 52：写了 placement new 也要写 placement delete

> 

placement new 最初的含义指的是“**接受一个指针指向对象该被构造之处**”的`operator new`版本，它在标准库中的用途广泛，其中之一是负责在 vector 的未使用空间上创建对象，它的声明如下：

```cpp
void* operator new(std::size_t, void* pMemory) noexcept;
```

我们此处要讨论的是广义上的 placement new，即**带有附加参数的`operator new`**，都叫placement new。例如下面这种：

```cpp
void* operator new(std::size_t, std::ostream& logStream);

auto pw = new (std::cerr) Widget;
```

当我们在使用 new 表达式创建对象时，共有两个函数被调用：一个是用以分配内存的`operator new`，一个是对象的构造函数。假设第一个函数调用成功，而第二个函数却抛出异常，那么会由 C++ runtime 调用`operator delete`，归还已经分配好的内存。

> 如：`Widget* pw new Widget;`共有两个函数被调用：一个是用以分配内存的operator new，一个是Widget的 default构造函数。

这一切的前提是 C++ runtime 能够找到`operator new`对应的`operator delete`。

如果我们使用的是自定义的 placement new，而没有为其准备对应的 placement delete 的话，就无法避免发生内存泄漏。

在下面的情景下我们希望在动态创建一个Widget时将相关的分配信息志记(Iogs)于cerr：

```cpp
Widget *pw=new (std:cerr) Widget;
```

因此，合格的代码应该是这样的：

```cpp
class Widget {
public:
    static void* operator new(std::size_t size, std::ostream& logStream);   // placement new

    static void operator delete(void* pMemory);                             // delete 时调用的正常 operator delete
    static void operator delete(void* pMemory, std::ostream& logStream);    // placement delete，需要配套提供
};
```

另一个要注意的问题是，由于成员函数的名称会掩盖其外部作用域中的相同名称（见条款 33），所以单纯提供 placement new 会导致无法使用正常版本的`operator new`：

```cpp
class Base {
public:
    static void* operator new(std::size_t size, std::ostream& logStream);
    ...
};

auto pb = new Base;             // 无法通过编译！因为正常形式的operator new被掩盖。
auto pb = new (std::cerr) Base; // 正确
```

同样道理，派生类中的`operator new`会掩盖全局版本和继承而得的`operator new`版本：

```cpp
class Derived : public Base {
public:
    static void* operator new(std::size_t size); //重新声明正常形式的new
    ...
};

auto pd = new (std::clog) Derived;  // 无法通过编译！因为Base的 placement new被掩盖了.
auto pd = new Derived;              // 正确
```

为了避免名称遮掩问题，需要确保以下形式的`operator new`对于定制类型仍然可用（这些是C++标准程序库默认提供的），除非你的意图就是阻止客户使用它们：

```cpp
void* operator(std::size_t) throw(std::bad_alloc);           // normal new
void* operator(std::size_t, void*) noexcept;                 // placement new
void* operator(std::size_t, const std::nothrow_t&) noexcept; // nothrow new
```

> 这一部分的逻辑和类的构造函数类似。

一个最简单的实现方式是，准备一个基类，内含所有正常形式的 new 和 delete：

```cpp
class StadardNewDeleteForms{
public:
    // normal new/delete
    static void* operator new(std::size_t size){
        return ::operator new(size);
    }
    static void operator delete(void* pMemory) noexcept {
        ::operator delete(pMemory);
    }

    // placement new/delete
    static void* operator new(std::size_t size, void* ptr) {
        return ::operator new(size, ptr);
    }
    static void operator delete(void* pMemory, void* ptr) noexcept {
        ::operator delete(pMemory, ptr);
    }

    // nothrow new/delete
    static void* operator new(std::size_t size, const std::nothrow_t& nt) {
        return ::operator new(size,nt);
    }
    static void operator delete(void* pMemory,const std::nothrow_t&) noexcept {
        ::operator delete(pMemory);
    }
};
```

凡是想以自定义形式扩充标准形式的客户，可以利用继承和`using`声明式（见条款 33）取得标准形式：

```cpp
class Widget: public StandardNewDeleteForms{
public:
    using StandardNewDeleteForms::operator new;
    using StandardNewDeleteForms::operator delete;

    static void* operator new(std::size_t size, std::ostream& logStream);
    static void operator detele(std::size_t size, std::ostream& logStream) noexcept;
    ...
};
```
