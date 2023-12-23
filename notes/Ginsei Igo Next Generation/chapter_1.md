# 银星围棋(PSV) 汉化
## 第一章 解包
  
### 得到游戏的pkg文件
  
 安装和配置[nps brower](https://nopaystation.com/faq) (参照FAQ中的*Configuration and Usage*)，在Option中不要勾选*Delete files after successful unpack*。
 
 搜索 *Ginsei Igo* 下载得到游戏的pkg文件。

### 解包pkg
  
  如果在nps brower中配置了*pkg dec tool*，例如 [pkg2zip](https://github.com/mmozeiko/pkg2zip)，则在下载完pkg文件后，会自动解压出包内文件，但是这些文件还是加密的，需要使用 [psvpfstools](https://github.com/motoharu-gosuto/psvpfstools) 继续解密。

  其实，还有个更简单的方法。使用 PSV 模拟器 [Vita3K](https://github.com/Vita3K/Vita3K) 安装pkg文件，安装完后，选择菜单`File`==>`Open Pref Path`，在`ux0\app `中会出现一个该游戏“Title ID”的目录，里面的文件都是已经解密的。

  至此，游戏 rom 文件解包完毕。

  