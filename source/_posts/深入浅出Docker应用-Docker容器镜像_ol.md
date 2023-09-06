---
title: 深入浅出Docker应用-Docker容器镜像
categories: 笔记
tags:
  - Docker
abbrlink: 10725
date: 2023-09-06 11:58:42
---
# 深入浅出docker应用-Docker容器镜像

## 容器镜像管理命令

### 镜像的下载，显示和删除

在docker中镜像保存了容器创建时的基础文件内容和相关的配置信息，镜像一旦创建其中的文件就不可修改了。用户在通过镜像启动容器之后所有对文件的操作，都保存在容器对象当中而不会影响原有的容器镜像。接下来我们来讲解镜像相关的命令。

1. 实验资源准备

通过`docker pull`可以实现镜像的下载，通过`docker images`可以显示。此处我们下载一个新的镜像`debian`来进行测试相关的操作。

```shell
docker pull debian
docker images
```

![image-20230905111740289](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115336118310_589_image-20230905111740289.png)

2. 镜像的查看

对于已经保存在本地的镜像，我们可以使用`docker inspect`命令来查看镜像的详细信息，其用法为`docker inspect` 镜像名，接下来我们来查看`debian`镜像的属性。会发现`docker inspect`命令会输出大量JSON格式的镜像详细信息。

```
docker inspect debian
```

![image-20230905111840241](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115340457256_880_image-20230905111840241.png)

3. 镜像的删除

当镜像下载之后，我们可以通过`docker rmi`命令进行删除。

```shell
docker run -itd --name debian-3 debian
docker rm -f debian-3
docker images
```

![image-20230905112209925](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115345002211_731_image-20230905112209925.png)

要注意的是`docker rmi`无法删除已经创建了容器的镜像，如果需要删除需要先停止相关的容器，并添加`--force`参数。接下来我们再来测试通过镜像创建容器，然后在删除容器之后删除`debian`镜像。

```shell
docker rmi --force debian
docker images`
```

![image-20230905112249614](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115349316003_313_image-20230905112249614.png)

### 镜像的保存和加载

一般情况下我们可以通过`docker pull`的方式通过镜像仓库将镜像下载到本地docker内部。但是这种方法需要保证docker宿主机可以访问到外网且访问速度有保证。如果用户在网络条件不好的情况下希望获取镜像，则可以将镜像的保存到本地文件，然后通过文件复制到容器宿主机上加载方式获得镜像。本小节将为大家介绍这种方法。

1. 镜像的本地保存

首先我们可以通过`docker save`命令可以将docker内部的一个或多个镜像导出成文件。下面的命令中我们先下载nginx，hello-world两个镜像，然后再将镜像导出到`images.tar`文件中。docker save的格式为：`docker save -o [导出文件名] [需要导出的镜像列表]...`

```shell
docker pull hello-world
docker pull nginx
docker save -o images.tar nginx hello-world 
ll images.tar
```

![image-20230905112510946](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115604979456_700_image-20230905112510946.png)

2. 删除已有镜像

上一步已经将nginx，hello-world两个镜像保存到文件images.tar。接下面我们将现有的两个镜像从docker内部删除。为后面的镜像读取做准备。

```shell
docker rmi hello-world
docker rmi nginx
docker images 
```

3. 从本地加载镜像文件

接下来我们通过`docker load`命令将`images.tar`中的两个镜像导入回docker内部。即可实现在没有网络访问的情况更新镜像。`docker load`的格式为：`docker load -i [导入文件名]`。要注意的是：如果docker内部已经存在了相关的镜像，文件中的镜像会被忽略。

在镜像导入完毕之后，我们可以通过`docker image`进行验证。

```shell
docker load -i images.tar
docker images 
```

### 容器快照的导出和导入

上一个小节我们学习了通过`docker save`和` docker load`的方法实现docker内部的镜像保存和加载。在docker中我们除了可以对镜像进行保存和加载，还可以对已经已经创建的容器进行保存和加载。接下来我们就来带领大家学习相关的命令。

1. 创建实验容器

首先我们创建一个容器`python-1`，然后在`python-1`创建一个文本文件。此处我们可以使用`docker exec bash -c` "命令行" 方式直接在宿主机执行命令。我们通过`echo`命令在容器中创建名为`snapshot.txt`的文件。在创建之后再使用`cat`命令验证容器中的文件。

```shell
docker run -itd --name python-1 python
docker exec python-1 bash -c "echo snapshot > snapshot.txt"
docker exec python-1 bash -c "cat snapshot.txt"`
```

