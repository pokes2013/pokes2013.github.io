# 一、持续集成及Jenkins的介绍

## 1、软件开发的生命周期

五个阶段：需求分析——需求设计——项目开发——测试——部署



![image-20200912181452971](jenkins学习笔记.assets\image-20200912181452971.png)

## 2、软件开发瀑布模型





![image-20200912182620425](jenkins学习笔记.assets\image-20200912182620425.png)

![image-20200912182922511](jenkins学习笔记.assets\image-20200912182922511.png)



## 3、软件的敏捷开

### 什么是敏捷开发？

敏捷开发的核心是迭代开发与增量开发

### 何为迭代开发？

对于大型软件项目，传统的开发方式是采用一个大周期进行开发，整个过程就是以此“大开发”；

迭代开发的方式则不一样，它将开发过程拆分成多个小周期，即以此“大开发”编程多个“小开发”，每次小开发都是同样的流程，所以看上去就好像重复在做同样的步骤。

举例：

某公司想造一个大推力火箭，将人类送到火星。但是，它不是一开始就造大火箭，而是先造一个最简陋的小火箭。结果，第一次发射就爆炸了，直到第四次发射，才成功进入轨道。然后，开发了中型火箭，九年中发射了70次。最后，才开发重型火箭。如果不采用迭代开发，它可能直到现在还无法上天。



### 何为增量开发？

软件的每个版本，都会新增一个用户可以感知的完整功能。也就是说，按照新增功能来划分迭代。

举例：

房地产公司开发一个10栋楼的小区。如果采用增量开发的模式，该公司第一个迭代就是交付1号楼，第二个迭代交付2号楼……每个跌倒都是完成一栋完整的楼。而不是第一个迭代挖好10栋楼的地基，第二个迭代剑豪每栋楼的骨架，第三个迭代架设屋顶……



### 敏捷开发如何迭代？

虽然敏捷开发将软件开发分成多个迭代，但是也要求，每次迭代都是一个完整的软件开发周期，必须安装软件工程的方法论，进行正规的流程管理

![image-20200912184131022](jenkins学习笔记.assets\image-20200912184131022.png)



### 敏捷开发带来的好处

早起交付

敏捷开发的第一个好处，就是早起交付，从而大大降低成本。

还是以上一节房地产公司为例，如果按照传统的“瀑布流开发模式”，先挖10栋楼的地基，再盖骨架、然后架设屋顶，每个阶段都是等到前一个阶段完成后开始，可能需要两年才能一次性交付10栋楼。也就是说，如果不考虑预售，该项目必须等到两年后才能回款。

敏捷开发是六个月交付1号楼，后面每两个月交付一栋楼。因此，半年就能回款10%，后面每个月都会有现金流，资金压力就大大减轻了。



降低风险

敏捷开发的第二个好处是，及时了解市场需求，降低产品不适用的风险。请想一想，哪一种清空损失比较小：10栋楼都造好以后，才发现卖不出去，还是造好一栋楼，就发现卖不出去，从而改进或停建后面9栋楼？



## 4、什么是持续集成

持续集成（Continuous integration，简称CI）指的是，频繁的将代码集成到主干。

持续集成的目的，就是让产品可以快速迭代，同时还能保持高质量。它的核心措施是，代码集成到主干之前，必须通过自动化测试。只要有一个测试用例失败，就不能集成。

通过持续集成，团队可以快速的从一个功能到另一个功能，简而言之，敏捷软件开发很大一部分都要归功于持续集成。



### 持续集成的流程

提交代码——第一轮测试——构建——第二轮测试——部署——回滚



![image-20200912190855167](jenkins学习笔记.assets\image-20200912190855167.png)





### 持续集成的组成要素

- 一个自动构建过程，从检出代码，编译构建、运行测试，结果记录，测试统计等都是自动完成的，无需人为干预。
- 一个代码存储库，即需要版本控制软件来保障代码的可维护性，同时作为构建过程的素材库，一般使用SVN或者Git;
- 一个持续集成服务器，Jenkins就是一个配置简单和使用方便的持续集成服务器。



![image-20200912191223062](jenkins学习笔记.assets\image-20200912191223062.png)



### 没有持续集成的情形

- 项目做模块集成的时候，发现很多接口都不通==>浪费大量时间

- 需要手动去编译打包最新的代码==>构建过程不透明

