---
title: C++拾遗
categories: 笔记
tags:
  - C++
abbrlink: 41371
---
## C++回顾复习

#### Lec1-2

##### 保留字

main不是C++中的保留字。因此`int main;`在C++中合法。

##### 枚举常量

`enum t1 {a1,a2=7,a3,a4=15}time;`

则枚举常量`a1`和`a3`的值分别是0和8

以下对枚举类型名的定义中正确的是

![image-20221006143112706](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/c%2B%2B/20221006205903569808_152_image-20221006143112706.png)

枚举值对应的整数值可以是任意整数。

注意区分枚举类型定义和枚举类型变量定义。前者定义的数据类型，后者是定义变量。定义类型名时不应该有=

还可以这样写

```c++
enum team{my, your=4, his, her=his+10};
cout<<my<<' '<<your<<' '<<his<<' '<<her<<endl;
```

结果`0 4 5 15`



##### string

关于字符串类型

![image-20221006142909708](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/c%2B%2B/20221006205904459199_980_image-20221006142909708.png)