![image-20230905113832779](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115609558385_183_image-20230905113832779.png)

2. 容器快照的导出

当容器文件修改之后，我们可以通过`docker export`命令将容器以快照的形式导出到文件。其命令的格式为`docker export 容器名 > 快照文件名`。和镜像导出不同，快照的导出，会将容器的镜像，和容器在镜像之上的修改部分同时导出。

```shell
docker export python-1 > python-snapshot.tar
ll python-snapshot.tar
```

![image-20230905114017315](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115614943354_328_image-20230905114017315.png)

3. 容器快照的导入

对于通过`docker export`导出的容器快照文件。我们可以通过`docker import`命令将其导入到docker中，在这里需要特别注意的是：`docker import`是以镜像而不是容器的形式导入快照。也就是说导入的快照并不能直接运行，而是需要根据此快照镜像再次创建容器才可以使用。docker import命令的格式为docker import 快照文件 导入镜像名称:版本号

```shell
docker import python-snapshot.tar python-snapshot:latest
```

快照导入后，我们可以利用导入的快照镜像创造一个新的容器。并验证通过快照创建的容器中包含着之前容器中创建的文件。

```shell
docker run -itd --name snapshot python-snapshot /bin/bash
docker exec snapshot cat snapshot.txt
```

![image-20230905114307524](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115620362425_973_image-20230905114307524.png)

### 镜像内部层次关系

镜像是docker中非常重要的资源，因此了解镜像的内部结构对学习docker来说相当重要，事实上docker镜像采用的是多个只读结构层叠的方式进行实现和存储的。本小节我们来学习如何查看镜像的层级关系。

1. inspect过滤器的使用

上面的小节我们了解到通过`docker inspect`命令查看镜像属性，会获得一个非常庞大的JSON格式字符串的详细信息。为了能从字符串中只获得我们需要的内容，我们可以使用`-f`参数对详细信息进行过滤和格式化。

在使用`-f`参数时其语法为`docker inspect -f "模板字符串" 镜像名`，其中模板字符串为go语言的模板语法，在后面的实验中我们会详细讲解。在本次实验中我们要求docker inspect输出JSON格式的结果，为了便于显示，我们在参数后面再加入` | jq`，将docker inspect的输出结果交给`jq`命令进行格式化和美化。

```shell
docker inspect -f "{\"Id\":{{json .Id}},\"RepoTags\":{{json .RepoTags}}}" python | jq
```

![image-20230905114742181](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115623529198_693_image-20230905114742181.png)

2. 镜像的层次关系

当docker设计镜像底层结构时，为了节约存储控件，会将镜像设计成只读的分层结构。这样每一层只记录和前一层的文件差别。如果两个不同的镜像底层使用了相同的镜像层，则只需要存储一份就可以。这样就大大减小了冗余镜像存储的情况。

![image-20230905114904603](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115627866613_645_image-20230905114904603.png)

通过`docker inspect`命令我们同样可以查看镜像的层次信息。通过在镜像信息的`.RootFS.Layers`位置，保存的就是镜像的层次信息。通过下面的命令，我们发现，`python`镜像中包含了8层。

```shell
docker inspect -f "{{json .RootFS.Layers}}" python | jq
```

![image-20230905115015870](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115633796078_312_image-20230905115015870.png)

3. 普通镜像和快照镜像的区别

接下来我们来查看普通镜像和快照镜像直接的层次区别，通过观察我们可以发现，通过`docker import`导入的镜像快照。会将所有的层压缩成一层。

![image-20230905115304575](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115637121367_978_image-20230905115304575.png)

同时我们通过`docker images`和`ls -ll`命令我们可以看到快照镜像，快照镜像虽然体积较大，有比较多的冗余内容，但是不会依赖其他的镜像；因此比较适合导出到文件和导入的操作。

![image-20230905115404487](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115642297654_383_image-20230905115404487.png)

## 容器镜像的制作-commit

### 通过容器生成镜像

在前面的实验中，我们学习了容器管理的基本命令。在使用容器的时候我们不但会使用已有的容器镜像，也经常需要制作新的容器镜像。

