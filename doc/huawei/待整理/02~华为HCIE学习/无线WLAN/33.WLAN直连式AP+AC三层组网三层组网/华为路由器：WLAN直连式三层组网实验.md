# 华为路由器：WLAN直连式三层组网实验



## 一、实验环境

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210718142504623.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fubml0YTIwMTk=,size_16,color_FFFFFF,t_70)

## 二、创建VLAN

```bash
[huawei]sy AC1
[AC1]un in en
[AC1]vlan batch 100 101 102 800

interface GigabitEthernet0/0/3
 port link-type access
 port default vlan 800
 q

interface Vlanif800
 ip address 192.168.240.1 255.255.255.252
 q
```

## 三、AP上线

AP与AC之间打trunk。将管理vlan100设为trunk的本征vlan。

**什么是本征vlan？**

> 关于本征vlan的概念总是忘记，重新搜索了一下加深一下记忆，总结了几条：
> 1、本征vlan默认是vlan1，并且是可以修改的，修改后，不加tag的帧全都送给本征vlan来在中继端口上传输；
> 2、交换机的access口是不存在本征vlan的概念的，这个概念只存在中继端口上；
> 3、本来所有经过中继口上的帧都应该打上标记的，中继通过allow vlan *** 来放行相关vlan通行，但是交换机之间不管存在穿越帧，还存在交换机之间协商信息的帧，如果将这些帧打上tag，也就是那些交换机管理信息，那么这些信息传递到目的地，并不需要送往对应vlan中，而是让交换机接收的信息，那么这时候就需要本征vlan了，不打tag的帧全送到本征vlan进行传送；
> 4、本征vlan收到带tag的帧是会丢弃的。
>
 默认情况下，Trunk 端口的缺省VLAN 为VLAN1。对 Trunk 端口，执行undo vlan 命令删除端口的缺省VLAN 后，端口的缺省VLAN 配置不会改变的，即使用已经不存在的VLAN 作为缺省VLAN。

```bash
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk pvid vlan 100                #将vlan100配置为本征vlan
 port trunk allow-pass vlan 100 to 101   #允许vlan100和vlan101通过
 q
 
interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk pvid vlan 100                #将vlan100配置为本征vlan
 port trunk allow-pass vlan 100 to 102   #允许vlan100和vlan101通过
 q
```

注意事项：<font color='red'>将vlan100配置为本征vlan，目的是使得AP发来的不打tag的DHCP请求报文，归为vlan100的流量，从而使得AP获取到IP地址。</font><font color='red'>AP和AC之间交互的管理流量都是不打tag的。</font>

查看一下vlan接口信息

```bash
[AC1]dis port vlan
Port                        Link Type    PVID  Trunk VLAN List
-------------------------------------------------------------------------------
GigabitEthernet0/0/1        trunk        100   1 100-101
GigabitEthernet0/0/2        trunk        100   1 100-102
GigabitEthernet0/0/3        access       800   -                               
GigabitEthernet0/0/4        hybrid       1     -                               
GigabitEthernet0/0/5        hybrid       1     -                               
...
```

### 创建AP地址池

这里是基于接口的DHCP配置，用于给AP分配IP地址。

```bash
dhcp enable
interface Vlanif100
 ip address 192.168.100.1 255.255.255.0
 dhcp select interface
 dhcp server dns-list 114.114.114.114 8.8.8.8
```

### 验证AP上线

在AC上查看

```bash
[AC1]dis ip pool interface Vlanif100 used  
  Pool-name        : Vlanif100
  Pool-No          : 0
  Lease            : 1 Days 0 Hours 0 Minutes
  Domain-name      : -
  DNS-server0      : 114.114.114.114 
  DNS-server1      : 8.8.8.8         
  NBNS-server0     : -               
  Netbios-type     : -               
  Position         : Interface       Status             : Unlocked
  Gateway-0        : -               
  Network          : 192.168.100.0
  Mask             : 255.255.255.0
  Logging          : Disable
  Conflicted address recycle interval: -
  Address Statistic: Total       :254       Used        :2          
                     Idle        :252       Expired     :0          
                     Conflict    :0         Disabled    :0      

 -------------------------------------------------------------------------------
  Network section 
         Start           End       Total    Used Idle(Expired) Conflict Disabled
 -------------------------------------------------------------------------------
   192.168.100.1 192.168.100.254     254       2        252(0)       0     0
 -------------------------------------------------------------------------------
 Client-ID format as follows:             
   DHCP  : mac-address                 PPPoE   : mac-address             
   IPSec : user-id/portnumber/vrf      PPP     : interface index             
   L2TP  : cpu-slot/session-id         SSL-VPN : user-id/session-id
 -------------------------------------------------------------------------------
  Index              IP             Client-ID    Type       Left   Status     
 -------------------------------------------------------------------------------
     83  192.168.100.84        00e0-fc59-48f0    DHCP      85055   Used       
    156 192.168.100.157        00e0-fcd9-2cc0    DHCP      85055   Used       
 -------------------------------------------------------------------------------
```

