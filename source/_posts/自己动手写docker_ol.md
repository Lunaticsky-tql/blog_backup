---
title: 自己动手写docker
categories: 笔记
tags:
  - 云原生
date: 2024-07-02 23:28:21
---
# 自己动手写docker

## docker run

### 子进程

`/proc/self/exe`，这个表示调用当前文件，目的是再起一个 `docker init` 进程，这个` init` 进程是真正"干活的"进程，一开始和CLI进程一模一样，后面马上将通过 `execve` 变成要跑命令的进程了。CLI进程 通过 `Wait()` 等待其退出。

`int execve(const char *filename, char *const argv[], char *const envp[]);`

这个系统函数，它的作用是执行当前 filename 对应的程序,它会覆盖当前进程的镜像、数据和堆栈等信息，包括 PID，这些都会被将要运行的进程覆盖掉。

也就是说，调用这个方法，将用户指定的进程运行起来，把最初的 init 进程给替换掉，这样当进入到容器内部的时候，就会发现容器内的第一个程序就是我们指定的进程了。

这其实也是目前 Docker 使用的容器引擎runC的实现方式之一。

### Namespace

Docker 使用 namespace 进行隔离。

Namespace 的本质：Linux Namespace 是 Linux 提供的一种内核级别环境隔离的方法，本质就是对全局系统资源的一种封装隔离。

Namespace 的使用：Namespace API 一共 4个，最常用的就是 clone，而 Go 已经把 clone 调用给封装好了，使用时只需要传入不同参数即可控制创建不同 Namespace。

```
ERRO[0000] fork/exec /proc/self/exe: no such file or directory
```

在引入了`systemd`之后的 linux 中，mount namespace 是 shared by default，也就是说宿主机上的`/proc` 目录也被影响了。

mount 官方文档的完整解释：

https://man7.org/linux/man-pages/man7/mount_namespaces.7.html#NOTES

The propagation type assigned to a new mount depends on the propagation type of the parent mount. If the mount has a parent (i.e., it is a non-root mount point) and the propagation type of the parent is MS_SHARED, then the propagation type of the new mount is also MS_SHARED. Otherwise, the propagation type of the new mount is MS_PRIVATE.

Notwithstanding the fact that the default propagation type for new mount is in many cases MS_PRIVATE, MS_SHARED is typically more useful. For this reason, systemd(1) automatically remounts all mounts as MS_SHARED on system startup. Thus, on most modern systems, the default propagation type is in practice MS_SHARED.

Since, when one uses unshare(1) to create a mount namespace, the goal is commonly to provide full isolation of the mounts in the new namespace, unshare(1) (since util-linux version 2.27) in turn reverses the step performed by systemd(1), by making all mounts private in the new namespace. That is, unshare(1) performs the equivalent of the following in the new mount namespace: mount --make-rprivate /

To prevent this, one can use the --propagation unchanged option to unshare(1).

An application that creates a new mount namespace directly using clone(2) or unshare(2) may desire to prevent propagation of mount events to other mount namespaces (as is done by unshare(1)). This can be done by changing the propagation type of mounts in the new namespace to either MS_SLAVE or MS_PRIVATE, using a call such as the following:

mount(NULL, "/", MS_SLAVE | MS_REC, NULL);

按照手册所述一共有四种共享方式:

A call to mount() performs one of a number of general types of operation, depending on the bits specified in mountflags. The choice of which operation to perform is determined by testing the bits set in mountflags, with the tests being conducted in the order listed here:

Change the propagation type of an existing mount: mountflags includes one of MS_SHARED, MS_PRIVATE, MS_SLAVE, or MS_UNBINDABLE.

> Linux手册页的一般章节划分：
>
> 1：用户命令和可执行文件 
>
> 2：系统调用 
>
> 3：库函数、标准C库函数 
>
> 4：特殊文件（通常是`/dev`目录下的设备文件） 
>
> 5：文件格式和约定、配置文件 
>
> 6：游戏和屏幕保护程序 
>
> 7：杂项（例如：协议、文件格式、程序、宏等） 
>
> 8：系统管理命令和守护进程

