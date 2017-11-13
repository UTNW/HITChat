## 软件工程实践项目
#### Team：Up To New World(UTNW)
#### Member：Zhang Xinghua/Wei Bowen/Xiao Tengzhao
### 项目选题（自选题目）
**HITChat（面向哈工大师生的交流平台）**

背景：

·贴吧为人们提供了一个宽松的交流平台，人们可以在自由在上面对特定话题进行评论，也可以匿名发表自己的看法。

·今日哈工大目前发表的所有新闻均没有评论功能，师生渴望一个可以交流今日事件的平台。

适应需求：

-能够使用学号注册一个唯一账号，设置密码登入；

-将不同类型的话题归类，并提供查询功能；

-用户可以发布话题，自由评论、匿名评论，删除自己的评论、话题，对话题评论点赞；

-用户可以设置个人中心（包含头像、密码、简介等）；

-面向今日哈工大：使用爬虫技术，将今日哈工大每天发布的新闻和政策集成到系统中，日常发布。

### 项目工作计划
#### **第一次迭代周期工作安排：**
1.搭建python环境，安装virtualenv，并在虚拟环境里面配置flask，安装MySQL数据库和Navicat数据库管理工具

2.构思web网页的基本框架和功能，拟定题目

3.学习flask框架的基本知识，熟悉温习python语法知识

4.学习html语言、css基础知识

5.动手搭建简单的web程序，包括登录、注册、发布问答、问答评论、问答搜索

6.在基础web架构上美化（如：背景图、底部版权条等）、添加新功能：
* 用户注册、登录界面的验证、错误提示以及用户注册信息的安全性管理
* 用户可以在发布问答或评论时上传图片及表情等
* 用户可以对评论和文章进行点赞和评论
* 问答分类（暂定为通知、二手、失物招领、问答咨询、活动五类）
* 用户管理自己的问答及评论（删除、修改等）
* 用户管理界面（自定义用户名、用户头像、注册信息等、可以查看自己发布的文章）

7.搭载到远程服务器上

#### **第二次迭代周期工作安排：**
8.用户消息提醒（当有其他用户回复该问题后，对用户进行短信/邮件等提醒）

9.利用python Web spider技术对今日哈工大上的新闻进行提取，集成到系统中，在发布的同时，并对用户的相关问题进行回答。

10.增加web聊天界面（暂定）

11.搭载到远程服务器上

**Created by UTNW(2017.10.01)**

