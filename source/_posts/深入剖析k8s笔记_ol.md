---
title: 深入剖析k8s笔记
categories: 笔记
tags:
  - 云原生
date: 2024-07-02 23:11:59
---
### 整体架构

https://blog.frognew.com/2021/08/relearning-k8s-02.html

![image-20240407183224098](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/深入剖析k8s笔记/20240702231149380463_679_image-20240407183224098.png)

#### 当你创建了一个 Deployment 时，Kubernetes 内部发生了什么?

https://learnku.com/articles/61364

用户通过 kubectl 向 kube-apiserver 发起一个创建 Deployment 对象的请求。

kube-apiserver 在对上述请求进行认证（authn）、授权（authz）、准入控制（admission control）、验证（validation）等一系列操作后，会创建一个 Deployment 对象。

上述的 Deployment 创建事件，会被 DeploymentController 通过其内部的 DeploymentInformer 监听到，然后根据 DeploymentController 内部设定的逻辑，它将会创建一个 ReplicaSet 对象。源码 syncDeployment

上述的 ReplicaSet 创建事件，会被 ReplicaSetController 通过其内部的 ReplicaSetInformer 监听到，然后根据 ReplicaSetController 内部设定的逻辑，它将创建一个 Pod 对象，而此时 Pod 的 Spec.nodeName 字段的值为空；源码 syncReplicaSet

上述的 Pod 创建事件，会被 Scheduler 通过其内部的 PodInformer 监听到，Scheduler 会根据其内部的调度算法，选择一个合适的 Node 节点，例如 node-A，并更新 Pod 的 Spec.nodeName 字段。源码 Schedule

上述的 Pod 更新事件，会被 node-A 节点上 kubelet 感知到，它会发现自己的 nodeName 和 Pod 的 Spec.nodeName 相匹配，接着 kubelet 将按照一定的步骤顺序启动 Pod 中的容器，并将容器已启动的信息写入 Pod 的 Status 中。源码 syncPod

DeploymentController、ReplicaSetController 等许多独立的控制循环都是通过**监听 kube-apiserver 上对象的变化进行通信**，而这些变化会通过各种 **Informer 触发事件**，执行其对应的业务逻辑。之所以这么设计，是为了减少对 **apiserver 的压力**。

再详细一点的路径

https://www.cnblogs.com/ryanyangcs/p/11167380.html

### Volume

bind mount和data volume对比

    A、bind mount方式， docker容器直接访问host的目录或文件，性能是最好的。
    B、bind mount方式， docker容器直接访问host的目录或文件，对于该host绝对目录可能会引入权限问题。 如果容器仅需要只读访问权限，最好是显式设定只读方式。
    C、对于 volume方式， 如果host中落地目录为空， docker先将容器中的对应目录复制到host下， 然后再进行挂载操作；对于bind mount方式，挂载之前没有复制操作。容器要依赖host主机的一个绝对路径, 使得容器的移植性变差, docker 官方并不推荐bind mount， 而是推荐使用volume。

虽然不使用 Docker，但 Google 内部确实在使用一个包管理工具，名叫 Midas Package Manager (MPM)，其实它可以部分取代 Docker 镜像的角色。

迁移可以简单分为两类：磁盘数据文件不变，进程重启；磁盘数据文件不变、内存数据也不变，相当于连带进程一起挪过去。第一种类型有很简单的方法：挂载云盘，从空间上解耦。第二种类型就复杂了，需要将内存数据一点点迁移过去，最后瞬间切换。IaaS很早就应用热迁移技术了。 Kubernetes则讨巧了，只着眼于应用，直接约定容器是可以随时被杀死的，热迁移就没有那么重要了。甚至连IP都隐藏了，又绕过了一个大难题～

在 Kubernetes 中，有几种特殊的 Volume，它们存在的意义不是为了存放容器里的数据，也不是用来进行容器和宿主机之间的数据交换。这些特殊 Volume 的作用，是为容器提供预先定义好的数据。所以，从容器的角度来看，这些 Volume 里的信息就是仿佛是被 Kubernetes“投射”（Project）进入容器当中的。这正是 Projected Volume 的含义。

### Pod

#### 为什么需要Pod

https://freegeektime.com/100015201/40092/

**为什么**总是最重要的，这一节讲述了容器的核心设计模式，也是大规模基础设施管理“痛点”的解决方式

重新理解“单进程模型”

容器的“单进程模型”，并不是指容器里只能运行“一个”进程，而是指容器没有管理多个进程的能力。这是因为容器里 PID=1 的进程就是应用本身，其他的进程都是这个 PID=1 进程的子进程。可是，用户编写的应用，并不能够像正常操作系统里的 init 进程或者 systemd 那样拥有进程管理的功能。比如，你的应用是一个 Java Web 程序（PID=1），然后你执行 docker exec 在后台启动了一个 Nginx 进程（PID=3）。可是，当这个 Nginx 进程异常退出的时候，你该怎么知道呢？这个进程退出后的垃圾收集工作，又应该由谁去做呢？

所以，像 imklog、imuxsock 和 main 函数主进程这样的三个容器，正是一个典型的由三个容器组成的 Pod。Kubernetes 项目在调度时，自然就会去选择可用内存等于 3 GB 的 node-1 节点进行绑定，而根本不会考虑 node-2。

像这样容器间的紧密协作，我们可以称为“超亲密关系”。这些具有“超亲密关系”容器的典型特征包括但不限于：互相之间会发生直接的文件交换、使用 localhost 或者 Socket 文件进行本地通信、会发生非常频繁的远程调用、需要共享某些 Linux Namespace（比如，一个容器要加入另一个容器的 Network Namespace）等等。

所以，在 Kubernetes 项目里，Pod 的实现需要使用一个中间容器，这个容器叫作 Infra 容器。在这个 Pod 中，Infra 容器永远都是第一个被创建的容器，而其他用户定义的容器，则通过 Join Network Namespace 的方式，与 Infra 容器关联在一起。这样的组织关系，可以用下面这样一个示意图来表达：

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/深入剖析k8s笔记/20240702231154886419_779_image-20240409115032186.png" alt="image-20240409115032186" width="50%" height="50%" />