- 发布代码，上线，基本靠手工==>脚本乱飞

### 持续集成的好处

- 降低风险，由于持续集成不断去构建，编译和测试，可以很早起就发现问题，所以修复的代价小；
- 对系统健康持续检查，减少发布风险带来的问题；
- 减少重复性工作；
- 持续部署，提供可部署单元宝；
- 持续交付可供使用的版本；
- 增强团队信心。



## 5、Jenkins

### Jenkins的介绍

Jenkins是一个开源软件项目，是基于Java开发的一种持续集成工具，用于监控持续重复的工作，旨在提供一个开放易用的软件平台，使软件的持续集成变成可能。

Jenkins提供了一种易于使用的持续集成系统，使开发者从繁杂的集成中解脱出来，专注于更为重要的业务逻辑实现上。同时Jenkins能实现监控集成中存在的错误，提供详细的日志文件和提醒功能，还能用图表的形式形象地展示项目构建的趋势和稳定性。Jenkins的前身是Hudson，是一个可扩展的持续集成引擎。

Jenkins是一个独立的开源自动化服务器，可以用来自动化，例如构建、测试和部署软件等各种任务。Jenkins可以通过本地系统包、Docker安装，甚至可以在安装Java运行时环境的机器上独立运行。



### Jenkins的特征

- 开源的java语言开发持续集成工具，支持持续集成，持续部署。
- 易于安装部署：可通过yum安装或下载war包以通过docker容器等快速实现安装部署，可方便的web界面配置管理。
- 消息通知及测试报告：集成RSS/Email通过RSS发布构建结果或当构建完成时通过mail通知，生成JUnit/TestNG测试报告。
- 分布式构建：支持Jenkins能够让多台计算机一起构建/测试。
- 文件识别：Jenkins能够跟踪哪次构建生成拿些jar，哪次构建使用哪个版本的jar等。
- 丰富的插件支持：支持扩展插件，你可以开发适合自己团队使用的工具，如：git、snv、maben、docker等。



`Jenkins`只是一个平台，真正运作的都是插件。这就是jenkins流行的原因，因为jenkins什么插件都有 
`Hudson`是Jenkins的前身，是基于Java开发的一种持续集成工具，用于监控程序重复的工作，Hudson后来被收购，成为商业版。后来创始人又写了一个`jenkins`，jenkins在功能上远远超过hudson

