---
title: 深入浅出Docker应用-Docker网络模型
categories: 笔记
tags:
  - Docker
abbrlink: 36160
date: 2023-09-06 12:16:35
---
# 深入浅出docker应用-Docker网络模型

## 容器的网络入门

### 创建实验环境镜像

在前面的实验中我们学习了Docker中的容器和容器镜像的用法。而容器作为一种虚拟机技术，其网络和存储模型也是非常重要的知识重点，因此本实验中我们讲的带领大家学习容器的网络模型的基本概念。

1. 编写自定义Dockerfile

为了后续实验的进行，我们先来创建一个包含`python`环境的自定义镜像，我们基于python3.7构建实验镜像。接下来我们为实验镜像配置aliyun的ubuntu的apt源，并且进行apt的初始化操作，在初始化完成之后。我们为镜像安装`curl`，`ping`，`ifconfig`，`traceroute`等常用网络工具。最后我们设置镜像运行时在`8000`端口启动python3内置的`http`服务。

我们通过vi编辑Dockerfile，并将下面的内容添加到中Dockerfile中，注意使用vim编辑器时：

1. 需要先按`i`键进入编辑模式。
2. 编辑完成之后按esc退出编辑模式。
3. 然后按`:wq`保存并退出vim。

```shell
vim Dockerfile
```

```dockerfile
  FROM python:3.7
  
  EXPOSE 8000
  
  RUN echo "deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse \n\
  deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse \n\
  deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse \n\
  deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse \n\
  deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse \n\
  deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse \n\
  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse \n\
  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse \n\
  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse \n\
  deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse" > /etc/apt/sources.list
  
  RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
  
  RUN apt-get update
  RUN apt-get install -y curl net-tools inetutils-ping traceroute
  
  CMD ["python3", "-m", "http.server", "8000"]
```

2. 编译镜像

编辑好Dockerfile之后，通过`docker build`命令生成新的镜像。注意镜像生成过程中，需要通过网络安装相关组件，因此容器构建时间可能会比较长。

```shell
docker build -t py/http .
docker images
```

3. 验证镜像

容器制作完毕后，我们创建容器，然后使用`docker exec`命令在容器中执行`curl 127.0.0.1:8000`验证服务的启动。

```shell
docker run -itd --name check py/http
docker exec check curl 127.0.0.1:8000
docker rm -f check
```

![image-20230905162033315](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115927011432_829_image-20230905162033315.png)

### 容器和宿主机中的网卡

实验环境创建成功后，接下来我们来学习容器和宿主机中的网卡信息

1. 容器的网卡信息 

创建容器后。docker会为容器默认创建一块虚拟网卡。容器通过这块网卡实现网络连接，为了验证容器的网卡，我们首先用自定义镜像py/http创建两个容器，当容器创建好之后，我们通过docker inspect命令查看容器详细信息，详细信息中包含容器网卡的IP。为了简化容器信息的查看，我们可以使用-f参数来筛选容器的信息。

```shell
docker run -itd --name py1 py/http
docker run -itd --name py2 py/http
docker inspect -f '{{.NetworkSettings.IPAddress }}' py1
docker inspect -f '{{.NetworkSettings.IPAddress }}' py2
```

![image-20230905162231861](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115930659188_491_image-20230905162231861.png)

2. 多容器信息查询

当Docker中的容器或者容器镜像数量较多的时候，每次使用一条命令来查询一个容器或者镜像信息就会变得非常的繁琐。这时我们就可以使用`docker ps`中`-f "name=value"`参数过滤所需要的对象，再用`-q`参数只获得所需要对象的ID。

接下来再配合linux命令行的`$()`，将对象的ID作为参数传给`docker inspect`命令。这样就可以一次性获得所有对象的配置信息。我们通过下列命令显示所有容器名称包含`py`的容器的IP地址。

```shell
docker ps -f "name=py" -q
docker inspect -f '{{.Name}} {{.NetworkSettings.IPAddress }}' $(docker ps -f "name=py" -q) 
```

![image-20230905163325242](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115935274383_307_image-20230905163325242.png)

3. 宿主机的网卡信息 

