---
title: 深入浅出Docker应用-Docker存储模型
categories: 笔记
tags:
  - Docker
abbrlink: 30866
date: 2023-09-06 12:22:15
---
# 深入浅出docker应用-Docker存储模型

## 容器的配置和存储

### 快速上手

在上面的实验中我们学习了容器的网络用法和网络模型，接下来我们来学习几种配置容器中的服务，以及管理容器存储系统的方式。

1. 容器环境变量

在容器的配置中，最简单的方式是配置容器的环境变量。当我们使用docker run运行容器是，可以添加`-e`参数为容器设置环境变量。在配置环境变量时，也可以和`-p`参数一样同时设置多个`-e`参数。

参数配置完成后，进入容器使用`echo`命令输出设置的环境变量。验证`-e`参数的使用。

```shell
docker run -it --name env1 -e ECHO=环境变量 -e NUM=123456 busybox
```

```shell
echo $ECHO $NUM
exit
```

![image-20230905205658055](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122021966682_985_image-20230905205658055.png)

2. 容器文件复制

容器中的另一个存储方式是使用`docker cp`命令，在宿主机和容器之间进行文件的复制。在文件复制时容器中文件的描述方式为，`容器名:容器文件路径`。

我们在宿主机中通过`echo`命令创建文件`local.txt`。然后创建容器`file1`，接下来通过`docker cp`复制到容器中。最后在容器中通过`cat`命令显示文件命令。

```shell
echo 本机生成的文件 > local.txt
docker run -itd --name file1 busybox
docker cp local.txt file1:/local.txt
docker exec file1 cat local.txt
```

![image-20230905205826324](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122024468499_912_image-20230905205826324.png)

3. 文件的挂载

除了使用`docker cp`文件复制的办法之外，我们还可以在创建容器的时候使用`-v`参数将宿主机中的文件直接挂载到容器中。该参数的用法为`-v 宿主机文件的绝对路径:容器文件的绝对路径`。这种方式在后面会进行详细讲解。

```shell
docker run -itd --name file2 -v $(pwd)/local.txt:/mount.txt busybox
docker exec file2 cat mount.txt
```

![image-20230905210015001](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122028923771_476_image-20230905210015001.png)

### MYSQL镜像的基本用法

在上一个步骤中，我们讲解了容器的管理和存储的基本用法。接下来我们用一个MySQL容器来演示这些用法的具体实战。为了实验演示，我们先来学习一下MySQL容器的基本用法。

传统启动MySQL服务的方式，是在操作系统中安装MySQL的服务，并且通过`systemctl`命令进行启动，但是这种方式需要在系统目录中复制相应的文件，同时向系统中注册服务。这样的流程不但复杂，一旦服务的文件或者配置被破坏或者篡改会导致服务不可用，且难以定位问题。

因此在使用了Docker之后，我们可以从官方仓库中下载已经配置好的MySQL容器镜像。然后直接通过镜像的方式启动服务。这样做不会在宿主机的系统中保存任何文件和配置。服务的稳定性大大提高。

1. MySQL容器的启动配置

在本实验中我们使用**mysql容器的8.0版本**进行实验。我们来看一下MySQL容器镜像的启动配置方式，MySQL数据库是通过网络对外提供服务的，当服务启动后，默认会打开并监听3306端口，用来接受客户端得各种命令。

在这里我们使用默认的Bridge网络模型，同时使用`-p`参数设置端口映射，将MySQL得服务暴露到宿主机的网卡上。

除此之外在启动MySQL容器得时候，我们还可以通过设置`MYSQL_ROOT_PASSWORD`环境变量的方式，设置MySQL中`root`用户的初始化密码。这里我们使用`-e`参数来设置。

在配置好启动命令之后，我们启动容器，并且使用`bash`登录到容器中，验证环境变量的配置成功。

```shell
docker pull mysql:8.0
docker run -itd --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=[MYSQL密码] mysql:8.0
docker exec -it mysql bin/bash
```

```shell
echo $MYSQL_ROOT_PASSWORD
exit
```

![image-20230905210810439](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122032462368_350_image-20230905210810439.png)

2. 进入MySQL服务的控制台

MySQL服务启动后，我们可以使用mysql命令登录服务得控制台，该命令的用法为`mysql -u用户名 -p`，其中`-p`表示登录账户需要密码。命令执行后输入在上一个步骤中设置的密码即可进入控制台。

```shell
docker exec -it mysql mysql -uroot -p
[输入MYSQL密码]
```

![image-20230905210931741](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122037142229_199_image-20230905210931741.png)

