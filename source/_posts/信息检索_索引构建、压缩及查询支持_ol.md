---
title: 信息检索_索引构建、压缩及查询支持
categories: 笔记
tags:
  - 信息检索
---
## 信息检索第一部分--索引构建

### 倒排索引构建

六个步骤

序列化，语言预处理，分配DocID，排序，归并，添加频率标签

<p class="note note-info">为什么要加文本频率？
便于进行词频的排序，利于后续查询优化</p>

### 倒排索引布尔查询

略。并行课有涉及。比如当求交时可以先将短的链表求交。

### 倒排索引优化改进

![image-20220922093753305](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143627586751_718_image-20220922093753305.png)

为了减少字符串所占用的内存，我们可以将键进行序列化。

Assume we have 1GB of text 800,000 documents 100 million tokens （Reuters-RCV1 collection）

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143628933413_566_image-20220922094643439.png" alt="image-20220922094643439" width="50%" height="50%" />

（假设是用int存docID）

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143629914308_735_image-20220922095054178.png" alt="image-20220922095054178" width="50%" height="50%" />

16*1.4

看上去很好。

然而，代价是必须要维护一张termID和字符串的映射表。

当需要处理的数据特别多时，由于排序，归并过程中所有的数据都需要这个表，就不得不一直将它放到内存里。

#### BSBI（Blocked Sort-Based Indexing）

仍然保留进行映射的策略

此算法的主要步骤如下：

1、将文档中的词进行id的映射，这里可以用hash的方法去构造

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143631068932_652_image-20220922100056227.png" alt="image-20220922100056227" width="50%" height="50%" />

当然，可以先把全部文档读一遍构建映射，再分块构建倒排索引，也可以在构建每一块的倒排索引的时候边构建边映射。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143632700535_256_image-20220922101046446.png" alt="image-20220922101046446" width="50%" height="50%" />

2、将文档分割成大小相等的部分。分治

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143634153162_211_image-20220922095854934.png" alt="image-20220922095854934" width="50%" height="50%" />

3、将每部分按照词ID对上文档ID的方式进行排序（保证分块可以在内存里放下）

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143635299312_759_image-20220922095946828.png" alt="image-20220922095946828" width="50%" height="50%" />

![image-20220922100557902](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143636457198_361_image-20220922100557902.png)

4、将每部分排序好后的结果进行合并，最后写出到磁盘中。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143637743125_385_image-20220922095721101.png" alt="image-20220922095721101" width="50%" height="50%" />

归并的过程中也可以分治，比如内存中只能放100个词条的总倒排索引，可以在第100个的时候写出磁盘（因为已经确定是最后结果了），从101个再继续。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143639158715_536_image-20220922102146120.png" alt="image-20220922102146120" width="50%" height="50%" />

#### SPIMI（Single-Pass In-Memory Indexing）

不作映射，其他与BSBI一样

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143640277003_250_image-20220922101959755.png" alt="image-20220922101959755" width="50%" height="50%" />

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143641398914_475_image-20220922102104189.png" alt="image-20220922102104189" width="50%" height="50%" />

因为D显然要比T小的多

#### 分布式解决方案MapReduce

大数据实训有涉及，略。

### 在线索引构建

#### 朴素方案

##### 朴素方案一：重建索引

![image-20220928141323699](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143642866848_892_image-20220928141323699.png)

##### 朴素方案二：辅助索引

![image-20220928141427687](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143644019596_168_image-20220928141427687.png)

使用辅助索引的话，一个很简便的思路是一个词建一个文档，归并便变为两个文档的合并。

![image-20220928141820357](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143645445454_230_image-20220928141820357.png)

有什么缺陷？文件大小可能差距很大，且大量小文件不便于存储和对索引的快速读写（存储系统的问题）

![image-20220928142759774](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143646682137_270_image-20220928142759774.png)

更大的问题，随着文档的数量变大，归并会越来越慢！



![image-20220928142854979](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143647947499_639_image-20220928142854979.png)

合并时termID是有序的，归并时类似于归并排序，最坏复杂度是较大的那个索引的termID个数。而单个倒排索引合并只需要把新的list放到旧的后面就可以了，因为新的list中的docID肯定会比旧的大（就像上面图上所示）
$$
O\left(n+2n+\ldots+\frac{T}{n}\right)=O\left(\frac{T^2}{n}\right)
$$


#### 文档删除怎么操作？

无效向量

![image-20220928142307585](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143649321808_563_image-20220928142307585.png)

### 倒排索引压缩

#### 一些朴素的偷懒方法

![image-20220928155207922](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143650616612_634_image-20220928155207922.png)



但是现代检索系统一般不会这么做，因为会导致一些信息的丢失。

#### 词典压缩

##### 方法一：使用数组

是一种很蠢的方法

 <img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143654714754_145_image-20220928152210011.png" alt="image-20220928152210011" width="50%" height="50%" />

##### 方法二：指针

![image-20220928151740804](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143655839716_271_image-20220928151740804.png)

##### 方法二的优化：分段指针

![image-20220928152418457](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143657755792_576_image-20220928152418457.png)

当然，找termID对应的词项会慢一些。

