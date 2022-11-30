---
title: Ucore Lab0 on Apple Silicon Mac
categories: 操作系统实验
tags:
  - 操作系统
---
## Ucore Lab0 on Apple Silicon Mac

### 介绍

M1芯片是2020年之后推出的全新适配于Macbook的Arm64芯片。因为底层的指令集与x86_64不同，因此面临着很多兼容性的问题。在ucore的编译，运行和调试的环境配置中也因此踩了一些坑。当然最终得以能够优雅的在这台具有独特架构的PC上探索实现操作系统的魅力。

现在将其记录下来，以供参考。

### qemu安装

qemu是非常成熟的虚拟化解决方案，通过软件的方式逐条将目标文件的二进制指令翻译成目标架构支持的二进制指令，虽然效率不高，但是使用方便，对M1芯片支持也比较完善，足够用来调试ucore了。

指导书中针对linux给出了使用包管理工具的安装方案。在mac上这个过程也同样比较简单。安装`homebrew`包管理工具后只需要

```shell
brew install qemu
```

即可。当然为了保证是最新版本，安装之前可以更新一下homebrew：`brew update`。

### i386-elf-gcc和i386-elf-gdb安装

按照网上的解决方案，我安装了`macport`，并

```
sudo port -v selfupdate
sudo port install i386-elf-gcc
```

但是发现它安装过程中构建失败了。

![image-20221003224714488](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221003231400206876_223_image-20221003224714488.png)

查看发现果然是架构问题：

![image-20221003224809467](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221003231401953713_177_image-20221003224809467.png)

查看报错信息。谷歌后从[github issue](https://github.com/riscv-collab/riscv-gnu-toolchain/issues/800)中得知是有支持apple silicon版本的最新i386-elf-gcc的。

![image-20221003225239013](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221003231403860364_202_image-20221003225239013.png)

![image-20221003225245971](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221003231405125684_549_image-20221003225245971.png)

有希望！但是按官网命令安装问题也没有解决，所谓补丁也不起效。后来尝试用homebrew安装：`brew install i386-elf-gdb`，但没有安装成功。提示

```
fatal: not in a git directory Error: Command failed with exit 128: git
```

又经过一番谷歌找到了[解决方法](https://www.jianshu.com/p/07243d214abd)。执行

```shell
git config --global --add safe.directory 报错信息中homebrew-core路径
git config --global --add safe.directory 报错信息中homebrew-cask路径
```

即可。

然后需要添加一下环境变量。

这时尝试qemu生成ucore的dmg，发现提示`i386-elf-gcc`找不到。这才注意到通过homebrew下载的是`x86_64-elf-gcc`。

经过搜索，得知在make时需要添加`make GCCPREFIX=x86_64-elf-`指定交叉编译工具。这时可以高兴的看到控制台闪烁，执行也很顺利。

### 执行

然后`make qemu`执行的过程也比较顺利。

![image-20221003230427926](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221003231407841829_266_image-20221003230427926.png)

### 调试

首先，ARM 架构的Mac目前是不能使用`gdb`进行程序的调试的，默认的调试工具是`lldb`。然而经过查阅，对于交叉编译反而可以使用实验中对应的`gdb`工具：运行`brew install i386-elf-gdb`安装即可。

以调试lab1中的BIOS的执行为例。

下面的过程与指导书中“使用远程调试”部分类似。除此之外，额外将运行的汇编指令保存在q.log中。

在一个终端先执行：

```shell
qemu-system-i386 -S -s -d in_asm -D bin/q.log -monitor stdio -hda bin/ucore.img
```

后在另一个终端执行:

```shell
i386-elf-gdb
```

进入gdb调试界面。

```shell
(gdb) file bin/kernel
Reading symbols from bin/kernel...
(gdb) target remote :1234
Remote debugging using :1234
0x0000fff0 in ?? ()
```

上述的过程相比原来`makrfile`中提供的`make debug`主要有两个好处：一是能够重定向到`q.log`方便进行对比；二是可以绕开`make`中的`TERMINAL:=gnome-terminal`(`gnome-terminal`仅在linux下可使用)

查看 CS:EIP 由于此时在实际模式下 CPU 在加电后执行的第一条指令的地址为 0xf000:0xfff0 => 0xffff0

```shell
(gdb) x/i $cs
	0xf000:	add    %al,(%eax)
(gdb) x/i $eip
	0xfff0:	add    %al,(%eax)
```

再来看看这个地址的指令是什么
```shell
(gdb) x/2i 0xffff0
   0xffff0:	ljmp   $0x3630,$0xf000e05b
   0xffff7:	das
```

可以看到 第一条指令执行完以后 会跳转到` 0xf000e05b `也就是说 BIOS 开始的地址是 `0xfe05b`。

打上断点

```shell
(gdb) b *0x7c00
Breakpoint 1 at 0x7c00
(gdb) c
Continuing.

Breakpoint 1, 0x00007c00 in ?? ()
```

一开始为了方便后续在终端中配置了永久别名：

```shell
alias makeq="make GCCPREFIX=x86_64-elf-"
```

当然更优雅的方法其实是修改make中的宏：

```makefile
# try to infer the correct GCCPREFX
ifndef GCCPREFIX
# GCCPREFIX := $(shell if i386-elf-objdump -i 2>&1 | 
#...comment the original shell function
# 	echo "***" 1>&2; exit 1; fi)
GCCPREFIX := x86_64-elf-
endif
```

但是，由于`makefile`里默认认为调试工具一定叫`gdb`，且mac里没有gdb对应的command，因此这时候用永久别名是比较合适的。

```shell
alias gdb="i386-elf-gdb"
```

这时候也可以修改make来达到自动化调试的目的：

```makefile
WORKING_DIR=$(shell pwd)
debug: $(UCOREIMG)
	$(V)$(QEMU) -S -s -parallel stdio -hda $< -serial null &
	$(V)sleep 2
	$(V) osascript -e 'tell application "Terminal" to do script "cd $(WORKING_DIR); gdb -q -x tools/gdbinit"'
```

其中最后一句是为了产生一个在当前工作目录的新终端。

### 总结

前前后后也花了相当长的时间来应对环境的不同。后续的内容其实更吸引着我们去深入探索。

### 后续

已知问题: lab1 的`chellenge`无法正常切换`user_mode`，初步排查发现是出现了操作数异常，可能是`%esp`未正确赋值，但目前还没有找到方案。如果对此部分有较深研究，也欢迎交流。

![image-20221130221829874](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/Ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221130222055575294_180_image-20221130221829874.png)

![image-20221130221851517](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/Ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221130222057952350_733_image-20221130221851517.png)

chellenge以外的部分以及后两个实验均可正确得到结果。

![image-20221130222030887](https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/Ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221130222100838376_161_image-20221130222030887.png)