在Docker中，容器镜像的制作有两种方法，分别是`commit`方法和`build`方法。实际上不论是哪种容器镜像的制作方法，基本上我们都会选择基于一个已有的容器镜像为基础，在此之上进行镜像制作。在本实验中我们先来学习直接通过容器生成新的镜像的`commit`方法。

1. 实验环境准备

在本实验中我们会基于官方的`ubuntu镜像`来制作自定义镜像，在`commit`方法中，为了制作镜像，我们需要先利用基础镜像创建一个容器。接下来我们使用`docker run`创建容器`ubuntu-commit`。

除此之外，我们再使用`docker inspect` 命令查看基础容器镜像的层信息

![image-20230905121132394](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115647711148_393_image-20230905121132394.png)

2. 查看容器修改内容

接下来我们对容器的内容进行修改，我们在容器中执行`apt-get update`命令修改容器中的文件。在文件修改之后，我们可以通过`docker diff`命令查看文件的修改详情，该命令格式为d`ocker diff 容器名`。

```shell
docker exec ubuntu-commit apt-get update
docker diff ubuntu-commit
```

![image-20230905121240110](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115653000478_838_image-20230905121240110.png)

3. 生成新的镜像

在前面的实验中，我们讲到，容器镜像的是以只读分层的方式进行存储的。当我们通过镜像创建容器之后，每一个容器都会生成一个可以编写的存储层，所有用户对容器的文件修改，都会记录在容器存储层中。当我们把容器镜像的只读层和容器存储层叠加起来之后，就得到了容器的完整存储内容。而`docker diff`命令查看的，正是容器存储层所保存的内容。

在了解容器存储层的相关知识之后，我们就可以执行`docker commit`命令生成新的镜像，其命令的格式为`docker commit 容器名 新镜像名`。镜像生成之后我们使用docker images进行验证

```shell
docker commit ubuntu-commit ub/commit
docker images
```

![image-20230905121504361](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115657893023_850_image-20230905121504361.png)

4. 查看新镜像的层

接下来我们使用`dcoker inspect`来查看新镜像的层信息。会发现`ub/commit`在ubuntu的层之上构建了一个新的层。事实上这一层的内容就是将之前的`ubuntu-commit`容器存储层转化成镜像只读层。

```shell
docker inspect -f "{{json .RootFS.Layers}}"  ub/commit | jq
```

![image-20230905121727324](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115703246580_756_image-20230905121727324.png)

### 部署私人镜像仓库

在Docker 中推送镜像的命令是`docker push`，但是默认的`docker push`命令会将镜像推送到docker公共仓库。为了能将镜像推送到私人仓库，我们首先要使用`docker tag`命令为镜像设置需要推送的仓库信息。其命令的参数为`docker tag [本地镜像名] [私有仓库的URL][私有仓库的镜像名称]`。在标记镜像之后，我们使用`docker images`命令查看会发现，为本地镜像设置tag之后，会在本地镜像列表中生成一个新的镜像。

1. 部署私人镜像仓库

首先我们来学习如何启动docker私人镜像仓库。docker的默认私人镜像仓库`registry`应用也提供了镜像的部署方式。也就是说我们可以像启动其他容器一样的方式，本机用docker来启动默认的私有镜像仓库。当默认的私有镜像仓库启动之后，会使用http接口方式对外提供服务。

此处我们使用`--network=host`参数，指定容器在启动时使用Host网络模型。

```shell
docker run -d  --network=host --name registry-1 registry 
```

2. 验证网络服务

当使用Host网络模型创建容器后，容器会和宿主机共享网络设置，这也就意味着，容器中启动网络服务，同样可以在宿主机中使用`127.0.0.1`的网络地址访问。关于Host网络模型的详细用法，在后面的实验中还会有讲解。

当仓库容器启动后，会在5000端口启动服务。我们可以在宿主机中使用netstat命令验证。

```shell
netstat -tunple | grep 5000
```

> - `-t`: 显示 TCP 协议相关的信息。
> - `-u`: 显示 UDP 协议相关的信息。
> - `-n`: 使用数字形式显示地址和端口，而不是尝试解析主机名和服务名称。
> - `-p`: 显示与进程相关的信息。
> - `-l`: 仅显示监听状态的端口。
> - `-e`: 显示详细的扩展信息。