https://blog.frognew.com/2021/05/relearning-container-07.html

要查看一个进程所属的namespace信息，可以到`/proc/<pid>/ns`目录下查看

### 管道

在使用命名管道前，先需要通过 mkfifo 命令来创建，并且指定管道名字：

```
mkfifo myPipe
```

myPipe 就是这个管道的名称，基于 Linux 一切皆文件的理念，所以管道也是以文件的方式存在，我们可以用 ls 看一下，这个文件的类型是 p，也就是 pipe（管道） 的意思。

匿名管道传参

管道有一个固定大小的缓冲区，一般是4KB。 这种通道是单向的，即数据只能在一个方向上流动。 当管道被写满时，写进程就会被阻塞，直到有读进程把管道的内容读出来。 同样地，当读进程从管道内拿数据的时候，如果这时管道的内容是空的，那么读进程同样会被阻塞，一直等到有写进程向管道内写数据。

和golang的channel性质很像

怎么使用

```
readPipe, writePipe, err := os.Pipe()
```

主要是这句：

`cmd.ExtraFiles = []*os.File{readPipe}` 将 `readPipe` 作为 `ExtraFiles`，这样 cmd 执行时就会外带着这个文件句柄去创建子进程。

一些细节：

如果未启动子进程就往管道中写，写完了再启动子进程，大部分情况下也可以，但是如果 cmd 大于 4k 就会导致永久阻塞。 因为子进程未启动，管道中的数据永远不会被读取，因此会一直阻塞。

```golang
func readUserCommand() []string { 
  // uintptr(3 ）就是指 index 为3的文件描述符，也就是传递进来的管道的另一端，至于为什么是 3，具体解释如下： /* 因为每个进程默认都会有3个文件描述符，分别是标准输入、标准输出、标准错误。这3个是子进程 一创建的时候就会默认带着的， 前面通过ExtraFiles方式带过来的 readPipe 理所当然地就成为了第4个。 在进程中可以通过index方式读取对应的文件，比如 index0：标准输入 index1：标准输出 index2：标准错误 index3：带过来的第一个FD，也就是readPipe 
  //由于可以带多个FD过来，所以这里的3就不是固定的了。 比如像这样：cmd.ExtraFiles = []*os.File{a,b,c,readPipe} 这里带了4个文件过来， 分别的index就是3,4,5,6 那么我们的 readPipe 就是 index6,读取时就要像这样：pipe := os.NewFile(uintptr(6), "pipe") */ 
  pipe := os.NewFile(uintptr(fdIndex), "pipe")
  msg, err := io.ReadAll(pipe) 
  if err != nil { 
    log.Errorf("init read pipe error %v", err) return nil 
  } 
  msgStr := string(msg) 
  return strings.Split(msgStr, " ")
}
```

runC也是这么做的 https://github.com/opencontainers/runc/blob/main/libcontainer/sync.go 

传参过程： 

父进程创建匿名管道，得到 readPiep FD 和 writePipe FD； 

父进程中构造 cmd 对象时通过 ExtraFiles 将 readPiep FD 传递给子进程 

父进程启动子进程后将命令通过 writePipe FD 写入子进程

子进程中根据 index 拿到对应的 readPipe FD 子进程中 readPipe FD 中读取命令并执行 

## cgroup(重点)

### cgroup v1

https://tech.meituan.com/2015/03/31/cgroups.html

典型的子系统介绍如下(v1)：

1. cpu 子系统，主要限制进程的 cpu 使用率。

2. cpuacct 子系统，可以统计 cgroups 中的进程的 cpu 使用报告。

3. cpuset 子系统，可以为 cgroups 中的进程分配单独的 cpu 节点或者内存节点。

4. memory 子系统，可以限制进程的 memory 使用量。

