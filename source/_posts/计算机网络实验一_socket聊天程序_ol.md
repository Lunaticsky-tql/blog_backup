---
title: 计算机网络实验一_socket聊天程序
categories: 作业
date: 2022-12-21 10:00:00
tags:
  - 寄网
abbrlink: 54779
---
# 计算机网络实验一_Socket聊天程序

2013599 田佳业

## 实验要求

使用流式Socket，设计一个两人聊天协议，要求聊天信息带有时间标签。请完整地说明交互消息的类型、语法、语义、时序等具体的消息处理方式。拓展实现功能（如群聊、多线程等）

## 程序流程展示

### 模块说明

此实验使用了Windows多线程的方式实现了多人聊天功能，流程和协议设计如下图所示：

![connect](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210335407540_697_20221026193748648308_976_connect.png)

对于每一个用户的聊天过程，分为建连阶段和聊天阶段。

### 建连阶段

#### 流程设计

##### 服务器

服务器主要做了以下工作：

+ 设置最大聊天人数并在接收连接前验证

+ 建立socket，绑定ip和端口号，进入监听模式进行等待

+ 客户端连接后，得到客户端输入的用户名，验证是否在已有用户列表，若否，为其单独创建线程并在`socket`池中为其分配`socket`

+ 连接成功，向其发送欢迎信息并通知在线的用户

+ 每当用户连接成功后，服务器显示用户信息及连接时间。

注：下图包含了一次客户端断开重连的过程，可以看到服务器能够正确的识别这一过程，且对在线人数进行更新。

![image-20221022211508575](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210336576641_482_20221026193750618844_199_image-20221022211508575.png)

##### 客户端 

+ 由于程序默认在`localhost`上运行，因此客户端只需要手动选择正确的端口号与服务器进行连接，若连接失败，退出程序。

+ 之后输入用户名，这里需要注意用户名不能与关键字(在该程序中为`quit`和`all`)。当然在本地验证即可。等待服务器确认信息后，建立两个线程：发送和接收线程，以防止阻塞。

![客户端](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210337806803_216_20221026193752409499_274_image-20221022211345244.png)

下面是上线通知的实现效果：

![上线通知](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210339188874_417_20221026193754614735_579_image-20221022211828762.png)

#### 协议设计

由于此部分界限明确，且不涉及与其他服务器的交互，为保证速度和效率，从简设计即可。只传输最需要的东西。并且由于这个过程顺序是且必须是确定的，串行执行共用端口不至混淆。

### 聊天阶段

#### 流程设计

##### 服务器事件

程序在调度设计中着重注意了一点：在整个聊天室中，服务器可以作为“管理员”向用户发送消息，而不仅仅实现转发功能。为了实现这一点，程序采用了子线程的方式。主线程除了创建socket便将与客户端建立连接的过程交给子线程去干，服务端负责转发的线程由子线程创建。主线程自己则进入等待输入的过程。

主线程有输入分一下两种情况：正常字符串和`exit`。正常字符串会即时群发给所有在线用户并标记为`SERVER` 信息。若输入`exit`则退出服务器，并在退出之前向客户端群发通告，并同时退出客户端的程序。

以下两幅图片展示了客户端收到的对应的情况。

![image-20221022214111930](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210340324749_887_20221026193756459285_459_image-20221022214111930.png)

![image-20221022213615110](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210341264659_427_20221026193758300289_769_image-20221022213615110.png)

##### 客户端事件

按照同样的方式可以实现客户端离线群发功能。不再赘述。当然，断开后删除个人信息并更新计数也是必要的。

##### 私聊和群聊

可以从上述图片中看出客户端命令行有两个参数：发送对象和消息。

从实现上，这两种方式没有本质的区别。稍微需要注意的一些细节主要是群发不需要发给请求方，但私发时如果选择发送给自己，自己仍然可以收到消息。

下图展示了私聊和群聊的结果。

![image-20221022224632714](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210343217430_922_20221026193759994557_881_image-20221022224632714.png)

![image-20221022224533046](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210344165219_729_20221026193801774887_602_image-20221022224533046.png)

#### 协议设计

协议设计中关注了一下几点：

