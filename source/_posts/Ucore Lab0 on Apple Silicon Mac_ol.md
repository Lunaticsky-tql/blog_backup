---
title: Ucore Lab0 on Apple Silicon Mac
categories: 操作系统实验
tags:
  - 操作系统
abbrlink: 34966
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

这时尝试qemu生成ucore的dmg，发现提示`i386-elf-gdb`找不到。这才注意到通过homebrew下载的是`x86_64-elf-gcc`。

经过搜索，得知在make时需要添加`make GCCPREFIX=x86_64-elf-`指定交叉编译工具。这时可以高兴的看到控制台闪烁，执行也很顺利。

### 执行

然后`make qemu`执行的过程也比较顺利。

![image-20221003230427926](https://raw.githubusercontent.com/Lunaticsky-tql/my_picbed/main/ucore%20Lab0%20on%20Apple%20Silicon%20Mac/20221003231407841829_266_image-20221003230427926.png)



最后需要使用gdb调试。则运行`brew install i386-elf-gdb`安装即可。

### 总结

前前后后也花了大概三个小时。后续的内容其实更吸引着我们去深入探索。