对于 Pod 里的容器 A 和容器 B 来说：

它们可以直接使用 localhost 进行通信；

它们看到的网络设备跟 Infra 容器看到的完全一样；

一个 Pod 只有一个 IP 地址，也就是这个 Pod 的 Network Namespace 对应的 IP 地址；

当然，其他的所有网络资源，都是一个 Pod 一份，并且被该 Pod 中的所有容器共享；

Pod 的生命周期只跟 Infra 容器一致，而与容器 A 和 B 无关。

#### Pod理解

Pod 看成传统环境里的“机器”、把容器看作是运行在这个“机器”里的“用户程序”，那么很多关于 Pod 对象的设计就非常容易理解了

凡是调度、网络、存储，以及安全相关的属性，基本上是 Pod 级别的。

这些属性的共同特征是，它们描述的是“机器”这个整体，而不是里面运行的“程序”。比如，配置这个“机器”的网卡（即：Pod 的网络定义），配置这个“机器”的磁盘（即：Pod 的存储定义），配置这个“机器”的防火墙（即：Pod 的安全定义）。更不用说，这台“机器”运行在哪个服务器之上（即：Pod 的调度）。

凡是跟容器的 Linux Namespace 相关的属性，也一定是 Pod 级别的。这个原因也很容易理解：Pod 的设计，就是要让它里面的容器尽可能多地共享 Linux Namespace，仅保留必要的隔离和限制能力。这样，Pod 模拟出的效果，就跟虚拟机里程序间的关系非常类似了。

```
shareProcessNamespace: true
```

这就意味着这个 Pod 里的容器要共享 PID Namespace。

**Pod，实际上是在扮演传统基础设施里“虚拟机”的角色；而容器，则是这个虚拟机里运行的用户程序。**

> 注意：Pod 这个概念，提供的是一种编排思想，而不是具体的技术方案。所以，如果愿意的话，你完全可以使用虚拟机来作为 Pod 的实现，然后把用户容器都运行在这个虚拟机里。比如，Mirantis 公司的virtlet 项目就在干这个事情。甚至，你可以去实现一个带有 Init 进程的容器项目，来模拟传统应用的运行方式。这些工作，在 Kubernetes 中都是非常轻松的，也是我们后面讲解 CRI 时会提到的内容。

#### pod生命周期

Pod 生命周期的变化，主要体现在 Pod API 对象的 Status 部分，这是它除了 Metadata 和 Spec 之外的第三个重要字段。其中，pod.status.phase，就是 Pod 的当前状态，它有如下几种可能的情况：

Pending。这个状态意味着，Pod 的 YAML 文件已经提交给了 Kubernetes，API 对象已经被创建并保存在 Etcd 当中。但是，这个 Pod 里有些容器因为某种原因而不能被顺利创建。比如，调度不成功。

Running。这个状态下，Pod 已经调度成功，跟一个具体的节点绑定。它包含的容器都已经创建成功，并且至少有一个正在运行中。

Succeeded。这个状态意味着，Pod 里的所有容器都正常运行完毕，并且已经退出了。这种情况在运行一次性任务时最为常见。

Failed。这个状态下，Pod 里至少有一个容器以不正常的状态（非 0 的返回码）退出。这个状态的出现，意味着你得想办法 Debug 这个容器的应用，比如查看 Pod 的 Events 和日志。

Unknown。这是一个异常状态，意味着 Pod 的状态不能持续地被 kubelet 汇报给 kube-apiserver，这很有可能是主从节点（Master 和 Kubelet）间的通信出现了问题。

#### 静态Pod

**静态 Pod** 在指定的节点上由 kubelet 守护进程直接管理，不需要 [API 服务器](https://kubernetes.io/zh-cn/docs/concepts/overview/components/#kube-apiserver)监管。 与由控制面管理的 Pod（例如，[Deployment](https://kubernetes.io/zh-cn/docs/concepts/workloads/controllers/deployment/)） 不同；kubelet 监视每个静态 Pod（在它失败之后重新启动）。

### Deployment

Kubernate控制器模型

1. Deployment控制器从Etcd中获取到所有携带了“app：nginx”标签的Pod，然后统计它们的数量，这就是实际状态；

2. Deployment对象的Replicas字段的值就是期望状态;

3. Deployment控制器将两个状态做比较，然后根据比较结果，确定是创建Pod，还是删除已有的Pod（具体如何操作Pod对象，我会在下一篇文章详细介绍)。

类似 Deployment 这样的一个控制器，实际上都是由上半部分的控制器定义（包括期望状态），加上下半部分的被控制对象的模板组成的。

### ServiceAccount

相信你一定有过这样的想法：我现在有了一个 Pod，我能不能在这个 Pod 里安装一个 Kubernetes 的 Client，这样就可以从容器里直接访问并且操作这个 Kubernetes 的 API 了呢？

这当然是可以的。

不过，你首先要解决 API Server 的授权问题。

Service Account 对象的作用，就是 Kubernetes 系统内置的一种“服务账户”，它是 Kubernetes 进行权限分配的对象。比如，Service Account A，可以只被允许对 Kubernetes API 进行 GET 操作，而 Service Account B，则可以有 Kubernetes API 的所有操作权限。

一旦 Pod 创建完成，容器里的应用就可以直接从这个默认 ServiceAccountToken 的挂载目录里访问到授权信息和文件。这个容器内的路径在 Kubernetes 里是固定的，即：/var/run/secrets/kubernetes.io/serviceaccount ，而这个 Secret 类型的 Volume 里面的内容如下所示：

```
ls /var/run/secrets/kubernetes.io/serviceaccount 
ca.crt namespace token
```

这种把 Kubernetes 客户端以容器的方式运行在集群里，然后使用 default Service Account 自动授权的方式，被称作“InClusterConfig”，也是我最推荐的进行 Kubernetes API 编程的授权方式。

但一定要强调的是，Pod 的恢复过程，永远都是发生在当前节点上，而不会跑到别的节点上去。事实上，一旦一个 Pod 与一个节点（Node）绑定，除非这个绑定发生了变化（`pod.spec.node` 字段被修改），否则它永远都不会离开这个节点。这也就意味着，如果这个宿主机宕机了，这个 Pod 也不会主动迁移到其他节点上去。