在docker安装之后，也会在宿主机上安装一块默认的虚拟网卡`docker0`，该网卡可以和容器中的虚拟网卡互联互通。我们先通过`ifconfig`查看docker0的网卡信息。

```shell
ifconfig docker0
```

![image-20230905163118101](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115939701805_748_image-20230905163118101.png)

### 容器和宿主机的连通性

本小节中我们来测试容器和宿主机网络连通性

1. 测试宿主机和容器之间的连通性

接下来我们来测试的宿主机和容器网卡的互联互通，会发现在默认情况下，宿主机可以通过`docker0`网卡访问容器中的服务。

```shell
ping -c 4 [py1容器IP]
curl [py1容器IP]:8000
ping -c 4 [py2容器IP]
curl [py2容器IP]:8000
```

![image-20230905162945636](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115944397056_252_image-20230905162945636.png)

2. 容器之间的网络连接

接下来我们来测试容器之间的网络连通性，我们通过`ifconfig`命令查看容器详细信息，会可以发现各容器的的IP地址属于同一个子网，这种设置保证了容器之间的网卡可以互联互通，为了验证我们进入py1容器的控制台，然后测试py1到宿主机和py2的连通性。

```shell
docker exec -it py1 /bin/bash
ping -c 4 [docker0 IP]
ping -c 4 [py2容器IP]
curl [py2容器IP]:8000
exit 
```

![image-20230905163234783](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115949958075_213_image-20230905163234783.png)

3. 容器的外网访问

在上一个步骤中查看容器的网络信息时，我们会发现容器的网卡中**网关IP**正是宿主机的`docker0`网卡的IP。

> 注：可通过`netstat -rn`查看。
>
> ![image-20230905165716152](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115952557471_924_image-20230905165716152.png)

这就意味着，如果容器的宿主机可以访问互联网，容器就可以通过宿主机的`docker0`网卡转发网络数据包访问互联网。为了验证我们进入py1容器的控制台，`ping`访问`aliyun.com`验证连通性，再通过`traceroute`命令验证容器访问外网的路径。会发现容器访问外网的第一条就是`docker0`网卡。

```shell
docker exec -it py1 /bin/bash
ping -c 4 www.aliyun.com
traceroute www.aliyun.com -w 0.1
exit
```

![image-20230905164231855](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115956774933_957_image-20230905164231855.png)

### 容器的端口映射

在上面的几个小节中我们学习了了，容器和宿主机的互相访问，容器和容器的互相访问，以及容器对外网的访问。但是由于容器本身使用了Docker创建的私有网络地址，虽然可以通过`docker0`网卡转发访问外网，但是无法提供服务，让外网的使用者来访问。

为了解决这个问题，我们就需要用到容器的端口映射功能。通过端口映射功能，我们可以将宿主机的一个端口和一个指定容器的端口进行映射绑定，所有对宿主机端口的访问数据包，都会自动转发到指定容器的端口上。这样只要外网访问者只要能访问到宿主机，就可以通过端口映射功能，访问到容器中的服务。从而实现了通过容器对外发布服务的能力。

本小节中我们就来为大家演示Docker端口映射的常用用法。

1. 端口映射的基本用法

第一种用法就是在`docker run`中通过`-p`参数进行容器和宿主机的端口映射绑定。`-p`参数有两种用法，第一种是分别指定宿主机端口和容器端口，其语法格式为 `-p 宿主机端口:容器端口`；第二种是只指定容器端口，由docker自动分配宿主机端口。其语法格式为 `-p 容器端口`。

如果需要为容器指定映射多个端口，可以在`docker run`中使用多个`-p`参数。在使用端口映射启动容器之后，我们可以通过`docker ps`命令查看容器的端口映射配置。

```shell
docker run -itd -p 18000:8000 -p 18001:8000 --name port1 py/http
docker run -itd -p 8000 --name port2 py/http
docker ps -f "name=port"
```

![image-20230905164540108](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906115959456283_323_image-20230905164540108.png)

2. 查看端口映射

端口映射完成后，我们往往需要查看映射信息，尤其是对docker自动分配宿主机端口的映射方式。除了可以用`docker ps`命令查看映射信息之外。还可以使用`docker port`命令查看映射信息，其调用格式为`docker port 容器名`或者`docker port 容器名 容器端口`。