3. MySQL控制台验证命令

在MySQL控制台中，我们可以使用`status`命令查看服务的运行状态，使用`show Database;`查看服务中的数据库，也可以使用`help`命令查看其他命令的用法。

```mysql
status
show Databases;
help
exit
```

### 复制修改MYSQL配置文件

在MySQL容器中，环境变量只能对一些简单的属性进行配置，实际上大多数属性都是通过位于`/etc/mysql/my.cnf`的配置文件进行管理的。接下来我们来学习如何使用文件复制的方式进行配置管理。

1. 查看MySQL配置属性值

在MySQL服务中包含了大量的属性值，这些属性值影响服务的运行状态。如果希望修改属性值，就需要修改`my.cnf`配置文件。在本次实验中，我们使用一个对服务影响不大的属性`general_log`来演示配置文件的用法。

首先我们先进入控制台，然后使用`show variables`命令查看设置前的属性值。可以发现属性值现在为`OFF`。

![image-20230905212216832](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122041622614_523_image-20230905212216832.png)

2. 复制修改配置文件

如果单纯的为了修改配置，我们可以直接在容器中修改配置文件。但是为了防止容器被删除或者被破坏时，修改好的配置文件丢失，我们先使用`docker cp`将配置文件复制到宿主机中的`/root/mysql/config/`目录中作为副本。

```shell
mkdir -p /root/mysql/config/
docker cp mysql:/etc/my.cnf /root/mysql/config/my.cnf
cat /root/mysql/config/my.cnf
```

![image-20230905212510404](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122046212049_831_image-20230905212510404.png)

3. 当配置文件复制完毕后，我们使用vi编辑该文件，在[mysqld]段落的末尾添加如下内容，修改后的段落如下。

- 输入`/secure-file-priv`按回车可快速定位，修改`secure-file-priv`的值为`NULL`。
- 添加`general_log = 1`

```shell
vi /root/mysql/config/my.cnf
```

```shell
general_log = 1
```

![image-20230905212718393](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122048592517_741_image-20230905212718393.png)

### 挂载MYSQL配置文件

在上一步我们完成了配置文件的复制和修改，接下来我们来将配置文件应用到容器服务中

1. 应用配置文件

我们将配置文件复制回容器中，为了让配置文件生效，我们需要使用docker restart命令重新启动容器。

```shell
docker cp /root/mysql/config/my.cnf mysql:/etc/my.cnf
docker restart mysql
```