而如果你想让 Pod 出现在其他的可用节点上，就必须使用 Deployment 这样的“控制器”来管理 Pod，哪怕你只需要一个 Pod 副本。这就是我在第 12 篇文章《牛刀小试：我的第一个容器化应用》最后给你留的思考题的答案，即一个单 Pod 的 Deployment 与一个 Pod 最主要的区别。

只要 Pod 的 restartPolicy 指定的策略允许重启异常的容器（比如：Always），那么这个 Pod 就会保持 Running 状态，并进行容器重启。否则，Pod 就会进入 Failed 状态 。

对于包含多个容器的 Pod，只有它里面所有的容器都进入异常状态后，Pod 才会进入 Failed 状态。在此之前，Pod 都是 Running 状态。此时，Pod 的 READY 字段会显示正常容器的个数，比如：

对于一个 Deployment 所管理的 Pod，它的 ownerReference 是谁？

所以，这个问题的答案就是：ReplicaSet。

通过这些讲解，你应该了解到：Deployment 实际上是一个两层控制器。首先，它通过 ReplicaSet 的个数来描述应用的版本；然后，它再通过 ReplicaSet 的属性（比如 replicas 的值），来保证 Pod 的副本数量。

### Statefulset

首先，StatefulSet 的控制器直接管理的是 Pod。这是因为，StatefulSet 里的不同 Pod 实例，不再像 ReplicaSet 中那样都是完全一样的，而是有了细微区别的。比如，每个 Pod 的 hostname、名字等都是不同的、携带了编号的。而 StatefulSet 区分这些实例的方式，就是通过在 Pod 的名字里加上事先约定好的编号。

其次，Kubernetes 通过 Headless Service，为这些有编号的 Pod，在 DNS 服务器中生成带有同样编号的 DNS 记录。只要 StatefulSet 能够保证这些 Pod 名字里的编号不变，那么 Service 里类似于` web-0.nginx.default.svc.cluster.local`这样的 DNS 记录也就不会变，而这条记录解析出来的 Pod 的 IP 地址，则会随着后端 Pod 的删除和再创建而自动更新。这当然是 Service 机制本身的能力，不需要 StatefulSet 操心。

> 具体的，怎么定义headless service？
>
> ```yaml
> apiVersion: v1
> kind: Service
> metadata:
>  name: nginx
>  labels:
>  app: nginx
> spec:
>  ports:
>  - port: 80
>  name: web
>  clusterIP: None
>  selector:
>  app: nginx
> ```
>
> clusterIP: None

最后，StatefulSet 还为每一个 Pod 分配并创建一个同样编号的 PVC。这样，Kubernetes 就可以通过 Persistent Volume 机制为这个 PVC 绑定上对应的 PV，从而保证了每一个 Pod 都拥有一个独立的 Volume。

在这种情况下，即使 Pod 被删除，它所对应的 PVC 和 PV 依然会保留下来。所以当这个 Pod 被重新创建出来之后，Kubernetes 会为它找到同样编号的 PVC，挂载这个 PVC 对应的 Volume，从而获取到以前保存在 Volume 里的数据。

/var 包括系统运行时要改变的数据。其中包括每个系统是特定的，即不能够与其他计算机共享的目录，如/var/log，/var/lock，/var/run。有些目录还是可以与其他系统共享，如/var/mail, /var/cache/man,  /var/cache/fonts,/var/spool/news。var目录存在的目的是把usr目录在运行过程中需要更改的文件或者临时生成的文件及目录提取出来，由此可以使usr目录挂载为只读的方式。隐含要求var目录必须挂载为可以读写的方式。

### Sidecar工作示例

我们现在有一个 Java Web 应用的 WAR 包，它需要被放在 Tomcat 的 webapps 目录下运行起来。

假如，你现在只能用 Docker 来做这件事情，那该如何处理这个组合关系呢？

一种方法是，把 WAR 包直接放在 Tomcat 镜像的 webapps 目录下，做成一个新的镜像运行起来。可是，这时候，如果你要更新 WAR 包的内容，或者要升级 Tomcat 镜像，就要重新制作一个新的发布镜像，非常麻烦。

另一种方法是，你压根儿不管 WAR 包，永远只发布一个 Tomcat 容器。不过，这个容器的 webapps 目录，就必须声明一个 hostPath 类型的 Volume，从而把宿主机上的 WAR 包挂载进 Tomcat 容器当中运行起来。不过，这样你就必须要解决一个问题，即：如何让每一台宿主机，都预先准备好这个存储有 WAR 包的目录呢？这样来看，你只能独立维护一套分布式存储系统了。

实际上，有了 Pod 之后，这样的问题就很容易解决了。我们可以把 WAR 包和 Tomcat 分别做成镜像，然后把它们作为一个 Pod 里的两个容器“组合”在一起。这个 Pod 的配置文件如下所示：

```yaml
apiVersion: v1
kind: Pod
metadata:
 name: javaweb-2
spec:
 initContainers:
- image: geektime/sample:v2
 name: war
 command: ["cp", "/sample.war", "/app"]
 volumeMounts:
- mountPath: /app
 name: app-volume
 containers:
- image: geektime/tomcat:7.0
 name: tomcat
 command: ["sh","-c","/root/apache-tomcat-7.0.42-v2/bin/start.sh"]
 volumeMounts:
- mountPath: /root/apache-tomcat-7.0.42-v2/webapps
 name: app-volume
 ports:
- containerPort: 8080
 hostPort: 8001 
 volumes:
- name: app-volume
 emptyDir: {}
```



在这个 Pod 中，我们定义了两个容器，第一个容器使用的镜像是 geektime/sample:v2，这个镜像里只有一个 WAR 包（sample.war）放在根目录下。而第二个容器则使用的是一个标准的 Tomcat 镜像。

不过，你可能已经注意到，WAR 包容器的类型不再是一个普通容器，而是一个 Init Container 类型的容器。

在 Pod 中，所有 Init Container 定义的容器，都会比 spec.containers 定义的用户容器先启动。并且，Init Container 容器会按顺序逐一启动，而直到它们都启动并且退出了，用户容器才会启动。