5. blkio 子系统，可以限制进程的块设备 io。

6. devices 子系统，可以控制进程能够访问某些设备。

7. net_cls 子系统，可以标记 cgroups 中进程的网络数据包，然后可以使用 tc 模块（traffic control）对数据包进行控制。

8. freezer 子系统，可以挂起或者恢复 cgroups 中的进程。

9. ns 子系统，可以使不同 cgroups 下面的进程使用不同的 namespace

对 cpu 资源的限制是通过进程调度模块根据 cpu 子系统的配置来完成的；对内存资源的限制则是内存模块根据 memory 子系统的配置来完成的，而对网络数据包的控制则需要 Traffic Control 子系统来配合完成。 而对于 Docker 等 Linux 容器项目来说，它们只需要在每个子系统下面，为每个容器创建一个控制组 （即创建一个新目录），然后在启动容器进程之后，把这个进程的 PID 填写到对应控制组的 tasks 文件中就可以了。

下面的内容是理解Cgroup v1 如何工作的重要部分。

上面这个图从整体结构上描述了进程与 cgroups 之间的关系。最下面的 P 代表一个进程。每一个进程的 描述符中有一个指针指向了一个辅助数据结构 css_set （cgroups subsystem set）。 指向某一个

css_set 的进程会被加入到当前 css_set 的进程链表中。一个进程只能隶属于一个 css_set ，一个 css_set 可以包含多个进程，隶属于同一 css_set 的进程受到同一个 css_set 所关联的资源限制。

上图中的”M×N Linkage”说明的是 css_set 通过辅助数据结构可以与 cgroups 节点进行多对多的关联。 但是 cgroups 的实现不允许 css_set 同时关联同一个cgroups层级结构下多个节点。 这是因为 cgroups 对同一种资源不允许有多个限制配置。

一个 css_set 关联多个 cgroups 层级结构的节点时，表明需要对当前 css_set 下的进程进行多种资源的控制。而一个 cgroups 节点关联多个 css_set 时，表明多个 css_set 下的进程列表受到同一份资源的相同限制。

同样是cgroup v1的一个简要介绍：

https://blog.frognew.com/2021/05/relearning-container-06.html

对于bulkio使用的一个介绍

https://www.cnblogs.com/jimbo17/p/8145582.html

### cgroup v2

Am I using cgroup v2?

Yes if`/sys/fs/cgroup/cgroup.controllers`

is present.

1. In inroups v2, you can only create subgroups in a single hierarchy.
2. In cgroups v2 you can attach processes only to leaves of the hierarchy. You cannot attach a process to an internal subgroup if it has any controller enabled. The reason behind this rule is that processes in a given subgroup competing for resources with threads attached to its parent group create significant implementation difficulties.
3. In cgroups v1, a process can belong to many subgroups, if those subgroups are in different hierarchies with different controllers attached. But, because belonging to more than one subgroup made it difficult to disambiguate subgroup membership, in cgroups v2, a process can belong only to a single subgroup.

cgroup v1 缺点

https://zhuanlan.zhihu.com/p/410053058

cgroup v1  通常是每个层级对应一个子系统，子系统需要挂载使用，而每个子系统之间都是独立的，很难协同工作，比如 memory cgroup 和 blkio  cgroup 能分别控制某个进程的资源使用量，但是blkio cgroup 对进程资源限制的时候无法感知 memory cgroup  中进程资源的使用量，导致对 Buffered I/O 的限制一直没有实现。

目前看到的关于cgroup v2讲的最清晰的资料：

http://arthurchiao.art/blog/cgroupv2-zh/

所有 cgroup 组成一个**树形结构**（tree structure），

- 系统中的**每个进程都属于且只属于**某一个 cgroup；
- 一个**进程的所有线程**属于同一个 cgroup；
- 创建子进程时，继承其父进程的 cgroup；
- 一个进程可以被**迁移**到其他 cgroup；
- 迁移一个进程时，**子进程（后代进程）不会自动**跟着一起迁移；