![image-20230905122954351](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115706345292_473_image-20230905122954351.png)

3. 测试服务

接下来我们验证私人仓库的http服务接口是否可用，我们可以通过curl命令验证仓库的运行，常用的验证地址为`[私人仓库IP]:5000/v2/_catalog`。通过验证我们发现私人镜像仓库服务已经启动

```shell
curl 127.0.0.1:5000/v2/_catalog
```

![image-20230905123129251](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115712465251_580_image-20230905123129251.png)

### 向私有仓库中推送镜像

在前面的小节中，我们学习了如何启动本地的私人镜像仓库，在本小节中我们将学习如何将本地docker中的镜像推送到私有仓库中。

1. 为镜像设置仓库信息

默认的`docker push`命令会将容器推送到docker公共仓库，为了能将镜像推送到私人仓库，我们要使用docker tag命令为镜像设置需要推送的仓库信息。其命令的参数`为docker tag [本地镜像名] [私有仓库的URL][私有仓库的镜像名称]`。标记镜像之后，我们使用`docker images`命令查看会发现，为本地镜像设置tag之后，会在本地镜像列表中生成一个新的镜像。

```shell
docker tag ub/commit 127.0.0.1:5000/ub/commit
docker images
```

![image-20230905123255932](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115718659476_124_image-20230905123255932.png)

2. 向仓库推送镜像

通过docker tag命令生成新的镜像之后，我们就可以使用`docker push`将已经标记过的镜像，直接推送到私人仓库中。命令的参数为`docker push tag后的镜像名:镜像版本`。

```shell
docker push 127.0.0.1:5000/ub/commit:latest
```

![image-20230905123356587](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115722159957_760_image-20230905123356587.png)

3. 通过私有仓库API验证推送

当镜像上传到私人仓库之后。我们可以通过访问`curl [私人仓库IP]:5000/v2/_catalog`列出仓库中的镜像信息。同时还可以通过`curl [私人仓库IP]:5000/v2/[镜像名称]/list`来查看镜像的版本信息。

```shell
curl 127.0.0.1:5000/v2/_catalog
curl 127.0.0.1:5000/v2/ub/commit/tags/list
```

![image-20230905123429963](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115726481615_338_image-20230905123429963.png)

### 从私有仓库中拉取镜像

1. 删除本地镜像

为了验证从私有仓库下载镜像，我们先通过docker rmi命令删除本地的容器镜像。

```shell
docker rmi ub/commit 
docker rmi 127.0.0.1:5000/ub/commit
```

![image-20230905123531029](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115731763472_727_image-20230905123531029.png)

2. 从私有仓库中拉取镜像

当通过docker push将镜像推送到私人仓库之后。其他人就可以通过docker pull命令将其拉取到本地。拉取私有仓库镜像的命令格式为`docker pull [私有仓库的URL][私有仓库的镜像名称]`。

```shell
docker pull 127.0.0.1:5000/ub/commit
docker images
```

![image-20230905145350810](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115735113092_916_image-20230905145350810.png)

3. 查看本地镜像信息

对于已经拉取到本地的容器镜像，我们可以通过`docker inspcet`来查看镜像的仓库信息和`repo tag`信息。在使用`docker inspcet`命令时，我们可以使用`-f`参数进行信息过滤，具体的过滤语法我们会在后面的实验中详细讲解。

```shell
docker inspect -f \
"{\"RepoTags\":{{json .RepoTags}}, \"RepoDigests\":{{json .RepoDigests}}}" \
127.0.0.1:5000/ub/commit | jq
```

![image-20230905123713888](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115738615710_639_image-20230905123713888.png)

## 容器镜像的制作-build

### docker build 快速上手

前面的实验中我们学习了如何通过`docker commit`命令将一个编辑好的容器，生成一个新的镜像。但是这种方法生成的容器可以查看的只有文件层面的变更内容，容器的使用者往往会搞不清楚在容器制作过程中执行了什么命令，按什么顺序执行了这些命令或者操作。因此除了这种方法之外，Docker还提供了另一种`docker build`的方式来构建容器。

1. 制作Dockerfile文件

要使用docker build的方式制作容器，我们需要先制作`Dockerfile`文件。`Dockerfile`是纯文本文件，我们可以使用`vi`等纯文本文件编辑工具进行编写。接下来我们使用vi命令生成Dockerfile。注意使用vi编辑器时：