所以，这个 Init Container 类型的 WAR 包容器启动后，我执行了一句"cp /sample.war /app"，把应用的 WAR 包拷贝到 /app 目录下，然后退出。

而后这个 /app 目录，就挂载了一个名叫 app-volume 的 Volume。

接下来就很关键了。Tomcat 容器，同样声明了挂载 app-volume 到自己的 webapps 目录下。

所以，等 Tomcat 容器启动时，它的 webapps 目录下就一定会存在 sample.war 文件：这个文件正是 WAR 包容器启动时拷贝到这个 Volume 里面的，而这个 Volume 是被这两个容器共享的。

像这样，我们就用一种“组合”方式，解决了 WAR 包与 Tomcat 容器之间耦合关系的问题。

实际上，这个所谓的“组合”操作，正是容器设计模式里最常用的一种模式，它的名字叫：sidecar。

顾名思义，sidecar 指的就是我们可以在一个 Pod 中，启动一个辅助容器，来完成一些独立于主进程（主容器）之外的工作。

### DaemonSet

DaemonSet 只管理 Pod 对象，然后通过 nodeAffinity 和 Toleration 这两个调度器的小功能，保证了每个节点上有且只有一个 Pod。

DaemonSet 使用 ControllerRevision，来保存和管理自己对应的“版本”。这种“面向 API 对象”的设计思路，大大简化了控制器本身的逻辑，也正是 Kubernetes 项目“声明式 API”的优势所在。

### Job

定义了 restartPolicy=Never，那么离线作业失败后 Job Controller 就会不断地尝试创建一个新 Pod

定义的 restartPolicy=OnFailure，那么离线作业失败后，Job Controller 就不会去尝试创建新的 Pod。但是，它会不断地尝试重启 Pod 里的容器。

### 声明式API

如何使用控制器模式，同 Kubernetes 里 API 对象的“增、删、改、查”进行协作，进而完成用户业务逻辑的编写过程。

实际上，可以简单地理解为，kubectl replace 的执行过程，是使用新的 YAML 文件中的 API 对象，替换原有的 API 对象；而 kubectl apply，则是执行了一个对原有 API 对象的 PATCH 操作，前者是“命令式”，后者是“声明式”

kube-apiserver 在响应命令式请求（比如，kubectl replace）的时候，一次只能处理一个写请求，否则会有产生冲突的可能。而对于声明式请求（比如，kubectl apply），一次能处理多个写操作，并且具备 Merge 能力。

典型应用：Istio 项目

24，25讲如何在 Kubernetes 里添加 API 资源

APIServer

/api/version/core_source

/apis/group/version/resource

#### API编程

所谓的 Informer，就是一个自带缓存和索引机制，可以触发 Handler 的客户端库。这个本地缓存在 Kubernetes 中一般被称为 Store，索引一般被称为 Index。

Informer 使用了 Reflector 包，它是一个可以通过 ListAndWatch 机制获取并监视 API 对象变化的客户端封装。

Reflector 和 Informer 之间，用到了一个“增量先进先出队列”进行协同。而 Informer 与你要编写的控制循环之间，则使用了一个工作队列来进行协同。

在实际应用中，除了控制循环之外的所有代码，实际上都是 Kubernetes 为你自动生成的，即：pkg/client/{informers, listers, clientset}里的内容。

而这些自动生成的代码，就为我们提供了一个可靠而高效地获取 API 对象“期望状态”的编程库。

所以，接下来，作为开发者，你就只需要关注如何拿到“实际状态”，然后如何拿它去跟“期望状态”做对比，从而决定接下来要做的业务逻辑即可。

### RBAC

角色（Role），其实就是一组权限规则列表。而我们分配这些权限的方式，就是通过创建 RoleBinding 对象，将被作用者（subject）和权限列表进行绑定。

而对于 Kubernetes 的内置“用户”ServiceAccount 来说，“用户组”的概念也同样适用。

实际上，一个 ServiceAccount，在 Kubernetes 里对应的“用户”的名字是：

```yaml
system:serviceaccount:<Namespace名字>:<ServiceAccount名字>
```

而它对应的内置“用户组”的名字，就是：

```yml
system:serviceaccounts:<Namespace名字>
```

比如，现在我们可以在 RoleBinding 里定义如下的 subjects：

```yml
subjects:
- kind: Group
  name: system:serviceaccounts:mynamespace
  apiGroup: rbac.authorization.k8s.io
```

这就意味着这个 Role 的权限规则，作用于 mynamespace 里的所有 ServiceAccount。这就用到了“用户组”的概念。

而下面这个例子：

```yml
subjects:
- kind: Group
  name: system:serviceaccounts
  apiGroup: rbac.authorization.k8s.io
```

就意味着这个 Role 的权限规则，作用于整个系统里的所有 ServiceAccount。

在 Kubernetes 中已经内置了很多个为系统保留的 ClusterRole，它们的名字都以 system: 开头

**典型应用场景：所有Namespace 下的默认 ServiceAccount，绑定一个只读权限的 Role。**

```yml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: readonly-all-default
subjects:
  - kind: ServiceAccount
    name: system.serviceaccount.default
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
```

解释：

 ClusterRole 和 ClusterRoleBinding 这两个 API 对象的用法跟 Role 和 RoleBinding 完全一样。只不过，它们的定义里，没有了 Namespace 字段，是针对整个Cluster的。

Kubernetes 提供了四个预先定义好的 ClusterRole 来供用户直接使用：

- cluster-admin；

- admin；

- edit；

- view

### Operator

Operator 的工作原理，实际上是利用了 Kubernetes 的自定义 API 资源（CRD），来描述我们想要部署的“有状态应用”；然后在自定义控制器里，根据自定义 API 对象的变化，来完成具体的部署和运维工作。

举例： Etcd Operator（已经Archive了，简单了解下思想ok）

Etcd Operator 部署 Etcd 集群，采用的是静态集群（Static）的方式。