![](https://github.com/UTNW/HITChat/raw/master/time1.png)

**Created by UTNW(2017.10.01) Update 2017.10.17 2017.11.1**

#### 第一次迭代Burndown Chart
![](https://github.com/UTNW/HITChat/raw/master/BurndownChart.png)

**Created by UTNW(2017.10.01)**


### 2017.10.1-10.7 任务汇总
![](https://github.com/UTNW/HITChat/raw/master/onlyoffice1.jpg)

![](https://github.com/UTNW/HITChat/raw/master/pic.png)

#### 这是HITChat 1.0 版本，目前实现的功能有：注册、登录、发布问答、查询、评论

* 1.在进行该项目之前，必须安装 Flask 以及一些我们会用到的扩展。首选的方式就是创建一个虚拟环境 ,这个环境能够安装所有的东西，而此时我们的主Python不会受到影响。另外一个好处就是这种方式不需要我们拥有root权限。具体参考网站：http://www.pythondoc.com/flask-mega-tutorial/helloworld.html

* 2.该项目中需要用到SQLAlchemy，它提供了SQL工具包及对象关系映射（ORM）工具，将数据可视化，并与数据库相关联

* 3.该项目采用的是MySQL数据库(Server version:5.7.19 MySQL Community Server),需要首先创建需要用到的数据库，如本实验的hitqa数据库

* 4.在models.py文件中是数据模型，当增添新的数据模型时，需要将其重新映射到数据库中，步骤如下：
  首先进入虚拟环境的命令环境下，其次，进入到manage.py项目文件目录下，依次在命令行窗口下执行如下两条命令：python manage.py db migrate 和 python manage.py db upgrade ,映射成功，可到数据库命令行窗口查看

**详细页面展示：**
![](https://github.com/UTNW/HITChat/raw/master/login.png)

![](https://github.com/UTNW/HITChat/raw/master/register.png)

![](https://github.com/UTNW/HITChat/raw/master/first_page.png)

![](https://github.com/UTNW/HITChat/raw/master/question.png)

![](https://github.com/UTNW/HITChat/raw/master/answer.png)

###### 总结：在我们小组成员的共同努力下，第一次任务基本完成
**Created by UTNW(2017.10.09)**


### 2017.10.8-10.14 任务汇总
![](https://github.com/UTNW/HITChat/raw/master/onlyoffice2.jpg)

#### 这是HITChat 2.0 版本，目前实现的功能有：注册、登录、发布问答、查询、评论、用户管理
##### 本周期任务：
* 在基础web架构上美化（如：背景图、底部版权条等）、添加新功能：
>* 用户信息的安全管理
>* 登录注册页面的美化
>* 发布问答时上传图片、表情
>* 用户管理界面（自定义用户头像、管理自己的问答交流等）

**详细页面展示：**
![](https://github.com/UTNW/HITChat/raw/master/login1.png)

![](https://github.com/UTNW/HITChat/raw/master/register1.png)

![](https://github.com/UTNW/HITChat/raw/master/question1.jpg)

![](https://github.com/UTNW/HITChat/raw/master/detail1.jpg)

![](https://github.com/UTNW/HITChat/raw/master/user1.jpg)

###### 总结：在我们小组成员的共同努力下，第二次任务按照预定计划基本完成
**Created by UTNW(2017.10.17)**


### 2017.10.15-10.21 任务汇总
![](https://github.com/UTNW/HITChat/raw/first_iteration/onlyoffice3.jpg)

#### 这是HITChat 2.1 版本，目前实现的功能有：注册、登录、发布问答、查询、评论、个人中心界面，用户对评论和文章进行点赞和评论。

##### 本周任务：
*实现用户对评论和文章进行点赞和评论（二次评论）

**详细页面展示：**

![](https://github.com/UTNW/HITChat/raw/first_iteration/praise1.png)

![](https://github.com/UTNW/HITChat/raw/first_iteration/praise2.png)

###### 总结：在我们小组成员的共同努力下，第三次任务按照预定计划基本完成
**Created by UTNW(2017.10.24)**



### 2017.10.22-10.28 任务汇总

#### 这是HITChat 2.2 版本，目前实现的功能有：注册、登录、发布问答、查询、评论、用户管理、话题分类、即时交流
##### 本周期任务：
* 在基础web架构上美化（如：背景图、底部版权条等）、添加新功能：
* 问答分类（暂定为通知、二手、失物招领、问答咨询、活动五类）

**详细页面展示：**
![](https://github.com/UTNW/HITChat/raw/master/user.png)

![](https://github.com/UTNW/HITChat/raw/master/huati.png)

![](https://github.com/UTNW/HITChat/raw/master/hitchat.jpg)

###### 总结：在我们小组成员的共同努力下，第四次任务按照预定计划基本完成
**Created by UTNW(2017.11.1)**

### 2017.10.29-10.13 任务汇总
#### 这是HITChat 2.3 版本，目前实现的功能有：注册、登录、发布问答、查询、评论、用户管理、话题分类、即时交流、新闻速览、在线聊天Robot
##### 本周期任务：
* 用户管理自己的问答及评论
* 暂时将网站程序搭载到服务器
**Robot详细页面展示：**
![](https://github.com/UTNW/HITChat/raw/master/robot.png)
###### 总结：在我们小组成员的共同努力下，第一次迭代任务按照预定计划基本完成
**Created by UTNW(2017.11.13)**
```
我们已经将网站（目前只有基本功能)部署到服务器上，可访问： http://www.hitchat.cn:5000 查看
```