Jenkins官网：[https://jenkins.io/](https://www.abcdocker.com/wp-content/themes/begin2.0-1/inc/go.php?url=https://jenkins.io/)

Jenkins下载：http://updates.jenkins-ci.org/

 jenkins的全部镜像：http://mirrors.jenkins-ci.org/status.html

# 二、Jenkins安装和持续集成环境部署

## 持续集成流程说明

![image-20200912232753552](https://img-blog.csdnimg.cn/2020091321123224.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

- 首先，开发人员每天进行代码提交，提交到Git仓库
- 然后，Jenkins作为持续集成工具，使用Git工具到仓库拉去代码到集成服务器，再配合JDK，Maven等软件完成代码编译，代码测试和审查，测试，打包等工作，在这个过程中每一步出错，都需要重新再执行一次整个流程。
- 最后，Jenkins把生成的jar和war包分发到测试服务器或者生成服务器，测试人员或用户就可以访问使用。



## Gitlab代码托管服务器的部署

Gitlab安装

1、安装相关依赖

```
yum -y install policycoreutils openssh-server openssh-clients postfix
```

2、启动ssh服务&设置为开机启动

```
systemctl enable sshd && systemctl start sshd
```

3、设置postfix开机启动和开机自启

postfix支持gitlab发信功能

```
systemctl enable postfix && systemctl start postfix
```

4、防火墙开放ssh以及http服务

```
firewall-cmd --add-serice=ssh --permanent
firewall-cmd --add-serice=http --permanent
firewall-cmd --reload
```

5、下载gitlab并安装

在线下载安装包

```
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-11.1.6-ce.0.el7.x86_64.rpm
```

安装rpm包

```
rpm -ivh gitlab-ce-11.1.6-ce.0.el7.x86_64.rpm
```

修改配置文件gitlab.rb

```
## GitLab configuration settings
##! This file is generated during initial installation and **is not** modified
##! during upgrades.
##! Check out the latest version of this file to know about the different
##! settings that can be configured by this file, which may be found at:
##! https://gitlab.com/gitlab-org/omnibus-gitlab/raw/master/files/gitlab-config-template/gitlab.rb.template
 
 
## GitLab URL
##! URL on which GitLab will be reachable.
##! For more details on configuring external_url see:
##! https://docs.gitlab.com/omnibus/settings/configuration.html#configuring-the-external-url-for-gitlab
#external_url 'http://gitlab.example.com'
external_url 'http://10.10.30.1'        # 修改这个地方
```

如果你需要更改端口，则需要更改：

```
10.10.30.1:82
```

还需要更改配置中的如下：

```
nginx[ 'listen_port' ]= 82
```

这个选项默认是注释的，需要放开

![image-20200912224850709](C:\Users\Anita\Desktop\jenkins学习笔记.assets\image-20200912224850709.png)

重新加载配置文件

```
gitlab-ctl reconfigure
gitlab-ctl restart
```

查看gitlab版本

```
head -1 /opt/gitlab/version-manifest.txt
```

下载汉化包

```
git clone https://gitlab.com/xhang/gitlab.git
```







## Jenkins的安装部署

### 安装openjdk

Jenkins需要依赖JDK,所以先安装JDK1.8(openjdk).在这里有个坑，对于一个初学者来说。老师你给我说JDK1.8我一脸懵逼，我只听过JDK8/9/10....从来就没听说过狗屁1.8，百度找了半天原来是openjdk

如果你想知道openjdk： https://blog.csdn.net/u014116780/article/details/92440115

```
yum -y install java-1.8.0-openjdk*
```

安装目录为：`/usr/lib/jvm`

### 下载Jenkins并安装

这里我们采用国内清华镜像下载

```
wget https://mirrors.tuna.tsinghua.edu.cn/jenkins/redhat-stable/jenkins-2.190.3-1.1.noarch.rpm
rpm -ivh jenkins-2.190.3-1.1.noarch.rpm
```

修改配置文件

```
vim /etc/sysconfig/jenkins
修改
JENKINS_USER="root"
JENKINS_PORT="8888"
```

启动Jenkins

```
systemctl start jenkins
```

浏览器访问

访问地址：10.10.30.2:8888

注意打开之后这里有个初始化的过程需要等待一会

![image-20200913003102633](https://img-blog.csdnimg.cn/2020091321123217.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

然后就会出现下面的界面：

![image-20200913002651867](https://img-blog.csdnimg.cn/2020091321123213.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)



查看密码

```
[root@localhost ~]# cat /var/lib/jenkins/secrets/initialAdminPassword
74d25c29aabc41a38195f197de86d9f2
```

复制到浏览器的管理员密码框内，点击继续。

在这里出现了一片白的状态

![image-20200913003412177](https://img-blog.csdnimg.cn/20200913211231893.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

我们可以从浏览器复制一个标签，然后就会出现内容：

![image-20200913003505416](https://img-blog.csdnimg.cn/2020091321123219.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

在这里我们选择：==选择插件来安装==

![image-20200913003706745](https://img-blog.csdnimg.cn/20200913211232105.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)



![在这里插入图片描述](https://img-blog.csdnimg.cn/20200913211231981.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

![在这里插入图片描述](https://img-blog.csdnimg.cn/202009132112328.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200913211231997.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

到此就部署成功了。

### Jenkins插件的安装

 Jenkins——Manage Jenkins——Manage Piugins ，点击Available

我们先安装中文插件：

Localization: Chinese (Simplified)

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200913211231963.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)

完成之后要重启，在下图箭头处勾选会自动重启。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200913211231961.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)



重启后需要重新登录，默认的账户是admin，密码还是上面查看的密码。下面是查看密码：

```
[root@localhost ~]# cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Jenkins更改国内插件地址

待写

## Jenkins用户权限的管理

在我们开发过程中，有很多用户需要登录到Jenkins中来。那么我们可能需要针对不同用户授予不同的角色和权限。

Jenkins本身对角色和权限的管理比较单一粗略，我们需要通过安装`Role-based Authorization Strategy`插件来实现细致化的权限管理。

![image-20200913010614039](jenkins学习笔记.assets\image-20200913010614039.png)

重启之后我们来到：

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020091321123258.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)



![image-20200913011421310](https://img-blog.csdnimg.cn/20200913211231956.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70#pic_center)



# 三、Jenkins构建Maven项目

