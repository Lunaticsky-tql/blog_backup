---
title: 如何编写 Hammerspoon Spoon 插件
categories: 小寄巧
tags:
  - Hammerspoon
date: 2023-10-03 17:04:08
---
# 如何编写 Hammerspoon Spoon 插件

[TOC]

## 写在前面

此文章是对Hammerspoon SPOON.md官方文档的翻译。Hmmerspoon是macOS上强大的自动化工具，其采用lua包装了macOS系统中的一些调用。对应于Windows平台上的AutoHotkey，lua语法更加简洁优雅，可玩性也很高。但相比AutoHotkey，相关的资料也较少，想要写出符合自己预期的脚本，还是需要多下功夫阅读官方API文档，多参考英文论坛。将部分内容进行翻译一方面方便自己学习，另一方面也希望更多的Programmer on macOS能够了解这个强大的工具。

## 什么是Spoon?

Spoons （直译：勺子）是纯 Lua 插件，供用户在 Hammerspoon 配置中使用。

作为一个社区，我们已经为 Hammerspoon 创建了许多优秀的配置，但在它们之间共享代码是很困难且兼容性差（不同人写的脚本风格迥异）。为了解决这些问题，我们创建了 Spoons。
用户应该能够下载一个 Spoon 并快速将其集成到自己的配置中，而不用担心它内部在做什么。

之所以能做到这一点，是因为以下两点：

 * Hammerspoon 中有用于从 Spoons 中加载 Lua 代码的自动化脚本
 * Spoons 的作者尽可能坚持使用标准的 API 供用户使用

## 我从哪里可以获得Spoon?

