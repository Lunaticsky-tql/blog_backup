---
title: makefile急速入门
categories: 小寄巧
tags:
  - 环境配置
index_img: /img/makefile急速入门.png
abbrlink: 23557
---



# Makefile 急速入门

或许你和我一样在没有接触过`makefile`的时候看到相对复杂一点的项目依赖感到头大。这里从最简单的情况，到常见用法，快速把`makefile`的基本用法捋一遍。

## 最小示例

考察下面的示例代码：

*main.c*

```c++
#include <stdio.h>
int main(){

printf("hello world!");

return 0;

}
```

正常情况下，通过 `gcc` 在命令行将其编译后产出相应文件，可执行文件或 object 文件等。

```shell
$ gcc -o main.out main.c
```

上面命令编译后运行 `main.out` 可执行文件。

```shell
$ ./main.out
hello world!
```

## Make 认知

通过 `make` 命令，可以将上面的编译进行有效自动化管理。通过将从输入文件到输出文件的编译无则编写成 Makefile 脚本，Make 工具将自动处理文件间依赖及是否需要编译的检测。

`make` 命令所使用的编译配置文件可以是 `Makefile`，`makefile` 或 `GUNMake`。

其中定义任务的基本语法为：

```
target1 [target2 ...]: [pre-req-1 pre-req-2 ...]
	[command1
	 command2
	 ......]
```

上面形式也可称作是一条编译规则（rule）。

其中，

- `target` 为任务名或文件产出。如果该任务不产出文件，则称该任务为 `Phony Targets`。`make` 内置的 phony target 有 `all`, `install` 及 `clean` 等，这些任务都不实际产出文件，一般用来执行一些命令。
- `pre-req123...` 这些是依赖项，即该任务所需要的外部输入，这些输入可以是其他文件，也可以是其他任务产出的文件。
- `command` 为该任务具体需要执行的 shell 命令。

## Makefile 实战

比如文章最开始的编译，可通过编写下面的 Makefile 来完成：

在与`main.c`同目录下创建文件‘`makefile`:

```shell
touch makefile
```

填入以下内容：

*Makefile*

```makefile
all:main.out
main.out: main.c

gcc -o main.out main.c
clean:

rm main.out
```

上面的 Makefile 中定义了三个任务，调用时可通过 `make <target name>` 形式来调用。

比如:

```shell
$ make main.out
gcc -o main.out main.c
```

产出 `main.out` 文件。

再比如：

```shell
$ make clean
rm main.out
```

该 `clean` 任务清除刚刚生成的 `main.out` 文件。

三个任务中，`all` 为内置的任务名，一般一个 Makefile 中都会包含，当直接调用 `make` 后面没有跟任务名时，默认执行的就是 `all`。

```shell
$ make
gcc -o main.out main.c
```

## 任务间的依赖

前面调用 `all` 的效果等同于调用 `main.out` 任务，因为 `all` 的输入依赖为 `main.out` 文件。Make 在执行任务前会先检查其输入的依赖项，执行 `all` 时发现它依赖 `main.out` 文件，于是本地查找，发现本地没有，再从 Makefile 中查找看是否有相应任务会产生该文件，结果确实有相应任务能产生该文件，所以先执行能够产生依赖项的任务。

## 增量编译

使用 Makefile 进行编译有个好处是，在执行任务时，它会先检查依赖项是否比需要产出的文件新，如果说依赖项更新新，则说明我们需要产出的目标文件属于过时的产物，需要重新生成。

什么意思。比如上面的示例，当执行

```shell
$ make main.out 
```

试图生成 `main.out` 产出时，会检查这个任务的依赖文件 `main.c` 是否有修改过。

比如前面我们已经执行过该任务产生过 `main.out`。再次执行时，会得到如下提示：

```shell
$ make main.out 
make: `main.out' is up to date.
```

**NOTE:** 上面是 Mac 上最新版本的 Make 工具（GNU Make 3.81）的提示语，老版或其他变种工具得到的可能是 `Nothing to be done for main.out` 。

现在对输入文件 `main.c` 进行修改：

```c++
#include <stdio.h>
int main(){

-     printf("hello world!");

+     printf("hello wayou!");

return 0;

}
```

再次执行 `make main.out` 会发现任务正常执行并产生了新的输出，

```shell
$ make main.out
gcc -o main.out main.c
$ ./main.out