1. 需要先按i键进入编辑模式。
2. 编辑完成之后按esc退出编辑模式。
3. 然后按大写的ZZ保存并退出vim。

```shell
vi Dockerfile
```

然后将下面的内容复制到Dockerfile中：

```dockerfile
FROM ubuntu:latest

RUN apt-get update
```

2. 制作容器镜像

`Dockerfile`文件编写完毕后，我们就就可以根据该文件，使用`docker build`命令来制作容器镜像，该命令的格式为`docker build -t 容器镜像名 Dockerfile所在路径`。命令的第三个参数用于指定Dockerfile文件的位置，如果Dockerfile文件就在控制台的当前目录下，一般使用.来设置。

```
docker build -t ub/build .
docker images
```

![image-20230905150014762](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115742023909_762_image-20230905150014762.png)

![image-20230905150038126](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115747150545_234_image-20230905150038126.png)

3. Dockerfile命令列表

Dockerfile文件的格式于脚本文件，每一行是一条命令，每行的格式为`命令 参数`。Dockerfile主要支持的命令如下表，因篇幅的原因，本实验中我们无法具体演示每一条指令的用法，只会讲解一些重要的命令。

| 命令       | 功能                                                         |
| ---------- | ------------------------------------------------------------ |
| FROM       | 指定基础镜像，必须为第一个命令                               |
| LABEL      | 为镜像添加标签                                               |
| RUN        | 构建时执行的命令行指令                                       |
| ADD        | 将本地文件添加到容器中，如果为tar类型文件，则会自动解压，可以访问网络资源，类似wget（网络资源不会被解压） |
| COPY       | 将本地文件添加到容器中，不会解压，也不可以访问网络资源       |
| CMD        | 容器启动时执行的命令，只有最后一条可以生效，可以被docker run的启动命令覆盖。 |
| ENTRYPOINT | 容器启动时执行的入口，只有最后一条可以生效，一定会被执行，不可以被覆盖。 |
| EXPOSE     | 设置默认开放的网络端口（后面的实验会涉及到）                 |
| VOLUME     | 设置默认加载的VOLUME卷（后面的实验会涉及到）                 |
| ENV        | 设置环境变量。                                               |
| WORKDIR    | 设置默认的工作目录。                                         |
| USER       | 设置容器运行时的用户。                                       |
| ONBUILD    | 构建触发器，当此镜像被其他镜像用作基础镜像时，触发器会被执行。 |
| ARG        | 设置构建参数，可以通过docker build --build-arg将参数从外部传到到Dockerfile构建过程中。 |

### Dockerfile命令详解-1

在上一个小节中我们讲解了`Dockerfile`文件的格式，以及`docker build`命令的基本用法。在执行`docker build`时，docker会先根据`Dockerfile`文件生成并按顺序操作容器。然后再根据按顺序操作好的容器生成镜像。并且在新的容器镜像中保存了容器的操作顺序。接下来我们来介绍`Dockerfile`文件中的常用的`FROM`，`RUN`，`WORKDIR`，`ADD`四个命令。

1. 命令讲解和环境准备

这两个命令是最常见的Dockerfile命令。一般来讲我们不会从头创建一个镜像，而是会在已有镜像的基础上添加新的内容。这种情况下我们就需要使用`FROM`命令来指定基础镜像。

在指定基础镜像之后，我们可以使用`RUN`命令在基础镜像之上执行一些命令。需要注意的是这些命令都是在基础镜像而不是宿主机中运行，同时每一条命令需要使用一个`RUN`命令。

除了可以在容器中执行命令之外，我们还可以使用`ADD`命令从宿主机向容器中复制文件。使该命令复制文件时，默认只能复制Dockerfile文件所在目录中或者其子目录中的文件。

如果需要修改需要复制文件的目标路径，我们可以在Dockerfile中使用`WORKDIR`命令设置容器中的目标路径。

Docker中`ADD`命令除了可以从宿主机中复制文件，还可以从网络上下载文件到本地。使用该命令远程下载除了支持`HTTP/S`协议外，也支持`GIT`等协议。

ADD命令的另一个非常使用的功能是，当复制源文件的扩展名是`.tar.gz`格式时，该命令会将压缩包解压缩并复制到容器当中。

接下来我们先来进行本小节的实验环境准备。我们创建目录并保存需要上传到镜像中的文件。

