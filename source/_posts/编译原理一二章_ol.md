---
title: 编译原理一二章
categories: 笔记
tags:
  - 编译原理
abbrlink: 34738
---
## 编译原理一二章

### Lec1从代码到可执行文件

#### 编译器要做哪些事情？

![image-20220929095525300](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190733227216_229_image-20220929095525300.png)

##### 一些gcc编译选项

###### [Actions](https://clang.llvm.org/docs/ClangCommandLineReference.html#id6)

The action to perform on the input.

```shell
-E, --preprocess
Only run the preprocessor

-S, --assemble
Only run preprocess and compilation steps

-c, --compile
Only run preprocess, compile, and assemble steps

-emit-llvm
Use the LLVM representation for assembler and object files
```

###### [Compilation flags](https://clang.llvm.org/docs/ClangCommandLineReference.html#id7)

Flags controlling the behavior of Clang during compilation. These flags have no effect during actions that do not perform compilation.

```shell
-Xassembler <arg>`
Pass <arg> to the assembler

-Xclang <arg>, -Xclang=<arg>
Pass <arg> to clang -cc1
```



![image-20220920154109066](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190735472529_960_image-20220920154109066.png)

上面是**抽象语法树**：简化，只包含程序中出现的单词

下面是**语义分析树（具体语法树）**：完整，还包含抽象出的语法概念

##### 对过程的相关理解

<p class="note note-info">C++编译器检查相容类型计算是否合规是在语义分析阶段
编译器识别出标识符是在词法分析阶段</p>

<p class="note note-warning">C++编译器过滤注释是在___阶段。
答案是词法分析，但实践表明预处理阶段就已经过滤注释了。
C++编译器检查数组下标越界是在___阶段
C++并不会检查数组下标越界。</p>

![image-20220920162038518](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190736776341_330_image-20220920162038518.png)

显然符号表中不会存变量值，因为变量值在运行时才会确定。

````info
符号表是在词法分析阶段创建的。(习题)
````

但是据龙书：

![image-20221004193852281](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190738941427_725_image-20221004193852281.png)

### Lec2 构造一个简单的编译器

#### 上下文无关文法

##### 感性理解

BNF 是一种 **上下文无关文法**，举个例子就是，人类的语言就是一种 上下文**有关**文法，我随时都可以讲一句 “以上说的都是废话”，改变我所说的话的涵义。

##### 形式化定义

![image-20220927144906987](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190740496671_209_image-20220927144906987.png)

![image-20220927144926174](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190741666990_453_image-20220927144926174.png)

![image-20220927144938067](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190742819758_795_image-20220927144938067.png)

对闭包的理解

![image-20220927144950874](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190743880629_933_image-20220927144950874.png)

正闭包也叫正则闭包

![image-20220927145026025](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190746344914_185_image-20220927145026025.png)

![image-20221004164810301](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190747551802_775_image-20221004164810301.png)

![image-20220927150609696](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190748466161_250_image-20220927150609696.png)

在词法分析阶段，所有的expr都是同等对待的，因此不需要加下标

![image-20220927150731839](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190749626754_765_image-20220927150731839.png)

idlist也可用右递归表示。两种方式等价，但生成的语法分析树不一样。

另外一种设计方案

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190750857129_584_image-20220927155732458.png" alt="image-20220927155732458" style="zoom:50%;" />

##### 二义性语法和非二义性语法

非二义性语法

![image-20220927154102321](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190751862164_535_image-20220927154102321.png)

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190753296213_768_image-20220927154131189.png" alt="image-20220927154131189" style="zoom:50%;" />

采用二义性语法，则会产生歧义问题，同一段代码在不同编译器上产生不一样的结果，显然是我们不想看到的

![image-20220927154314035](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190754314719_452_image-20220927154314035.png)

但是在一定的场合下，通过设计合理的语法分析算法，我们是容许一定的二义性的，因为可以减小语法分析树的复杂性。

文法左递归，体现出运算符左结合，右递归则是右结合。

一个右结合的例子

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190755524185_246_image-20220927155426816.png" alt="image-20220927155426816" style="zoom:50%;" />

![image-20220927161055294](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190756637988_463_image-20220927161055294.png)

注意：不要跳级！左结合的，且从左往右替换。

![image-20220927161040537](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190758243317_959_image-20220927161040537.png)

![image-20220928164050330](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190759789619_359_image-20220928164050330.png)

![image-20220928164220732](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190801270074_244_image-20220928164220732.png)

#### 翻译模式

构造翻译模式，中缀->后缀
构造9-5+2的带语义动作的语法分析树，即输出其后缀表达式95-2+

![image-20220927164002512](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190802895392_835_image-20220927164002512.png)

按后序遍历即可打印（翻译）出后缀表达式

#### Yacc

见实验

#### 语法分析

![image-20221004152318374](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190804367395_700_image-20221004152318374.png)

##### 自顶向下

###### 平凡算法：扫描输入分析

![image-20221004153229852](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190808051693_827_image-20221004153229852.png)

###### 优化：预测分析

![image-20221004152448359](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190811525061_463_image-20221004152448359.png)

$lookahead$在构造编译器的时候就可以完成。

实例分析

![image-20221004152827769](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190813022183_796_image-20221004152827769.png)

对于$simple$类似构造方法。

$lookahead$怎么构造？

![image-20221004153753520](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190816136501_201_image-20221004153753520.png)

总体思路是什么，还有什么问题？

![image-20221004154007046](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190818280251_227_image-20221004154007046.png)

##### 左递归问题

针对上面的预测分析法，我们发现：左递归会导致递归下降程序无限循环，还会导致

![image-20221004160548627](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190819993463_865_image-20221004160548627.png)

怎么消除？

固定的算法：

![image-20221004160612826](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190821656013_971_image-20221004160612826.png)

理解：$A=\beta \alpha \alpha ...$

采用右递归进行翻译

![image-20221004161628877](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190823148967_751_image-20221004161628877.png)

![image-20221004161643180](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E4%B8%80%E4%BA%8C%E7%AB%A0/20221008190827034211_692_image-20221004161643180.png)