hello wayou!⏎
```

这里 `main.c` 修改后，它在文件上来说，就比 `main.out` 更新了，所以我们说 `main.out` 这个目标， **过时（out-dated）** 了。

过时的任务才会被重新执行，而未过时的会跳过，并输出相应信息。

以上，Makefile 天然实现了增量编译的效果，在大型项目下会节省不少编译时间，因为它只编译过期的任务。

## Phony 类型任务的执行

需要注意的是，phony 类型的任务永远都属于过时类型，即，每次 `make` 都会执行。因为这种类型的任务它没有文件产出，就无所谓检查，它的主体只是调用了另外的命令而以。

拿这里的 `all` 来说，当我们执行 `make` 或 `make all` 时，得到：

```shell
$ make
make: Nothing to be done for `all'.
```

这里看不出来 `all` 有没有执行，因为目前它还没有包含任何一句命令，调用 `all` 后实际执行的是它的依赖文件 `main.out` 中的任务，而因为后者已经是最新的了，所以无须执行，所以得到了如上的输出。

为了验证 phony 类型任务是否每次都执行，向 `all` 及 `main.out` 中添加 `echo` 命令打印一些信息、

```makefile
all:main.out
+	echo "[all] done"
main.out: main.c

gcc -o main.out main.c

+	echo "[main.out] done"
clean:

rm main.out
```

再次执行：

```shell
$ make
echo "[all] done"
[all] done
$ make

echo "[all] done"

[all] done
$ make main.out

make: `main.out' is up to date.
```

可以看到，属于 phony 类型的任务 `all` 每次都会执行其中定义的 shell 命令，而非 phony 类型的任务 `main.out` 则走了增量编译的逻辑。

## 变量/宏

Makefile 中可使用变量（宏）来让脚本更加灵活和减少冗余。

其中变量使用 `$` 加圆括号或花括号的形式来使用，`$(VAR)`，定义时类似于 C 中定义宏，所以变量也可叫 Makefile 中的宏，

```shell
CC=gcc
```

这里定义 `CC` 表示 `gcc` 编译工具。然后在后续编译命令中，就可以使用 `$(CC)` 代替 `gcc` 来书写 shell 命令了。

```makefile
+ CC=gcc
all:main.out
main.out: main.c

-	gcc -o main.out main.c

+	$(CC) -o main.out main.c
clean:

rm main.out
```



这样做的好处是什么？因为编译工具可能随着平台或环境或需要编译的目标不同，而不同。比如 `gcc` 只是用来编译 C 代码的，如果是 C++ 你可能要用 `g++` 来编译。如果是编译 WebAssembly 则需要使用 `emcc`。

无论怎样变，我们只需要修改定义在文件开头的 `CC` 变量即可，无须修改其他地方。这当然只是其中一点好处。

## 自动变量/Automatic Variables

自动变量/Automatic Variables 是在编译规则匹配后工具进行设置的，具体包括：

- `$@`：代表产出文件名
- `$*`：代表产出文件名不包括扩展名
- `$<`：依赖项中第一个文件名
- `$^`：空格分隔的去重后的所有依赖项
- `$+`：同上，但没去重
- `$?`：同上，但只包含比产出更新的那些依赖

这些变量都只有一个符号，区别于正常用字母命名的变量需要使用 `$(VAL)` 的形式来使用，自动变量无需加括号。

利用自动变量，前面示例可改造成：

```makefile
CC=gcc
TARGET=main.out
all:$(TARGET)
$(TARGET): main.c

$(CC) -o $@ $^
clean:

rm $(TARGET)
```

减少了重复代码，更加易于维护，需要修改时，改动比较小。

## VPATH & vpath

可通过 `VPATH` 指定依赖文件及产出文件的搜索目录。

```makefile
VPATH = src include
```

通过小写的 `vpath` 可指定具体的文件名及扩展名类型，

```makefile
vpath %.c src
vpath %.h include
```

此处 `%` 表示文件名。

## 依赖规则/Dependency Rules

```makefile
Main.o : Main.h Test1.h Test2.h
Test1.o : Test1.h Test2.h
Test2.o : Test2.h
```

像这种，只定义了产出与依赖没包含任务命令的无则，叫作依赖无则。因为它只定义了某个产出依赖哪些输入，故名。

这种规则可达到这种效果，即，右边任何文件有变更，左边的产出便成为过时的了。

## 匹配规则/Pattern Rules

区别于明确指定了产出与依赖，如果一条规则包含通配符，则称作匹配规则（Pattern Rules）。

比如，

```makefile
%.o: %.c
    gcc -o $@ $^
```

上面定义了这么一条编译规则，将所有匹配到的 c 文件编译成 Object 产出。

有什么用？

这种规则一般不是直接调用的，是被其他它规则触间接使用。比如上面的依赖规则。

```makefile
%.o : %.cpp
  g++ -g -o $@ -c $<
Main.o : Main.h Test1.h Test2.h

Test1.o : Test1.h Test2.h

Test2.o : Test2.h
```

当右侧这些头文件有变动时，左边的产出会在 `make` 时被检测到过时，于是会被执行。当执行时匹配规则 `%.o` 会被匹配到，所以匹配规则里面的命令会执行，从而将 `cpp` 文件编译成相应 Object 文件。达到了依赖更新后批量更新产出的目的，而不需要写成这样：

```makefile
Main.o : Main.h Test1.h Test2.h
    g++ -g -o $@ -c $<
Test1.o : Test1.h Test2.h
    g++ -g -o $@ -c $<
Test2.o : Test2.h
    g++ -g -o $@ -c $<
```

## Makefile 函数

函数主要分为两类：make内嵌函数和用户自定义函数。对于 GNU make内嵌的函数，直接引用就可以了；对于用户自定义的函数，要通过make的call函数来间接调用。

### 通配符函数

当我们想要对文件名进行通配时，可以采用通配符\*或%来进行，如上所述。但只能将其用于规则目标或依赖以及`shell`命令中：

```makefile
test: *.o  
	gcc -o $@ $^
*.o: *.c    
	gcc -c $^
```

但是其他情况比如如果我们想要获取某个目录下所有的C文件列表，可以使用扩展通配符函数`wildcard`

```makefile
SRC  = $(wildcard *.c)
HEAD = $(wildcard *.h)
all:    
@echo "SRC = $(SRC)"    
@echo "HEAD = $(HEAD)"
```

### 文本处理函数

如果需要在makefile里进行文件名查找、替换、过滤等操作，则文本处理函数能够帮到忙。可以参阅[这个网站](https://www.zhaixue.cc/makefile/makefile-text-func.html)的介绍。

### shell 函数 		

用shell 函数在`makefile`执行过程中使用shell命令。函数的参数就是命令，返回值是命令的执行结果。它和反引号 `` 具有相同的功能。

```makefile
.PHONY: all
current_path = $(shell pwd)
all:    
@echo "current_path = $(current_path)"
```

### 用户自定义函数

GNU make提供了大量的内嵌函数，大大方便了makefile编写。但根据需要，我们也需要自定义一些函数，然后在makefile中引用它们：

```makefile
PHONY: all
define func    
@echo "pram1 = $(0)"    
@echo "pram2 = $(1)"
endef
all:    
$(call func, hello zhaixue.cc)
```

用户自定义函以define开头，endef结束，给函数传递的参数在函数中使用\$(0)、\$(1)引用，分别表示第1个参数、第2个参数…
调用时要使用call函数间接调用，各个参数之间使用空格隔开。

## 参考链接

如果希望进行更深入的了解可以参阅：

[官网](https://www.gnu.org/software/make/)

[GCC and Make Compiling, Linking and Building C/C++ Applications](https://www3.ntu.edu.sg/home/ehchua/programming/cpp/gcc_make.html#zz-2.)

以及中文教程：

[宅学部落](https://www.zhaixue.cc/makefile/makefile-intro.html)