``` shell
mkdir dir6-1
cd dir6-1
echo 本地文件 > info.txt
echo 压缩文件 > tar.txt
tar zcvf info.tar.gz tar.txt
```

2. 构建容器镜像

接下来我们使用vi命令在dir6-1目录下创建Dockerfile文件，并编辑为如下内容。

```shell
vi Dockerfile
```

```shell
FROM ubuntu:latest

WORKDIR data
RUN echo 容器中生成的文件 > img.txt
ADD info.txt info.txt
ADD info.tar.gz .

WORKDIR dir-robots
ADD https://www.aliyun.com/robots.txt robots.txt
```

然后使用`docker build`编译容器镜像

```shell
docker build -t img6-1 .
```

![image-20230905150654738](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115755964064_755_image-20230905150654738.png)

1. 验证容器镜像

接下来我们来验证编译好的容器镜像，我们通过`docker run`启动镜像，然后验证容器中的内容。我们发现容器在运行之后，默认的目录为`/data/dir-robots`这说明`WORKDIR`命令不但会改变镜像生成时的操作目录，也会影像到容器运行时的默认目录。 

接下来我们看到了从`www.aliyun.com/robots.txt`地址下载的同名文件。验证了ADD命令的网络下载功能。

```shell
docker run -itd --name container6-1 img6-1
docker exec container6-1 pwd
docker exec container6-1 cat robots.txt
```

![image-20230905150901490](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115800290600_894_image-20230905150901490.png)

我们继续验证其他目录的文件。这里我们使用了`docker exec container6-1 ls`和`docker exec container6-1 cat`命令。来查看文件列表和文件内容。会发现目录中的3个文件和内容符合期望

```shell
docker exec container6-1 ls ..
docker exec container6-1 cat ../img.txt
docker exec container6-1 cat ../info.txt
docker exec container6-1 cat ../tar.txt
```

![image-20230905150957871](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115806535609_183_image-20230905150957871.png)

### Dockerfile命令详解-2

接下来的这个小节我们再来看另外的三个Dockerfile命令，分别是`ENV`，`CMD`，`ENTRYPOINT`。

1. ENV和CMD命令讲解

Dockfile中的`ENV`命令的功能相对比较简单。通过该命令我们可以为容器镜像设置环境变量。通过环境变量我们可以将一些配置信息固化在镜像中。

接下来再来看`CMD`命令，这个命令用来设置容器的初始化命令。通过此命令我们可以让容器在启动时候执行一条命令，通过这条命令我们可以实现容器启动后，运行一个服务，或者在控制台输出一段文字等功能。此命令的格式为`CMD [”参数1“, ”参数2“...]`。

在使用`CMD`命令是我们需要注意的几点是：

a. 这条命令虽然可以设置很多次，但是只有最后一次会生效。

b. 当我们使用`docker run`命令启动容器时，我们可以`docker run `容器镜像名后面加入`参数1 参数2..`的形式 代替容器镜像中原有的`CMD`命令。

我们创建子目录，并使用`vi`修改`Dockerfile`为如下内容。并编辑为如下内容。

```shell
cd /
mkdir dir6-2
vi dir6-2/Dockerfile
```