```shell
docker port port1
docker port port1 8000
docker port port2
```

![image-20230905164647019](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906120003330128_908_image-20230905164647019.png)

> 总结：配端口映射的时候是宿主:容器，查看时是容器 -> 宿主。

3. 验证端口映射

当我们确定了容器在宿主机上的映射端口之后，我们就可以在宿主机上通过`curl`命令来验证映射功能。为了控制`curl`命令的输出，我们可以使用linux的|语法，配置`head -n1`压缩网页输出。

```shell
curl 127.0.0.1:18000 | head -n1
curl 127.0.0.1:18001 | head -n1
curl 127.0.0.1:[port2宿主机端口]  | head -n1
```

![image-20230905164942645](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906120005817916_620_image-20230905164942645.png)

## 容器的自定义网络

### 使用自定义网络

在上一个实验中我们讲解了Docker中默认网络模式下的网卡，连通性和端口映射。实际上在Docker中，一共包含了五种网络模式。分别是`None`，`Bridge`，`Host`，`Container`和`自定义模型`。其中`None`模式为无网络容器，在默认情况下Docker中的容器使用的是`Bridge`网络模型。`Host`和`Container`是两种共享网络模型。在本实验中我们来重点讲解`Bridge`模型。

Bridge网络模式的网络架构，是一种类似家用路由器的NAT网络架构。在这种架构中内网和外网使用不同的网络地址，容器中的网卡和宿主机中的Docker网卡（默认为Docker0）使用**私有的内网地址**，同时宿主机Docker网卡作为容器中的网卡的默认网关。而宿主机的物理网卡作为外网使用**外网地址**。

当容器需要访问外网时，Docker通过网络地址转换（NAT）将内网对外的访问请求转发到宿主机的物理网卡实现外网访问。当外网需要访问容器中的服务时，Docker使用目标网络地址转换（DNAT）,实现容器的端口映射功能。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121438023132_943_image-20230905171448071.png" alt="image-20230905171448071" width="50%" height="50%" />

1. 自定义Bridge网络

在上面的说明中，为大家简单介绍了Docker的Bridge网络模型。在默认情况下新创建的容器会使用Bridge网络模型，同时使用`docker 0`网卡作为默认网关。在使用bridge模型时，除了使用默认的docker0网卡之外。我们还可以使用`docker network`创建新的宿主机容器网络。

在创建新的容器网络时我们使用`docker network create`命令，并且可以使用`--gateway`参数指定网卡的地址，以及使用`--subnet`内网地址的网络地址段。

```shell
docker network create --gateway 192.168.0.1 --subnet 192.168.0.0/24  network1
```

2. 查看Bridge网络

docker network除了可以创建自定义网络之外，还可以使用`docker network ls`查看已有的Docker网络。对于单个网络也可以使用`docker inspect`命令查看详细配置。

另外当自定义bridge网络创建之后，通过宿主机的`ifconfig`命令可以发现在宿主机中生成了一块新的网卡，网卡的名称前缀为`br-`。

```shell
docker network ls
docker inspect network1
```

![image-20230905171940633](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121443459226_284_image-20230905171940633.png)

```shell
ifconfig -s
ifconfig br-[网络ID]
```

![image-20230905172129476](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121448940363_596_image-20230905172129476.png)

3. 加入自定义Bridge网络

自定义网络创建完毕后，就可以在`docker run`运行容器的时候，使用`--network`参数指定容器使用某一个网络，同时我们还可以使用`--ip`参数指定容器的IP地址。

```shell
docker run -itd --name busybox1 --network network1 --ip 192.168.0.101 busybox
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' busybox1
```

![image-20230905172402430](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121454346633_249_image-20230905172402430.png)

### 多网络的连通性

在上一个小节中，我们介绍了通过docker network自定义Bridge网络。接下来我们来看一下不同网络之间的容器的连通性问题。

1. 不同Bridge网络的连通性

我们尝试在默认的`docker0`网络中再创建一个容器`busybox2`，然后通过`docker exec`命令在`busybox2`中执行`ping`命令，来测试该容器和上一个步骤中创建的`busybox1`之间的连通性。会发现不同网络之间的容器无法互联互通。

