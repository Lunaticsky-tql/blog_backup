---
title: 操作系统第一讲
categories: 笔记
tags:
  - 操作系统
  - 汇编语言
abbrlink: 3864
---
## 操作系统

### 第一节：体系结构回顾和再认识

![image-20220919142617931](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170925026934_411_image-20220919142617931.png)

北桥发展更快，性能优化是核心

![image-20220919142955621](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170926438747_545_image-20220919142955621.png)

![image-20220919145003123](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170928189986_749_image-20220919145003123.png)

smartNIC,RDMA等对体系结构本身的新改进方向。

![image-20220919153015066](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170930043845_772_image-20220919153015066.png)

8086总貌

![image-20220919153535949](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170932139747_409_image-20220919153535949.png)

为什么上面的代码是不对的？

字符串作为数据存在DS中，而CS和DS都是只读的。（段寄存器）

![image-20220919161823365](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170933262250_497_image-20220919161823365.png)

<p class="note note-info">CS determines the "code" segment; this is where the executable code of a program is located. It is not directly modifiable by the programmer, except by executing one of the branching instructions. One of the reasons for separating the code segment from other segments is that well-behaved programs never modify their code while executing; therefore, the code segment can be identified as "read-only".</p>

![image-20220919160634237](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170934583004_994_image-20220919160634237.png)

堆由程序员控制，显然不需要有”堆寄存器“

![image-20220919161419678](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F/20220919170936060355_988_image-20220919161419678.png)

操作系统：软件和硬件的交互