##### 采用前缀的方式

![image-20220928153011321](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143659531464_413_image-20220928153011321.png)

#### 索引表压缩

##### Encoding gaps

![image-20220928153421273](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143700905497_456_image-20220928153421273.png)

##### Variable length codings

![image-20220928153533933](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143702089613_543_image-20220928153533933.png)

例子：可变长UTF-8

![image-20220928153849498](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143703419174_526_image-20220928153849498.png)

UTF-8 的编码规则很简单，只有二条：

1）对于单字节的符号，字节的第一位设为`0`，后面7位为这个符号的 Unicode 码。因此对于英语字母，UTF-8 编码和 ASCII 码是相同的。

2）对于`n`字节的符号（`n > 1`），第一个字节的前`n`位都设为`1`，第`n + 1`位设为`0`，后面字节的前两位一律设为`10`。剩下的没有提及的二进制位，全部为这个符号的 Unicode 码。

下表总结了编码规则，字母`x`表示可用编码的位。

 ```
 Unicode符号范围     |        UTF-8编码方式
 (十六进制)        	|              （二进制）
 -------------------+---------------------------------------------
 0000 0000-0000 007F | 0xxxxxxx
 0000 0080-0000 07FF | 110xxxxx 10xxxxxx
 0000 0800-0000 FFFF | 1110xxxx 10xxxxxx 10xxxxxx
 0001 0000-0010 FFFF | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
 ```

根据上表，解读 UTF-8 编码非常简单。如果一个字节的第一位是`0`，则这个字节单独就是一个字符；如果第一位是`1`，则连续有多少个`1`，就表示当前字符占用多少个字节。

下面，以汉字`严`为例，演示如何实现 UTF-8 编码。

`严`的 Unicode 是`4E25`（`100111000100101`），根据上表，可以发现`4E25`处在第三行的范围内（`0000 0800 - 0000 FFFF`），因此`严`的 UTF-8 编码需要三个字节，即格式是`1110xxxx 10xxxxxx 10xxxxxx`。然后，从`严`的最后一个二进制位开始，依次从后向前填入格式中的`x`，多出的位补`0`。这样就得到了，`严`的 UTF-8 编码是`11100100 10111000 10100101`，转换成十六进制就是`E4B8A5`。

##### Gamma Encoding

根据[维基百科](https://en.wikipedia.org/wiki/Elias_gamma_coding)所述，gamma编码过程如下图所示。虽具体过程与课上讲述稍有不同，但原理是一样的。

![image-20220930155723916](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143704774266_595_image-20220930155723916.png)

编码具体案例和解码过程。

![image-20220930155802505](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143706251591_500_image-20220930155802505.png)

### 查询优化

#### 倒排索引数据结构优化

##### “跳表”

动机

![image-20221005150319520](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143708733468_476_image-20221005150319520.png)

怎么选取间隔？“摔瓶子”。开根号

![image-20221005150404678](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143710120784_928_image-20221005150404678.png)

实例：

![image-20221005150523460](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143711476304_852_image-20221005150523460.png)

<p class="note note-info">为什么是先跳再判断，如果跳过了再倒回去，而不是比较之后再跳？后者比较次数太多，开销大，且慢。</p>

#### 词项数据结构

##### 哈希表

优点：快

缺点：不支持模糊查询

![image-20221005152131580](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143713258991_492_image-20221005152131580.png)

##### B树

实际使用

![image-20221005152231798](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143716445073_262_image-20221005152231798.png)

#### 通配符查询支持

前缀：B树天然支持

![image-20221005153943805](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143718721740_938_image-20221005153943805.png)

后缀：对逆序建B树

![image-20221005154022485](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143720264162_261_image-20221005154022485.png)

中间的？好像有点问题。。。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143721509249_850_image-20221012140726185.png" alt="image-20221012140726185" width="50%" height="50%" />

#### 轮排索引

![image-20221012141847402](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143722646249_170_image-20221012141847402.png)

采用B树。但通常这种方法产生的B树会非常大

![image-20221012143335531](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143723834048_694_image-20221012143335531.png)

#### K-gram

一定程度上的优化

在一定长度的字串上建索引

![image-20221012143730369](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143725269033_823_image-20221012143730369.png)

查\$co,ter,er\$,\$代表起始和结束符号

![image-20221012144353569](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143726834159_151_image-20221012144353569.png)

### 拼写检查支持

#### 动态规划：编辑距离

动态规划求字符串距离？

![image-20221012150059012](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143728315657_544_image-20221012150059012.png)

词项太多，算法显得有些复杂，慢

#### 在K-gram基础上进行

Jaccard distance判断相似度

![image-20221012151057155](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2_%E7%B4%A2%E5%BC%95%E6%9E%84%E5%BB%BA%E3%80%81%E5%8E%8B%E7%BC%A9%E5%8F%8A%E6%9F%A5%E8%AF%A2%E6%94%AF%E6%8C%81/20221013143729475948_696_image-20221012151057155.png)

求并集的小trick

#query term's k-grams +#found term's k-grams-#intersection

#### 上下文相关检查

利用搜索历史，启发式