```shell
docker run -itd --name busybox2 busybox
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' busybox2
docker exec busybox2 ping 192.168.0.101 -w 1
```

![image-20230905172614913](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121458521078_985_image-20230905172614913.png)

2. 容器连接多网络

如果我们需要让处在不同docker网络之间的容器互联互通，从宿主机网络上配置，一般我们可以采用手动配置路由的方式。

除此之外我们还可以从容器上进行配置来解决这个问题。而解决的方式就是通过`docker network connect`命令为容器创建一个新的网络连接。接下来我们来演示将已经运行容器`busybox2`，连接到`network1`网络上。

```shell
docker network connect --ip 192.168.0.102 network1 busybox2
```

3. 验证多网络连接

网络联通之后，我们再次测试ping命令。会发现busybox2容器已经可以ping通busybox1容器的网络地址。通过ip add命令。我们发现当使用`docker network connect`命令创建连接之后，在容器中会生成一块与之对应的新的网卡。

```shell
docker exec busybox2 ping 192.168.0.101 -w 1
docker exec busybox2 ip addr
```

![image-20230905173151504](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121502122637_753_image-20230905173151504.png)

### 容器中的域名解析

在我们实际使用Docker时，一般来说并不建议将所有的服务的部署在一个容器中，而是尽量让一个容器中只包含一个服务。然后将多个容器加入同一个网络时，如果一个容器中的服务希望访问另一个容器中的服务，就需要知道另一个容器的网络地址才能进行调用。

但是在应用开发阶段，开发者往往并不知道应用所依赖的服务会被部署到具体哪个网络地址。在这种情况下，我们通常会使用域名来解决这个问题，也就是使用一个字符串作为域名表述一个服务的网络地址。然后再容器之上配置DNS域名解析服务，将域名字符串转换成具体IP地址。

1. 默认网络容器链接

在docker0默认网络中，我们可以使用`--link`参数链接一个已经启动的容器。当一个容器使用`--link`链接到另一个容器之后，在该容器在创建时会在容器中配置本地静态DNS域名文件，将被链接容器的容器名解析成被链接容器的IP地址。

```shell
docker run -itd --name domain1 --network network1 busybox
docker exec domain1 ping busybox1 -c1
docker exec domain1 ping domain1 -c1
```

![image-20230905173743604](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121505575156_739_image-20230905173743604.png)

> 注：下面两条是为了验证 domain1 正确的加入到network1。

2. 自定义网络中得DNS

而在自定义网络中，docker会为自动为网络中的容器添加一个内置的动态DNS服务。在同一网络中容器之间，可以直接使用容器名进行访问。

```shell
docker run -itd --name domain3 --network network1 busybox
docker run -itd --name domain4 --network network1 busybox
docker exec domain3 ping domain3 -c1
docker exec domain3 ping domain4 -c1
```

![image-20230905174021497](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121513885053_753_image-20230905174021497.png)

> domain3和domain4在同一网络，验证通过动态DNS配置的容器名域名能够ping的通。

3. 网络别名

除了使用容器名称之外，我们还可在使用`docker run`创建容器得时候使用`--network-alias`参数设置网络别名作为域名。`--network-alias`参数和`-p`参数一样，可以并列设置多个，同时设置多个域名。

```shell
docker run -itd --name domain2 --network-alias web --network-alias db --network network1 busybox
docker exec domain1 ping domain2 -c1
docker exec domain1 ping web -c1
docker exec domain1 ping db -c1
```

![image-20230905174308569](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121519436040_631_image-20230905174308569.png)

### 容器实现Nginx代理

在上面的步骤中我们讲解了容器中的自定义网络。接下来我们来看一个简单的Nginx代理，来理解自定义网络。在这个例子中，我们创建三个容器，一个通过Python启动http服务，一个启动apahce服务，然后在一个Nginx服务中配置代理，让他转发其他两个服务，并且对外通过端口映射提供服务。

1. 容器准备

首先为了避免干扰，我们先删除全部容器。接下来我们创建两个容器，一个是名为python1的python容器，创建之后在80端口启动内置http服务(`python3 -m http.server 80`)。另一个名为httpd1的httpd容器，也就是apahce服务，默认在80端口启动服务。