静态集群的好处是，它不必依赖于一个额外的服务发现机制来组建集群，非常适合本地容器化部署。而它的难点，则在于你必须在部署的时候，就规划好这个集群的拓扑结构，并且能够知道这些节点固定的 IP 地址。Etcd Operator，就是要把上述过程自动化，这其实等同于：用代码来生成每个 Etcd 节点 Pod 的启动命令，然后把它们启动起来。

### 存储

#### [PV&PVC](https://freegeektime.com/100015201/42698/)

PV 描述的，是持久化存储数据卷，PVC 描述的，则是 Pod 所希望使用的持久化存储的属性

而用户创建的 PVC 要真正被容器使用起来，就必须先和某个符合条件的 PV 进行绑定。这里要检查的条件，包括两部分：

第一个条件，当然是 PV 和 PVC 的 spec 字段。比如，PV 的存储（storage）大小，就必须满足 PVC 的要求。

而第二个条件，则是 PV 和 PVC 的 storageClassName 字段必须一样。

**PersistentVolumeController** 会不断地查看当前每一个 PVC，是不是已经处于 Bound（已绑定）状态。如果不是，那它就会遍历所有的、可用的 PV，并尝试将其与这个“单身”的 PVC 进行绑定。

对于为容器准备一个持久化Volume这件事。需要经过K8s“两阶段处理”：

Attach：为虚拟机挂载远程磁盘

Mount：将磁盘设备格式化并挂载到 Volume 宿主机目录

> 对应地，在删除一个 PV 的时候，Kubernetes 也需要 Unmount 和 Dettach 两个阶段来处理。远程文件存储不需要attach

StorageClass 的作用，是充当 PV 的模板。并且，只有同属于一个 StorageClass 的 PV 和 PVC，才可以绑定在一起

StorageClass 的另一个重要作用，是指定 PV 的 Provisioner（存储插件）。这时候，如果你的存储插件支持 Dynamic Provisioning 的话，Kubernetes 就可以自动为你创建 PV 了

![image-20240305141902205](C:\Users\12926\AppData\Roaming\Typora\typora-user-images\image-20240305141902205.png)

总结一下：

用户提交请求创建pod，Kubernetes发现这个pod声明使用了PVC，那就靠PersistentVolumeController帮它找一个PV配对。 

没有现成的PV，就去找对应的StorageClass，帮它新创建一个PV，然后和PVC完成绑定。

 新创建的PV，还只是一个API 对象，需要经过“两阶段处理”变成宿主机上的“持久化 Volume”才真正有用： 

第一阶段由运行在master上的AttachDetachController负责，为这个PV完成 Attach 操作，为宿主机挂载远程磁盘；

第二阶段是运行在每个节点上kubelet组件的内部，把第一步attach的远程磁盘 mount 到宿主机目录。这个控制循环叫VolumeManagerReconciler，运行在独立的Goroutine，不会阻塞kubelet主循环。 

完成这两步，PV对应的“持久化 Volume”就准备好了，POD可以正常启动，将“持久化 Volume”挂载在容器内指定的路径。

#### [Local Persistent Volume](https://freegeektime.com/100015201/42819/)

目的：用户希望 Kubernetes 能够直接使用宿主机上的本地磁盘目录，而不依赖于远程存储服务，来提供“持久化”的容器 Volume

> 你绝不应该把一个宿主机上的目录当作 PV 使用。不同的本地目录之间也缺乏哪怕最基础的 I/O 隔离机制。因此需要“一个 PV 一块盘”

如何实现本地持久化存储

PV 的定义里：local 字段，指定了它是一个 Local Persistent Volume

它的 provisioner 字段，我们指定的是 no-provisioner。这是因为 Local Persistent Volume 目前尚不支持 Dynamic Provisioning

StorageClass 还定义了一个 volumeBindingMode=WaitForFirstConsumer 的属性。它是 Local Persistent Volume 里一个非常重要的特性，即：延迟绑定。

在删除 PV 时需要按如下流程执行操作：

- 删除使用这个 PV 的 Pod；

- 从宿主机移除本地磁盘（比如，umount 它）；

- 删除 PVC；

- 删除 PV。

### Network

#### 单机容器的网络理解

https://freegeektime.com/100015201/64948/

Host模式最简单，作为一个容器，它可以声明直接使用宿主机的网络栈（–net=host），即：不开启 Network Namespace。

Bridge模式复杂一点，但是是理解后面网络模型的基础。

在 Linux 中，能够起到虚拟交换机作用的网络设备，是网桥（Bridge）。它是一个工作在数据链路层（Data Link）的设备，主要功能是根据 MAC 地址学习来将数据包转发到网桥的不同端口（Port）上。

Docker 项目会默认在宿主机上创建一个名叫 docker0 的网桥，凡是连接在 docker0 网桥上的容器，就可以通过它来进行通信。

docker0 处理转发的过程，则是扮演二层交换机的角色。此时，docker0 网桥根据数据包的目的 MAC 地址（也就是 nginx-2 容器的 MAC 地址），在它的 CAM 表（即交换机通过 MAC 地址学习维护的端口和 MAC 地址的对应表）里查到对应的端口，然后把数据包发往这个端口。

容器要想跟外界进行通信，它发出的 IP 包就必须从它的 Network Namespace 里出来，来到宿主机上。

而解决这个问题的方法就是：为容器创建一个一端在容器里充当默认网卡、另一端在宿主机上的 Veth Pair 设备。

在 Linux 中，TUN 设备是一种工作在三层（Network Layer）的虚拟网络设备。TUN 设备的功能非常简单，即：在操作系统内核和用户应用程序之间传递 IP 包。

#### 怎么跨node进行容器通信

首先从容易理解比较简单的方法开始讲解：

打隧道，flannel，需要对二层三层网络有比较深的理解

https://freegeektime.com/100015201/65287/

UDP模式和VXLAN，即 Virtual Extensible LAN（虚拟可扩展局域网）模式。后者是主流，实现方式是在二层三层之间加一个VXLAN header，然后再套二层。

总体概述：

Kubernetes通过一个叫做CNI的接口，维护了一个单独的网桥来代替docker0。这个网桥的名字就叫作：CNI网桥，它在宿主机上的设备名称默认是：cni0。

