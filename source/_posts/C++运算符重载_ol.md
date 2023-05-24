---
title: C++运算符重载
categories: 笔记
tags:
  - C++
abbrlink: 53807
---
# C++运算符重载

关于重载自增自减运算符的一些深入讨论：

[参考](http://c.biancheng.net/view/247.html)

通常我们重载前置`++`运算符的返回值类型是 Obj &，而后置`++`运算符的返回值类型是 Obj，这是因为运算符重载最好保持原运算符的用法。C++ 固有的前置`++`运算符的返回值本来就是操作数的引用，而后置`++`运算符的返回值则是操作数值修改前的复制品。

例如：

```C++
int a = 5;(++a) = 2;
```

上面两条语句执行后，a 的值是 2，因为 ++a 的返回值是 a 的引用。而

```C++
(a++) = 2;
```

这条语句是非法的，因为 a++ 的返回值不是引用，不能作为左值。

换句话说，前置`++`返回左值，后置`++`返回右值。

当然，如果我们还重载了对象的加减等运算符，希望自增自减参与对象的这些运算，返回的应当是对象(这也是推荐的做法)，如果希望得到自增自减的“数值”，可以返回`int`。

但如果重载后置运算符时返回的是引用，有可能破坏类的封装性。如下：

```c++
#include<iostream>
using namespace std;
class Sample{
    int n;
public:
    Sample():n(0){}
    explicit Sample(int m){n=m;};
    int& operator--(int){
        n--;
        return n;
    }
    void disp(){
        cout<<n<<endl;
    }
};
int main(){
    Sample s(10);
    (s--)++;
    s.disp();
    return 0;
}
```

`(s--)`直接返回内部私有变量`n`的引用，则外部的++可越过限制改变其值。

## 继承和多态

![image-20230421161915507](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/C%2B%2B%E8%BF%90%E7%AE%97%E7%AC%A6%E9%87%8D%E8%BD%BD/20230519102654183213_668_image-20230421161915507.png)

![image-20230421161949156](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/C%2B%2B%E8%BF%90%E7%AE%97%E7%AC%A6%E9%87%8D%E8%BD%BD/20230519102655890997_284_image-20230421161949156.png)