### systemd

### cgroup使用

限制容器进程最大数量

https://blog.frognew.com/2021/07/relearning-container-30.html

限制CPU使用状况

https://blog.frognew.com/2021/07/relearning-container-29.html

`cpu.cfs_quota_us/cpu.cfs_period_us`决定cpu控制组中所有进程所能使用CPU资源的最大值，而`cpu.shares`决定了cpu控制组间可用CPU的相对比例，这个比例只有当主机上的CPU完全被打满时才会起作用。

## fs

#### pivot_root 和 chroot 有什么区别？

pivot_root 是把整个系统切换到一个新的 root 目录，会移除对之前 root 文件系统的依赖，这样你就能够 umount 原先的 root 文件系统。 而 chroot 是针对某个进程，系统的其他部分依旧运行于老的 root 目录中。

遇到的问题：

```
/bin/sh: ls: not found
```

环境变量这时候和宿主机还是不隔离的，宿主机的/bin不在当前shell的$PATH里就会出现这种情况。

That's the "echo" command followed by a dollar sign (\$) and a zero. \$0 represents the zeroth segment of a command (in the command echo \$0, the word "echo" therefore maps to $1), or in other words, the thing running your command. Usually this is the Bash shell, although there are others, including Dash, Zsh, Tcsh, Ksh, and Fish. volume

> 1、$# 表示参数个数。
>
> 2、$0 是脚本本身的名字。
>
> 3、$1 是传递给该shell脚本的第一个参数。
>
> 4、$2 是传递给该shell脚本的第二个参数。
>
> 5、$@ 表示所有参数，并且所有参数都是独立的。
>
> 6、$$ 是脚本运行的当前进程ID号。
>
> 7、$? 是显示最后命令的退出状态，0表示没有错误，其他表示有错误。

首先要理解 linux 中的 bind mount 功能。

是一种将一个目录或者文件系统挂载到另一个目录的技术。它允许你在文件系统层级中的 不同位置共享相同的内容，而无需复制文件。

本质：绑定挂载实际上是一个 inode 替换的过程。在 Linux 操作系统中，inode 可以理解为存放文件内容的“对象”，而 dentry，也叫目录项，就是访问这个 inode 所使用的“指针”。

![image-20240406202234088](自己动手写docker.assets/image-20240406202234088.png)

其次，则是要理解宿主机目录和容器目录之间的关联关系。

以`-v /root/volume:/tmp`

参数为例：

1）按照语法`-v /root/volume:/tmp`就是将宿主机`/root/volume`挂载到容器中的

`/tmp`目录。

2）由于前面使用了 pivotRoot 将/root/merged目录作为容器的 rootfs，因此，容器中的根目录实际上就是宿主机上的`/root/merged`目录

3）那么容器中的 /tmp 目录就是宿主机上的 /root/merged/tmp 目录。

4）因此，我们只需要将宿主机 /root/volume目录挂载到宿主机的/root/merged/tmp

目录即可实现 volume 挂载。

进程眼中的文件接口：

file&dir接口层定义了进程在内核中直接访问的文件相关信息，这定义在file数据结构中，具体描述如下：

```
struct file {
   enum { 
      FD_NONE, FD_INIT, FD_OPENED, FD_CLOSED, 
   } status; //访问文件的执行状态 
   bool readable; //文件是否可读 
   bool writable; //文件是否可写 
   int fd; //文件在filemap中的索引值 
   off_t pos; //访问文件的当前位置 
   struct inode *node; //该文件对应的内存inode指针 int open_count; //打开此文件的次数

};
```

而在`kern/process/proc.h`中的proc_struct结构中描述了进程访问文件的数据接口files_struct，其数据结构定义如下：

```
struct files_struct { 
   struct inode *pwd; //进程当前执行目录的内存inode指针
   struct file *fd_array;  //进程打开文件的数组
   atomic_t files_count;  //访问此文件的线程个数
   semaphore_t files_sem;  //确保对进程控制块中fs_struct的互斥访问
};
```