在容器创建成功后，我们使用curl进行测试。这里我们使用组合命令，先获取容器得IP，然后作为参数传递给curl。

```shell
docker rm -f $(docker ps -aq)
docker run -d --name python1 python python3 -m http.server 80
docker run -d --name httpd1 httpd

curl $(docker inspect python1 -f {{.NetworkSettings.IPAddress}})
curl $(docker inspect httpd1 -f {{.NetworkSettings.IPAddress}})
```

> 注：该过程下载较慢，需要耐心等待。

![image-20230905175352061](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121524109420_497_image-20230905175352061.png)

![image-20230905175403597](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121529331977_884_image-20230905175403597.png)

2. 编写Nginx配置文件

接下来我们来配置Nginx容器作为代理服务器。首先我们宿主机中生成Nginx的配置文件`proxy.conf`。在配置文件中，我们设置两个配置信息，分别是对8001端口的访问转发到**python1的80端口**，以及对8002端口的访问转发到**httpd1的80端口**。我们使用`vi`命令编写`proxy.conf`并编辑为如下内容。注意使用vi编辑器时：

1. 需要先按i键进入编辑模式。
2. 编辑完成之后按esc退出编辑模式。
3. 然后按大写的ZZ保存并退出vi。

```shell
vi proxy.conf
```

```nginx
server {
    listen       8001;
    server_name  0.0.0.0;

    location / {
        proxy_pass   http://python1;
    }
}

server {
    listen       8002;
    server_name  0.0.0.0;

    location / {
        proxy_pass   http://httpd1;
    }
}
```

3. 编写Dockerfile

Nginx配置文件生成完毕之后，接下来我们来编辑`Dockerfile`。在`Dockerfile`中，我们将配置文件复制到`/etc/nginx/conf.d/proxy.conf`目录中。我们使用vi命令生成`Dockerfile`并编辑为如下内容：

```shell
vi Dockerfile
```

```dockerfile
FROM nginx:latest
ADD proxy.conf /etc/nginx/conf.d/proxy.conf
```
>注：此处原文表述有较多处错误，已订正。

4. 启动代理服务

Dockerfile编辑完成后，我们继续生成容器镜像`proxy`。镜像生成成功后，我们通过该镜像创建容器`proxy1`。在创建容器的时候，我们使用`--link`参数添加python1和httpd1域名，同时将proxy容器的80，8001，8002端口映射到宿主的8000，8001，8002。

```shell
docker build -t proxy .
docker run -d --name proxy1 -p 8000:80 -p 8001:8001 -p 8002:8002 \
--link python1 --link httpd1 proxy
```

![image-20230905180422754](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121533471480_288_image-20230905180422754.png)

5. 验证Nginx代理服务

代理服务启动之后，我们使用`curl`命令进行验证。分别访问127.0.0.1的8000，8001，8002三个端口，我们会发现通过容器proxy在宿主机上的端口映射，我们实现了对三个容器的统一访问入口。

```
curl 127.0.0.1:8000
curl 127.0.0.1:8001
curl 127.0.0.1:8002
```

![image-20230905180212999](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121539097331_620_image-20230905180212999.png)

## 容器的共享网络模型

### Host网络模型简介

在上一个实验中我们学习了docker中的bridge网络模式。在bridge网络模式下，容器和宿主机网络隔离。不同网络下的容器具有不同的网络地址，这种网络模式的优点是架构比较清晰，资源具有必要的隔离。

但是这种架构的缺点是容器和容器，容器和宿主机之间的网络通讯的数据包需要在不同的虚拟网卡之间传输。这种传输需要通过操作系统的底层驱动，在网络数据量大的时候会对系统资源造成消耗。同时在当容器和外网互相访问时，需要使用NAT/DNAT修改网络数据包的地址字段。这也会对系统资源造成消耗，并且对容器的网络吞吐造成影响。

因此当我们需要在容器中部署对外网网络吞吐量很大，或者对网络延迟比较敏感的服务时，采用Bridge模式并不是最好的选择，这种情况下我们可以选择**Host网络模式**。

1. Host网络模式

