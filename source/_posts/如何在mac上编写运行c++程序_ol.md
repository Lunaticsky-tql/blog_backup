---
title: 如何在mac上编写运行c++程序
categories: 小寄巧
date: 2022-9-30 10:00:00
tags:
  - C++
  - 环境配置
abbrlink: 51388
---
## 如何在mac上编写运行c++程序

有一部分同学买的电脑是mac，也有很多同学问怎么在mac上写c++代码。在这里解答一下。

### 方案一：使用Clion

#### 下载

[下载网址](https://www.jetbrains.com/clion/download/#section=mac)

如果你的苹果电脑是M1/M2芯片，那么请选择Apple Sillcon，否则选Intel

![image-20220927201026604](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211348592840_486_20220929230752211301_738_image-20220927201026604.png)

然后打开dmg文件将其拖到applcation文件夹即可。

#### 激活

Clion并不是一个免费的软件。但是作为学生，可以向其申请免费使用。点击[这里](https://www.jetbrains.com/zh-cn/community/education/#students)进入申请页面。正常情况下用你的学生邮箱就可以申请。申请之后会自动跳转到Clion，激活成功。

#### 创建第一个项目

点击“新建项目”，选择默认的c++ excutable

![image-20220927203943145](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211349779426_650_20220929230754550529_520_image-20220927203943145.png)

在location处可以改变项目路径和名称。

如果之前你没写过代码，可能会提示

![image-20220927204027175](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211350791432_948_20220929230756221193_195_image-20220927204027175.png)

安装即可。可能需要等待亿些时间。（类似于visual studio的工具链，可能会捆绑一些你可能其实用不到的东西）

然后安装完确认一下

<p align="center"><img alt="image-20220927211547461" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211351901314_661_20220929230757928357_218_image-20220927211547461.png" width="50%"/></p>

项目配置没有报错

![image-20220927211608280](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211353707000_855_20220929230759316655_492_image-20220927211608280.png)

然后选中CMakeLists，点击2处的刷新符号，重新构建

![image-20220927211726878](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211354844990_772_20220929230801131735_750_image-20220927211726878.png)

你应当发现此处的项目配置发生了改变。

![image-20220927211737021](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211356099715_652_20220929230802745480_349_image-20220927211737021.png)

此时点击运行，运行helloworld程序，成功

![image-20220927211838631](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211357120705_322_20220929230804052581_398_image-20220927211838631.png)

#### 简单了解Cmake

如果你想要在这个项目下运行多个cpp文件，你有必要了解一下cmake。

![image-20220927212015622](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211358771376_527_20220929230805695741_398_image-20220927212015622.png)

你会发现cmakelist变成了这样。

![image-20220927212042215](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211400319222_292_20220929230808172534_771_image-20220927212042215.png)

然后你顺理成章的点击了main函数旁边的运行

![image-20220927212255496](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211401588397_383_20220929230809367068_211_image-20220927212255496.png)

报错了！查看倒数第三行的报错信息，你会发现出现了重复（duplicate）的符号。

你想到课上使用vs时讲的，一个项目只能使用一个main函数。你把另外一个main改成了main2。学着这样修改。你发现确实可以正常运行。

<font color="Apricot">但有没有更优雅的解决方案呢？</font>

![image-20220927212700579](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211403630984_240_20220929230811319016_339_image-20220927212700579.png)

你注意到了cmake中最后一行是add_executable，刚刚发生了变化。从含义可以推测出一定是它控制了程序的执行。

让它们各自生成各自的程序一定可以！

![image-20220927212920160](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211404584803_168_20220929230812325537_398_image-20220927212920160.png)

点击Reload changes。你会发现项目构建出现了两个程序。

![image-20220927213032997](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211405764265_135_20220929230813838131_522_image-20220927213032997.png)

然后你高兴的发现点击哪个程序运行，你就可以运行哪一个cpp文件！

事实上，你点击cmake_build_debug，你会发现add_excutable第一个参数正是生成程序的名称！

![image-20220927213245467](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211407249755_411_20220929230815024257_502_image-20220927213245467.png)



在访达打开![image-20220927213323515](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211408513055_721_20220929230816481939_447_image-20220927213323515.png)



双击---helloworld出现了！它正是你刚刚编写的程序！

![image-20220927213343594](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211409899559_387_20220929230818933782_519_image-20220927213343594.png)

Cmake在大型项目管理中有着重要的用途，其本身也是十分复杂的。但在课程中只需要了解这些即可。

同时Clion在windows下也可以使用。

### 方案二：使用xcode

xcode是专为mac平台打造的全功能IDE（当然你要问我能不能写exe，只能说emmm）

xcode比较大，下载需要耐心等待。

#### 项目搭建

点击新建项目

![image-20220927213913046](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211411524873_100_20220929230821620085_933_image-20220927213913046.png)

选择macOS控制台应用

![image-20220927213932265](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211413302664_259_20220929230823254664_156_image-20220927213932265.png)

项目选项

![image-20220927214102217](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211414769754_153_20220929230824771816_210_image-20220927214102217.png)

注意组织名称写com，别的其实也行，但此处不作介绍。

语言选择c++。

选择项目位置后就可以愉快开发了！

![image-20220927214344955](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211416321696_447_20220929230826057443_745_image-20220927214344955.png)

控制台在屏幕下方。

![image-20220927214423776](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211417576173_303_20220929230827635084_833_image-20220927214423776.png)

#### 运行多个cpp

这个时候已经创建了一个cpp-project的项目，里面包含了一个main.cpp文件
如果这个时候想要在同一个工程里面创建第二个带main函数的c++文件并运行，就需要通过创建Target来实现

Project是一个工程项目，一个Project可以包含多个Target
Target之间互相没有关系，Target于Project的关系是：Target的Setting一部分继承自Project的Setting

![image-20220927214845054](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211418623132_866_20220929230828821606_386_image-20220927214845054.png)

新建target，同样选择commandline tool，填写一个的名称

![image-20220927215021382](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211420060785_695_20220929230831064192_247_image-20220927215021382.png)

在上方，想运行哪一个target，选择对应的即可。

<p align="center"><img alt="image-20220927215233319" height="50%" src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211421185173_773_20220929230832540286_682_image-20220927215233319.png" width="50%"/></p>

### 方案三：命令行方式

安装homebrew（如果已经下载过xcode可以跳过，不过既然如此为什么不用xcode呢？）

在你的终端输入这行指令：

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

如果下载很慢一般是网络问题，请自行解决。

安装完成后

```
brew install g++
```

任意位置新建cpp文件。

cpp文件可以用你喜欢的方式打开编辑。

按⌘（command）+ ⌥（option）+c复制当前文件夹路径

终端输入

```
cd 刚才的路径
```

然后

```
g++ yourprogram.cpp -o target
```

target 是生成的可执行文件的名字。

然后会发现生成了可执行文件，点击即可运行。

![image-20220927220347236](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E5%A6%82%E4%BD%95%E5%9C%A8mac%E4%B8%8A%E7%BC%96%E5%86%99%E8%BF%90%E8%A1%8Cc%2B%2B%E7%A8%8B%E5%BA%8F/20230828211422353231_803_20220929230833974800_101_image-20220927220347236.png)



