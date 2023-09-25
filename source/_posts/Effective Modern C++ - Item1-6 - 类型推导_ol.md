---
title: Effective Modern C++ - Item1-6 - 类型推导
categories: 笔记
tags:
  - EffectiveC++
abbrlink: 27022
date: 2023-09-25 14:27:09
---
# Effective Modern C++ - Item1-6- 类型推导

## 总览

这一部分是阅读Effective Modern C++的笔记。在此结合自己的理解和编程实践对其进行补充，并订正一些错误，以方便自己后续总结回顾，同时在尽可能保持简洁的前提下提高可读性。原书可在[这里](https://cntransgroup.github.io/EffectiveModernCppChinese)查看非官方的中文翻译。

本部分整合了原书内容的一到二章，对**条款1-6**进行介绍，同时结合阅读的体验适当调整了顺序或改变了叙述方式。原作者可能假设我们已经对C++非常了解，着重讲述了很多特例，一开始阅读很容易迷失在细节里。和原书顺序相比，我更希望适应从简单到复杂，从一般到特例的学习规律去总结讲述。

同时，将可能需要补充的前置知识或者作者补充的不那么重要的“冷知识”，以及可能需要的进一步解释放到块引用中，避免喧宾夺主的同时对内容进行适当补充或简略。

阅读本节前你需要知道对C++的移动语义有所了解。这一部分在原书简介有介绍。如果你已经有最基本的了解，可以跳过下面内容。

> 首先我们想为什么要有移动语义。
>
> 某个对象包含一些指针，这些指针所指的内容很多。回顾一下，我们知道在拷贝对象的时候，编译器默认会按值拷贝所有的数据。对于指针，我们需要自定义拷贝构造函数重新分配内存并复制原对象指针的数据，以保证和原对象独立（不知道的话该重学C++了）。这些指针所指的内容很多，导致新开辟内存，复制数据的开销很大。而有了移动语义，我们可以仅仅改变指针的指向，将原对象的指针置为空，便实现了内存资源从原对象到目标对象的迁移。可以看出，移动后的原对象**通常不再有效**，直到被赋予新的值。
>
> 移动语义的基础是区分右值和左值表达式。那是因为右值表明这个对象适合移动操作，而左值一般不适合。
>
> 概念上（尽管不经常在实际上用），右值对应于**临时对象**，而左值对应于你**可以引用**的（can refer to），实实在在存在的对象，或者通过名字，或者通过指针或左值引用。
>
> 临时对象包含字面量，函数返回的临时值等。
>
> 顾名思义，接受左值的引用是左值引用，接受右值的引用是右值引用，如下：
>
> ```cpp
> class A{};
> A & rl = A();  //错误，无名临时变量 A() 是右值，因此不能初始化左值引用 r1
> A && r2 = A();  //正确，因 r2 是右值引用
> ```
>
> 有两种实践上的心智模型帮助判断一个值是左值还是右值。一种是，可以被赋值的是左值，不能的是右值，
>
> ```cpp
> int a = 5; // a是左值
> 5 = a; //错误，5 不能为左值
> ```
>
> 另一种贴近本质，看看能否取得它的地址。如果能取地址，那么通常就是左值。如果不能，则通常是右值。
>
> 比如：
>
> ```cpp
> class Widget {
> public:
>     Widget(Widget&& rhs);   //rhs(right-hand side)是个左值，
>     …                       //尽管它有个右值引用的类型
> };
> 
> ```
>
> `rhs`虽然用`&&`修饰，但它是实实在在的左值。因为它是函数的参数，被放到栈上。在函数里`rhs`的地址非常合理。事实上这个`&&`仅代表它是`Widget`的**移动构造函数**，以和拷贝构造函数区分。
>
> 至于移动构造函数怎么用，怎么移动对象，这一部分会涉及，但是都会给出解释。现在你只需要理解移动语义和左值右值的概念就可以了。

## 条款一：理解模板类型推导

类型推导其实算不上新东西。C++98早有一套类型推导的规则：用于函数模板的规则。这一部分看上去可能有点抽象和无聊。不要着急。理解模版类型推导对理解C++11中的`auto`非常重要，因此单独拎出来讲解。

> 如果对于类型推导操作没有一个扎实的理解，要想写出有现代感的C++程序是不可能的。

考虑这样一个函数模版：

```cpp
template<typename T>
void f(ParamType param);
```

编译器会通过表达式`expr`推导出两个类型：一个是`T`的类型，另一个是`ParamType`的类型。马上就可以看到，这两个类型往往不一样。

先举个例子理解一下概念：

如果模板这样声明：

```cpp
template<typename T>
void f(const T& param);         //ParamType是const T&
```

然后这样进行调用：

```cpp
int x = 0;                      //expr
f(x);                           //用一个int类型的变量调用f
```

`T`被推导为`int`，`ParamType`被推导为`const int&`。

### Case 1: `ParamType`既不是指针也不是引用

先看“看上去”最简单的情况。当`ParamType`既不是指针也不是引用时，我们通过传值（pass-by-value）的方式处理，也即，无论传入的是什么，`param`都会是它的一个**副本**。

```cpp
template<typename T>
void f(T param);                //以传值的方式处理param
```

声明这些变量：

```cpp
int x=27;                       //x是int
const int cx=x;                 //cx是const int
const int& rx=x;                //rx是指向作为const int的x的引用
```

在不同的调用中，对`param`和`T`推导的类型会是这样：

```cpp
f(x);                           //T和param的类型都是int
f(cx);                          //T和param的类型都是int
f(rx);                          //T和param的类型都是int
```

你会发现不管是`T`还是`prarm`，都无视了引用和`const`。事实上如果有`volatile`也会忽略。

这很容易理解。`param`是一个**完全独立**于`cx`和`rx`的对象，都值传递了自然不会带着引用，具有常量性的`cx`和`rx`不可修改并不代表`param`也是一样。

理解了值传递的内涵，我们看下面的“特例”：

```cpp
template<typename T>
void f(T param);                //仍然以传值的方式处理param

const char* const ptr =         //ptr是一个常量指针，指向常量对象 
    "Fun with pointers";

f(ptr);                         //传递const char * const类型的实参
```

解引用符号（*）的右边的`const`表示`ptr`本身是一个`const`，不能指向其他对象；左边表示指向的是`const char*`。这时值传递会去除指针本身的常量性，而显然没有能力影响指针所指数据的类型。所以推导结果`T`和`param`的类型都是`const char*`。

### Case 2: `ParamType`是一个指针或引用

这种情况依旧很自然：

首先`T`不会带引用。

然后`expr`的类型与`ParamType`进行模式匹配，少啥补啥。

看例子。对于模版

```cpp
template<typename T>
void f(T& param);               //param是一个引用
```

```cpp
int x=27;                       //x是int
const int cx=x;                 //cx是const int
const int& rx=x;                //rx是指向作为const int的x的引用
```

看推导结果：

```cpp
f(x);                           //T是int，param的类型是int&
f(cx);                          //T是const int，param的类型是const int&
f(rx);                          //T是const int，param的类型是const int&
```

对象的常量性`constness`会被保留为`T`的一部分。因为当调用者传递一个`const`对象给一个**引用**类型的形参时，他们期望对象保持不可改变性。

显然我们指定了函数的参数是引用，抛开模版不谈，这时候不管是传值还是引用，函数都会以引用方式处理。所以`T`便不需要再重复说是个引用了。

对于指针本质是一样的：

```cpp
template<typename T>
void f(T* param);               //param现在是指针

int x = 27;                     //同之前一样
const int *px = &x;             //px是指向作为const int的x的指针

f(&x);                          //T是int，param的类型是int*
f(px);                          //T是const int，param的类型是const int*
```

### Case 3: `ParamType`是一个通用引用

首先，你可能疑惑什么是通用引用（Universal Reference）。通用引用也叫万能引用。可能还是什么也没说。那就先看例子：

```cpp
template<typename T>
void f(T&& param);
```

> 你想，这不是右值引用的符号吗？

条款24详细的介绍了通用引用。后面你会知道，**通用引用总是以`T&&`或等价的形式出现**。其必定和类型推导相关联。

简单的说，它既可以是右值引用，也可以是左值引用。如果传入的是左值，它会被推导为左值，传入的是右值，它会被推导为右值。

具体一点，先看它的推导结果：

```cpp
template<typename T>
void f(T&& param);              //param现在是一个通用引用类型
        
int x=27;                       //如之前一样
const int cx=x;                 //如之前一样
const int & rx=cx;              //如之前一样

f(x);                           //x是左值，所以T是int&，
                                //param类型也是int&

f(cx);                          //cx是左值，所以T是const int&，
                                //param类型也是const int&

f(rx);                          //rx是左值，所以T是const int&，
                                //param类型也是const int&

f(27);                          //27是右值，所以T是int，
                                //param类型就是int&&
```

如果你想从理论上理解这一部分的推导规则，可以参考条款28的引用折叠。

> C++不允许引用的引用。类型推导时多个引用撞到一起的时候（如 `Widget& &&`）如果任一引用为左值引用，则结果为左值引用。否则（即，如果引用都是右值引用），结果为右值引用。

你也可以直接从感性的角度理解：

首先看`ParamType`，通用引用之所以叫通用，就是它遇到左值变左值，遇到右值变右值。又因为本质是引用，常量性得到保留。

再看`T`。这是模板类型推导中唯一一种`T`被推导为引用的情况，而且传入左值的时候推导为引用，右值推导为值。这使得`T`本身可以保留传入变量是否为右值的信息，从而可以通过`std::forward`进行有条件的转换。

> `std::forward`的行为是，如果原始对象是右值，可以将其移动到返回值中（避免拷贝开销），但是如果原始对象是左值，必须创建副本。详见条款23和条款25。

可以看到，这一部分耦合了C++中移动语义的具体实现。不过后面也将会看到，这些概念也都是相互配套使用的，以达到移动语义潜在的性能优势。

### 特例：数组和函数实参

> 这一部分更像是冷知识，对这部分语法感兴趣可以看看，不看也不影响理解。

我们知道，C++中数组可以退化为指针，比如可以将`const char []`类型的数组赋值给一个`const char *`。

对于传值形参模版：

```cpp
const char name[] = "J. P. Briggs";     //name的类型是const char[13]
template<typename T>
void f(T param);                        //传值形参的模板

f(name);                                //T和param会推导成什么类型?
```

`T`被推导为`const char*`。

因为在C语言中，数组与指针形参是完全等价的，C++又保持了和C的兼容性。

```cpp
void myFunc(int param[]);
void myFunc(int* param);                //与上面相同的函数
```

但引用是C++的东西。虽然函数不能声明形参为真正的数组，但是**可以**接受指向数组的**引用**。

```cpp
template<typename T>
void f(T& param);                       //传引用形参的模板
```

```cpp
f(name);                                //T被推导为const char[13]
```

`f`的实参类型为`const char (&)[13]`。

> 是的，这种语法看起来简直有毒，但是知道它将会让你在关心这些问题的人的提问中获得**大**神的称号。
>
> 有趣的是，可声明指向数组的引用的能力，使得我们可以创建一个模板函数来推导出数组的大小：
>
> ```cpp
> //在编译期间返回一个数组大小的常量值（//数组形参没有名字，
> //因为我们只关心数组的大小）
> //constexpr使得结果在编译期间可用
> template<typename T, std::size_t N>
> constexpr std::size_t arraySize(T (&)[N]) noexcept
> {
>     return N;
> }
> ```
>
> 可以这样用：
>
> ```cpp
> int keyVals[] = { 1, 3, 7, 9, 11, 22, 35 };             //keyVals有七个元素
> 
> int mappedVals[arraySize(keyVals)];                     //mappedVals也有七个
> std::array<int, arraySize(keyVals)> mappedVals;         //mappedVals的大小为7
> ```

对于函数上面的讨论依旧是一样的，传值时，函数退化成函数指针，传引用是变成函数指针的引用。

```cpp
void someFunc(int, double);         //someFunc是一个函数，
                                    //类型是void(int, double)

template<typename T>
void f1(T param);                   //传值给f1

template<typename T>
void f2(T & param);                 //传引用给f2

f1(someFunc);                       //param被推导为指向函数的指针，
                                    //类型是void(*)(int, double)
f2(someFunc);                       //param被推导为指向函数的引用，
                                    //类型是void(&)(int, double)
```

## 条款二：理解auto类型推导

### 推导规则

前面之所以详细的讲模版类型推导的规则，是因为**`auto`类型推导和模板类型推导有一个直接的映射关系。**

很可能看例子就明白了：

```cpp
auto x = 27;
const auto cx = x;
const auto & rx=cx;
```

分别对应于下面的模型：

```cpp
template<typename T>            //概念化的模板用来推导x的类型
void func_for_x(T param){
      //推导结果对应于param类型
    cout << "deduced type: "
         << type_id_with_cvr<decltype(param)>().pretty_name()
         << '\n';
}

func_for_x(27);                 //概念化调用：
                                //param的推导类型是x的类型，int

template<typename T>            //概念化的模板用来推导cx的类型
void func_for_cx(const T param);

func_for_cx(x);                 //概念化调用：
                                //param的推导类型是cx的类型，const int

template<typename T>            //概念化的模板用来推导rx的类型
void func_for_rx(const T & param);

func_for_rx(x);                 //概念化调用：
                                //param的推导类型是rx的类型，const int&
```

**对于`auto`的修饰对应于函数形参中对模板参数`T`的修饰，推导结果对应于函数形参`param`的推导结果。**

理解了其中的对应关系，便不难理解下面的结果。这一部分对应于条款1中通用引用的case。

```cpp
auto x = 27;
const auto cx = x;
const auto & rx=cx;

auto&& uref1 = x;               //x是int左值，
                                //所以uref1类型为int&
auto&& uref2 = cx;              //cx是const int左值，
                                //所以uref2类型为const int&
auto&& uref3 = 27;              //27是int右值，
                                //所以uref3类型为int&&
```

模版类型推导中关于数组和函数参数推导的特例也适用于`auto`。

### 特例

`auto`会假定用大括号括起的初始化表达式代表一个`std::initializer_list`，但模板类型推导不会。

```cpp
auto x = { 11, 23, 9 };         //x的类型是std::initializer_list<int>
template<typename T>            //带有与x的声明等价的
void f(T param);                //形参声明的模板
f({ 11, 23, 9 });               //错误！不能推导出T
```

C++11添加了用于支持统一初始化（**uniform initialization**）的语法，但是由于这个特性，统一初始化和`auto`混用的时候还是要非常谨慎。关于这个语法的详细内容可以参见条款7。

## 条款三：理解decltype

### decltype基本用法

通常情况下`decltype`只是简单的返回名字或者表达式的类型。

```cpp
const int i = 0;                //decltype(i)是const int

bool f(const Widget& w);        //decltype(w)是const Widget&
                                //decltype(f)是bool(const Widget&)

struct Point{
    int x,y;                    //decltype(Point::x)是int
};                              //decltype(Point::y)是int
vector<int> v;                  //decltype(v)是vector<int>
```

一点都不奇怪。

`decltype`最主要的用途就是**用于声明函数模板，而这个函数返回类型依赖于形参类型**。下面举例说明。

假定我们写一个函数，一个形参为容器，一个形参为索引值，这个函数支持使用方括号的方式（也就是使用“`[]`”）访问容器中指定索引值的数据，然后在返回索引操作的结果前执行认证用户操作。

首先需要了解，对一个`T`类型的容器使用`operator[]` 通常会返回一个`T&`对象，比如`std::deque`就是这样。

> 但是`std::vector`有一个例外，对于`std::vector<bool>`，`operator[]`不会返回`bool&`，它会返回一个全新的对象。它实际上是一个代理对象。后面条款6会在再次提到这个问题。当然，Effective STL中也提到，尽量避免使用`vector<bool>`（条款18）。同时，也不应该期望写一个能适配所有容器的函数（条款2）。

如果我们使用C++14，我们可能会写成这样：

```cpp
template<typename Container, typename Index>    //C++14版本，
auto authAndAccess(Container& c, Index i)       //不那么正确
{
    authenticateUser();
    return c[i];                                //从c[i]中推导返回类型
}
```

C++14扩展到允许自动推导所有的*lambda*表达式和函数，甚至它们内含多条语句。但是，这里的问题是，尽管`operator[]`对于大多数`T`类型的容器会返回一个`T&`，但**函数的返回值是值传递**，按照模版类型推导规则（条款1case1），引用会被忽略。所以最终还是返回了右值。我们事实上期望的是和直接调用`operator[]`的行为一样，返回一个左值的引用。

我们这时应当使用`decltype`。

```cpp
template<typename Container, typename Index>
auto authAndAccess(Container& c, Index i)
    ->decltype(c[i])
{
    authenticateUser();
    return c[i];
}
```
这时候`decltype(c[i])`忠实的推导出我们想要返回的是`T&`。

> 函数名称前面的`auto`不会做任何的类型推导工作。相反的，他只是暗示使用了C++11的**尾置返回类型**语法，即在函数形参列表后面使用一个”`->`“符号指出函数的返回类型，尾置返回类型的好处是我们可以在函数返回类型中使用函数形参相关的信息。

### decltype(auto)

在C++14中也可以用`decltype(auto)`进行简化。

```cpp
template<typename Container, typename Index>
decltype(auto)
authAndAccess(Container& c, Index i)
{
    authenticateUser();
    return c[i];
}
```

我们可以这样理解`decltype(auto)`：`auto`说明符表示这个类型将会被推导，`decltype`说明`decltype`的规则将会被用到这个推导过程中。

> 上面的代码其实还有潜在的问题。如果传入的是一个右值容器，它是一个临时对象，那么它通常会在`authAndAccess`调用结束被销毁，但这时候却返回了指向其内部元素的引用，会造成未定义行为。
>
> ```cpp
> //你应该早已知道返回临时变量的引用的危险性。
> int& getLocalVariable() {
>     int x = 10;
>     return x; // x 在函数返回后销毁，但引用仍然存在
> }
> int main(){
>     int a=getLocalVariable();
>     std::cout<<a; //未定义行为！
> }
> ```
>
> 至于这个例子，我们可能会这样调用：
>
> ```cpp
> std::deque<std::string> makeStringDeque();      //工厂函数
> 
> //从makeStringDeque中获得第五个元素的拷贝并返回
> auto s = authAndAccess(makeStringDeque(), 5);
> ```
>
> 这就有问题。我们可以使用t通用引用和`std::forward`解决这个问题。这时传入左值容器返回左值，传入右值容器返回右值。
>
> ```cpp
> template<typename Container, typename Index>    //最终的C++14版本
> decltype(auto)
> authAndAccess(Container&& c, Index i)
> {
>     authenticateUser();
>     return std::forward<Container>(c)[i];
> }
> ```

当然，`decltype(auto)`的使用不仅仅局限于函数返回类型。当你想对初始化表达式使用`decltype`推导的规则，你也可以使用：

```cpp
Widget w;

const Widget& cw = w;

auto myWidget1 = cw;                    //auto类型推导
                                        //myWidget1的类型为Widget
decltype(auto) myWidget2 = cw;          //decltype类型推导
                                        //myWidget2的类型是const Widget&
```

### 特殊情况

将`decltype`应用于**单纯的变量名**会产生该变量名的声明类型。虽然变量名都是左值表达式，但这不会影响`decltype`的行为。

但是比单纯的变量名更复杂的左值表达式，`decltype`保证报告的类型始终是左值引用。

从这种行为的原因上讲倒是没什么太奇怪的，因为大多数左值表达式的类型天生具备一个左值引用修饰符。

具体的：

```cpp
int x = 0;
```

`decltype(x)`为`int`，但`decltype((x))`却是`int&`。用小括号覆盖一个名字可以改变`decltype`对于名字产生的结果。

所以当使用`decltype(auto)`的时候一定要加倍的小心。

## 条款四：掌握查看类型推导结果的方法

上面详细的介绍了关于类型

### IDE 编辑器

编辑代码的时候获得类型推导的结果。

`Clion`会显示，结果一般会比较准确。

### 编译器诊断信息

在编译期间获得结果。

```cpp
template<typename T>    // 只声明 TD 而不定义
class TD;               // TD 是 “类型显示类”（Type Displayer）的缩写

TD<decltype(x)> xType;  // 诱发包括 x 和 y 的类型的错误信息
TD<decltype(y)> yType;
```

如clang：`error: implicit instantiation of undefined template 'TD<int>'`

### 运行时输出

在运行时获得结果。

针对某个对象调用`typeid`，可以得到一个`std::type_info`对象，其拥有一个成员函数`name`，该函数产生一个代表类型的 C-style 的字符串。

但遗憾的是，不同编译器对于`std::type_info::name`的实现各不相同，无法保证完全可靠。并且按照标准，`std::type_info::name`中处理类型的方式和向函数模板按值传参一样，因此类型的引用性以及`const`和`volatile`限定符也将被忽略。

原书中介绍了 Boost.TypeIndex 第三方库用于代替`typeid`：

```cpp
#include <boost/type_index.hpp>

template<typename T>
void f(const T& param) {
    using std::cout;
    using boost::typeindex::type_id_with_cvr;

    // 显示 T 的类型
    cout << "T =          "
         << type_id_with_cvr<T>().pretty_name()
         << '\n';

    // 显示 param 的类型
    cout << "param =          "
         << type_id_with_cvr<decltype(param)>().pretty_name()
         << '\n';
    ...
}
```

## 条款五：优先选用 auto，而非显式类型声明

`auto`不仅简短，可以在用于复杂类型时少敲几个字，而且也降低了出错的可能。

它可以避免一些移植性和效率性的问题，也使得重构更方便。

首先，`auto`必须要求初始化，声明不初始化本来就是坏文明。

```cpp
auto x2;                        //错误！必须要初始化
```

再比如，对STL不那么了解的程序员可能会写出这样的代码：

```cpp
std::unordered_map<std::string, int> m;
...

for (const std::pair<std::string, int>& p : m) {
    ...
}
```

`std::unordered_map`的键值部分是 `const` 的（这在Effective STL条款22也有所提及）。所以哈希表中的`std::pair`类型应为`std::pair<const std::string, int>`而非`std::pair<std::string, int>`，类型的不匹配会导致额外的临时对象被复制出来，降低了运行效率。

使用`auto`就可以轻松避免这种问题：

```cpp
for (const auto& p : m) {
    ...
}
```

## 条款六：auto推导若非己愿，使用显式类型初始化惯用法

“隐形” 的代理类型可以导致`auto`根据初始化表达式推导出 “错误的” 类型，应该防止写出这样的代码：

```cpp
auto someVar = " 隐形 " 代理类型表达式;
```

一个隐形代理类的典型例子是`std::vector<bool>`，它经过了特化，与一般的`std::vector`的行为不同，和`std::bitset`的行为相似，使用一种压缩形式表示其持有的`bool`元素，每个`bool`元素用一个比特来表示。因此，`std::vector<bool>`的`operator[]`并不会直接返回一个`bool&`，而是会返回一个具有类似行为的`std::vector<bool>::reference`类型的对象，并可以隐式转换为`bool`类型。

```cpp
std::vector<bool> features(const Widget& w);
Widget w;

bool highPriority1 = features(w)[5];    // 得到正确的 bool 变量
auto highPriority2 = features(w)[5];    // 错误地得到了 std::vector<bool>::reference 对象
```

除了`std::vector<bool>`以外，标准库中的智能指针和另外一些 C++ 库中的类也使用了代理类的设计模式，例如为了提高数值计算代码效率的**表达式模板**技术：

```cpp
Matrix sum = m1 + m2 + m3 + m4; // 通过使 operator+ 返回结果的代理来提高效率
```

> 在实际编写代码时，记得通过查看文档或头文件中的函数原型来确认手头上的类是否为代理类。

解决代理类问题的做法是：使用带显式类型的初始值设定项来强制`auto`推导出你想要的类型。

```cpp
auto highPriority = static_cast<bool>(features(w)[5]);
```

这种用法并不仅限于会产生代理类型的初始值设定项，它同样可以应用于你想要强调创建一个类型不同于初始化表达式类型的场合，例如：

```cpp
double calcEpsilon();

float ep1 = calcEpsilon();                      // 进行从 double 到 float 的隐式类型转换
auto ep2 = static_cast<float>(calcEpsilon());   // 强调了类型转换的存在
```

总结一下：

- 不可见的代理类可能会使`auto`从表达式中推导出“错误的”类型
- 显式类型初始器惯用法强制`auto`推导出你想要的结果