首先我们来看Docker中的Host网络模式的架构。在Host网络模式下，容器在创建之时，并不会创建虚拟网卡。而是共享使用宿主机的默认网卡，因此Host模式下，容器网卡的网络地址和宿主机网卡的网络地址一致。

![host](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121542480155_579_zfjcruuaylg7m_f3201d02623c49dc80d06754a0021d63.png)

在了解了Host网络模式之后，我们来看如何创建Host模式的容器。在上一个实验中我们学过可以通过`docker network ls`命令查看Docker网络。细心的同学可能会观察到，在Docker的默认网络中就包含一个`host网络`。这个网络的驱动使用的就是host。	

因此当我们创建创建容器时，只需要使用`--network=host`参数，加入这个网络容器就会设置成Host网络模式。

2. 获得宿主机网卡信息

接下来我们来验证Host网络模式中的容器和宿主机的网络设置。我们首先在宿主机中使用`ip addr`命令查看网卡IP。在宿主机中我们可以找到`默认网卡eth0`，和`docker默认Bridge网络docker0`。

![image-20230905201850370](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121547691885_678_image-20230905201850370.png)

3. 获得容器网卡配置

接下来我们通过`docker exec`在容器中执行`ip addr`。我们会发现容器和宿主机的网卡完全一致。我们尝试ping docker0网卡，发现也可以ping通。这也就验证了Host网络模式下，容器的网卡和宿主机属于共享状态。

```shell
docker exec host1 ip addr
ping [docker0 IP] -c1
```

![image-20230905202117058](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121553078213_743_image-20230905202117058.png)

###  Host模型的python案例

在上一个小节中我们学习了Host网络模型的基本用法，在本小节中我们来看一个Host共享网络的案例。我们创建一个Python容器并启动一个Http服务。然后将容器连接到Host网络。然后再上一个小节中创建的`host1`容器中访问Python服务。

1. 创建Host容器

Host网络模型和Bridge模型一样，支持多个容器接入。我们创建一个接入Host网络的Python容器`host2`，并在创建容器的时候通过`bash -c "python -m http.server 端口号"`启动python内置http服务的命令。

```shell
docker run -itd --name host2 --network=host python \
bash -c "python -m http.server 8000"
```

2. 查询网络端口

在Host网络模型中，为了保证网络传输效率，宿主机和所有的容器都使用了相同的网卡配置。因此在Host模型中，无论是在宿主机中或是容器中启动的服务绑定了端口。端口占用会对宿主机和所有容器生效。

接下来我们在宿主机中也启动一个python内置的http服务，服务绑定端口`8001`。然后再容器和宿主机中通过`netstat`命令查看端口占用情况。会发现无论是宿主机还是容器host1，端口8000和8001都被占用了。

![image-20230905202712250](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121558730303_763_image-20230905202712250.png)

3. 访问容器服务

由于容器和宿主机都绑定了相同的网卡，因此即使是在服务中启动的服务，也不需要端口映射就可以在宿主机中访问。Host模式的这种设计简化了容器服务的发布流程，同时也提高了网络吞吐的效率。不过需要注意的是，由于容器和宿主机共享了网卡。因此我们要小心的分配宿主机和容器中服务的端口，以避免端口绑定冲突。

```shell
curl 127.0.0.1:8000 | head -n1
```

![image-20230905202812343](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121602244999_405_image-20230905202812343.png)

### Container网络模型

在上面两个小节中我们了解了Docker中的一种共享网络模型Host。这种模式主要用于灵活的在宿主机网卡上发布应用，或者提高网络吞吐效率。除了这种共享网络模式之外，Docker还提供了另一种共享网络模式Container。接下来我们来学习这种网络模式的特点和用法。

1. 创建容器

Host网络模式下，新创建的容器共享使用宿主机的网卡。而在Container网络模式和Host模式类似，只不过新创建的容器，共享的是**另一个容器的网卡**。

当我们希望创建一个使用Container网络模式的容器时，我们需要在docker run中使用`--network container:[已有容器名]`的参数格式。

```shell
docker run -itd --name container1 busybox
docker run -itd --name container2 --network=container:container1 busybox
```

2. 查看地址

Container网络模型的容器创建完毕后，我可以在两个容器中使用ip addr命令查看网卡信息，会发现两块网卡的信息完全一致。

