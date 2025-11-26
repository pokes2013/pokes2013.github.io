[华为路由器：多区域OSPF协议实验](https://blog.csdn.net/pokes/article/details/131100507?spm=1001.2014.3001.5501)
==================================================================================================

### 一、实验拓扑

![](华为路由器-多区域OSPF协议实验.assets/1c9cf5c2bdf3e553a1850e08f365e64a.png)

### 二、[ospf](https://so.csdn.net/so/search?q=ospf&spm=1001.2101.3001.7020)基本概念复习

*   区域划分：`area0`为骨干区域，其他`area1`、`area2`都为普通区域/常规区域。普通区域必须和骨干区域直接相连。
*   ABR：区域边界路由器。R2、R3位于两个区域的中间，我们称之为`区域边界路由器` ；ABR用来链接骨干区域和普通区域。
*   ASBR ：自制系统边界路由器。进行了重新分布操作的路由器。例如上图中的R5链接着两个自制系统，我们把R5称作`自制系统边界路由器`，自制系统边界路由器用来链接ospf的AS与外部其他的路由。
*   route id：表示ospf的路由器身份ID，身份ID不能重复。一般在配置时都会指定route id。如果没有指定则进行选举。华为的路由器比较特殊，它会选举最先配置好的接口。这个实验我们没有指定route id。手动指定route id：

```
[AR2]router id 2.2.2.2    #手动指定route id
[AR2]q              
<AR2>reset ospf process   #重启ospf进程，使route id生效
```

*   ospf的路由优先级：preference默认为10，可以手动修改 。

![](https://i-blog.csdnimg.cn/blog_migrate/08a112c02f3d9d64b07a560dbc8e7a3d.png#pic_center)

### 三、实验步骤

#### AR1

##### 先按照拓扑图配好IP

```
<Huawei>sys
Enter system view, return user view with Ctrl+Z.
[Huawei]sys AR1
[AR1]int s4/0/0

[AR1-Serial4/0/0]ip add 12.1.1.1 24
[AR1-Serial4/0/0]q
[AR1]un in en
Info: Information center is disabled.
[AR1]
[AR1]int lo 0
[AR1-LoopBack0]ip add 1.1.1.1 24
```

##### 配置[ospf协议](https://so.csdn.net/so/search?q=ospf%E5%8D%8F%E8%AE%AE&spm=1001.2101.3001.7020)

把R1换回也配置到area 1内。

```
[AR1]ospf 1          #1为自治系统ID
[AR1-ospf-1]area 1   #自治系统内的区域ID
[AR1-ospf-1-area-0.0.0.1]network 12.1.1.0 0.0.0.255   #将12.1.1.0网段宣告到area 1区域
[AR1-ospf-1-area-0.0.0.1]network 1.1.1.0 0.0.0.255
```

#### AR2

##### 先按照拓扑图配好IP

```
<Huawei>sys    
Enter system view, return user view with Ctrl+Z.
[Huawei]sys AR2

[AR2]int s4/0/0
[AR2-Serial4/0/0]ip add 12.1.1.2 24
[AR2-Serial4/0/0]q      
[AR2]un in en

[AR2]int g0/0/0
[AR2-GigabitEthernet0/0/0]ip add 23.1.1.2 24
[AR2-GigabitEthernet0/0/0]q

[AR2]int LoopBack 0
[AR2-LoopBack0]ip add 2.2.2.2 24
[AR2-LoopBack0
```

\>由 \[Circle 阅读助手\](https://circlereader.com) 生成