```dockerfile
FROM ubuntu:latest

ENV IMG_STRING img6-2的环境变量
# CMD ["echo", "$IMG_STRING"]
CMD echo $IMG_STRING
```
**注意，在原教程中`CMD`指令编写有误，上面已经给出了更正**。下面进行简单的[解释](https://yeasy.gitbook.io/docker_practice/image/dockerfile/cmd)。

>在指令格式上，一般推荐使用 `exec` 格式，这类格式在解析时会被解析为 JSON 数组，因此一定要使用双引号 `"`，而不要使用单引号。
>
>如果使用 `shell` 格式的话，实际的命令会被包装为 `sh -c` 的参数的形式进行执行。比如：
>
>`CMD echo $IMG_STRING`
>
>`CMD ["sh","-c","echo $IMG_STRING"]`
>
>这就是为什么我们可以使用环境变量的原因，因为这些环境变量会被 shell 进行解析处理。

`Dockerfile`编写完毕后，使用`docker build`进行编译。

```shell
docker build -t img6-2 dir6-2
```

![image-20230905151434617](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115810025076_444_image-20230905151434617.png)

2. CMD和ENTRYPOINT命令讲解

除了`CMD`命令之外我们还可以使用`ENTRYPOINT`命令来实现类似的功能。该命令和`CMD`命令的格式和功能基本一致，其区别在于`docker run`命令只能使用`--entrypoint`参数替换镜像中的`ENTRYPOINT`设置。

在编写`Dockerfile`时，如果`ENTRYPOINT`和`CMD`命令同时出现的时候，容器启动时会将两个指令的参数串联起来，以`ENTRYPOINT参数1, ENTRYPOINT参数2..., CMD参数1, CMD参数2...`的形式执行启动命令。因此在具体使用时，我们一般在`ENTRYPOINT`中设置初始化命令，在`CMD`中设置初始化命令的参数。需要注意的是，`ENTRYPOINT`和`CMD`命令联合使用的时候，只能使用`[”参数1“, ”参数2“...]`格式的参数。

我们创建子目录，并使用`vi`修改`Dockerfile`为如下内容。并编辑为如下内容。

```shell
cd /
mkdir dir6-3
vi dir6-3/Dockerfile
```

```dockerfile
FROM ubuntu:latest

CMD ["-c", "echo CMD作为ENTRYPOINT的参数"]
ENTRYPOINT ["bash"]
```

Dockerfile编写完毕后，然后使用docker build编译容器镜像

```shell
docker build -t img6-3 dir6-3
```

![image-20230905152110713](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115815811340_658_image-20230905152110713.png)

3. 验证容器镜像

我们来验证编译好的`img6-2`容器镜像，我们通过`docker run`启动镜像，然后验证容器中的内容。

```shell
docker run img6-2
docker run img6-2 ls -ll
```

![image-20230905153928461](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115820729711_808_image-20230905153928461.png)

接下来我们来验证编译好的img6-3容器镜像，我们通过`docker run`启动镜像，然后验证容器中的内容。

```shell
docker run img6-3
docker run --entrypoint echo img6-3 "手动设置ENTRYPOINT和CMD"
docker run img6-3 -c "echo 手动设置CMD参数"
```

![image-20230905152521488](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115826074004_456_image-20230905152521488.png)

### 容器镜像的层次关系

在上一个实验中我们验证了通过`docker commit`命令生成镜像时，会在原有的镜像层之上添加一个新的层。接下来我们来看一下通过`docker build`方式生成的镜像的层次结构。

1. 查看镜像层次

我们也用`docker inspect`命令来查看一下镜像`img6-1`的层次信息，结果会发现`docker build`在基础镜像之上构建多个了新的镜像。

![image-20230905154527625](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115829877225_831_image-20230905154527625.png)

2. 查看镜像历史

通过`docker build`生成的镜像。除了`docker inspcet`之外，还可以通过`docker history`命令来查看通过`Dockerfile`定义的镜像的生成方式。我们可以看到`docker history`命令输出了镜像构建的过程信息，通过这一信息我们能比较清晰的看到镜像作者在制作镜像时的具体操作。

![image-20230905154617548](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115833217733_117_image-20230905154617548.png)

3. 镜像层次和镜像历史之间的关系

当我们执行上两个步骤的时候，细心的同学可能会发现，`docker history`中的每一个步骤都会生成一个中间状态的镜像，但是镜像的层数和镜像的步骤并不是严格的一一对应关系。这是因为docker会自动压缩一些没有实际产生数据修改的镜像，将多个临时镜像压缩成一层。比如`WORKDIR`命令所生成的中间状态。

同样我们可以比较`img6-2`和`img6-3`镜像。我们会发现虽然这两个镜像包含了很多的步骤，但是由于没有实际向镜像中写入文件，因此这两个镜像的存储层实际上和基础镜像ubuntu的存储层保持一致，这就意味着这两个镜像并没有在本地镜像仓库中额外消耗存储控件。

```shell
docker history img6-2
docker inspect -f "{{json .RootFS.Layers}}" img6-2 | jq
docker history img6-3
docker inspect -f "{{json .RootFS.Layers}}" img6-3 | jq
docker inspect -f "{{json .RootFS.Layers}}" ubuntu | jq
```

![image-20230905154829449](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%E5%AE%B9%E5%99%A8%E9%95%9C%E5%83%8F/20230906115838928038_319_image-20230905154829449.png)