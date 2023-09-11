---
title: 设计模式之美-重新认识面向对象
categories: 笔记
tags:
  - 设计模式
abbrlink: 43433
date: 2023-09-11 16:28:09
---
# 设计模式之美-重新认识面向对象

## 大纲

写在前面：这是王争的《设计模式之美》阅读笔记，原文发表在[极客时间](https://time.geekbang.org/column/intro/100039001)，也有纸质书版本。阅读完整内容可购买正版支持。

设计模式或许显得有些“屠龙技”，但有了这些思想，能让我们站在更高的视角去看软件开发，而不是迷失在框架的细节里。

这一部分主要对“设计原则与思想：面向对象”进行总结。

![image-20230911102731242](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E7%BE%8E-%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1/20230911162803575003_338_image-20230911102731242.png)

## 面向对象

### 面向对象四大特性

面向对象的四大特性：封装、抽象、继承、多态

尽管很呆，但小公司爱问

**封装：访问控制**

保护数据不被随意修改，提高代码的可维护性；另一方面是仅暴露有限的必要接口，提高类的易用性。

**抽象：面向接口**

让使用者只需要关心方法提供了哪些功能，不需要知道这些功能是如何实现的。以便有效地过滤掉不必要关注的信息，处理复杂的系统。

**继承和多态：代码复用**

只有当符合“is a"的模型，且更具体的，对父类的任何操作都应当对子类合法，才应当用继承。接口类和”鸭子类型“可以在保留多态的拓展性的同时避免继承造成的强耦合。关于这一部分后面会详细讨论。

> 参见Effective C++ 条款32：确定你的public继承塑模出 is-a 关系。
>
> 如果某个函数可施行于某class身上，一定也可施行于其derived classes身上。

### 面向对象vs面向过程

在实际的面向对象编程中也很难逃出面向过程的编程范式。比如：

**滥用 getter、setter 方法会破坏类的封装。**

用IDE自动生成或者Lombok一把梭确实很省时间，但是有时候也违背了使用getter，setter的初衷，比如无意中引入不应当出现的setter。

**滥用全局变量和全局方法会影响代码的可维护性，增加代码的编译时间。**

原因是把全局变量集中在一起(比如创建一个Constant类)，一旦由于业务需求对其进行增加或修改，依赖它的代码都会受到影响。

对于全局或静态方法，如果极端一点就像C语言中的宏，

**如何避免**

在设计实现类的时候，除非真的需要，否则尽量不要给属性定义 setter 方法。除此之外，尽管 getter 方法相对 setter 方法要安全些，但是如果返回的是集合容器，那也要防范集合内部数据被修改的风险。

设计Constants 类、Utils  类时，我们尽量能做到职责单一，定义一些细化的小类，比如  RedisConstants、FileUtils，而不是定义一个大而全的 Constants 类、Utils  类。除此之外，如果能将这些类中的属性和方法，划分归并到其他业务类中，那是最好不过的了，能极大地提高类的内聚性和代码的可复用性。

### 接口&抽象类

抽象类是对成员变量和方法的抽象，是一种 is-a 关系，是为了解决代码复用问题。接口仅仅是对方法的抽象，是一种 has-a 关系，表示具有某一组行为特性，是为了解决解耦问题，隔离接口和具体的实现，提高代码的扩展性。

> 在C++中，一个所有方法都是纯虚函数，没有数据成员的抽象类显然可以看做是接口。
>
> <details>
> <summary>对C++虚函数和接口实现关系的详细讨论</summary>
>
> > 参见Effective C++ 条款34：区分接口继承和实现继承。
> >
> > 接口继承和实现继承不一样。在public继承下，派生类总是继承基类的接口。
> >
> > 声明一个纯虚函数的目的，是为了让派生类只继承函数接口。
> >
> > > 如一个Shape类的Draw()方法。
> >
> >  声明简朴的非纯虚函数的目的，是让派生类继承该函数的接口和缺省实现。
> >
> > > 如一个Person类的Sleep()方法。
> >
> >  声明非虚函数的目的，是为了令派生类继承函数的接口及一份强制性实现。
> >
> > > 如一个继承体系中的getObjectID()方法。
> >
> > 同时，纯虚函数是可以提供具体实现的，并且用于替代简朴的非纯虚函数，提供更平常更安全的缺省实现。
> >
> > 用非纯虚函数提供缺省的默认实现：
> >
> > ```cpp
> > class Airplane {
> > public:
> >     virtual void Fly() {
> >         // 缺省实现
> >     }
> > };
> > 
> > class Model : public Airplane { ... };
> > ```
> >
> > 这是最简朴的做法，但是这样做会带来的问题是，由于不强制对虚函数的覆写，在定义新的派生类时可能会忘记进行覆写，导致错误地使用了缺省实现。
> >
> > 使用纯虚函数并提供默认实现：
> >
> > ```C++
> > class Airplane {
> > public:
> >     virtual void Fly() = 0;
> > };
> > 
> > void Airplane::Fly() {
> >         // 缺省实现
> > }
> > 
> > class Model : public Airplane { 
> > public:
> >     virtual void Fly() override {
> >         Airplane::Fly();
> >     }
> > };
> > ```
>
> </details>

### 基于接口而非实现编程

抽象是好的。

> 越抽象、越顶层、越脱离具体某一实现的设计，越能提高代码的灵活性，越能应对未来的需求变化。好的代码设计，不仅能应对当下的需求，而且在将来需求发生变化的时候，仍然能够在不破坏原有代码设计的情况下灵活应对。

我们都知道抽象的好，但如何变抽象呢？

1. 先想好要做什么，再去想怎么做。这也是抽象人的思考方式。

   > 在定义接口的时候，希望通过实现类来反推接口的定义。先把实现类写好，然后看实现类中有哪些方法，照抄到接口定义中。如果按照这种思考方式，就有可能导致接口定义不够抽象，依赖具体的实现。

2. 定义接口时，命名要足够通用，特别不能包含跟具体实现相关的字眼；另一方面，与特定实现有关的方法不要定义在接口中。

   - 函数的命名不能暴露任何实现细节
   - 封装具体的实现细节
   - 为实现类定义抽象的接口

   > 这一点更加接近具体的实践。原文中举的例子我也踩过类似的坑，所以也把它放在这里：
   >
   > <details>
   > <summary>具体案例</summary>
   >
   > 假设我们的系统中有很多涉及图片处理和存储的业务逻辑。图片经过处理之后被上传到阿里云上。为了代码复用，我们封装了图片存储相关的代码逻辑，提供了一个统一的 AliyunImageStore 类，供整个系统来使用。具体的代码实现如下所示：
   >
   > ```java
   > public class AliyunImageStore {
   >   //...省略属性、构造函数等...
   >   public void createBucketIfNotExisting(String bucketName) {
   >     // ...创建bucket代码逻辑...
   >     // ...失败会抛出异常..
   >   }
   >   public String generateAccessToken() {
   >     // ...根据accesskey/secrectkey等生成access token
   >   }
   >   public String uploadToAliyun(Image image, String bucketName, String accessToken) {
   >     //...上传图片到阿里云...
   >     //...返回图片存储在阿里云上的地址(url）...
   >   }
   >   public Image downloadFromAliyun(String url, String accessToken) {
   >     //...从阿里云下载图片...
   >   }
   > }
   > // AliyunImageStore类的使用举例
   > public class ImageProcessingJob {
   >   private static final String BUCKET_NAME = "ai_images_bucket";
   >   //...省略其他无关代码...
   >   public void process() {
   >     Image image = ...; //处理图片，并封装为Image对象
   >     AliyunImageStore imageStore = new AliyunImageStore(/*省略参数*/);
   >     imageStore.createBucketIfNotExisting(BUCKET_NAME);
   >     String accessToken = imageStore.generateAccessToken();
   >     imagestore.uploadToAliyun(image, BUCKET_NAME, accessToken);
   >   }
   > }
   > ```
   >
   > 代码实现非常简单，类中的几个方法定义得都很干净，用起来也很清晰，乍看起来没有太大问题，完全能满足我们将图片存储在阿里云的业务需求。不过，软件开发中唯一不变的就是变化。过了一段时间后，我们自建了私有云，不再将图片存储到阿里云了，而是将图片存储到自建私有云上。
   >
   > 首先，AliyunImageStore  类中有些函数命名暴露了实现细节，比如，uploadToAliyun() 和  downloadFromAliyun()。如果开发这个功能的同事没有接口意识、抽象思维，那这种暴露实现细节的命名方式就不足为奇了，毕竟最初我们只考虑将图片存储在阿里云上。我们要修改项目中所有使用到这两个方法的代码，代码修改量可能就会很大。
   >
   > 其次，将图片存储到阿里云的流程，跟存储到私有云的流程，可能并不是完全一致的。比如，阿里云的图片上传和下载的过程中，需要生产 access token，而私有云不需要 access token。代码中用到了generateAccessToken() 方法，如果要改为私有云的上传下载流程，这些代码都需要做调整。
   >
   > 我们可以这样重构：
   >
   > ```java
   > public interface ImageStore {
   >   String upload(Image image, String bucketName);
   >   Image download(String url);
   > }
   > public class AliyunImageStore implements ImageStore {
   >   //...省略属性、构造函数等...
   >   public String upload(Image image, String bucketName) {
   >     createBucketIfNotExisting(bucketName);
   >     String accessToken = generateAccessToken();
   >     //...上传图片到阿里云...
   >     //...返回图片在阿里云上的地址(url)...
   >   }
   >   public Image download(String url) {
   >     String accessToken = generateAccessToken();
   >     //...从阿里云下载图片...
   >   }
   >   private void createBucketIfNotExisting(String bucketName) {
   >     // ...创建bucket...
   >     // ...失败会抛出异常..
   >   }
   >   private String generateAccessToken() {
   >     // ...根据accesskey/secrectkey等生成access token
   >   }
   > }
   > // 上传下载流程改变：私有云不需要支持access token
   > public class PrivateImageStore implements ImageStore  {
   >   public String upload(Image image, String bucketName) {
   >     createBucketIfNotExisting(bucketName);
   >     //...上传图片到私有云...
   >     //...返回图片的url...
   >   }
   >   public Image download(String url) {
   >     //...从私有云下载图片...
   >   }
   >   private void createBucketIfNotExisting(String bucketName) {
   >     // ...创建bucket...
   >     // ...失败会抛出异常..
   >   }
   > }
   > // ImageStore的使用举例
   > public class ImageProcessingJob {
   >   private static final String BUCKET_NAME = "ai_images_bucket";
   >   //...省略其他无关代码...
   >   public void process() {
   >     Image image = ...;//处理图片，并封装为Image对象
   >     ImageStore imageStore = new PrivateImageStore(...);
   >     imagestore.upload(image, BUCKET_NAME);
   >   }
   > }
   > ```
   >
   > **但凡抱着写脚本的心态写代码，就很容易出现这样的问题**，我给我自己的博客文章写了一个上传图文到Github的GUI脚本，就出现了这样的问题：`upload_to_github`方法写死，`hexo`命令写死，甚至上传函数中还硬编码了对GUI的控制。。。中间有一次希望整合为命令行批量上传，就费一些功夫。比如以后想把博客迁移到Hugo，或者更换图床等等，就又需要改动很多代码。
   >
   > </details>
   >
   > 如果在我们的业务场景中，某个功能只有一种实现方式，未来也不可能被其他实现方式替换，那我们就没有必要为其设计接口。但大多数情况下还是需要预见变化的。因此学习优秀的框架是如何组织接口的，是非常有益的实践。

### 多用组合少用继承

关于继承，我们不得不提经典的”是不是所有的鸟都会飞“的案例。

<details>
<summary>关于这个"鸟事"的详细讲解</summary>

假如我们我们将“鸟类”这样一个抽象的事物概念，定义为一个抽象类 AbstractBird。所有更细分的鸟，比如麻雀、鸽子、乌鸦等，都继承这个抽象类。我们知道，大部分鸟都会飞，那我们可不可以在 AbstractBird 抽象类中，定义一个 fly() 方法呢？答案是否定的。

当然，你可能会说，我在鸵鸟这个子类中**重写（override）fly() 方法**，让它抛出 UnSupportedMethodException 异常不就可以了吗？

这种设计思路虽然可以解决问题，但不够优美。

因为除了鸵鸟之外，不会飞的鸟还有很多，比如企鹅。对于这些不会飞的鸟来说，我们都需要重写 fly() 方法，抛出异常。这样的设计，一方面，徒增了编码的工作量；另一方面，也违背了我们之后要讲的最小知识原则（Least  Knowledge Principle，也叫最少知识原则或者迪米特法则），暴露不该暴露的接口给外部，增加了类使用过程中被误用的概率。同时，这种行为将错误拖延到了运行期，我们知道越早发现错误，越容易解决问题。

那我们再通过 AbstractBird 类**派生出两个更加细分的抽象类**：会飞的鸟类 AbstractFlyableBird 和不会飞的鸟类 AbstractUnFlyableBird？

这确实更忠实的反映了原本的意思，但是更复杂的情况，比如会不会叫，会不会下蛋等，阁下又该如何应对？那估计就要组合爆炸了。类的继承层次会越来越深、继承关系会越来越复杂。

![image-20230910223118620](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%E4%B9%8B%E7%BE%8E-%E9%87%8D%E6%96%B0%E8%AE%A4%E8%AF%86%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1/20230911162807231208_166_image-20230910223118620.png)

我们可以利用**组合（composition）、接口(interface)、委托（delegation）**三个技术手段，一块儿来解决刚刚继承存在的问题。

针对“会飞”这样一个行为特性，我们可以定义一个 Flyable 接口，只让会飞的鸟去实现这个接口。对于会叫、会下蛋这些行为特性，我们可以类似地定义 Tweetable 接口、EggLayable 接口。

```java
public interface Flyable {
  void fly();
}
public interface Tweetable {
  void tweet();
}
public interface EggLayable {
  void layEgg();
}
public class Ostrich implements Tweetable, EggLayable {//鸵鸟
  //... 省略其他属性和方法...
  @Override
  public void tweet() { //... }
  @Override
  public void layEgg() { //... }
}
public class Sparrow impelents Flyable, Tweetable, EggLayable {//麻雀
  //... 省略其他属性和方法...
  @Override
  public void fly() { //... }
  @Override
  public void tweet() { //... }
  @Override
  public void layEgg() { //... }
}
```

接口只声明方法，不定义实现。也就是说，每个会下蛋的鸟都要实现一遍 layEgg() 方法，并且实现逻辑是一样的，这就会导致代码重复的问题。那这个问题又该如何解决呢？

我们可以针对三个接口再定义三个实现类，它们分别是：实现了 fly() 方法的 FlyAbility 类、实现了 tweet() 方法的 TweetAbility 类、实现了 layEgg() 方法的  EggLayAbility 类。然后，通过组合和委托技术来消除代码重复。具体的代码实现如下所示：

```java
public interface Flyable {
  void fly()；
}
public class FlyAbility implements Flyable {
  @Override
  public void fly() { //... }
}
//省略Tweetable/TweetAbility/EggLayable/EggLayAbility

public class Ostrich implements Tweetable, EggLayable {//鸵鸟
  private TweetAbility tweetAbility = new TweetAbility(); //组合
  private EggLayAbility eggLayAbility = new EggLayAbility(); //组合
  //... 省略其他属性和方法...
  @Override
  public void tweet() {
    tweetAbility.tweet(); // 委托
  }
  @Override
  public void layEgg() {
    eggLayAbility.layEgg(); // 委托
  }
}
```

> 来自 Effective C++ 条款32：确定你的public继承塑模出is-a关系
>
> 即便如此，此刻我们仍然未能完全处理好这些鸟事，因为对某些软件系统而言， 可能不需要区分会飞的鸟和不会飞的鸟。如果你的程序忙着处理鸟喙和鸟翅，完全不在乎飞行，原先的“双classes继承体系”或许就相当令人满足了。这反映出一个事实，世界上并不存在一个“适用于所有软件”的完美设计。所谓最佳设计，取于系统希望做什么事，包括现在与未来。

</details>

继承主要有三个作用：表示 is-a  关系，支持多态特性，代码复用。而这三个作用都可以通过其他技术手段来达成。

比如 is-a 关系，我们可以通过组合和接口的 has-a  关系来替代；比如鸵鸟是(is-a)鸟，可以理解成鸵鸟有(has-a)鸟的特点，这个”特点“或者说像鸟的行为可以抽象为方法。

多态特性我们可以利用接口来实现，这一点Go或python的鸭子类型体现更加明显：只要某个类实现了某个接口的所有方法，就可以看做是某个接口的实现，调用时只管调用接口方法，而不需要区分调用的是什么。这和多态所诉求的"动态联编"(通过基类使用子类，运行时调用子类实现)是吻合的。

代码复用我们可以通过组合和委托来实现。上面案例中的代码已经有所体现。

所以，从理论上讲，通过组合、接口、委托三个技术手段，我们完全可以替换掉继承，在项目中不用或者少用继承关系，特别是一些复杂的继承关系。

### 贫血模型和充血模型

作者将将**数据与操作分离**的模型，如传统的**MVC**，称作“贫血模型”，而将**数据和对应的业务逻辑被封装到同一个类**中的模型，**如领域驱动设计**（Domain Driven Design，简称 DDD），称作“充血模型”。

抛开华丽的概念不谈，具体到实践，最常见的前后端分离项目，即后端负责暴露接口给前端调用。我们一般就将后端项目分为 Repository 层、Service 层、Controller 层。其中，Repository 层负责数据访问，Service  层负责业务逻辑，Controller 层负责暴露接口。如果熟悉Java Web开发，可能会非常耳熟能详，比如对一个用户类，UserEntity 和 UserRepository 组成了数据访问层，UserBo 和 UserService 组成了业务逻辑层，UserVo 和 UserController 属于接口层。

作者的主要观点，传统MVC中，BO 通常只包含数据，不包含具体的业务逻辑。这样的后果就是我们可能会不觉的将过多的业务逻辑放到Service层，甚至更极端的，可能会变成“面向SQL编程”。

将过多的业务逻辑放到Service层，业务一多了，就会变得臃肿而且难以维护，特别是多人开发时间紧迫的情况下，很容易出现复制黏贴代码，反正能跑就行的情况，积重难返。面向SQL编程更是将业务逻辑与实际的存储模型耦合，要开发另一个业务功能的时候，只能重新写个满足新需求的 SQL 语句，这就可能导致各种长得差不多、区别很小的 SQL 语句满天飞。假设某一部分数据换到Redis上存储，需要改动的代码又很多。

而“领域驱动设计”**则提倡如果业务逻辑只依赖BO/领域模型的数据，那么就应该把业务逻辑下放到BO/领域模型中**。

事实上，领域驱动设计与微服务的概念不谋而合。将领域模型提取出来，便可以很容易的进行复制，提高系统的容灾能力。

Service层应该完成的事情只包含：

- 与 Repository 交流。获取数据库中的数据，转化成领域模型，然后由领域模型来完成业务逻辑，最后调用 Repository 类的方法，将数据存回数据库。
- 负责跨领域模型的业务聚合功能。比如一个业务需要用到多个领域模型，那么可以将其放到Service层中，当然也可以提取为新的领域模型。
- 非功能性及与三方系统交互的工作。比如幂等、事务、发邮件、发消息、记录日志、调用其他系统的 RPC 接口等。换句话说，就是中间件所做的工作。

## 总结

这一部分在谈设计模式之前，首先明确了什么是面向对象，怎样才是面向对象过程，同时也结合实际对面向对象中的精华和糟粕进行分析，帮助我们清晰的认识面向对象编程。