容器“跨主通信”的三种主流实现方法：UDP、host-gw、VXLAN。  之前介绍了UDP和VXLAN，它们都属于隧道模式，需要封装和解封装。

接下来介绍一种纯三层网络方案，host-gw模式和Calico项目 Host-gw模式通过在宿主机上添加一个路由规则：      

<目的容器IP地址段> via <网关的IP地址> dev eth0 

IP包在封装成帧发出去的时候，会使用路由表里的“下一跳”来设置目的MAC地址。这样，它就会通过二层网络到达目的宿主机。 这个三层网络方案得以正常工作的核心，是为每个容器的IP地址，找到它所对应的，“下一跳”的网关。

所以说，Flannel  host-gw模式必须要求集群宿主机之间是二层连通的，如果宿主机分布在了不同的VLAN里（三层连通），由于需要经过的中间的路由器不一定有相关的路由配置（出于安全考虑，公有云环境下，宿主机之间的网关，肯定不会允许用户进行干预和设置），部分节点就无法找到容器IP的“下一跳”网关了，host-gw就无法工作了。

 Calico项目提供的网络解决方案，与Flannel的host-gw模式几乎一样，也会在宿主机上添加一个路由规则：     

<目的容器IP地址段> via <网关的IP地址> dev eth0 

其中，网关的IP地址，正是目的容器所在宿主机的IP地址，而正如前面所述，这个三层网络方案得以正常工作的核心，是为每个容器的IP地址，找到它所对应的，“下一跳”的网关。

区别是如何维护路由信息： 

Host-gw :  Flannel通过Etcd和宿主机上的flanneld来维护路由信息 

Calico: 通过BGP（边界网关协议）来实现路由自治，所谓BGP，就是在大规模网络中实现节点路由信息共享的一种协议。 

隧道技术（需要封装包和解包，因为需要伪装成宿主机的IP包，需要三层链通）：Flannel UDP / VXLAN  / Calico IPIP 三层网络（不需要封包和解封包，需要二层链通）：Flannel host-gw / Calico 普通模式

### Service

Service 提供的是 Round Robin 方式的负载均衡。对于这种方式，我们称为：ClusterIP 模式的 Service。

Service 的负载均衡策略，有iptables 和 ipvs 模式

iptables模式，会在宿主机上创建一个规则，提供统一ip入口跳转到一组规则，然后这一组规则实际上是一组随机模式（–mode random）的 iptables 链。

但kube-proxy 通过 iptables 处理 Service 的过程，其实需要在宿主机上设置相当多的 iptables 规则。而且，kube-proxy 还需要在控制循环里不断地刷新这些规则来确保它们始终是正确的。

一直以来，基于 iptables 的 Service 实现，都是制约 Kubernetes 项目承载更多量级的 Pod 的主要障碍。

ClusterIP 模式的 Service 为你提供的，就是一个 Pod 的稳定的 IP 地址，即 VIP。并且，这里 Pod 和 Service 的关系是可以通过 Label 确定的。

而 Headless Service 为你提供的，则是一个 Pod 的稳定的 DNS 名字，并且，这个名字是可以通过 Pod 名字和 Service 名字拼接出来的。

#### 如何从集群外界访问Service

https://freegeektime.com/100015201/68964/

从外部访问 Service 的三种方式（NodePort、LoadBalancer 和 External Name）

NodePort顾名思义，就是访问宿主机（Node）的ip:port，就可以访问某个被Service代理Pod的端口，这是通过在每台宿主机上生成iptables 规则转发到随机模式的 iptables 规则。

在公有云提供的 Kubernetes 服务里，都使用了一个叫作 CloudProvider 的转接层，来跟公有云本身的 API 进行对接。所以，在上述 LoadBalancer 类型的 Service 被提交后，Kubernetes 就会调用 CloudProvider 在公有云上为你创建一个负载均衡服务，并且把被代理的 Pod 的 IP 地址配置给负载均衡服务做后端。

ExternalName 类型的 Service，其实是在 kube-dns 里为你添加了一条 CNAME 记录。这时，访问 my-service.default.svc.cluster.local 就和访问 my.database.example.com 这个域名是一个效果了。

Kubernetes 的 Service 还允许你为 Service 分配公有 IP 地址。不过，在这里 Kubernetes 要求 externalIPs 必须是至少能够路由到一个 Kubernetes 的节点。

所谓 Service，其实就是 Kubernetes 为 Pod 分配的、固定的、基于 iptables（或者 IPVS）的访问入口。而这些访问入口代理的 Pod 信息，则来自于 Etcd，由 kube-proxy 通过控制循环来维护。

### Ingress

Kubernetes 提出 Ingress 概念的原因其实也非常容易理解，有了 Ingress 这个抽象，用户就可以根据自己的需求来自由选择 Ingress Controller。比如，如果你的应用对代理服务的中断非常敏感，那么你就应该考虑选择类似于 Traefik 这样支持“热加载”的 Ingress Controller 实现。

实例：

这种全局的、为了代理不同后端 Service 而设置的负载均衡服务，就是 Kubernetes 里的 Ingress 服务。

所以，Ingress 的功能其实很容易理解：所谓 Ingress，就是 Service 的“Service”。

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
 name: cafe-ingress
spec:
 tls:
 - hosts:
 - cafe.example.com
 secretName: cafe-secret
 rules:
 - host: cafe.example.com
 http:
 paths:
 - path: /tea
 backend:
 serviceName: tea-svc
 servicePort: 80
 - path: /coffee
 backend:
 serviceName: coffee-svc
 servicePort: 80