![img](https://ucc.alicdn.com/pic/developer-ecology/zfjcruuaylg7m_e5d7202a965b493a9ed0349b2f8df7fe.png)

1. 查看配置结果

容器重启之后，我们再次进入控制台查看属性值，会发现新的属性值已经生效。

```shell
docker exec -it mysql mysql -uroot -p[MYSQL密码]
show variables like 'general_log';
exit
```

![image-20230905213126926](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122050783249_178_image-20230905213126926.png)

### 容器的文件系统挂载

### 容器的共享挂载

在上一个实验我们学习了容器的配置和存储的几种基本用法，在实验中我们发现相比较文件复制，文件挂载的用法更加的便捷。这种方法也是我们在实际应用中常用的方法。

在本实验中我们来继续学习文件系统挂载的进一步知识。

1. 实验准备

当我们使用`docker cp`向容器中复制文件时，会以宿主机中的文件为样本向容器中复制一个文件的副本。在复制完成之后宿主机和容器中的文件是没有关联的。

但是当我们使用文件挂载的时候，宿主机和容器中的文件的关系更像是linux中的硬链接。也就是虽然看起来是两个文件，但是双方实际上在**共享同一个物理文件**。本小节中我们将学习并验证容器的共享挂载能力。

首先我们先来做实验准备，首先我们先创建一个本地文件`share.txt`，然后让容器挂载这个文件。

```shell
echo '宿主机初始化文件' > share.txt
docker run -itd --name share1 -v $(pwd)/share.txt:/share.txt busybox
docker exec share1 cat /share.txt
```

![image-20230905214440354](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122053619676_734_image-20230905214440354.png)

2. 本地修改文件

当宿主机和容器双方共享同一个物理文件，这就意味着双方都可以修改文件的内容，且在另一方生效。下面我们在宿主机方修改`share.txt`文件，并在容器端验证文件修改是否生效。

```shell
echo '从宿主机中修改文件' >> share.txt
docker exec share1 cat /share.txt
```

![image-20230905214532760](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122056313837_145_image-20230905214532760.png)

3. 容器中修改文件

同样我们也可以在在容器端修改share.txt文件，并在宿主机方验证文件修改。

```shell
docker exec share1 sh -c "echo '从容器中修改文件' >> /share.txt"
cat share.txt
```

![image-20230905214555887](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122100915140_351_image-20230905214555887.png)

### 挂载的权限配置

1. 容器挂载的权限

如果用户希望控制文件在容器中是否可以被修改，那么可以用`rw`或者`readwrite`参数将挂载文件设置为读写权限，或者使用`ro`或者`readonly`参数设置为只读权限。如果文件被设置为的文件，那么只有在宿主机侧才可以进行修改。

先重置实验环境：

```shell
docker rm -f $(docker ps -aq)
```

```shell
echo '宿主机初始化文件' > share.txt
docker run -itd --name share-readonly -v $(pwd)/share.txt:/share.txt:ro busybox
docker exec share-readonly cat /share.txt
```

> 注：`>`：覆盖重定向，`>>`：追加重定向

![image-20230905215029607](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122106103843_206_image-20230905215029607.png)

2. 验证只读权限

接下来我们来验证只读挂载属性，我们分别在宿主机和容器中尝试修改文件，会发现在share-readonly容器中，我们无法修改文件。

```shell
echo '从宿主机中修改文件' >> share.txt
docker exec share-readonly cat /share.txt
docker exec share-readonly sh -c "echo '从只读容器中修改文件' >> /share.txt"
cat share.txt
```

![image-20230905215129674](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122108599300_956_image-20230905215129674.png)

3. 多个容器同时挂载一个文件

宿主机中一个文件，可以挂载到多个不同的容器，每个容器在挂载时可以设定不同的挂载权限，我们再来创建一个容器，并使用读写权限挂载share.txt文件。

挂载成功后我们尝试分别在读写权限容器和只读权限容器中修改文件。不同的容器可以使用不同的权限挂载同一个文件。

```shell
echo '宿主机初始化文件' > share.txt
docker run -itd --name share-readwrite -v $(pwd)/share.txt:/share.txt:rw busybox

docker exec share-readonly sh -c "echo '从只读容器中修改文件' >> /share.txt"
docker exec share-readwrite sh -c "echo '从读写容器中修改文件' >> /share.txt"

cat share.txt
docker exec share-readonly cat /share.txt
```

![image-20230905220547182](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122113368297_956_image-20230905220547182.png)

### 文件夹的挂载

除了挂载文件之外，我们还可以挂载文件夹到容器上，当宿主机的文件或者文件夹挂载到容器时。如果容器的挂载点上已经存在同名的文件夹对象，则容器挂载点上的对象会被**屏蔽**。

1. 实验准备 

为了演示挂载文件夹，我们先创建本地文件夹`mount`，并在文件夹中添加一个文件`mount\text`。然后再制作一个新的容器镜像，在容器中创建一个文件`/mount`。

```shell
mkdir mount
echo '宿主机中的文件' > mount/host
vi Dockerfile 
```

我们使用vi 编辑Dockerfile文件：

```shell
FROM busybox:latest
RUN mkdir mount
RUN echo '容器中的文件' > /mount/image
```

2. 挂载文件夹

接下来我们构建容器镜像，并使用该镜像创建容器。在创建容器时，我们将mount挂载到容器中。

```shell
docker build -t folder .
docker run -itd --name folder1 -v $(pwd)/mount:/mount folder
```

![image-20230905221232424](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122116918938_377_image-20230905221232424.png)

3. 验证文件夹挂载

```shell
docker exec folder1 ls /mount
docker exec folder1 cat /mount/host
```

![image-20230905221441505](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122119641893_184_image-20230905221441505.png)

### Apache挂载案例

在前面的小节中，我们讲解了文件夹挂载的基本用法，接下来我们来看一个实际的案例。在这个案例中我们在容器中启动一个Apache网页服务器。同时为了保证网页可以动态更新，我们将宿主机中的一个文件夹绑定到服务中的存放网页的文件夹上。这样外部应用只需要更新宿主机中的网页文件夹，就可以动态的为容器中的服务更新网页。

1. 实验准备

首先我们在宿主机中创建一个文件夹`webfile`，然后通过`echo >`命令在文件夹中生成一个简单的纯文本网页`index.html`。

```shell
mkdir webfile
echo '默认网页' > ./webfile/index.html
```

2. 挂载网页文件夹

然后我们在启动服务时，通过`-v`参数将宿主机中的文件夹，覆盖挂载到Apache容器的`/usr/local/apache2/htdocs`目录上；并且通过端口映射将容器中的服务发布到宿主机的`8000`端口上。

容器启动成功之后，我们通过`curl`命令访问`127.0.0.1:8000`验证容器服务。

```shell
docker run -itd --name file_server1 -p 8000:80 \
 -v /root/webfile:/usr/local/apache2/htdocs httpd

curl 127.0.0.1:8000
```

![image-20230905221837730](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122121908293_573_image-20230905221837730.png)

3. 动态修改网页

当容器启动后，我们在宿主机中修改`/webfile/index.html`文件，同时创建一个新文件`/webfile/host.html`，然后通过`curl`命令验证，发现宿主机中的修改，对容器中的Apache服务已经生效。

```shell
echo '修改默认网页' >> ./webfile/index.html
echo '添加Host页面' > ./webfile/host.html

curl 127.0.0.1:8000
curl 127.0.0.1:8000/host.html
```

![image-20230905221908534](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122125472121_394_image-20230905221908534.png)

## 容器中的volume卷

### Volume挂载简介

在上面的实验中我们为大家介绍了如何在容器中挂载文件和文件夹，这种采用绝对路径，直接挂载宿主机中的文件或者文件夹的方法又叫`bind mount`。这种方式比较适合将宿主机中的文件共享到容器中的场景。

除此之外docker还提供了另一种`volume`的方式进行挂载。这种方式通常会先在宿主机中通过docker volume命令创建一个具有名称的volume，然后再将这个volume挂载到容器中。

相比较于bind mount方式，这种方式在使用的时候完全使用docker命令，并不需要像bind mount方式那样依赖于宿主机的绝对目录，主要用于将容器中的数据持久化保存到宿主机中。

1. 创建volume

在使用volume之间，通常需要先通过`docker volume create`命令创建volume。该命令的格式为`docker volume create [volume名]`，和bind mount方式不同的是，volume创建之后默认并没有内容。这里我们创建名为`file-vol`的volume。

```shell
docker volume create file-vol
```

2. 挂载volume

在volume创建好之后，我们就可以通过docker run 的-v参数进行挂载。在使用-v参数挂载volume时，用volume名称代替宿主机路径即可。这里我们创建并启动一个busybox容器，并将`file-vol`挂载到`/file`目录。

在容器创建之后，我们向volume挂载的文件夹中写入一个文件`/file/text`。验证挂载成功。

```shell
docker run -itd --name vol1 -v file-vol:/file busybox
docker exec vol1 sh -c "echo '向volume中写入文件' > /file/text"

docker exec vol1 ls /file
docker exec vol1 cat /file/text
```

![image-20230905222708156](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122128026982_637_image-20230905222708156.png)

3. 查看volume信息

当我们在容器的挂载点中保存数据之后，数据文件会被写入到volume中，这时我们可以通过`docker volume inspect`或者`docker inspect`来查看volume的信息。

```shell
docker volume inspect file-vol
```

![image-20230905222835618](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122131531627_519_image-20230905222835618.png)

### Volume的持久化

在上一个小节中我们介绍了volume的基本用法。在容器中我们使用volume的主要作用，是为容器中的文件提供一种持久化的保存方法。

在前面讲解容器基本用法的时候，我们了解到每一个容器都是一个轻量级的虚拟机，在容器中创建的文件和宿主机以及其他容器并没有关系。如果容器被删除了，那么容器上的文件也就都丢失了。但是在某些情况下，我们在容器中存放了有价值的文件，比如数据库，邮件服务器，文件备份等。这个时候我们就希望能有一种即使容器被销毁了文件还可以存在的技术。这就是volume持久化的由来。

1. 删除容器

接下来我们来验证volume的持久化能力。我们停止并删除刚才创建的容器`vol1`。在删除之后我们查看名为file-vol的volume。我们会发现容器的删除并不会影响volume的存在。

```shell
docker stop vol1
docker rm -f vol1
docker volume inspect file-vol
```

![image-20230905223042132](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122135953291_496_image-20230905223042132.png)

2. 重用volume

然后我们再创建一个新的容器vol2，并将`file-vol`挂载到另一个目录`/file-other`上。由于之前的容器把数据存储在了volume中，因此新容器中的`/file-other`目录中保存vol1容器中的数据。

```shell
docker run -itd --name vol2 -v file-vol:/file-other busybox

docker exec vol2 ls /file-other
docker exec vol2 cat /file-other/text
```

![image-20230905223318221](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122139537200_575_image-20230905223318221.png)

3. volume的多重绑定

如同容器可以使用多个端口绑定，容器在启动时也可以使用多个-v参数绑定多个volume，同时一个volume也可以同时绑定到多个容器中。在容器绑定volume之后，我们还可以通过`docker inspec`t命令通过容器筛选Mounts字段查看volume的信息。

```shell
docker volume create ext-vol
docker run -itd --name vol3 -v ext-vol:/ext -v file-vol:/file busybox 
docker inspect -f "{{json .Mounts}}" vol3 | jq
```

![image-20230905223606048](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122144097385_795_image-20230905223606048.png)

### Volume的常用命令

在前面的小节中我们学习了volume的持久化，本小节我们再来学习一下volume相关的一些命令。

1. 查看整体磁盘占用

在docker中，占用磁盘的对象包括容器镜像，容器，volume等，我们还可以通过`docker system df -v`命令可以查看所有对象的的磁盘占用。

如果docker的镜像，容器，或者volume对象较多，则可以使用-f参数添加过滤器来筛选具体某一个volume的信息。下面的命令可以筛选出名为`file-vol`的volume的过滤器的信息。

```shell
docker system df -v
docker system df -v --format=\
'{{range .Volumes}}{{if eq .Name "file-vol"}}\
{{.Name}} - {{.Size}}\n{{end}}{{end}}' 
```

![image-20230905223927214](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122148633154_903_image-20230905223927214.png)

2. 自动创建volume

当我们使用`docker run`创建容器并使用`-v`挂载volume的时候，如果需要加载的volume还没有被创建，则`docker run`会自动创建volume。

```shell
docker run -itd --name vol4 -v auto-vol:/auto busybox 
docker inspect auto-vol
```

![image-20230905224103151](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122153361471_217_image-20230905224103151.png)

3. volume的自动删除

docker也提供了删除所有当前没有被挂载的volume的指令`docker volume prune`，需要注意的是使用此指令时需要小心，防止数据被误删除！下面的代码可以删除全部的容器，并清空所有的volume。下面的例子我们演示了删除所有的容器，并且删除所有的volume：

```shell
docker rm -f $(docker ps -aq) 
docker volume prune -a
docker volume ls
```

![image-20230905224733590](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122155893833_356_image-20230905224733590.png)

![image-20230905224722864](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122158059102_164_image-20230905224722864.png)

### 在MySQL中使用Volume

上面的小节中，我们学习了volume的相关知识，本小节中我们来演示一个通过volume管理MySQL容器的例子。

1. volume的自动创建

事实上当我们在使用`docker run -v` 创建数据挂载时，如果没有预先创建volume，docker会自动创建对应的volume，如果用户连volume名称都没有指定，docker会自动为volume分配名称。

接下来我们直接创建名为mysql1的mysql容器，在容器创建成功后接入mysql控制台。

```shell
docker run -itd --name mysql1 -v db-vol:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=[MYSQL密码] mysql
docker exec -it mysql1 mysql -uroot -p[MYSQL密码]
```

![image-20230905225110593](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122201439818_823_image-20230905225110593.png)

2. 操作数据库

在一个MySQL服务中，可以包含多个数据库，每一个数据库中又可以包含多个数据表。每一个数据表中又可以包含多个数据行。

接下来我们再控制台中通过`CREATE DATABASE`创建一个新数据库`ali_db`，创建数据库之后需要通过`USE`命令选中要操作的数据库，然后通过`CREATE TABLE`命令在`ali_db`中添加一个数据表`ali_tab`，接下来使用`INSERT INTO`在数据表中添加一条记录。最后使用`SELECT`命令查询数据表中的记录。

```shell
CREATE DATABASE ali_db;
USE ali_db;
CREATE TABLE ali_tab (`name` VARCHAR(100));
INSERT INTO ali_tab VALUES('aliyun');
SELECT * FROM ali_tab;
exit
```

![image-20230905225127175](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122206199441_275_image-20230905225127175.png)

3. 重用MySQL数据库

接下来我们删除mysql1容器，删除之后在创建另一个名为mysql2的mysql容器。mysql2容器创建成功后进入mysql控制台，在控制台中通过`USE`命令选择数据库，然后用`SELECT`命令查看数据记录。会发现数据库中记录仍存存在。

```shell
docker rm -f mysql1
docker run -itd --name mysql2 -v db-vol:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=[MYSQL密码] mysql
docker exec -it mysql2 mysql -uroot -p[MYSQL密码]
```

![image-20230905225310167](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122208927409_686_image-20230905225310167.png)

```shell
USE ali_db;
SELECT * FROM ali_tab;
exit
```

![image-20230905225330187](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AD%98%E5%82%A8%E6%A8%A1%E5%9E%8B/20230906122211511426_681_image-20230905225330187.png)
