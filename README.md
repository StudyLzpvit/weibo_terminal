Weibo Terminal
==


----------
## 简介 ##

这个项目是基于weibo api的微博终端客户端项目, 可以运行在Linux或者mac OS的终端。在python3.6 环境下开发

### 特点

 1. **使用方便：** 第一次登陆只需要在配置文件中填入用户名密码即可,可以自动获取token保存在配置文件中以便后续使用。
 
 2. **操作简单：** 命令行操作简单，可定制性较高
 3. **界面简洁：** 只显示重要信息，并以颜色区分，在mac终端还可以看图。

----------
### 使用

将用户名和密码填入***ConfigParser.conf***
直接运行***python main.py*** 即可

 - 暂时分成两个界面 ***home  和detail*** 登陆以后可以默认在home界面。 home 可以理解为主页, 也就是刷微博的那里, detail 可以理解为微博详情页，可以显示评论。
 - help 登陆进去之后可以通过help查看帮助
 
 - home 带有4个参数 分别是-p(页数) -c(每页个数) -m(图片模式) -f(微博类别)
    **这些参数可以有任意个，顺序也不限**
    *例如： **home -p=2 -c=20 -m=1 -f=0**
    代表 获取当前用户第2页,20条微博,图片形式以链接形式放出,微博类型不限*
 - detail 是微博详情页有两个参数-p 和 -c 用于配置评论，意义与home的相同。 例如第8条微博 显示第一页5条评论可以表示为
    ***8 -p=1 -c=5***
 - n 代表下一页
 - p 代表前一页
 - clear 清屏
 - exit 退出


----------
### 展示
##### 主页
![home][1]
<br>
##### 显示图片
![img][2]
<br>
##### 显示评论
![comment][3]



 

----------
### 声明
纯粹无聊做的玩具,功能不全,两天做的目前只能算0.0.1版本，以后会加上写微博,评论,搜索等功能。

有什么意见建议欢迎联系我cugbaoyi@gmail.com

   
 


  [1]: http://111.230.251.140:8000/images/weibo_home.png
  [2]: http://111.230.251.140:8000/images/weibo_img.png
  [3]: http://111.230.251.140:8000/images/weibo_comment.png