当创建一个进程后，该进程的files_struct将会被初始化或复制父进程的files_struct。当用户进程打开一个文件时，将从fd_array数组中取得一个空闲file项，然后会把此file的成员变量node指针指向一个代表此文件的inode的起始地址。

volume 功能大致实现步骤如下：

- 1）run 命令增加 -v 参数,格式和 docker 一致
  - 例如 -v /etc/conf:/etc/conf 这样
- 2）容器启动前，挂载 volume
  - 先准备目录，其次 mount overlayfs，最后 bind mount volume
- 3）容器停止后，卸载 volume
  - 先 umount volume，其次 umount overlayfs，最后删除目录

注意：第三步需要先 umount volume ，然后再删除目录，否则由于 bind mount 存在，删除临时目录会导致 volume 目录中的数据丢失。

## 后台运行(-d)

https://www.lixueduan.com/posts/docker/mydocker/08-mydocker-run-d/

### ps&log

https://www.lixueduan.com/posts/docker/mydocker/10-mydocker-logs/

主要是需要实现可持久化。和docker类似，将相关信息存到

```
var/lib/docker/containers/{containerId}
```

```go
func NewParentProcess(tty bool, volume, containerId string) (*exec.Cmd, *os.File) {
// 省略其他内存
	if tty {
		cmd.Stdin = os.Stdin
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
	} else {
		// 对于后台运行容器，将 stdout、stderr 重定向到日志文件中，便于后续查看
		dirPath := fmt.Sprintf(InfoLocFormat, containerId)
		if err := os.MkdirAll(dirURL, constant.Perm0622); err != nil {
			log.Errorf("NewParentProcess mkdir %s error %v", dirURL, err)
			return nil, nil
		}
		stdLogFilePath := dirPath + LogFile
		stdLogFile, err := os.Create(stdLogFilePath)
		if err != nil {
			log.Errorf("NewParentProcess create file %s error %v", stdLogFilePath, err)
			return nil, nil
		}
		cmd.Stdout = stdLogFile
		cmd.Stderr = stdLogFile
	}
// ...
}

```

## exec

https://www.lixueduan.com/posts/docker/mydocker/11-mydocker-exec/

**`docker exec` 实则是将当前进程添加到指定容器对应的 namespace 中**，从而可以看到容器中的进程信息、网络信息等。

因此我们的 `mydocker exec` 具体实现包括两部分：

- 根据容器 ID 找到对应 PID，然后找到 Namespace
- 将当前进程切换到对应 Namespace

比较关键的一点在于，Go Runtime 是多线程的，和 setns 冲突，因此需要使用 Cgo 以`constructor` 方式在 Go Runtime 启动之前执行 setns 调用。

最后就是根据是否存在指定环境变量来防止重复执行。

## stop&rm

https://www.lixueduan.com/posts/docker/mydocker/12-mydocker-stop/

容器的本质是进程，那么停止容器就可以看做是结束进程。因此 mydocker stop 的实现思路就是先根据 containerId 查找到它的主进程 PID,然后 Kill 发送 SIGTERM 信号，等待进程结束就好。

https://www.lixueduan.com/posts/docker/mydocker/13-mydocker-rm/

`mydocker rm` 实现起来很简单，主要是文件操作，因为容器对应的进程已经被停止，所以只需要将对应记录文件信息的目录删除即可。

