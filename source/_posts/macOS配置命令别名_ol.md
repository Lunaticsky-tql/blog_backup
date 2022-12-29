---
title: macOS配置命令别名
categories: 小寄巧
tags:
  - linux
abbrlink: 42356
---
## macOS配置命令别名

### 临时别名

和在linux系统一样，直接输入`alias`命令即可。在当前的终端下生效。

比如：

```shell
alias v="vim"
```

### 永久别名

由于现在的macOS默认是采用的`zsh`而不是`bash`，因此配置文件路径为

```shell
sudo vim /etc/zshrc
```

当然也可以

```shell
chsh -s /bin/bash
```

进入`bash`，不过目前没什么理由这么干(

然后会发现这个文件是只读的。

有两个解决方案。

#### 简单粗暴的

去除写权限

```shell
sudo chmod u+w /etc/bashrc
```

然后写入别名，保存

```shell
source /etc/bashrc
```

最后将写权限去除

```shell
sudo chmod u-w /etc/bashrc
```

#### 安装插件

[**Oh My Zsh**](https://github.com/ohmyzsh/ohmyzsh)是一款社区驱动的命令行工具，可以配置主题，插件等。

用curl方式安装

```shell
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

在`.zshrc`中配置`alias`，`source`保存即可，里面还可以配置其他实用的配置。[这个博客](https://mrseawave.github.io/blogs/articles/2021/08/29/oh-my-zsh/)有较详细叙述。