1. 在线状况下，根据`socket ID`和用户信息表，可以知道是谁发的，因此传递报文时发送者只需要向服务器传递接受者是谁，服务器转发时将对应字段改为发送者姓名即可。这样虽然增加了服务器压力，但能够有效减少报文长度。

2. 控制位仅需一个字节。当然这就像`HTTP`状态码一样，是建立在共识之上的。

3. 消息中需要包含时间戳。因为聊天程序中的时间是需要以发送时间为准的。当然接收时间可以从系统获得，基于此也可以进行时延计算。

以下是程序中关于协议中控制部分的宏定义：

```c++
#define NEW_C 'N' // new client
#define PUB_C 'P' // public message
#define PRI_C 'R'  // private message
#define QUIT_C 'Q' // quit
#define HELLO_C 'H' // hello message from server
#define EXIT_C 'T' // exit message from server (server is closed)
#define ERR_C 'E' // error message from server
#define SERVER_C 'V' // normal server message
```

## 程序代码解释

具体代码的含义大多在程序中有注释。下面的文字叙述部分主要着眼函数和线程模块划分和功能实现上。

C++中对字符串的处理`char*`和`string`各有各的优势，有时也会出现各种奇怪的坑，在写代码时一度让人很头疼，因此也在某些地方会有一些不太优雅的写法。

### 环境配置

在`cmake`项目中进行`socket`编程需要在CMakeLists中添加以下内容，否则不能正常编译：

```cmake
cmake_minimum_required(VERSION 3.21)
project(chatting)
set(CMAKE_EXE_LINKER_FLAGS "-static")
set(CMAKE_CXX_STANDARD 14)
link_libraries(ws2_32 wsock32)
add_executable(server server.cpp)
add_executable(client client.cpp)
```

需额外包含的头文件：

```cmake
#include <windows.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")
```

### 工具类

`color.h`以及部分`helper.h`的代码主要定义了一些与控制台颜色以及格式化输出显示相关的宏及函数。

`print_toggle`主要用来格式化打印控制台输出。

```
print_toggle(const string& type,const string &txt,const string& time_str="")
```

第一个参数是打印格式，取值是下面的宏定义，决定了输出以怎样的颜色和格式进行。第二个参数是内容。并附带可选参数时间。

宏的定义如下：

```c++
//message datagram parameters
#define NAME_SIZE 12
#define TXT_SIZE 125
#define MSG_SIZE 144
#define TIME_SIZE 6
#define TXT_PTR 1
#define TIME_PTR 126
#define NAME_PTR 132
//console line type parameters
#define ERR "E"
#define INFO "I"
#define NEW "N"
#define LOG "L"
#define TIP "T"
#define SUC "S"
#define WARN "W"
#define SERVER "V"
#define GONE "G"
#define DUL "D" // dulplicate name
#define HELLO "H"
#define PUB "P"
#define PRI "R"
```

第一部分主要是方便对数据保处理时使用，第二部分则是在控制台上显示相关命令是需要的宏。

### 初始化工作

#### 服务器端

```c++
    //initialize websocket
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        print_toggle(ERR, "WSAStartup failed");
        return -1;
    }
    print_toggle(LOG, "WSAStartup success");
    SOCKET sock_server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    SOCKADDR_IN server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.S_un.S_addr = inet_addr(LOCALHOST);
    bind(sock_server, (SOCKADDR *) &server_addr, sizeof(SOCKADDR));
    if (listen(sock_server, 5) == SOCKET_ERROR) {
        print_toggle(ERR, "listen failed");
        return 0;
    }
    print_toggle(LOG, "listen success");
```

#### 客户端：

```c++
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        print_toggle(ERR, "WSAStartup failed");
        return -1;
    }
    print_toggle(LOG, "WSAStartup success");
    SOCKET sockClient = socket(AF_INET, SOCK_STREAM, 0);
    print_toggle(TIP, "the chat room is on the localhost");
    print_toggle(TIP, "please input port:");
    cin >> port;
    SOCKADDR_IN addrSrv;
    addrSrv.sin_family = AF_INET;
    addrSrv.sin_port = htons(port);
    addrSrv.sin_addr.S_un.S_addr = inet_addr(LOCALHOST);

    if (connect(sockClient, (SOCKADDR *) &addrSrv, sizeof(SOCKADDR)) != 0) {
        print_toggle(ERR, "connect failed");
        return -1;
    }
    print_toggle(SUC, "connect success", get_time_str());
```