```shell
docker exec container1 ip addr
docker exec container2 ip addr
```

![image-20230905203100315](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121607764416_189_image-20230905203100315.png)

3. 创建python服务

接下来我们再利用这块网卡创建一个名为python1的python容器，并在容器上启动一个python的http服务。由于docker run命令的参数较长，在此我们可以使用\分割符将命令分成几行输入。

```shell
docker run -itd --name container3 \
--network=container:container1 python \
bash -c "python -m http.server 8000"
```

4. 访问服务

在服务启动后，由于三个容器使用了相同的网卡，因此我们在container1容器使用127.0.0.1网络地址就可以访问到另一个容器中的服务。

由于在busybox容器中没有curl命令，这种情况下我们可以使用nc命令来访问http服务。具体访问命令解释如下：

- 首先我们使用exec命令进入容器的控制台。
- 在控制台中我们使用printf命令构建一个HTTP访问请求
- 然后通过|符号将请求发送给nc命令
- 在使用nc命令时，我们将IP和端口作为两个参数传入

执行后，命令返回了HTTP应答的全部信息。这也就验证了在container模型下，容器可以向访问本机服务一样，跨容器进行服务访问。

```shell
docker exec -it container1 sh
```

```shell
printf "GET / HTTP/1.1\r\n\r\n" | nc 127.0.0.1 8000
```

![image-20230905203413825](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121613687049_409_image-20230905203413825.png)

执行`exit`命令退出容器控制台。

### Container模型的redis案例

上一个小节中我们学习了Container模式的基本用法。相比较DNS而言，使用这种方式网络地址管理会更加的方便，同时由于不同的容器共享了一块网卡，网络传输的效率也有明显的提升。

在容器的使用实践时，我们在一个容器中一般只部署一个组件。对于一些由多个组件构成的服务，我们一般会使用Container网络模式。将不同的组件发布到同一个网卡上。这样不同的组件就可以向部署在同一个系统上一样使用。

接下来我们来学习一个redis和Python两个组件组成的服务的部署案例。

1. 启动redis容器

redis是一个上手容易，使用简单的内存存储服务组件。通常被用来当作web服务的缓存组件来使用。首先我们来创建一个名为redis1的redis容器。当容器创建之后，我们可以通过`redis-cli`命令进入redis的控制台。

![image-20230905204040328](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121619384406_970_image-20230905204040328.png)

2. 初始化redis数据

在redis中数据的存储结构采用的是`key/value`结构，在控制台中我们可以通过`set [key] [value]`命令存储数据。数据存储后可以使用`get [key]`命令读取数据。

```shell
set name aliyun
set year 2000

get name
get year

exit
```

![image-20230905204058709](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121623021954_340_image-20230905204058709.png)

3. 安装Python的redis工具

接下来我们再启动一个名为python1的python容器，并和redis1容器共享网卡。在容器创建成功后，我们在容器中使用pip install命令安装访问redis的工具。

```shell
docker run -itd --name python1 --network=container:redis1 python
docker exec python1 pip install redis
```

![image-20230905204353188](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121626357968_113_image-20230905204353188.png)

4. 通过Python脚本调用redis

接下来我们在python1容器中执行`python`命令，进入命令行模式。在命令行模式中，我们可以一条一条的输入命令。并观察命令的执行结果。

首先我们使用`import redis`命令加载访问工具，加载完成后，使用`redis.Redis()`命令创建到redis服务的连接。在创建连接时虽然python服务和redis服务不在同一个容器中，但是由于我们共享了网卡，我们还是可以使用127.0.0.1的网络地址来访问不同容器的服务。

连接创建之后，我们就可以使用`keys(*)`命令列出redis中所有的key，然后我们继续使用`get([key名字])`的命令获得key对应的value。我们发现通过python容器获得数据和在redis-cli中获得的数据是一致的。

```shell
docker exec -it python1 python

import redis
r = redis.Redis(host='127.0.0.1',port=6379,db=0)
print(r.keys('*'))
print(r.get('name'))
print(r.get('year'))
exit()
```

![image-20230905205150802](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%9E%8B/20230906121632033915_844_image-20230905205150802.png)