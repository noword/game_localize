# 银星围棋(PSV) 汉化
## 第一章 解包打包
  
### 得到游戏的pkg文件
  
 安装和配置 [nps brower](https://nopaystation.com/faq) (参照FAQ中的*Configuration and Usage*)，在Option中不要勾选 *Delete files after successful unpack*。
 
 搜索 *Ginsei Igo* 下载得到游戏的 pkg 文件。

### 解包pkg
  
  如果在 nps brower 中配置了 *pkg dec tool*，例如 [pkg2zip](https://github.com/mmozeiko/pkg2zip)，则在下载完pkg文件后，会自动解压出包内文件，但是这些文件还是加密的，需要使用 [psvpfstools](https://github.com/motoharu-gosuto/psvpfstools) 继续解密。

  其实，还有个更简单的方法。使用 PSV 模拟器 [Vita3K](https://github.com/Vita3K/Vita3K) 安装 pkg 文件，安装完后，选择菜单 `File` ==> `Open Pref Path`，在`ux0\app `中会出现一个该游戏“Title ID”的目录，里面的文件都是已经解密好的。
  
  这里面的文件修改后，对于安装有 rePatch 插件的实体机，可以直接放在的 `ux0:/rePatch/[Title ID]` 目录下（保持相同路径），即可生效。

  作为一个初涉 PSV 游戏汉化的萌新，我还不知道如何把整个游戏重新打包成 pkg、vpk、mia 格式。希望能有大佬不吝赐教。
  
  *注: 关于zRIF，可以在 tsv 文件中找，也可以在[网站](https://nopaystation.com/browse)上直接搜索得到。*

### 游戏中的自定义文件

这个游戏的结构还是比较简单的，data下面就5个目录，先用16进制编辑器（推荐 [Winhex](https://tool.kanxue.com/index-detail-33.htm)）随便打开看看，就IMG下面有些我们感兴趣的大文件。文件后缀是.T2G，文件开头是T2GF，文件中有多处类似文件名的字符串，这是文件资源包的典型特征。上google搜一圈，没有发现现成的文件格式或解包软件，只能自己写解包和打包的工具了。

首先我们要分析出文件的格式，这里没有太多的捷径可循，只能分享一些经验和技巧：
* 可以同时打开多个文件，比较发现其中的不同。最省事的是用16进制编辑器打开多个窗口后，来回切换，利用视觉残留找不同；也可以使用 [WinMerge](https://winmerge.org/)，打开2个文件后，菜单 `文件` ==> `重新比较` ==> `二进制`；当然也可以使用任何你习惯的二进制比较工具。
  
* 在 Winhex 中选中文件块，菜单 `编辑` ==> `复制选块` ==> `编辑器显示`，粘贴到 Word 编辑器中，选一个等宽的字体，并调小字号。把分析的结果用不同颜色的字进行标注。（这个方法虽然实用但是很土，不知道有没有更方便的工具。）
  

分析的结果如下：

  ![](images/001.JPG)


### 写一个解包打包的程序

接下来是写解包和打包的程序，有的人喜欢分两部分来写，一个用来解包和一个用来打包，好处是通用，能创建新的文件资源包，坏处是工作量比较大；我习惯是写一个资源的类，目标专注于替换里面的内容，这样对于从无到有的创建一个新的资源包，不是非常方便，但是毕竟我们的任务是替换源包里的文件，能少写一些代码就少写一些。

这个类中通常有这些函数：
* **load** 用于载入资源包，传入一个只读的文件句柄当参数。对于小的资源包，一次性载入所有信息，包括所有的资源；对于大的资源包，例如10G以上，则只载入基本的索引信息，并且记住文件句柄，需要读取资源时，再从文件中读取。
* **save** 用于保存资源包，传入一个可写的文件句柄当参数。在 save 之前，需要先执行 load。
* **replace** 传入需要替换的资源的信息，例如索引或文件名，以及替换的内容（bytes 类型）。
* **dump/dump_all** 导出资源包里面的资源。

源码在[这里](../../Ginsei%20Igo%20Next%20Generation/data/)

[t2g.py](../../Ginsei%20Igo%20Next%20Generation/data/t2g.py)  中实现了两个类，`class T2GF` 是最外层的，对应于 .t2g 文件；`class T2gFile` 对应于里面的子文件。

这两个类分别继承自 `NamedStruct` 和 `NamedStructWithMagic`。其中 `NamedStruct` 的主要目的是 ~~尽可能的少写代码。~~ 在 load 和 save 中，按照定义好的格式 `NamedStruct.FORMATS` 进行读写。`NamedStructWithMagic` 外加可以检查文件头。

***
* NamedStruct.FORMATS 的写法：
```python
  FORMATS = (
      ('I', 'index'),        # 32 位无符号整数
      ('52s', 'name_bytes'), # 长度为 52 字节的 bytes
      ('I', 'size'),         # 32 位无符号整数
      ('I', 'aligned_size'), # 32 位无符号整数
  )
```
  第一项是 python 的 struct [格式字符](https://docs.python.org/zh-cn/3/library/struct.html#format-characters)，不能添加[大小端的符号](https://docs.python.org/zh-cn/3/library/struct.html#byte-order-size-and-alignment)，默认是小端对齐；第二项是变量名，经过 load 后，就可以直接在类中使用了。

***
* NamedStructWithMagic.MAGIC 用于检查文件头。注意 MAGIC 变量的类型是 bytes 不是 string。也可以不重新定义，会直接用类名代替。

***

把类完成后，最好再写个 [测试脚本](../../Ginsei%20Igo%20Next%20Generation/data/test.py)，以确保 `load` 后什么都不改，再 `save` 回去，能够和原来的一模一样。

把所有的 t2g 文件复制到 data/backup 下面，执行

```bat
for /r %i in (backup\*.t2g) do t2g.py "%i" --dump_all
```

即可导出所有的文件。由于这个游戏的资源包内没有重名的子文件，所以不用做诸如改名或分别导出到不同的目录里等等的特别处理。当然，讲究点也可以写个即写即用即抛的 [extract.py](../../Ginsei%20Igo%20Next%20Generation/data/extract.py) 脚本。 

把文件导入回去的功能在 [gen.py](../../Ginsei%20Igo%20Next%20Generation/data/gen.py) 中实现。该程序会遍历 backup 中的所有 .t2g 文件，判断在当前目录中是否含有 t2g 的子文件，有的话则进行替换，并把新的 t2g 保存在当前目录。