但是现在我们没法分清楚哪个是AP1、AP2，接下来我们可以到AP上分别去查看。



我们看到AP1拿到的地址是192.168.100.84

```bash
#在AP1上查看
[Huawei]dis ip in b
*down: administratively down
^down: standby
(l): loopback
(s): spoofing
(E): E-Trunk down
The number of interface that is UP in Physical is 2
The number of interface that is DOWN in Physical is 0
The number of interface that is UP in Protocol is 2
The number of interface that is DOWN in Protocol is 0

Interface                         IP Address/Mask      Physical   Protocol  
NULL0                             unassigned           up         up(s)     
Vlanif1                           192.168.100.84/24    up         up

[Huawei]ping 192.168.100.1
  PING 192.168.100.1: 56  data bytes, press CTRL_C to break
    Reply from 192.168.100.1: bytes=56 Sequence=1 ttl=255 time=110 ms
    Reply from 192.168.100.1: bytes=56 Sequence=2 ttl=255 time=1 ms
    Reply from 192.168.100.1: bytes=56 Sequence=3 ttl=255 time=1 ms
    Reply from 192.168.100.1: bytes=56 Sequence=4 ttl=255 time=1 ms
    Reply from 192.168.100.1: bytes=56 Sequence=5 ttl=255 time=10 ms

  --- 192.168.100.1 ping statistics ---
    5 packet(s) transmitted
    5 packet(s) received
    0.00% packet loss
    round-trip min/avg/max = 1/24/110 ms
```

AP2拿到了192.168.100.157

```bash
在AP2上查看
<Huawei>dis ip in b
*down: administratively down
^down: standby
(l): loopback
(s): spoofing
(E): E-Trunk down
The number of interface that is UP in Physical is 2
The number of interface that is DOWN in Physical is 0
The number of interface that is UP in Protocol is 2
The number of interface that is DOWN in Protocol is 0

Interface                         IP Address/Mask      Physical   Protocol  
NULL0                             unassigned           up         up(s)     
Vlanif1                           192.168.100.157/24   up         up  
```


我们看到AP1拿到的地址是192.168.100.84，现在我们可以在AC上ping一下

```bash
[AC1]ping 192.168.100.84
  PING 192.168.100.84: 56  data bytes, press CTRL_C to break
    Reply from 192.168.100.84: bytes=56 Sequence=1 ttl=255 time=1 ms
    Reply from 192.168.100.84: bytes=56 Sequence=2 ttl=255 time=1 ms
    Reply from 192.168.100.84: bytes=56 Sequence=3 ttl=255 time=10 ms
    Reply from 192.168.100.84: bytes=56 Sequence=4 ttl=255 time=1 ms
    Reply from 192.168.100.84: bytes=56 Sequence=5 ttl=255 time=1 ms

  --- 192.168.100.84 ping statistics ---
    5 packet(s) transmitted
    5 packet(s) received
    0.00% packet loss
    round-trip min/avg/max = 1/2/10 ms
    
[AC1]ping 192.168.100.157
  PING 192.168.100.157: 56  data bytes, press CTRL_C to break
    Reply from 192.168.100.157: bytes=56 Sequence=1 ttl=255 time=1 ms
    Reply from 192.168.100.157: bytes=56 Sequence=2 ttl=255 time=1 ms
    Reply from 192.168.100.157: bytes=56 Sequence=3 ttl=255 time=1 ms
    Reply from 192.168.100.157: bytes=56 Sequence=4 ttl=255 time=10 ms
    Reply from 192.168.100.157: bytes=56 Sequence=5 ttl=255 time=1 ms

  --- 192.168.100.157 ping statistics ---
    5 packet(s) transmitted
    5 packet(s) received
    0.00% packet loss
    round-trip min/avg/max = 1/2/10 ms
```



## 四、创建用户群地址池

### 用户群A的DHCP

用于给用户群A分配IP地址

```bash
interface Vlanif101
 ip address 192.168.101.1 255.255.255.0
 dhcp select interface
 dhcp server dns-list 114.114.114.114 8.8.8.8
```

### 用户群B的DHCP

用于给用户群A分配IP地址

```bash
interface Vlanif102
 ip address 192.168.102.1 255.255.255.0
 dhcp select interface
 dhcp server dns-list 114.114.114.114 8.8.8.8
```

## 五、增加默认路由

AC增加指向R1出口的默认路由

```
ip route-static 0.0.0.0 0 192.168.240.2
```







未完待续，后续再做拨号的部分。