docker 可以通过 `-f` 强制删除运行中的容器，具体见 [moby/delete.go#L92](https://github.com/moby/moby/blob/master/daemon/delete.go#L92)，这里也加一下，指定 force 时先 stop 再删除即可。

## 环境变量

由于原来的 command 实际就是容器启动的进程，所以只需要在原来的基础上，增加一下环境变量的配置即可。

**默认情况下，新启动进程的环境变量都是继承于原来父进程的环境变量，但是如果手动指定了环境变量，那么这里就会覆盖掉原来继承自父进程的变量**。

由于在容器的进程中，有时候还需要使用原来父进程的环境变量，比如 PATH 等，因此这里会使用 os.Environ() 来获取宿主机的环境变量，然后把自定义的变量加进去。

这里看不到环境变量的原因是：exec 命令其实是 mydocker 创建 的另外一个进程，这个进程的父进程其实是宿主机的的进程，并不是容器进程的。

> 因为在 Cgo 里面使用了 setns 系统调用，才使得这个进程进入到了容器内的命名空间

由于环境变量是继承自父进程的，因此**这个 exec 进程的环境变量其实是继承自宿主机的，所以在 exec 进程内看到的环境变量其实是宿主机的环境变量**。

因此需要修改一下 exec 命令实现，使其能够看到容器中的环境变量。

由于进程存放环境变量的位置是`/proc/<PID>/environ`，因此根据给定的 PID 去读取这个文件，便可以获取环境变量。

在文件的内容中，每个环境变量之间是通过`\u0000`分割的，因此以此为标记来获取环境变量数组。

然后再启动 exec 进程时把容器中的环境变量也一并带上：

## 容器网络

关于iptables

https://www.liuvv.com/p/a8480986.html

简单的例子：禁止ssh

```sh
iptables -t filter -A INPUT -p tcp --dport  22 -j DROP
```

利用虚拟网络模拟容器的bridge网络，并通过NAT和DNAT实现与外网互通

https://www.lixueduan.com/posts/docker/10-bridge-network/

## 容器生态

### 什么是容器？

https://blog.frognew.com/2021/06/relearning-container-10.html

- 容器实际上是一种特殊的进程。它使用namespace进行隔离，使用cgroup进行资源限制，并且它还以联合文件系统的形式挂载了单独的rootfs。
- 为了更方便的准备运行容器所需的资源和管理容器的生命周期，还需要容器引擎如containerd。
- 容器镜像实际上就是一种特殊的文件系统，它包含容器运行所需的程序、库、资源配置等所有内容，构建后内容保持不变。在启动容器时镜像会挂载为容器的rootfs。

#### 怎么看容器中进程对应到宿主机的哪个进程？

```
docker inspect 751eb37752e3| grep Pid
```

容器作为一种特殊的操作系统进程，可以在系统的`/proc/<process-id>`中感受它的存在。

### CMD和ENTRYPOINT区别

https://yeasy.gitbook.io/docker_practice/image/dockerfile/entrypoint

### OCI

OCI 开放容器倡议，是一个由科技公司组成的团体，其目的是围绕容器镜像和运行时创建开放的行业标准。他们维护容器镜像格式的规范，以及容器应该如何运行。

OCI 背后的想法是，你可以选择符合规范的不同运行时，这些运行时都有不同的底层实现。

Docker 镜像

许多人所说的 Docker 镜像，实际上是以 Open Container Initiative（OCI）格式打包的镜像。

因此，如果你从 Docker Hub 或其他注册中心拉出一个镜像，你应该能够用 docker 命令使用它，或在 Kubernetes 集群上使用，或用 podman 工具以及任何其他支持 OCI 镜像格式规范的工具。

runc 的几个替代品：

    crun [5]一个用 C 语言编写的容器运行时（相比之下，runc 是用Go编写的。）
    来自 Katacontainers 项目的 kata-runtime [6] 它将 OCI 规范实现为单独的轻量级虚拟机（硬件虚拟化）。
    Google 的 gVisor [7]，它创建了拥有自己内核的容器。它在其运行时中实现了 OCI，称为 runsc。

### nerdctl

The goal of `nerdctl` is to facilitate experimenting the cutting-edge features of containerd that are not present in Docker (see below).

Note that competing with Docker is *not* the goal of `nerdctl`. Those cutting-edge features are expected to be eventually available in Docker as well.

Also, `nerdctl` might be potentially useful for debugging Kubernetes clusters, but it is not the primary goal.

