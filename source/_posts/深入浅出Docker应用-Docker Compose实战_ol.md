---
title: 深入浅出Docker应用-Docker Compose实战
categories: 笔记
tags:
  - Docker
abbrlink: 40623
date: 2023-09-06 14:16:11
---
# 深入浅出Docker应用-Docker Compose实战

## Docker Compose入门

### Docker Compose的安装

在之前的实验中，我们在创建和管理容器的时候，都是用的是docker的命令行，但是随着docker  run参数的增多，命令行的长度会越来越长。再加上复杂的服务往往由多个不同的容器共同组成，这样在创建一个完整的服务的时候，就会输入多条超长的命令。这时候我们就可以考虑使用docker compose。

docker compose 是一个用go语言开发的docker扩展程序，通过docker compose我可以使用配置文件的方式来同时管理多个容器。接下来我们先来学习docker compose的安装。

> 注：可参见[官网](https://docs.docker.com/compose/install/linux/#install-using-the-repository)

1. 插件安装（推荐）

docker  compose的安装有两种方式，分别为作为docker插件和单独应用。在centos或者redhat系统中，我们可以通过yum以插件的方式安装docker compose。这种方式在安装之后会将docker compose作为docker插件进行运行。我们可以通过`docker compose`命令进行调用。

```shell
yum install -y docker-compose-plugin
docker compose version
```

![image-20230906120028310](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906140854608011_980_image-20230906120028310.png)

2. 单独应用安装

略。不推荐使用。

### YML到JSON的转化工具

YML文件是一种适合人类阅读的配置文件格式，这种文件格式能够表示的数据结构和JSON格式配置文件类似。为了便于我们学习，我们先来制作一个YML和JSON的互相转换工具，以便于理解YML的格式。

1. 创建转换镜像

我们基于python中的yaml和json模块来实现解析功能。首先我们来创建Dockerfile，在镜像中首先通过`pip install`安装`pyyaml`模块。接下来再添加两条py格式的脚本`2json.py`和`2yml.py`。我们使用`vi`来编辑`Dockerfile`

```shell
vi Dockerfile
```

```dockerfile
FROM python:latest

RUN pip install pyyaml

RUN echo "import yaml, json, sys\n\
print(json.dumps(yaml.safe_load(sys.stdin.read()), indent=4))" > 2json.py

RUN echo "import yaml, json, sys\n\
print(yaml.safe_dump(json.load(sys.stdin), sort_keys=False))" > 2yml.py
```

Dockerfile编写好之后，我们生成容器镜像：

```shell
docker build -t yml/py . 
docker images
```

![image-20230906120814383](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906140858972702_400_image-20230906120814383.png)

2. YML转化为JSON

接下来我们使用刚才创建好的镜像，将yml文件转化为json格式。首先我们创建一个最简单的YML文件`demo.yml`。内容为`id: '10'`。

接下来在这里我们在执行docker run创建容器时使用`--rm`参数。该参数创建的容器在退出后会自动被删除，一般用于执行一次性任务的容器的创建。同时在命令中使用了`<` 重定向符号，将宿主机中的文件作为参数传递给容器中。

```shell
echo id: '10' > demo.yml
docker run -i --rm yml/py python 2json.py < demo.yml
```

![image-20230906120838553](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906140903420195_222_image-20230906120838553.png)

3. JSON转化为YML

然后我们再来尝试将JSON格式文件转化为YML格式。首先创建一个简单的JSON文件，然后使用下面命令执行容器中的`2yml.py`即可。

```shell
echo \{\"name\":\"aliyun\",\"age\":100} > demo.json
docker run -i --rm yml/py python 2yml.py < demo.json 
```

![image-20230906120923498](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906140906842553_579_image-20230906120923498.png)

### YML格式配置文件

在docker compose安装完毕后，我们需要编写YML格式的配置文件配合该工具进行使用。在本小节中我们先来学习YML格式配置文件的用法。

> 注：如果已经对YML比较熟悉，该节可以略过。

YML文件中包括了纯量，Key/Value对象，数组三种形式。但是和JSON使用`{}`表示层次关系不同的是，YML通过行前的空格来表明内容之间的层次关系。

1. YML的对象

接下来我们先来看YML中的第一种数据结构对象。对象是由多个Key/Value属性对对组成，属性对的格式为`key: value`。注意和JSON不同的是，一行中只包含一个属性对。

如果属性对的Value值为对象或者数组时，Value的内容需要新起一行，同时新起的一行要比上一行更多的空格（一般使用4个空格）缩进来表示。

接下来我们使用vi构建一个demo.yml文件来演示对象结构，并且转化成JSON结构和YML结构进行对比。

```shell
vi demo1.yml
```

```yaml
name: "aliyun"
attr: 
    age: 10
    addr: "HANGZHOU"
```

```shell
cat demo1.yml
docker run -i --rm yml/py python 2json.py < demo1.yml 
```

![image-20230906121133060](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141349874042_518_image-20230906121133060.png)

2. YML中的纯量

纯量是指对象的Value或者数组中不可分割的量，换句说话就是简单属性类型。YML的纯量包括：字符串，数字，布尔，日期，时间等类型。接下来我们编辑demo.yml来做演示。需要注意的是python默认的JSON编码模块不支持日期时间。因此我们使用`#` 注释日期时间属性对。

```shell
vi demo2.yml
```

```yaml
string: "aliyun"
number1: 10
number2: 10.01
boolean: true
# datatime: 2000-01-01 23:59:59   
```

```shell
cat demo2.yml
docker run -i --rm yml/py python 2json.py < demo2.yml
```

![image-20230906121351872](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141356359881_590_image-20230906121351872.png)

1. YML中的数组

YML中的数组不需要前后缀，只需要将数组中的元素前加入`-`即可，一行中只包含一个元素。

```shell
vi demo3.yml
```

```shell
scores: 
    - 100
    - 90.5
    - 78
```

```shell
cat demo3.yml
docker run -i --rm yml/py python 2json.py < demo3.yml
```

![image-20230906121553457](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141400821811_243_image-20230906121553457.png)

### Docker Compose快速上手

1. 编写配置文件

`docker compose`使用YML格式的配置文件代替`docker run`命令的各种参数，配置文件默认名称为`docker-compose.yml`。接下来我们使用`vi`构建该文件

```shell
vi docker-compose.yml
```

```yaml
version: "3.9"
services:
    busy:
        container_name: busy1
        image: "busybox:latest"
        stdin_open: true
        tty: true
```

2. 启动容器

配置文件编写完成之后，我们就可以使用`docker compose up`来启动配置文件中描述的容器。一般在执行docker compose up时会加入-d参数，其功能类似于docker run中的-d，表示容器在后台运行。

```shell
docker compose up -d
```

3. 验证容器启动

命令执行成功后，我们使用docker ps查看，会发现容器已经启动。相比较使用复杂的docker run命令，使用docker compose的方式管理容器，命令简单统一。

```shell
docker ps
```

![image-20230906122001303](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141406085546_790_image-20230906122001303.png)

## Docker Compose部署案例

### Docker Compose常用命令

在前面的实验中我们讲解了docker compose配置文件得常见用法，接下来我们再来学习一下docker compose的常用命令。

1. 环境准备

首先我们切换到命令行页面。进行试验环境准备。首先安装`docker compose`。

```shell
yum install -y docker-compose-plugin
vi docker-compose.yml
```

在安装成功后使用vi创建`docker-compose.yml`文件，在`docker-compose.yml`文件中加入下列内容。

```yml
version: "3.9"
services:
    web:
       container_name: web
       image: "httpd:latest"
       ports:
          - "5000:80"
          - "6000:8000"
    db:
       container_name: db
       image: "mysql"
       volumes:
          - "mysql-vol:/var/lib/mysql"
       environment:
          MYSQL_ROOT_PASSWORD: "[MYSQL密码]"
volumes:
    mysql-vol: {}
```

> 注意设置MYSQL_ROOT_PASSWORD的值，即[MYSQL密码]。

配置文件编写完毕后，我们通过docker compose来启动容器。

```shell
docker compose up -d
```

![image-20230906123052607](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141411787491_209_image-20230906123052607.png)

2. 类Docker命令

接下来我们来测试下面的3条docker compose命令，这3条命令的用法和原生docker命令类似，不同的是如果命令需要指定特定容器，我们需要在命令中使用service名来代替容器名。

```shell
docker compose exec db ls
```

```shell
docker compose cp docker-compose.yml db:/root/
docker compose exec db bin/bash -c "cat /root/docker-compose.yml"
```

![image-20230906123259414](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141417586371_108_image-20230906123259414.png)

3. 容器的启停删除

接下来我们来看通过docker compose进行容器服务组暂停/恢复，停止/重开，删除命令，这几条命令类似于docker compose up，只要使用默认配置文件docker-compose.yml，或者使用`-f`参数指定配置文件即可，不再需要指定容器名。

```shell
docker compose pause
docker compose unpause

docker compose stop
docker compose restart

docker compose down
```

![image-20230906123454662](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141423088385_967_image-20230906123454662.png)

### 部署WordPress论坛

之前的实验中我们介绍了Docker和Docker Compose的大部分常见用法。接下来我们来部署一个实际WordPress论坛作为Docker的综合案例。

启动wordpress论坛至少需要创建两个容器，一个mysql数据库容器，和一个运行wordpress的apache容器，除此之外如果安装了redis缓存插件，则还需部署redis容器。因此这次我们编写三个YML文件，通过Docker Compose来部署这三个容器。

1. 定义MySQL配置

首先我们先使用vi来编写`db.yml`作为MySQL的部署文件。在标准MySQL容器中，通过`EntryPoint`设置了启动命令，因此我们通过`command`设置启动参数。

除此之外标准的MySQL容器可以通过多种环境变量对服务进行配置，此处我们使用`MYSQL_DATABASE`环境变量指定默认数据库。

```shell
vi db.yml
```

```yaml
version: "3"
services:
  db:
    image: mysql:8.0
    command:
      - "--character-set-server=utf8mb4"
      - "--collation-server=utf8mb4_unicode_ci"
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: [MySQL root账号密码]
      MYSQL_DATABASE: wordpress
volumes:
  db_data:
```

> 注：注意设置MYSQL_ROOT_PASSWORD的值，即[MYSQL密码]。

2. 定义Redis配置

接下来我们使用`vi`来编写`cache.yml`作为Redis的部署文件。

```shell
vi cache.yml
```

```yaml
version: "3"
services:
  cache:
     depends_on:
       - db
     image: redis
     network_mode: "service:db"
     restart: always
```

3. 定义WordPress配置

最后我们使用`vi`来编写`app.yml`作为WordPress的部署文件。在WordPress配置中，需要依赖`db`和`cache`两个服务。使用`Container`网络模型，绑定``db服务的网卡。

同时我们希望将在宿主机的`8000`端口上发布应用的服务。由于WordPress服务共享了db服务的网卡，因此我们需要在`db`服务的网卡中进行端口绑定，此处我们可以使用属性值的多次定义功能。

在YML配置文件中，相同的属性值可以在不同的文件中进行定义，在docker compose加载的时候会将所有的属性值合并后统一处理，因此我们可以在`app.yml`中为db定义`ports`端口映射字段。

除此之外我们还可以在这里对db中的MYSQL_USER和MYSQL_PASSWORD两个环境变量的属性值进行覆盖。YML属性值允许覆盖，且以最后定义的为最终值。

在对db的环境变量覆盖时，我们可以使用`&wp_passwd`来将属性值定义为锚点。并且在wordpress中的`WORDPRESS_ROOT_PASSWORD`使用`*wp_passwd`来引用锚点作为属性值，这种写法表示这个属性值引用了锚点位置的属性值。也就是说在WordPress中数据库的root用户密码和db.yml中数据库的默认用户密码一致。这种写法可以避免因为拼写错误导致的数值不一致。

```shell
vi app.yml
```

```yaml
version: "3"
services:
  db:
    ports:
      - "8000:80"
    environment:
      MYSQL_ROOT_PASSWORD: &wp_passwd [MySQL wordpress账号密码]
  app:
    depends_on:
      - db
      - cache
    image: wordpress:6.0
    network_mode: "service:db"
    restart: always
    environment:
      WORDPRESS_DB_HOST: 127.0.0.1
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: *wp_passwd                    
```

> 注意设置MYSQL_ROOT_PASSWORD的值，即[MYSQL密码]。

```shell
version: "3"
services:
  db:
    ports:
      - "8000:80"
    environment:
      MYSQL_ROOT_PASSWORD: &wp_passwd Mysql#pwd
  app:
    depends_on:
      - db
      - cache
    image: wordpress:6.0
    network_mode: "service:db"
    restart: always
    environment:
      WORDPRESS_DB_HOST: 127.0.0.1
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: *wp_passwd   
```

![image-20230906124155038](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141429798156_187_image-20230906124155038.png)

4. 启动容器

配置文件编写完毕后我们就可以启动Project。这里需要注意的时，我们将三个服务写在了三个不同的文件中，当docker compose需要引用多个配置文件时，我们只需要在参数列表中添加多个`-f [配置文件名]`的方式即可。

```shell
docker compose -f db.yml -f cache.yml -f app.yml -p wp up -d
```

> 注：`-p wp`: 指定了项目名称（project name）`wp`

![image-20230906124528944](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141434316934_189_image-20230906124528944.png)

### 初始化WordPress论坛

> 注：如果不需要学习使用WordPress，下面两小节内容可以跳过。

接下来我们将在chromium浏览器对WordPress进行图形化配置。

1. 在浏览器中访问WordPress

在浏览器中输入`http://[ECS公网地址]:8000`，即可进入WordPress初始化界面。

![image-20230906124731571](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141438141138_443_image-20230906124731571.png)

2. 初始化WordPress

在初始化界面中我们首先选择wordpress的界面语言，并且按"继续"

继续配置wordpress的相关信息，输入论坛名称，用户名，密码等，在邮箱输入栏输入符合标准的邮箱格式即可。然后按"安装WordPress"

![image-20230906124928415](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141444671037_311_image-20230906124928415.png)

3. 登录WordPress

安装之后点击登录，即可进入登录界面，在登陆界面中输入上一个步骤填写的用户密码并点击登录。

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141450295097_479_image-20230906125010078.png" alt="image-20230906125010078" width="50%" height="50%" />

登录之后即可进入wordpress管理后台。后台界面主要由管理员使用。

![image-20230906125040580](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141455440508_502_image-20230906125040580.png)

接下来我们进入wordpress前台浏览界面。输入网址 `http://[ECS公网地址]:8000`。出现如下浏览界面即说明wordpress安装成功。

![image-20230906125109079](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141500006324_531_image-20230906125109079.png)

### 在WordPress中安装插件

1. 插件管理

![image-20230906125251276](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141507077816_757_image-20230906125251276.png)

2. 安装reids插件

![image-20230906125321678](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141511708977_268_image-20230906125321678.png)

然后点“启用”

![image-20230906125416859](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141517641595_463_image-20230906125416859.png)


切换至终端，执行如下命令验证插件生效。

```shell
docker exec -it wp-cache-1 redis-cli

keys *
```

![image-20230906125527715](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141522028216_638_image-20230906125527715.png)

## YML配置文件的常用属性

### YML配置文件简介

在上一个小节中我们学习了Docker compose 的基本用法，相比较使用docker run命令行和参数启动容器，使用yml配置文件大步幅简化命令输入。在本实验中我们再来看一下docker_compose.yml文件的常见配置信息

1. 环境准备

为了接下来的实验，首先我们安装docker compose插件。在安装成功后使用vi创建`docker-compose.yml`文件，在`docker-compose.yml`文件中加入下列内容。

```shell
yum install -y docker-compose-plugin
vi docker-compose.yml
```

```yaml
version: "3.9"
services:
    web:
       container_name: web
       image: "httpd:latest"
       ports:
          - "5000:80"
          - "6000:8000"
    db:
       container_name: db
       image: "mysql"
       volumes:
          - "mysql-vol:/var/lib/mysql"
       environment:
          MYSQL_ROOT_PASSWORD: "[MYSQL密码]"
volumes:
    mysql-vol: {}
```

```shell
docker compose up -d
```

2. 配置文件基本讲解

在通过`docker compose up`启动容器之后，我们来看一下`docker_comose.yml`的配置文件结构。在docker_compose中，一个`project`可以包含多个配置文件中的内容，如果没有设置所有的资源都会创建在root这个project中，在project中serviecs字段中的每一个key表示一个`serviec`，每个service下又可以由一个或多个`container`，在service中的基本配置选项如下表。

| container_name | 等同于--name         |
| -------------- | -------------------- |
| image          | 容器镜像             |
| volumes        | 等价于-v，类型为数组 |
| ports          | 等价于-p，类型为数组 |
| environment    | 等价于-e，类型为对象 |

需要注意的是，默认情况下docker compose会为每个project自动创建一个network，接下来创建的所有的容器都会连接到这个network，我们来验证容器的配置。

```shell
docker network ls
docker port web
docker inspect -f "{{json .Mounts}}"  db | jq
```

![image-20230906132436722](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141525957802_776_image-20230906132436722.png)

3. 容器状态查询

我们还可以通过docker compose命令对容器服务的状态查询。和使用docker原生命令相比，docker compose只会对配置文件中包含的容器生效。并不需要具体指定容器名，降低了操作复杂性。

这里我们演示`docker compose ps`，`docker compose top`，`docker compose images`三个命令：

```shell
docker compose ps
docker compose top
docker compose images
```

![image-20230906133510118](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141532886509_703_image-20230906133510118.png)

4. 容器的删除

当我们需要结束容器的使用，我们可以使用`docker compose down`来结束和删除配置文件中的容器。

需要注意的时，该命令会停止并且销毁配置文件中描述的容器。同时容器停止后相应的网络等组件都会被销毁，类似于使用`docker rm -f`加`docker network rm`

```shell
docker compose down
```

![image-20230906133558164](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141538989320_659_image-20230906133558164.png)

###  YML的常用配置项目

在上一个小节中我们演示了docker compose的主要配置和常用命令，接下来我们再来看一下docker  compose配置文件中的其他配置项目。yml中的一部分配置选项可以和`docker  run`中的命令行对应，这些属性主要包括在下表中，在本小节中我们来实验这些属性。

| command     | 容器的启动命令             |
| ----------- | -------------------------- |
| stdin_open  | 设置为true等价于-i参数     |
| tty         | 设置为true等价于-t参数     |
| networ_mode | 网络模式                   |
| networks    | 容器连接的网络，类型为数组 |

1. 编写配置文件。

在docker compose中默认使用docker-compose.yml配置文件， 如果我们想使用不同名称的配置文件，可以在docker compose后面添加`-f`参数指定yml文件。我们使用vi创建一个`web.yml`文件以演示配置选项。

创建之后，我们启动project，在启动时我们可以通过`-p`参数指定资源所在的Project，以避免资源橙色图，这里我们指定project为web。

```shell
vi web.yml
```

```yaml
version: "3.9"
services:
    busybox:
        container_name: sh
        image: "busybox:latest"
        tty: true
        stdin_open: true
        networks:
            - "custom"
    python:
        container_name: web
        image: "python"
        network_mode: "host"
        command: "python -m http.server 8000"
networks:
    custom:
        name: "custom"
```

```shell
docker compose -f web.yml -p web up -d
```

![image-20230906134113946](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141545186341_141_image-20230906134113946.png)

2. 创建Project并验证

web.yml创建成功后，我们来创建Project，需要注意的是在创建Proejct时，`-f[配置文件名]`参数需要放在up命令之前。在Proejct 创建之后我们来验证自定网络的创建和容器参数的指定。

```shell
docker inspect -f '{"Tty":{{.Config.Tty}},"OpenStdin":{{.Config.OpenStdin}}}' sh | jq
docker inspect -f "{{json .NetworkSettings.Networks}}" sh | jq
```

![image-20230906134131894](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141548725400_786_image-20230906134131894.png)

3. 查看配置信息

当Project创建成功后使用`docker compose convert`命令，可以显示service中某个容器的的配置信息。我们可以看到显示的配置信息中，包括yml中指定的选项，也包括yml中没有指定的默认选项。

```shell
docker compose -f web.yml -p web convert busybox
docker compose -f web.yml -p web convert python
```

![image-20230906134142775](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141552348830_501_image-20230906134142775.png)

### YML的其他配置项目

在本小节中我们再来看三个并不是和docker run 命令参数有对应关系的docker compose属性值的用法。

| deploy.replicas | 可以选择Service中容器的部署个数。 |
| --------------- | --------------------------------- |
| depends_on      | 可以选择Service启动的先后顺序     |
| restart         | 设置Service的重启策略             |

1. 容器个数

首先我们来看`deploy.replicas`，之前我们提到过在`docker  compose`中的层次结构为，`project->service->container`，这里面的service指的是不同的容器配置，而container是指可以为相同的配置建立多个容器实例。配置容器实例个数的属性就是`deploy.replicas`。我们使用`vi`创建一个`replicas.yml`文件以演示配置选项。

在编写配置文件时，我们要注意由于我们需要在相同的配置下创建多个容器，因此我们不能在配置中用`container_name`属性为容器指定一个固定的名字。因此我们需要删除此字段，由启动自动分配名字。

```shell
vi replicas.yml
```

```yaml
version: "3.9"
services:
    busybox:
        image: "busybox:latest"
        tty: true
        stdin_open: true
        deploy:
            replicas: 3
```

```shell
docker compose -f replicas.yml -p replicas up -d
docker compose -f replicas.yml -p replicas ps
```

![image-20230906134411157](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141557051770_456_image-20230906134411157.png)

2. 启动顺序

在容器启动时，如果不同service在启动时有互相依赖关系，比如redis缓存要先于web服务启动，这种情况下就可以使用`depends_on`来管理service的启动顺序。我们使用vi创建一个`dependson.yml`文件以演示启动顺序选项。会发现servie严格按照先后顺序进行了启动

```shell
vi dependson.yml
```

```yaml
version: "3.9"
services:
    busybox-before:
        image: "busybox"
        tty: true
        stdin_open: true
    busybox-after:
        image: "busybox"
        tty: true
        stdin_open: true
        depends_on:
            - "busybox-before"
            - "busybox"
    busybox:
        image: "busybox"
        tty: true
        stdin_open: true
        depends_on:
            - "busybox-before"
```

```shell
docker compose -f dependson.yml -p dependson up -d
```

![image-20230906134537758](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141600332437_952_image-20230906134537758.png)

3. 重启策略

在生产环境中，容器中服务难免会因为各种问题出现异常，错误，从而导致服务进程崩溃。一旦这种情况发生就会导致局部服务不可用，如果是关键服务出现问题，甚至会影响整个应用得稳定性。

因此在生产环境中，我们一般会配置使用`restart`属性。该属性可以根据值得不同设定容器得自动重启策略。常用得属性值包括：`no`不自动重启，`always`总是自动重启，`on-failure`错误退出时重启。

接下来我们启动一个busybox容器，在容器启动时执行`sleep 10`。这个命令表示命令行会在10秒后退出，以模拟容器服务出现错误。在project启动后等待超过10秒，然后再查看状态，会发现由于设置了always策略，容器会在退出后重新启动。

```shell
vi restart.yml
```

```yaml
version: "3.9"
services:
    busybox-auto:
        container_name: busybox-auto
        image: "busybox"
        command: sleep 10
        restart: "always"
```

```shell
docker compose -f restart.yml -p restart up -d
[等待超过10秒]
docker compose -f restart.yml -p restart ps
```

![image-20230906134857664](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141603517229_285_image-20230906134857664.png)

> 注：蓝框中已启动9秒而非50+秒，说明中间重启过

### Flask的build联动案例

在实际开发应用得过程中，我们往往不会直接使用原生容器进行部署，而是需要使用开发者自行build的镜像。这种情况下开发者部署应用时，需要先执行`docker build`构建镜像，然后再执行`docker compose up`来运行镜像。

除了这种方式之外，我们还可以在YML配置文件中使用`build`属性值，这种情况下`docker compose`在创建project之前会先执行`docker build`生成镜像，然后再创建容器。简化了开发者的部署工作。

本小节中我们就来通过一个Python语言的`Flask`框架来演示在开发过程中如何联动镜像的打包和部署。

1. 环境准备

首先我们需要构建三个文件，分别是应用开发的源代码文件`main.py`，制作镜像的打包文件`Dockfile`，和容器联动的配置文件`build.yml`。首先我们来构建`main.py`和`Dockfile`。

在`main.py`中我们通过Flask框架实现了一个简单的Http服务器。具体代码原理可以参考源码中的注释，在此不做过多讲解。

```shell
mkdir app
vi app/main.py
```

```python
# 导入Flask类
from flask import Flask 

# 创建app对象
app = Flask(__name__)
 
# 将对路径"/"得访问路由到函数index上
@app.route('/')
def index():
    return '网页首页\n'

# 将对路径"/Host"得访问路由到函数index上
@app.route('/host')
def host():
    return '访问Host路径\n'

# 启动app对象中得服务，并指导服务端口为8000
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
```

接下来我们来编写`Dockerfile`，这里我们主要做几件事：首先通过`pip`安装`Flask`框架，然后将`main.py`源码文件复制到`/app/`目录下，接下来设置`/app`为工作目录，最后使用CMD设置容器的启动命令。

```shell
vi app/Dockerfile
```

```dockerfile
FROM python

RUN pip install Flask

ADD main.py /app/main.py
WORKDIR /app/
CMD python main.py
```

2. 编写配置文件

源代码文件和打包文件编辑完毕后，我们继续通过`vi`来编写配置文件`build.yml`。在配置文件中，我们使用`build`属性值代替`image`。如果在执行`docker build`时使用的是默认的打包配置文件，那么将`build`的属性值设置为`Dockerfile`文件所在目录即可。

如果需要指定打包文件名，则需要将`build`的属性值设置为对象。对象中包含`context`和`dockerfile`两个属性值，分别表示配置文件所在路径和配置文件名。

```shell
vi build.yml
```

```yaml
version: "3.9"
services:
    app:
        build: app/
#       build: 
#           context: app/
#           dockerfile: Dockerfile
        ports: 
            - "8080:8000"
        restart: "always"
```

3. 验证部署结果

文件编写完成后我们即可进行编译打包和project部署的联动，proejct部署成功后。我们通过`docker compose ps`命令进行查看，发现容器使用了自动打包的镜像`build-app`。

最后我们使用`curl`访问8080端口映射，验证服务部署成功。

```shell
docker compose -f build.yml -p build up -d
docker compose -f build.yml -p build ps
curl 127.0.0.1:8080
curl 127.0.0.1:8080/host
```

![image-20230906135657253](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BADocker%E5%BA%94%E7%94%A8-Docker%20Compose%E5%AE%9E%E6%88%98/20230906141609065118_414_image-20230906135657253.png)