这一部分是服务器端创建`socket`和客户端连接`socket`必需的代码，课上也有讲述，此处不一一详细说明。

### 服务器进程

#### 主线程

这一部分主要做的工作是初始化套接字池，并使用`client_manager`函数创建线程，以监听客户端连接。之后便监听输入以控制服务器群发消息或退出。另外，如果没有客户端连接，显然套接字池中所有套接字都不可用，什么也不用做。

```c++
    //initialize socket array
    for (unsigned long long &sock_connect: sock_connects) {
        sock_connect = INVALID_SOCKET;
    }
    //create a thread to handle new clients
    HANDLE hThread = CreateThread(nullptr, 0, client_manager, (LPVOID) &sock_server, 0, NULL);
    if (hThread == nullptr) {
        print_toggle(ERR, "create thread failed");
        return 0;
    }
    //input "exit" to exit
    while (true) {
        char input[100];
        cin.getline(input, 100);
        if (strcmp(input, "exit") == 0) {
            // tell all clients that the server is going to shut down
            char msg[MSG_SIZE];
            memset(msg, 0, MSG_SIZE);
            msg[0] = EXIT_C;
            string content = "server has shut down";
            for (int i = 0; i < TXT_SIZE; i++) {
                msg[TXT_PTR + i] = content[i];
            }
            broadcast(msg, -1);
            //stop the client_manager thread
            TerminateThread(hThread, 0);
            //close server socket
            closesocket(sock_server);
            break;
        } else {
            //send msg to all clients
            char msg[MSG_SIZE];
            memset(msg, 0, MSG_SIZE);
            msg[0] = SERVER_C;
            char txt[TXT_SIZE];
            strcpy(txt, input);
            for (int j = 0; j < TXT_SIZE; j++) {
                msg[j + TXT_PTR] = txt[j];
            }
            //add time
            char time[TIME_SIZE];
            strcpy(time, get_time_str().c_str());
            for (int j = 0; j < TIME_SIZE; j++)
                msg[j + TIME_PTR] = time[j];
            broadcast(msg);
        }
    }
    return 0;
}
```

其中的`broadcast`函数便是群发消息所使用的是。下面看其实现：

```c++
void broadcast(char msg[MSG_SIZE], int id = -1) {
    for (int i = 0; i < MAX_CLIENT; i++) {
        if (sock_connects[i] != INVALID_SOCKET && i != id) {
            //we don't send the message to the sender
            send(sock_connects[i], msg, MSG_SIZE, 0);
        }
    }
}
```

依次检查`socket`池，然后给有效且不是`id`对应的socket发送消息。

#### 客户端连接线程

`[[noreturn]]`表明这个函数自始至终监听新加入的`socket`。连接时服务器不提示，发送用户名时服务器进行第一次消息接收并根据情况发送欢迎信息或要求客户端重新输入用户名。每次接收消息循环结束，表示有客户端进入或离开，更新一次在线信息，并启动`handle_msg`线程进行消息转发。

```c++
[[noreturn]] DWORD WINAPI client_manager(LPVOID lparam) {
    //accept new clients
    auto *sock_server = (SOCKET *) lparam;

    while (true) {
        int index = 0;
        for (; index < MAX_CLIENT; index++) {
            if (sock_connects[index] == INVALID_SOCKET)
                break;
        }
        if (index == MAX_CLIENT) {
            print_toggle(WARN, "the server is full");
            continue;
        }
        SOCKADDR_IN addrClient;
        int lenAddr = sizeof(SOCKADDR);
        sock_connects[index] = accept(*sock_server, (SOCKADDR *) &addrClient, &(lenAddr));
        if (sock_connects[index] == SOCKET_ERROR) {
            print_toggle(ERR, "could not accept client!");
            sock_connects[index] = INVALID_SOCKET;
            continue;
        }
        while (true) {
            char name[NAME_SIZE];
            recv(sock_connects[index], name, NAME_SIZE, 0);
            if (username_map.find(string(name)) == username_map.end()) {
                username_map.insert(pair<string, int>(string(name), index));
                send(sock_connects[index], HELLO, 1, 0);
                string new_client = "new client: " + string(name) + " entered the chat room";
                string online = "online:" + to_string(username_map.size());
                //get the id of the new client
                int id = username_map[string(name)];
                print_toggle(INFO, new_client,get_time_str());
                // broadcast
                char msg[MSG_SIZE];
                memset(msg, 0, MSG_SIZE);
                for (int j = 0; j < TXT_SIZE; j++)
                    msg[j + TXT_PTR] = new_client.c_str()[j];
                msg[0] = NEW_C;
                //add time
                char time[TIME_SIZE];
                strcpy(time, get_time_str().c_str());
                for (int j = 0; j < TIME_SIZE; j++)
                    msg[j + TIME_PTR] = time[j];
                broadcast(msg, id);
                break;
            } else {
                send(sock_connects[index], DUL, 10, 0);
            }
        }
        HANDLE h_thread_c=CreateThread(nullptr, 0, handle_msg, (LPVOID) &sock_connects[index], 0, nullptr);
        CloseHandle(h_thread_c);
        string online = "online: " + to_string(username_map.size());
        print_toggle(INFO, online,get_time_str());
    }
}
```

