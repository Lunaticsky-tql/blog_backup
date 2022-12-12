---
title: c++_基本语法和运算
categories: 笔记
tags:
  - C++
---
## C++回顾复习

<div class="note note-info">注：此系列内容仅供应对C++程序设计基础笔试使用。</div>

### 认识C++

#### 基本概念和词汇

main不是C++中的保留字。因此`int main;`在C++中合法。

<div class="note note-secondary">下列哪个是C++语言的合法的字符常量
"0"
'054’
‘\x89'
‘\092’</div>

> A选项，双引号表示的是字符串常量；B选项054表示八进制整数，但是缺少转义符号\；D选项是将其后的整数092表示八进制整数，但是八进制不存在9这个数。注意，单引号表示的字符常量，可以是整数，但必须带有转义符号\，其字符常量为整数表示的ASC码对应的字符

一个经常设坑的点：八进制表达中出现8或9

#### 枚举常量

`enum t1 {a1,a2=7,a3,a4=15}time;`

则枚举常量`a1`和`a3`的值分别是0和8

枚举值对应的整数值可以是任意整数。

注意区分枚举类型定义和枚举类型变量定义。前者定义的数据类型，后者是定义变量。定义类型名时不应该有=

<div class="note note-warning">因此 enum a=[one,two,three);是不对的</div>

还可以这样写

```c++
enum team{my, your=4, his, her=his+10};
cout<<my<<' '<<your<<' '<<his<<' '<<her<<endl;
```

结果`0 4 5 15`

#### string

关于字符串类型

使用`.length()`和`strlen()`时计算的字符串长度都不包含`\0`

<div class="note note-warning">注意:+不支持两个字符串字面常量的连接,如 string word4 "hello"+"world!";</div>

### 运算符和表达式

#### 基本概念

在学习了编译原理之后，对这些概念以及对应的“奇特”写法应当已经见怪不怪。但为应对考试，仍记录以备复习。

##### 表达式

![image-20221013141835992](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/c%2B%2B_%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95%E5%92%8C%E8%BF%90%E7%AE%97/20221027094522795684_122_image-20221013141835992.png)

注意，“表达式”不带分号，带了分号就是语句。

#### 优先级和结合性

```c++
#include <iostream>

int main() {
    //test 1
    int k, a, b, c;
    unsigned long w = 5;
    double x = 1.42;
//    x%(-3); <Invalid operands to binary expression ('double' and 'int')>
    w += -2; // w=3
    k = (a = 2, b = 3, a + b); // k=5
    c = k = a = 2, b = 3, a + b; // c=5, k=2, a=2, b=3
    a += a -= (b = 4) * (a = 3); // a=-18, b=4
    printf("a=%d", a);

    //test 2
    int d2i = 'A' + 1.6;
    printf("a2=%d", d2i); //'A'+1.6=66.6=66 (ASCII code of 'A' is 65)

    //test3
/*    d=9+e+f=d+9;
    expression is a value, not a variable in the memory,so it is not assignable */
}
```

[优先级和结合性一览](https://blog.csdn.net/zb_915574747/article/details/99704639)

#### 赋值运算

```c++
设有intx=11：，则表达式(x++*1/3)的值是
```

$\lfloor 11*1/3 \rfloor=3$

![image-20221013142054782](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/c%2B%2B_%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95%E5%92%8C%E8%BF%90%E7%AE%97/20221027094525768953_130_image-20221013142054782.png)

做题时容易犯的错误：

````c++
若d为double型变量，则表达式d=1，d+5，d++的值是
1。d+5不是d=d+5。虽然很明显，做题的时候也需要有注意的意识
````

#### 逻辑运算

![image-20221020095906292](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/c%2B%2B_%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95%E5%92%8C%E8%BF%90%E7%AE%97/20221027094527376104_753_image-20221020095906292.png)

注意算术运算符优先于关系和除非以外的逻辑运算符！

短路运算举例：

```c++
×=y=3;t=++x||++y后，y的值是
```

> 3，因为后面不会被运算

优先级只是起“加括号”的作用。

```c++
int c,h;
std::cout<<((c=2)&&(h=-2));
//always true
```

#### 位运算

![image-20221020105755065](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/c%2B%2B_%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95%E5%92%8C%E8%BF%90%E7%AE%97/20221027094529486139_294_image-20221020105755065.png)

![image-20221020104858172](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/c%2B%2B_%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95%E5%92%8C%E8%BF%90%E7%AE%97/20221027094532506509_144_image-20221020104858172.png)

注意位运算的“地位”不是平等的，不要想当然按顺序算

#### 条件和逗号运算符

![image-20221020111433316](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/c%2B%2B_%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95%E5%92%8C%E8%BF%90%E7%AE%97/20221027094533764720_298_image-20221020111433316.png)

```c++
#include <iostream>
#include<iomanip>

using namespace std;
int main(
{
cout<<(0101&101>>3|101<<3^~0x10)<<endl;
return 0;
}

```
> 优先级按位取反~最高，先将0x10（十六进制）按位取反，得到结果11111111 11111111 11111111 11101111，其次优先级按位左移和按位右移运算符优先级相同，计算101>>3得到 00000000 00000000 00000000 00001100，以及101<<3得到 00000000 00000000 00000011 00101000，接下来计算0101（八进制）按位与（101>>3）的结果，得到结果为0,0按位或一个数所得结果为原值。因此最终答案为(101<<3)按位异或(~0x10)的结果，其结果为11111111 11111111 11111100 11000111，为负数，求补得到绝对值。 特别需要注意的是取反的时候是对整个int取反，16变-17

```c++
设intm=5；float x=3.5；则表达式m+x+4.5的结果应占据[填空]个字节。
//8.在隐式类型转换中转向了double
```