```

### 资源管理

#### 资源分类

在 Kubernetes 中，像 CPU 这样的资源被称作“可压缩资源”（compressible resources）。它的典型特点是，当可压缩资源不足时，Pod 只会“饥饿”，但不会退出。

而像内存这样的资源，则被称作“不可压缩资源（incompressible resources）。当不可压缩资源不足时，Pod 就会因为 OOM（Out-Of-Memory）被内核杀掉。

而由于 Pod 可以由多个 Container 组成，所以 CPU 和内存资源的限额，是要配置在每个 Container 的定义上的。这样，Pod 整体的资源配置，就由这些 Container 的配置值累加得到。

我们知道，在使用容器的时候，你可以通过设置 cpuset 把容器绑定到某个 CPU 的核上，而不是像 cpushare 那样共享 CPU 的计算能力。

这种情况下，由于操作系统在 CPU 之间进行上下文切换的次数大大减少，容器里应用的性能会得到大幅提升。事实上，cpuset 方式，是生产环境里部署在线应用类型的 Pod 时，非常常用的一种方式。

#### QoS级别

当 Pod 里的每一个 Container 都同时设置了 requests 和 limits，并且 requests 和 limits 值相等的时候，这个 Pod 就属于 Guaranteed 类别

而当 Pod 不满足 Guaranteed 的条件，但至少有一个 Container 设置了 requests。那么这个 Pod 就会被划分到 Burstable 类别

而如果一个 Pod 既没有设置 requests，也没有设置 limits，那么它的 QoS 类别就是 BestEffort

正是基于上述讲述，在实际的使用中，我强烈建议你将 DaemonSet 的 Pod 都设置为 Guaranteed 的 QoS 类型。否则，一旦 DaemonSet 的 Pod 被回收，它又会立即在原宿主机上被重建出来，这就使得前面资源回收的动作，完全没有意义了。

### 容器调度

#### 默认调度器

Kubernetes 的整体架构中，kube-scheduler 的责任虽然重大，但其实它却是在社区里最少受到关注的组件之一。这里的原因也很简单，调度这个事情，在不同的公司和团队里的实际需求一定是大相径庭的，上游社区不可能提供一个大而全的方案出来。所以，将默认调度器进一步做轻做薄，并且插件化，才是 kube-scheduler 正确的演进方向。

K8s项目中默认调度器的主要职责是就是为了新创建出来的Pod寻找一个最合适的Node。 调度器首先会调用一组叫Predicate的调度算法，来检每一个Node。然后再调用一组叫作Priority的调度算法来给上一步得到的结果里的每一个Node打分。最终的调度结果就是得分最高的那个Node。

 Kubernetes 的调度器的核心，实际上就是两个相互独立的控制循环。第一个是Informer  Path，主要是启动一系列Informer用来监听(Watch)Etcd中的Pod,Node,  Service等与调度相关的API对象的变化。此外，Kubernetes 的默认调度器还要负责对调度器缓存（即：scheduler  cache）进行更新。事实上，Kubernetes 调度部分进行性能优化的一个最根本原则，就是尽最大可能将集群信息 Cache  化，以便从根本上提高 Predicate 和 Priority 调度算法的执行效率。第二个控制循环是Scheduling  Path，主要逻辑是不断从调度队列里调出Pod，然后用Predicates算法进行过滤，得到一组可以运行这个Pod的宿主机列表，然后再用Priority打分，得分高的称为Pod结果。

#### 详细的调度过程

待调度Pod被提交到apiServer -> 更新到etcd -> 调度器Watch  etcd感知到有需要调度的pod（Informer） -> 取出待调度Pod的信息 ->Predicates：  挑选出可以运行该Pod的所有Node -> Priority：给所有Node打分 -> 将Pod绑定到得分最高的Node上  -> 将Pod信息更新回Etcd -> node的kubelet感知到etcd中有自己node需要拉起的pod ->  取出该Pod信息，做基本的二次检测（端口，资源等） -> 在node 上拉起该pod 。 

Predicates阶段会有很多过滤规则：比如volume相关，node相关，pod相关 Priorities阶段会为Node打分，Pod调度到得分最高的Node上，打分规则比如： 空余资源、实际物理剩余、镜像大小、Pod亲和性等 Kuberentes中可以为Pod设置优先级，高优先级的Pod可以： 1、在调度队列中先出队进行调度  2、调度失败时，触发抢占，调度器为其抢占低优先级Pod的资源。

 Kuberentes默认调度器有两个调度队列： activeQ：凡事在该队列里的Pod，都是下一个调度周期需要调度的 unschedulableQ: 存放调度失败的Pod，当里面的Pod更新后就会重新回到activeQ，进行“重新调度” 默认调度器的抢占过程： 确定要发生抢占 -> 调度器将所有节点信息复制一份，开始模拟抢占 ->  检查副本里的每一个节点，然后从该节点上逐个删除低优先级Pod，直到满足抢占者能运行 -> 找到一个能运行抢占者Pod的node -> 记录下这个Node名字和被删除Pod的列表 -> 模拟抢占结束 -> 开始真正抢占 ->  删除被抢占者的Pod，将抢占者调度到Node上。

### GPU管理

Kuberentes通过Extended  Resource来支持自定义资源，比如GPU。为了让调度器知道这种自定义资源在各Node上的数量，需要的Node里添加自定义资源的数量。实际上，这些信息并不需要人工去维护，所有的硬件加速设备的管理都通过Device Plugin插件来支持，也包括对该硬件的Extended Resource进行汇报的逻辑。 Device Plugin 、kubelet、调度器如何协同工作： 汇报资源： Device Plugin通过gRPC与本机kubelet连接 -> Device  Plugin定期向kubelet汇报设备信息，比如GPU的数量 -> kubelet 向APIServer发送的心跳中，以Extended Reousrce的方式加上这些设备信息，比如GPU的数量 调度： Pod申明需要一个GPU -> 调度器找到GPU数量满足条件的node -> Pod绑定到对应的Node上 ->  kubelet发现需要拉起一个Pod，且该Pod需要GPU -> kubelet向 Device Plugin 发起  Allocate()请求 -> Device  Plugin根据kubelet传递过来的需求，找到这些设备对应的设备路径和驱动目录，并返回给kubelet ->  kubelet将这些信息追加在创建Pod所对应的CRI请求中 ->  容器创建完成之后，就会出现这个GPU设备（设备路径+驱动目录）-> 调度完成

### kubelet

kubelet 的 SyncLoop 和 CRI 的设计，是其中最重要的两个关键点。也正是基于以上设计，SyncLoop 本身就要求这个控制循环是绝对不可以被阻塞的。所以，凡是在 kubelet 里有可能会耗费大量时间的操作，比如准备 Pod 的 Volume、拉取镜像等，SyncLoop 都会开启单独的 Goroutine 来进行操作。

### 安全容器

https://freegeektime.com/100015201/71606/

Kata Containers 原生就带有了 Pod 的概念。即：这个 Kata Containers 启动的虚拟机，就是一个 Pod；而用户定义的容器，就是运行在这个轻量级虚拟机里的进程。在具体实现上，Kata Containers 的虚拟机里会有一个特殊的 Init 进程负责管理虚拟机里面的用户容器，并且只为这些容器开启 Mount Namespace。所以，这些用户容器之间，原生就是共享 Network 以及其他 Namespace 的。（Kata Containers 的本质，就是一个轻量化虚拟机）

gVisor 虽然现在没有任何优势，但是这种通过在用户态运行一个操作系统内核，拦截部分系统调用，来为应用进程提供强隔离的思路，的确是未来安全容器进一步演化的一个非常有前途的方向。不过，gVisor 就会因为需要频繁拦截系统调用而出现性能急剧下降的情况。此外，gVisor 由于要自己使用 Sentry 去模拟一个 Linux 内核，所以它能支持的系统调用是有限的，只是 Linux 系统调用的一个子集。

Firecracker 和 Kata Containers 的本质原理，其实是一样的。只不过， Kata Containers 默认使用的 VMM 是 Qemu，而 Firecracker，则使用自己编写的 VMM。

### 监控

#### 一个监控系统的典型架构

采集器：用于收集监控数据，业界有不少开源解决方案，大同小异，总体分为推拉两种模式，各有应用场景。Telegraf、Exporters用得最广泛，Grafana- Agent和Categraf是后来者，当然还有Datadog--Agent这种商业解决方案，我的建议是优先考虑Categraf，相对而言，它使用起来更加便捷。如果有些场景Categraf没有覆盖，可以考虑辅以一些特定的Exporter。

时序库：用于存储时序数据，是一个非常内卷的行业，有很多开源方案可供选择。如果规模比较小，1000台机器以下，通常一个单机版本的Prometheus 就够用了。如果规模再大一些，建议你考虑VictoriaMetrics，毕竟架构简单，简单的东西可能不完备，但是出了问题容易排查，更加可控。

告警引擎：用于做告警规则判断，生成告警事件。这是监控系统的一个重要组成部分，通常是基于固定阈值规侧来告警。当然，随着时代的发展，也有系统支持统计算法和机器学习的方式做告警预判，我觉得是可以尝试的。AiOps概念中最容易落地，或者说落地之后最容易有效果的，就是告警引擎。不过 Google SRE的观点是不希望在告警中使用太多magic的手段，这个就见仁见智了。

数据展示：用于渲染展示监控数据。最常见的图表就是折线图，可以清晰明了地看到数据变化趋势，有些人会把监控大盘配置得特别花哨，各种能用的图表类型都用一下，这一点我不敢苟同，我还是觉得实用性才是最核心的诉求。很多监控系统会内置看图功能，开源领域最成熟的就是Grafana，如果某个存储无法和Grafana对接，其流行性都会大打折扣。

#### 我们要监控啥子东西

Google的四个黄金指标

延迟：服务请求所花费的时间，比如用户获取商品列表页面调用的某个接口， 花费30毫秒。这个指标需要区分成功请求和失败请求，因为失败的请求可能会立刻返回，延迟很小， 会扰乱正常的请求延迟数据。

流量：HTTP服务的话就是每秒HTTP请求数，RPC服务的话就是每秒 RPCCal‖l的数量，如果是数据库，可能用数据库系统的事务量来作为流量指标。

**错误**：请求失败的速率，即每秒有多少请求失败，比如HTTP请求返回了 500错误码，说明这个请求是失败的，或者虽然返回的状态码是200，但是返回的内容不符合预期，也认为是请求失败。

饱和度：描述应用程序有多“满”，或者描述受限的资源，比如CPU密集型应用，CPU使用率就可以作为饱和度指标。

### 常见问题

Linux容器是共享宿主机内核的，宿主机的内核决定了容器内应用真正能够使用到的内核版本。

资源限制仅通过cgroups限制了固定几种资源的使用不会超限，但是它既不能隔离被共享的硬件比如L3 cache，也不能有效地防止容器逃逸的问题。

Windows应用需要的Windows内核能力是不可能由Linux宿主机提供的，但是基于虚拟化的容器可以提供独立的guest kernel所以没问题。

默认情况下宿主机的/proc文件系统是不被Linux容器隔离的，而top命令的数据源就是proc。

容器镜像都是只读层，可读写层、init层等是容器运行起来之后挂载上去的。

Linux容器的Volume，本质上就是一个挂载在可读写层的宿主机目录。既不是层，也不是任何层的一部分。

**Kubernetes的设计目标是一个容器化基础设施管理系统**，它的目标用户是基础设施以及平台层系统研发人员，不是业务研发人员。资源调度是Kubernetes的一个基础功能但是并不是Kubernetes的核心功能。

除了InitContainer之外，Pod中的其他容器不保证顺序。

Kubernetes中并没有“应用”的概念，Deployment是一种**Workload**(工作负载)

Deployment的滚动升级仅调节Pod实例数量，不调整不同版本的流量

StatefulSet控制器升级Pod严格按照一个一个的顺序来升级，不会同时出现多个版本的Pod(比如蓝绿发布的情况)，这是Deployment才可以做的事情

StatefulSet依靠PV/PVC机制来保证PV实例永远能够跟相应的Pod“绑定”在一起

Controller工作本身并不依赖于WorkQueue,但是声明和使用WorkQueue有助于编写性能更好的Controller,减少阻塞

PVC是用户角度对存储服务的诉求，PV是系统管理员角度对存储实例的描述，StorageClass是一类PV的抽象描述。

PVC跟PV是一对一绑定的，一旦绑定就意味着这个PVC的诉求得到了满足，用户可以使用了。

Kubernetes默认的Service由运行在宿主机上的kube-proxy配置iptables或者IPVS规则来实现，所以不可能在集群外产生作用

Kubernetes调度器使用一个Queue来进行串行调度，不是并发模型