#### 消息转发线程

消息转发线程主要根据收到的报文控制段对消息进行不同的处理并转发。同时在服务器端输出日志，如下图所示。

![image-20221022225008715](https://raw.githubusercontent.com/Lunaticsky-tql/blog_articles/main/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E5%AE%9E%E9%AA%8C%E4%B8%80_socket%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BA%8F/20230828210345322153_660_20221026193803523871_125_image-20221022225008715.png)

在程序中除了根据姓名找`socket id`,也常常出现反着找的情况。

这一部分需要注意的点是在`PRI_C`即私密聊天情况下，如果客户端给出的姓名不在当前上线用户的范围之内，会单独给发送者提示。

```c++
DWORD WINAPI handle_msg(LPVOID lparam) {
    auto *socket = (SOCKET *) lparam;
    int id = 0;
    for (int i = 0; i < MAX_CLIENT; i++) {
        if (sock_connects[i] == *socket) {
            id = i;
            break;
        }
    }
    // listen to the message from the client
    while (true) {
        char from_user[NAME_SIZE];
        char msg[MSG_SIZE];
        char content[TXT_SIZE];
        memset(from_user, 0, NAME_SIZE);
        memset(msg, 0, MSG_SIZE);
        memset(content, 0, TXT_SIZE);
        int ret = recv(*socket, msg, MSG_SIZE, 0);
        if (ret == SOCKET_ERROR) {
            print_toggle(WARN, "client closed unexpectedly");
            closesocket(*socket);
            //remove the socket from the list
            sock_connects[id] = INVALID_SOCKET;
            //remove the username from the ma according to the id
            for (auto it = username_map.begin(); it != username_map.end(); it++) {
                if (it->second == id) {
                    username_map.erase(it);
                    break;
                }
            }
            break;
        }
        char type = msg[0];
        //get the username from the map
        string username;
        for (auto &item: username_map) {
            if (item.second == id) {
                username = item.first;
                break;
            }
        }
        switch (type) {
            case QUIT_C: {
                // close client through the client's receive thread
                char msg_exit[MSG_SIZE];
                memset(msg_exit, 0, MSG_SIZE);
                msg_exit[0] = EXIT_C;
                string exit_msg ="you have been moved out of the chat room";
                send(*socket, msg_exit, MSG_SIZE, 0);
                closesocket(*socket);
                sock_connects[id] = 0;
                username_map.erase(username);
                string gone_saying = username + " has quit the chat room at ";
                print_message(GONE, gone_saying,get_time_str());
                //broadcast the quit message
                for (unsigned long long sock_connect: sock_connects) {
                    if (sock_connect != 0) {
                        // attach the content to the message
                        char msg_forwards[MSG_SIZE];
                        memset(msg_forwards, 0, MSG_SIZE);
                        msg_forwards[0] = QUIT_C;
                        for (int i = 0; i < TXT_SIZE; i++) {
                            msg_forwards[TXT_PTR + i] = gone_saying[i];
                        }
                    }
                }
                break;
            }
            case PUB_C: {
                //get the username from the map
                string info="received a public message from ";
                info+=username;
                print_toggle(LOG, info,get_time_str());
                broadcast(msg, id);
                break;
            }
            case PRI_C: {
                //get the username from the map
                string info="received a public message from ";
                info+=username;
                print_toggle(LOG, info,get_time_str());
                //get the target user
                char target_user[NAME_SIZE];
                for (int i = 0; i < NAME_SIZE; i++) {
                    target_user[i] = msg[NAME_PTR + i];
                }
                string target_user_s(target_user);
                //check if the target user is online
                if (username_map.find(target_user) == username_map.end()) {
                    //target user is not online
                    // show log on the server
                    string error_msg = "the target user ";
                    error_msg.append(target_user);
                    error_msg.append(" provided by ");
                    error_msg.append(username);
                    error_msg.append(" is not online!");
                    print_message(LOG, error_msg);
                    //send the error message to the sender
                    char msg_error[MSG_SIZE];
                    memset(msg_error, 0, MSG_SIZE);
                    msg_error[0] = ERR_C;
                    string ree_msg_to_send = target_user_s + " is not online!";
                    for (int i = 0; i < TXT_SIZE; i++) {
                        msg_error[TXT_PTR + i] = error_msg[i];
                    }
                    send(*socket, msg_error, MSG_SIZE, 0);
                } else {
                    string info_pri="received a private message from ";
                    info_pri+=username;
                    print_toggle(LOG, info_pri,get_time_str());
                    //target user is online
                    //send the message to the target user
                    int target_id = username_map[target_user];
                    // replace the target user's name with the sender's name
                    for (int i = 0; i < NAME_SIZE; i++) {
                        msg[NAME_PTR + i] = username[i];
                    }
                    send(sock_connects[target_id], msg, MSG_SIZE, 0);
                }
                break;
            }

        }

    }
}
```



### 客户端进程

#### 主线程

```c++
    if (connect(sockClient, (SOCKADDR *) &addrSrv, sizeof(SOCKADDR)) != 0) {
        print_toggle(ERR, "connect failed");
        return -1;
    }
    print_toggle(SUC, "connect success", get_time_str());
    // send username
    while (true) {
        print_toggle(SERVER, "please input your username:", get_time_str());
        cin >> user_name;
        // check if the name is "all" or "quit" that may cause conflict
        if (strcmp(user_name, "all") == 0 || strcmp(user_name, "quit") == 0) {
            print_toggle(ERR, "the username cannot be set to system reserved words");
            continue;
        }
        send(sockClient, user_name, NAME_SIZE, 0);
        //it must be a buffer, although it is only a char
        char status[1];
        recv(sockClient, status, 10, 0);
        if (status[0] == HELLO_C) {
            print_toggle(SUC, "welcome to the chat room!");
            break;
        }
        print_toggle(ERR, "the username has been used, please input another one");

    }
    HANDLE h_thread[2];
    // separate the sending and receiving thread to avoid blocking
    h_thread[0] = CreateThread(NULL, 0, handlerRec, (LPVOID) &sockClient, 0, NULL);
    h_thread[1] = CreateThread(NULL, 0, handlerSend, (LPVOID) &sockClient, 0, NULL);
    WaitForMultipleObjects(2, h_thread, TRUE, INFINITE);
    CloseHandle(h_thread[0]);
    CloseHandle(h_thread[1]);
    closesocket(sockClient);
    WSACleanup();
    return 0;
```

这一部分进行了用户信息发送以及创建了两个子线程用于发送和收取来自服务器的消息。之后阻塞等待线程结束。

#### 发送线程

首先将报文字段进行初始化，以便根据实际情况填入。循环等待用户输入，并在过程中两次检查是否需要退出。之后根据报文的控制段`TYPE`分别构建不同格式信息。注意在这一阶段并不是程报文中的每一个字段都一定用的到。

```c++
DWORD WINAPI handlerSend(LPVOID lparam) {
    auto *socket = (SOCKET *) lparam;
    char to_user[NAME_SIZE];
    char msg[MSG_SIZE];
    char saying[TXT_SIZE];
    memset(to_user, 0, NAME_SIZE);
    memset(msg, 0, MSG_SIZE);
    memset(saying, 0, TXT_SIZE);
    while (true) {
        print_toggle(TIP, "please input \"user message\", input 'all' to send to all users");
        scanf("%s", to_user);
        // if nothing is input, then continue to ask for input again
        if (strlen(to_user) == 0) {
            cout<<"please input something"<<endl;
            continue;
        }
        //check quit
        if (strcmp(to_user, "quit") == 0) {
            print_toggle(TIP, "you chose to quit the chat room");
            //send quit message to server
            msg[0] = QUIT_C;
            send(*socket, msg, MSG_SIZE, 0);
            return 0;
        }
        scanf("%[^\n]", saying);
        if(strlen(saying) == 0){
            continue;
        }
        //check quit
        if (strcmp(saying, "quit") == 0) {
            print_toggle(TIP, "you have quit the chat room");
            //send quit message to server
            msg[0] = QUIT_C;
            send(*socket, msg, MSG_SIZE, 0);
            return 0;
        }
        //send message to server for forwarding
        if(strcmp(to_user, "all") == 0){
            msg[0] = PUB_C;
            //construct the message
            //content
            for(int i = 0; i < TXT_SIZE; i++){
                msg[i + TXT_PTR] = saying[i];
            }
            // from user
            for(int i = 0; i < NAME_SIZE; i++){
                msg[i + NAME_PTR] = user_name[i];
            }
            //time stamp
            string time_stamp = get_time_str();
            for(int i = 0; i < TIME_SIZE; i++){
                msg[i + TIME_PTR] = time_stamp[i];
            }
            send(*socket, msg, MSG_SIZE, 0);
        }else{
            msg[0] = PRI_C;
            //construct the message
            //content
            for(int i = 0; i < TXT_SIZE; i++){
                msg[i + TXT_PTR] = saying[i];
            }
            // to user
            for(int i = 0; i < NAME_SIZE; i++){
                msg[i + NAME_PTR] = to_user[i];
            }
            //time stamp
            string time_stamp = get_time_str();
            for(int i = 0; i < TIME_SIZE; i++){
                msg[i + TIME_PTR] = time_stamp[i];
            }
            send(*socket, msg, MSG_SIZE, 0);
        }

    }
}
```

#### 接收线程

接收线程是一个解析的过程，并往控制台进行不同格式输出。模式基本类似。

```c++
DWORD WINAPI handlerRec(LPVOID lparam) {
    auto *socket = (SOCKET *) lparam;
    char msg[MSG_SIZE];
    memset(msg, 0, MSG_SIZE);
    while (true) {
        recv(*socket, msg, MSG_SIZE, 0);
        char type = msg[0];
        char content[TXT_SIZE];
        for (int i = 0; i < TXT_SIZE; i++)
            content[i] = msg[i + TXT_PTR];
        char time[TIME_SIZE];
        for (int i = 0; i < TIME_SIZE; i++)
            time[i] = msg[i + TIME_PTR];
        switch (type) {
            // new server message
            case NEW_C:
                print_message(NEW, content);
                break;
            // typed "quit" and all resources are released, exit the program
            case EXIT_C:
                // end of the program
                print_toggle(WARN, content);
                exit(0);
            // public normal message
            case PUB_C:
                // get the sender's name
                char fromUser[NAME_SIZE];
                for (int i = 0; i < NAME_SIZE; i++)
                    fromUser[i] = msg[i + NAME_PTR];
                // print the message
                print_message(PUB, content, time, fromUser);
                break;
            // handle message from server
            case SERVER_C:
                //get the time from the message
                char time_ser[TIME_SIZE];
                for (int i = 0; i < TIME_SIZE; i++)
                    time_ser[i] = msg[i + TIME_PTR];
                print_message(SERVER, content, time_ser);
                break;
            // private message
            case PRI_C:
                // get the sender's name
                char from_user[NAME_SIZE];
                for (int i = 0; i < NAME_SIZE; i++)
                    from_user[i] = msg[i + NAME_PTR];
                // print the message
                print_message(PRI, content, time, from_user);
                break;
        }


    }
}
```

## 思考

在Java程序设计课上，也编写过一个聊天程序。那时只是机械的学习API，虽然也大致了解TCP，UDP的概念，但对于协议的设计还是非常朴素的。虽然本次实验的协议设计也比较简单，但随着学习的深入也会对此有更新的认识。比如很明显的一个设计缺陷是把时间放到了数据段之后。如果把数据段放到最后，可以通过增加长度字段来支持变长数据的传输。其他的比如数据校验等方面也可以继续改进。