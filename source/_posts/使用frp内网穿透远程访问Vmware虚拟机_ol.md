---
title: 使用frp内网穿透远程访问Vmware虚拟机
categories: 小寄巧
tags:
  - 环境配置
abbrlink: 18710
---
# 使用frp内网穿透远程访问Vmware虚拟机

## 为什么需要内网穿透功能

大三的课程实验大多需要x86的linux环境，如果可以使用mac甚至手机或平板就可以远程访问Windows中的linux虚拟机，那就不用背着沉重又特别容易没电的游戏本跑来跑去了。经过一番探索发现内网穿透可以满足我的需求。

如果有自己的云服务器(关键是有公网ip)，便可以使用开源的frp工具进行内网穿透。开干！

## 参考

本文只供个人记录过程方便后续所用，若需详细过程可以参考下面的文章:

基础使用

https://sspai.com/post/52523

配置开机自启(注意需要管理员权限)

https://gofrp.org/docs/setup/systemd/

## 操作步骤

服务器和客户端都需要下载:

```shell
wget https://github.com/fatedier/frp/releases/download/v0.47.0/frp_0.47.0_linux_amd64.tar.gz
```

**注:下载时一定要注意选对系统架构。比如2016南京大学PA的环境是32位Ubuntu，就要下`frp_0.47.0_linux_386.tar.gz`。**

```shell
wget https://github.com/fatedier/frp/releases/download/v0.47.0/frp_0.47.0_linux_386.tar.gz
```

解压

```shell
tar -zxvf frp_0.47.0_linux_amd64.tar.gz
```
改名。非必须，但方便后续配置

```shell
mv frp_0.47.0_linux_amd64 frp
```
具体的配置项可以参见第一篇博客。[官方](https://gofrp.org/docs/examples/ssh/)也说的很简洁明了。

按照官网里的[开机自启](https://gofrp.org/docs/setup/systemd/)配置发现开机自启不成功，原因和解决方法可参见[这个博客](https://www.mmuaa.com/post/537d04e936b78620.html)

```shell
[Unit]
# 服务名称，可自定义
Description = frp client
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
# change to your own path of fps
ExecStart = /home/ubuntu32/frp/frpc -c /home/ubuntu32/frp/frpc.ini
Restart=always
RestartSec=5
[Install]
WantedBy = multi-user.target
```
