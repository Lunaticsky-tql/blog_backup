---
title: 深入浅出Docker应用-Docker容器入门
categories: 笔记
tags:
  - Docker
abbrlink: 41895
date: 2023-09-06 11:51:53
---
# 深入浅出docker应用-Docker容器入门

## 写在前面

本系列教程由[阿里云](https://developer.aliyun.com/adc/scenarioSeries/713c370e605e4f1fa7be903b80a53556?spm=a2c6h.13788135.J_5170737420.9.61281ff054pM5z)提供。首先感谢阿里云提供的实验资源。之前空闲时间做过一遍，收获颇丰，可以配得上标称的”深入浅出docker应用“。虽然只是对于基本概念和命令的讲解，现在在图形化界面上也有`Docker Desktop`方便的管理容器，但是在服务器上进行运维工作，还是需要对命令行的使用方式较为熟悉。由于最近也在深入使用docker，学习其原理，故快速重温一遍，并做转载供平时查阅和分享，以便能通过这些内容对docker有感性的认识。若有侵权，联系2013599@mail.nankai.edu.cn，收到将立即删除。

## Docker安装和配置

### 安装

Docker是基于Linux内核服务的轻量级开源容器产品，本系列实验我们将为大家介绍docker产品的安装，使用和案例。在本实验中，我们先来介绍docker 的安装。在centos系统中，我们一般通过yum进行软件包的安装。因此本次实验我们也通过yum来安装docker运行环境。

下面是基于实验环境的`centos`安装过程。其他系统可参见[官方指导](https://docs.docker.com/engine/install/ubuntu/)

1. 安装docker的依赖组件

在安装docker之前，我们需要先通过yum来安装docker的必要的依赖组件。同时为了编译后面的配置信息格式化输出，我们同时需要安装jq工具。

```shell
yum install -y yum-utils device-mapper-persistent-data lvm2
```

```shell
yum install -y jq
```

2. 添加Docker的安装来源

因为docker安装包不在yum的默认源列表中，因此在安装之前我们需要通过yum-config-manager --add-repo命令向yum默认源列表中添加docker源的地址。

```shell
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo 
```

源添加成功后，我们可以使用yum list命令查看当前的docker源中支持的安装包版本列表。

```shell
yum list docker-ce --showduplicates | sort -r
```

![image-20230904220149946](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113647495716_679_image-20230904220149946.png)

1. 安装Docker应用 

docker依赖和docker源安装完成之后，我们就可以使用yum install docker-ce.x86_64命令来安装docker 应用，在使用yum install安装时，默认会选择最新的版本进行安装。如果需要指定安装版本也可以在命令后面加入具体的版本号，接下来我们来安装docker的最新版本。

```shell
yum install -y docker-ce.x86_64 
```

![image-20230904220307344](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113649155016_953_image-20230904220307344.png)

安装成功之后，我们还需要通过systemctl start命令来启动docker服务

```shell
systemctl start docker.service
```

### 配置

1.镜像源配置

通过docker拉取镜像时，默认会通过国外的镜像源进行下载，因此可以配置国内的镜像源以加快下载速度。修改docker的镜像源时，我们使用vi编辑文件 `/etc/docker/daemon.json` 。注意使用vi编辑器时：

1. 需要先按i键进入编辑模式。
2. 编辑完成之后按esc退出编辑模式。
3. 然后按大写的ZZ保存并退出vi。

```shell
vi /etc/docker/daemon.json 
```

```shell
{
   "registry-mirrors":["https://registry.docker-cn.com"]
}
```

在编辑成功后，按ECS推出编辑模式，然后按ZZ退出vi。


2. 镜像源修改后，需要重新启动docker服务。

```shell
systemctl restart docker.service 
```

服务重启成功后，我们可以通过docker version查看docker版本信息。如果出现客户端版本信息和服务版本信息，则说明dcoker已经安装成功且服务已经启动

```shell
docker version
```

![image-20230904220736850](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113759513071_319_image-20230904220736850.png)

3. 服务启动之后，为了防止计算机重启之后docker服务被关闭，我们还可以通过systemctl enable命令将docker服务配置为开机自启动。（此步骤为可选操作）

```shell
systemctl enable docker.service
```

### 快速上手

在前面的小节中我们介绍了Docker 的安装的配置，接下来为大家介绍一些Docker的快速上手命令和用法。

1. 启动hello-world

Docker安装配置成功之后，我们就可以通过`docker run`命令启动轻量级的容器虚拟机。我们执行如下命令

```shell
docker run hello-world
```

会发现屏幕上输出了Hello from Docker!信息。这个信息输出表示hello-world容器虚拟机启动成功。

![image-20230904220824468](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113803659205_241_image-20230904220824468.png)

2. 启动长期运行的bash容器

在上一个步骤中，我们演示了docker最基本的用法，这种方式启动的`hello-world`容器，在启动之后会输出文字，在输出之后容器就会结束。

接下来我们来启动一个可以长期运行的bash容器。我们在命令行中输入如下命令，运行成功后会看到命令提示行变为bash，这表示容器虚拟机已经持续运行。

```shell
docker run -it bash
```

![image-20230904220909280](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113808950713_810_image-20230904220909280.png)

3. bash容器的退出

在运行的bash容器中我们可以使用一些基本的linux命令，如pwd，ls等

```shell
pwd
ls
```

![image-20230904221015298](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113813340599_640_image-20230904221015298.png)

如果希望退出bash容器，回到宿主机，我们在控制台中输入exit命令即可。

```shell
exit
```

![image-20230904221027326](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113818586520_163_image-20230904221027326.png)

在使用docker run命令运行容器时，我们会看到在容器运行之前，出现了Status: Downloaded newer image状态。这表示在容器虚拟机第一次运行时，会首先从远程容器源服务器中下载镜像到本地，然后才能在本地运行。

在本小节中，我们来学习如何分步骤从镜像源查找所需要的容器镜像，然后再来了解如何下载容器镜像，并且查看本地已经下载好的容器镜像列表。

1. 远程查找容器

当我们需要查找容器时，可以通过docker search命令在的镜像源中查找所需要的容器镜像。接下来我们来查找ubuntu容器。

```shell
docker search ubuntu
```

![image-20230904221056674](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113823028609_871_image-20230904221056674.png)



1. 查找容器的版本信息

在找到所需要的容器镜像的名称之后，通常需要进一步在docker的镜像源中查找该镜像的版本列表。由于docker本身没有直接提供查看版本的功能，因此在这里我们为大家提供了一个可以查看镜像版本的简单脚本`docker-tags`。我们生成docker-tags脚本并加入以下内容 ，

注意使用vi编辑器时：

1. 需要先按i键进入编辑模式。
2. 编辑完成之后按esc退出编辑模式。
3. 然后按大写的ZZ保存并退出vi。

```shell
vi docker-tags
```

```shell
curl -s -S "https://registry.hub.docker.com/v2/repositories/library/$1/tags/?page=$2" |
sed -e 's/,/\n/g' -e 's/\[/\\\[\n/g' |
grep -E '"name":|"count":' |
sed -e 's/"//g' -e "s/name:/$1:/g" -e "s/{count:/$1总版本数-/"
```

docker-tags脚本编辑好之后，需要通过chmod修改文件权限才可以执行。在权限修改完成之后，就可以使用docker-tags脚本来查询相关镜像的最近版本信息了。

```shell
chmod 777 docker-tags 
./docker-tags ubuntu
```

1. 拉取容器镜像

当我们查找到镜像的版本信息之后，就可以拉取镜像到本地了。在拉取镜像时我们可指定拉取镜像的版本，也可不指定版本默认拉取最新版本。首先我们使用docker pull命令来拉取ubuntu容器的jammy版本。

```shell
docker pull ubuntu:jammy
```

![image-20230904221220297](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113826463659_596_image-20230904221220297.png)

接下来我们来拉取ubuntu的最新版本。

```shell
docker pull ubuntu
```

![image-20230904221246435](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113831522600_650_image-20230904221246435.png)

当镜像源已经拉取到本地之后，我们可以通过docker images命令来查看已经拉取到的本地镜像。

```shell
docker images
```

![image-20230904221300207](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113834482846_648_image-20230904221300207.png)

## 容器启动和操作

镜像拉取到本地之后并不能直接运行，如果要启动容器，我们需要首先根据镜像创建容器。接下来我们将学习如何创建容器并启动ubuntu容器。

###  容器的分步骤启动流程

1. 创建ubuntu容器 

我们可以使用docker create命令，利用下载好的ubuntu镜像创建容器。注意：因为我们要创建一个可以持久运行的ubuntu容器，因此需要添加-it参数。

`-i`：这个参数代表“交互式（Interactive）”。它使容器的标准输入（stdin）保持打开状态，允许你与容器的命令行交互。这意味着你可以在容器内部执行命令，并从键盘输入内容，就像在本地计算机上的终端一样。

`-t`：这个参数代表“终端（TTY）”。它为容器分配了一个伪终端（pseudo-TTY），这使得容器内的命令行界面可以正常工作，包括支持终端窗口大小的调整和ANSI转义序列的处理。这通常与`-i`一起使用，以确保交互式终端在容器内部能够正常运行。

```shell
docker create -it ubuntu
```

容器创建成功之后，可以使用`docker ps`命令查看现有的容器，注意：如果docker ps默认只会显示正在运行的容器。如果想查看所有状态的容器，需要添加-a参数。

```shell
docker ps -a
```

注：换了一个服务器，因此只显示了一个

![image-20230904222052915](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113838384667_198_image-20230904222052915.png)

2. 创建指定名称的容器

在上一步的执行docker ps -a的返回结果中。CONTAINER ID表示系统为容器创建的ID，IMAGE为容器的镜像名称。STATUS表示容器当前的状态。NAMES为容器的名称。

使用默认的docker create命令所创建的容器并没有指定名称，因此docker会为容器生成一个随机的名字。如果用户想创建指定名称的容器，则可以使用`--name`参数。注意如果用户制定了容器名，则要注意容器不要重名，否则会创建失败。

```shell
docker create -it --name ubuntu-1 ubuntu
docker ps -a
```

![image-20230904222138404](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906113842660170_765_image-20230904222138404.png)

3. 启动ubuntu容器

当容器创建好之后，我们就可以通过docker start命令来启动容器，容器启动成功后通过docker ps命令可以查看到容器状态的变化。在这里我们要注意：同一个镜像创建的多个容器之间是不相关的。

```shell
docker start ubuntu-1
docker ps -a 
```

![image-20230904222232252](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115032403100_490_image-20230904222232252.png)

### 容器的快速启动方式

在上一个小节中我们介绍了docker容器创建的标准流程。而在实际操作过程中，使用标准步骤创建启动容器会比较繁琐，因此docker提供了更加简便的命令docker run。使用该命令时，docker会自动完成下载镜像，创建容器，启动容器的工作。

1. 创建容器指定名称的容器

通过以下的一条命令，我们就可以完成下载busybox的容器镜像，创建名为busybox-1的容器，为了让容器可以在创建之后长期运行我们要使用-it参数，为了让容器在启动之后在后台运行，我们需要使用-d参数。在容器启动之后我们使用docker ps命令查询正在运行的容器。

```shell
docker run -itd --name ubuntu-2 ubuntu
docker ps -a 
```

![image-20230904222752630](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115035769165_650_image-20230904222752630.png)

2. 操作已经创建的容器 

使用-d参数创建容器之后，容器在后台运行，前台的命令行仍然指向宿主机。为了能狗通过命令行操作容器，我们可以使用docker exec命令在ubuntu-2容器上启动bash控制台程序，从而对容器进行操作。

```shell
docker exec -it ubuntu-2 bin/bash
```

​	命令执行之后提示行提示符发生了改变。这说明当前用户所操作的已经是容器中的操作系统。

![image-20230904222911314](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115038972707_654_image-20230904222911314.png)

3. 创建一次性容器

上面我们为大家介绍的常见的容器创建方法，如果用户在使用docker run创建容器的时候，如果不使用-d参数。则启动容器成功之后，会自动进入容器操作系统控制台。但是此种方法进入容器操作系统之后，如果使用exit退出，容器会被关闭。因此此种方法只适用通过容器中执行一些临时性的操作时使用。

接下来我们创建一次性容器，并且在一次性容器退出之后使用docker ps -a查看容器，当我们使用docker ps时，只会列出正在运行的容器，而使用了-a参数之后，会列出包括了正在运行的和已经退出了的各种状态的容器。

```shell
docker run -it --name temp ubuntu
exit
```

```shell
docker ps -a 
```

![image-20230904223136488](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115043608109_578_image-20230904223136488.png)

### 为容器安装命令行工具

1. 启动容器并测试常用命令

首先用docker run创建一个新的ubuntu容器并启动

```shell
docker run -it --name ubuntu-3 ubuntu
```

接下来再通过`lsb_release`查看操作系统的状态。会显示命令无法找到，原因是通过容器安装的ubuntu属于极简版本，没有安装非必要的命令。为了能在容器虚拟机中执行常用的操作

```shell
lsb_release
```

![image-20230904223327185](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115049222439_512_image-20230904223327185.png)

1. 在容器中安装命令

对于ubuntu镜像的容器，我们可以使用apt-get命令来安装常用命令。接下来我们使用apt-get install来安装lsb_release， ifconfig，vim三个工具。需要注意的在使用apt-get install之前，需要首先使用apt-get udpate来更新本地资源库。另外就是此步骤受网络速度影响可能会有比大的延迟。

```shell
apt-get update
apt-get install -y lsb-core net-tools vim --fix-missing
```

在容器中体验安装命令后，使用exit退出容器继续下面操作。

1. busybox镜像的使用

在docker中，传统的ubuntu或者centos镜像所包含的命令数量都非常少，每次使用时都需要手动安装相关命令非常不方便，因此在实际使用docker时，我们经常使用busybox镜像来作为基础镜像。

接下来我们尝试创建busybox镜像，要注意的时，为了保证镜像体积，busybox镜像中并不包括bash命令，而是使用了替代的sh命令。因此我们创建busybox镜像的命令也需要做调整。

```shell
docker run -itd --name busybox-1 busybox
docker exec -it busybox-1 sh
```

![image-20230904223513737](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115052365509_199_image-20230904223513737.png)

容器创建成功之后，我们尝试ifconfig和vi命令发现已经内置在容器之中，不过需要注意的时busybox镜像并没有包含apt-get或者yum等自动包安装工具。因此和ubuntu或者centos镜像相比，安装新工具会比较繁琐。

注意使用vi编辑器时：

1. 需要先按i键进入编辑模式。
2. 编辑完成之后按esc退出编辑模式。
3. 然后按大写的ZZ保存并退出vi。

```shell
ifconfig
vi a.txt
```

体验完busybox镜像的使用后，我们执行exit退出继续下面操作。

### 查看容器系统信息

上一小节我们带大家学习了如何启动一个容器，当容器启动之后会作为轻量级的虚拟机在本地进行运行。本小节我们将学习如何在控制台操作作为虚拟机的容器。

1. 查看宿主机信息

为了对比容器和宿主机，我们先用lsb_release -a命令查看宿主操作系统

```shell
lsb_release -a
```

![image-20230904223838981](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115057562682_162_image-20230904223838981.png)

接下来我们再用ifconfig命令查看宿主机网络信息。

```shell
ifconfig
```

![image-20230904225731155](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115101741869_245_image-20230904225731155.png)

1. 查看容器信息

当上述命令(在`ubuntu-3`中)安装好之后，我们就可以查看容器操作系统的状态和网络状态了。查询后发现和宿主机的信息已经不同。说明我们的控制台已经在容器操作系统中了。

```shell
docker start ubuntu-3
docker exec -it ubuntu-2 bin/bash
```

```shell
lsb_release -a
```

![image-20230904225509265](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115105385086_458_image-20230904225509265.png)

我们接下来在查看容器的IP地址，（注意和宿主机网络信息的对比）

```shell
ifconfig
```

![image-20230904225756902](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115109519062_970_image-20230904225756902.png)

可以感受到容器对环境的隔离效果。

## 容器管理命令

### 构建实验环境

在前面的实验中，我们介绍了容器的启动和操作。在本实验中，我们继续介绍Docker中针对容器的操作命令。首先我们会在容器中用python启动一个简单的http服务，以便为后续的实验做准备。

1. 创建容器

首先我们来创建一个新的ubuntu容器。在创建成功后使用docker exec进入容器控制台。

```shell
docker run -itd --name ubuntu-3 ubuntu
docker exec -it ubuntu-3 /bin/bash
```

2. 安装工具

为了演示后面的实验，我们在容器中安装python3，ifconfig，curl三个命令行工具。其中ifconfig命令工具需要安装net-tools工具包。

```shell
apt-get update
apt-get install -y python3 net-tools curl
```

3. 运行服务

接下来我们启动一个默认的python3 http服务，服务启动在8000端口，并使用`nohup`命令将服务设置为在后台运行(nohup:ignoring input and appending output to 'nphup.out'按回车)。在服务启动之后，我们在容器中使用curl测试一下服务的运行状态。会看到http服务返回了网页。

```shell
nohup python3 -m http.server 8000 &
curl 127.0.0.1:8000 
```

![image-20230905102403283](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115112783989_685_image-20230905102403283.png)

### 访问容器中的应用

在上一个小节中，我们通过docker启动了一个容器，同时在这个容器中启动了一个http服务。本小节中我们来学习如何访问这个容器中的服务。以及如何查看容器中服务的进程状态查询命令。

1. 查看容器的网络地址 

在容器内部测试http服务成功后，接下来我们需要在宿主机中测试http服务。当容器创建之后，会自动创建属于容器自己的网卡和网络地址，并且保证容器的网卡可以和宿主机互相访问，因此我们先通过`ifconfig`命令来显示并记录`容器的ip地址`。然后退出容器的控制台。

![image-20230905102632272](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115117023864_642_image-20230905102632272.png)

2. 测试访问容器服务

在宿主机控制台中，我们同样使用`curl`命令来访问容器中的http服务，需要注意的是：在宿主机中我们需要通过上一步`容器IP地址`才能访问到容器中的服务。通过测试我们发现在宿主机中通过IP访问容器服务活得内容和在容器中获得的内容一致。

```shell
curl [容器IP]:8000 
```

![image-20230905102847301](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115120768011_197_image-20230905102847301.png)

在上一个步骤中我们通过宿主机访问了容器内的服务。除此之外我们还可以在宿主机中通过docker top命令来查看容器中正在运行的具体进程。其命令的语法为docker top 容器名。我们输入如下命令，可以看到ubuntu-3容器运行着2个进程，分别是bash控制台进程和python3http服务器进程。

```shell
docker top ubuntu-3
```

![image-20230905103123487](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115127139220_531_image-20230905103123487.png)

### 容器的暂停和恢复

对于已经启动的容器。我们可以使用docker pause/unpause命令对容器进行暂停/恢复。当容器被暂停之后，容器内的服务将会暂停，当容器恢复之后服务恢复。在上一小节中我们在容器中用python启动了一个简单的http服务，这一小节我们来测试容器的暂停和恢复对http服务的影响。

1. 通过`docker pause`命令暂停容器运行，容器暂停后通过`docker top`命令来查看容器中进程。发现进程依然存在，再通过`curl`测试http服务，发现已经无响应，证明服务已经停止。

```shell
docker pause ubuntu-3
docker ps -a
curL[容器IP]:8000 
Ctrl+C
```

![image-20230905103701392](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115130478163_735_image-20230905103701392.png)

2. 通过`docker unpause`命令恢复容器运行，测试http服务，发现已经恢复访问。

![image-20230905103928331](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115135872273_522_image-20230905103928331.png)

### 容器的停止，重启和删除

上一小节我们学习的容器的暂停和恢复。除了暂停/恢复之外，我们还可以对容器进行启动和停止操作。和暂停恢复不同的是，容器重启之后，容器内部运行的应用会被停止。比较类似于物理机的重新启动。

1. 容器的停止

首先我们利用`docker top`命令显示容器中正在运行的应用。接下来我们使用`docker stop`命令停止容器，停止之后用`docker ps -a`命令查看容器状态，会发现容器变成了`Exited`状态

看容器状态，会发现容器变成了Exited状态

```shell
docker top ubuntu-3
docker stop ubuntu-3
docker ps -a 
```

![image-20230905104252646](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115141294293_905_image-20230905104252646.png)

2. 容器的重启

对于已经进入`Exited`状态的容器，我们可以利用`docker restart`命令重新启动容器，当容器重新启动之后，我们再利用`docker top`和`curl`测试容器中的http服务，已经不可使用。

```shell
docker restart ubuntu-3
docker top ubuntu-3
```

```shell
curl [容器IP]:8000
```

![image-20230905104419168](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115145758825_431_image-20230905104419168.png)

3. 容器的删除

对于已经不再需要的容器，我们可以使用`docker rm`命令进行删除，`docker rm` 命令可以使用`CONTAINER ID`或者`NAME`作为参数。在默认情况下，我们只能删除`Exited状`态下的容器，如果容器的状态不是停止。则需要为`docker rm`添加`--force`或者`-f`参数才可以删除。

```shell
docker ps -a
docker rm --force [CONTAINER ID]
docker ps -a
```

或

```shell
docker rm --force ubuntu-3
docker ps -a
```

我们会发现容器已经被删除了。

![image-20230905104646099](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E5%85%A5%E9%97%A8/20230906115148957414_272_image-20230905104646099.png)

```
rm-bp1n5f8yed463o5d0.mysql.rds.aliyuncs.com
```

