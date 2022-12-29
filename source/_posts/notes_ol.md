---
title: notes
categories: 测试
tags:
  - test
abbrlink: 29406
date: 2022-12-29 20:17:26
---
查看库的路径

```python
import tensorflow
print(tensorflow.__file__)
```

启动radis

```shell
redis-server.exe redis.windows.conf
```

<img src="https://raw.githubusercontent.com/Lunaticsky-tql/blog_article_resources/main/notes/20221229200836148347_588_image-20220727113222196.png" alt="image-20220727113222196" style="zoom: 33%;" />

gitdir

```
usage: gitdir [-h] [--output_dir OUTPUT_DIR] [--flatten] urls [urls ...]

Download directories/folders from GitHub

positional arguments:
  urls                  List of Github directories to download.

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR, -d OUTPUT_DIR
                        All directories will be downloaded to the specified
                        directory.
  --flatten, -f         Flatten directory structures. Do not create extra
                        directory and download found files to output
                        directory. (default to current directory if not
                        specified)
```

连接mysql

```
mysql -u root -p
```

```python
# 亦可以使用下面语句完成单一单元格中多个变量的输出，但是仅在当前notebook中起作用
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
```

dataspell debug ctrl+f8

adb forward tcp:15511 localabstract:Unity-2048

meld默认使用GBK编码

```
gsettings set org.gnome.meld detect-encodings "['GBK', 'UTF-8', 'ISO-8859-15', 'UTF-16']"
```

test