Spoons 的官方资源库是 [https://www.hammerspoon.org/Spoons](https://www.hammerspoon.org/Spoons)（其来源可在 [https://github.com/Hammerspoon/Spoons](https://github.com/Hammerspoon/Spoons)）找到），但作者也可以选择在自己的网站上单独发布。

## 如何安装Spoon?

Spoon应该以`.zip`文件的形式发布。只需下载，解压缩（如果您的浏览器没有自动解压缩），然后双击Spoon。Hammerspoon 会将其安装到 `~/.hammerspoon/Spoons/` 中。

## 如何使用Spoon？

你需要做两步工作：一是加载Spoon，二是将其集成到您的配置中。
希望 Spoon 附带了一些文档，可以在其主页或 `~/.hammerspoon/Spoons/NAME.spoon` 中找到。在那里，你可以找到 Spoon 所提供的 API 的一些文档，以及它的一些特殊要求。

### 加载Spoon

对于大多数Spoon，只需在 Hammerspoon 配置中添加 `hs.loadSpoon("NAME")`（注意 `NAME` **不应**包含 `.spoon` 扩展名）。这将使Spoons在全局 Lua 命名空间中以 `spoon.NAME` 的形式存在。

加载Spoon后，如果Spoon有`start()`方法，您有责任在使用前调用该方法。

请注意，`hs.loadSpoon()` 使用 `package.path` 来查找 Spoons。因此，您可以将其他路径添加到 `package.path` 中，让它在其他路径下查找 Spoons，如下所示：

```lua
-- 也在 ~/.hammerspoon/MySpoons 中查找Spoon
package.path = package.path .. ";" .. hs.configdir .. "/MySpoons/?.spoon/init.lua"
```

如果你正在开发 Spoons，这将非常有用。

### 集成到您的配置中

在大多数情况下，API 应大致采取这种形式：

* `NAME:init()` - 这将由 `hs.loadSpoon()` 自动调用，并将完成所需的初始设置工作，但通常不应开始执行任何操作。
* `NAME:start()` - 如果需要任何类型的后台工作，该方法将启动它
* `NAME:stop()` - 如果正在运行任何类型的后台工作，本方法将停止它
* `NAME:bindHotkeys(mapping)` - 该方法用于告诉 Spoon 如何为其各种功能绑定热键。根据 Spoon 的不同，这些热键可以立即绑定，也可以在调用 `:start()`时绑定。该方法只接受一个参数，即一个表格：

```lua
  { someFeature = {{"cmd", "alt"}, "f"},
    otherFeature = {{"shift", "ctrl"}, "b"}}
```

Spoon 还应提供一些标准元数据：

 * `NAME.name` - 包含 Spoon 名称的字符串
 * `NAME.version` - 包含 Spoon 版本号的字符串
 * `NAME.author` - 包含Spoon 作者姓名/电子邮件的字符串
 * `NAME.license` - 包含Spoon 许可证信息的字符串，最好包含许可证的 URL

可选项

 * `NAME.homepage` - 包含Spoon 主页URL的字符串。

除此以外，许多 Spoon 还会提供额外的 API 点，你可以查阅它们的文档了解更多信息。

### 如何创建一个 Spoon？

最终，Spoon可以是一个以`.spoon`结尾的目录，并在其中包含一个`init.lua`。

然而，当Spoon符合API约定时，就能为Hammerspoon的用户提供最大的价值，允许用户以非常相似的方式与所有的Spoon进行交互。

### 应用程序接口约定

#### 命名

 * Spoon名称应使用标题大小写
 * Spoon方法/变量/常量等应使用 camelCase

#### 初始化

当用户调用`hs.loadSpoon()`时，Hammerspoon 将从相关的 Spoon 中加载并执行`init.lua`。

一般来说，您不应该在`init.lua`的主范围内执行任何工作、映射任何热键、启动任何计时器/监视器等。取而代之的是，它应简单地准备一个包含稍后使用的方法的对象，然后返回该对象。

如果您返回的对象有一个 `:init()`方法，Hammerspoon 会自动调用它（尽管用户可以覆盖此行为，所以请务必记录您的 `:init()`方法）。

在 `:init()`方法中，您应该做任何必要的工作来为以后的使用准备资源，不过一般来说，您不应该在这里启动任何定时器/监视器等或映射任何热键。

#### 元数据

至少应在对象中包含以下属性：

 * `NAME.name` - Spoon 的名称
 * `NAME.version` - Spoon 的版本
 * `NAME.author` - 您的姓名和可选的电子邮件地址
 * `NAME.license` - 适用于您的 Spoon 的软件许可证，最好带有许可证文本的链接（例如，[https://opensource.org/](https://opensource.org/)

可选项：

 * `NAME.homepage` - Spoon 主页的 URL，例如 GitHub 仓库。

#### 启动/停止

如果您的 Spoon 提供了某种后台活动，例如定时器、监视器、聚光灯搜索等，您通常应使用 `:start()`方法激活它们，并使用 `:stop()`方法停止激活它们。

#### 热键

如果您的 Spoon 提供了用户可以映射到热键的操作，您应该公开一个 `:bindHotKeys()`方法。该方法应接受一个参数，即一个表格。
表中的键应是描述热键执行的操作的字符串，表中的值应是包含修改器和键名/键码的表，以及触发热键时通过 `hs.alert()` 显示的信息。

例如，如果用户想映射两个操作，`show` 和`hide`，他们可以输入

```lua
  {
    show={{"cmd", "alt"}, "s", message="Show"}、
    hide={{"cmd", "alt"}, "h"}
  }
```

现在，您的 `:bindHotkeys()` 方法已拥有将热键绑定到其方法所需的全部信息。

虽然您可能想验证表中的内容，但只要您已经很好地记录了方法，对其范围进行相当有限的限制似乎也是合理的。

函数 `hs.spoons.bindHotkeysToSpec()`可以为您完成大部分艰巨的映射工作。例如，下面的代码可以将动作 `show` 和 `hide` 分别绑定到 `showMethod()` 和 `hideMethod()` 中：

```lua
function MySpoon:bindHotKeys(mapping)
  local spec = {
    show = hs.fnutils.partial(self.showMethod, self),
    hide = hs.fnutils.partial(self.hideMethod, self),
  }
  hs.spoons.bindHotkeysToSpec(spec, mapping)
  return self
end
```

#### 其他

您可以提出任何其他方法，虽然从技术上讲，用户可以访问所有这些方法，但您只应记录您真正打算作为公共 API 使用的方法。

### 文档

#### 编写

Spoon 方法/变量等的文档格式应与 Hammerspoon 自身 API 的文档格式相同。举个例子，一个添加 USB 设备到 Spoon 的方法，当 USB 设备连接时会采取一些行动，可能看起来像这样：

```lua
--- USBObserver:addDevice(vendorID, productID[, name])
--- Method
--- Adds a device to USBObserver's watch list
---
--- Parameters:
---  * vendorID - A number containing the vendor ID of a USB device
---  * productID - A number containing the product ID of a USB device
---  * name - An optional string containing the name of a USB device
---
--- Returns:
---  * A boolean, true if the device was added, otherwise false
```

按照 Hammerspoon 的惯例，方法倾向于返回它们所属的对象（因此方法可以是链式的，例如 `foo:bar():baz()`），但这并不总是合适的。

#### 生成

有几种工具可以对 Hammerspoon 和 Spoons 使用的文档说明进行操作。在最简单的情况下，每个 Spoon 都应包含一个 `docs.json` 文件，该文件只是各种文档strings 的集合。
该文件可使用 Hammerspoon 命令行工具生成（参见 [https://www.hammerspoon.org/docs/hs.ipc.html#cliInstall](https://www.hammerspoon.org/docs/hs.ipc.html#cliInstall)）：

首先在`init.lua`中：

```lua
require("hs.ipc")
hs.ipc.cliInstall()
```

运行一次，会自动下载命令行工具并配置环境变量。然后可以在命令行使用：

```bash
cd /path/too/your/Spoon
hs -c "hs.doc.builder.genJSON(\"$(pwd)\")" | grep -v "^--" > docs.json
```

任何提交到 Spoons 官方仓库的 Spoons 都将由 GitHub 生成并托管其 HTML 文档。

如果您也想为自己的文档生成 HTML/Markdown 版本：

 * 克隆 [https://github.com/Hammerspoon/hammerspoon](https://github.com/Hammerspoon/hammerspoon)
 * 安装所需的 Python 依赖项（例如 Hammerspoon 仓库中的 `pip install --user -r requirements.txt`)
 * 然后在 Spoon 的目录下运行

```bash
/path/to/hammerspoon_repo/scripts/docs/bin/build_docs.py --templates /path/to/hammerspoon_repo/scripts/docs/templates/ --output_dir . --json --html --markdown --standalone .
```

这将搜索当前工作目录中的任何 `.lua` 文件，从中提取 docstrings，并将 `docs.json` 与 HTML 和 Markdown 输出一起写入当前目录。更多选项请参见 `build_docs.py --help` 。

### 加载文件

如果你的 Spoon 不只是`init.lua`那么复杂，你很快就会遇到一个问题，那就是如何加载额外的`.lua`文件或其他类型的资源（如图片）。

不过，有一个简单的方法可以发现 Spoon 在文件系统中的真实路径。只需使用 `hs.spoons.scriptPath()` 函数即可：

```lua
-- 获取 Spoon 的 init.lua 脚本路径
obj.spoonPath = hs.spoons.scriptPath()
```
#### 资源文件

要访问与 Spoon 绑定的资源文件，请使用 `hs.spoons.resourcePath()` 函数：

```lua
-- 获取与 Spoon 绑定的资源的路径
obj.imagePath = hs.spoons.resourcePath("images/someImage.png")
```

#### 代码

不能使用 `require()` 在 Spoon 中加载 `.lua` 文件，而应使用

```lua
dofile(hs.spoons.resourcePath("someCode.lua"))
```

这样，`someCode.lua`文件就会被加载并执行（如果它返回任何内容，你可以从`dofile()`中获取这些值）。
