# MSTP



## 一、MSTP简介

### 1、多生成树协议的定义

多生成树协议MSTP（Multiple Spanning Tree Protocol）是IEEE802.1s中定义的生成树协议，通过生成多个生成树，来解决以太网环路问题。

### 2、MSTP的功能

> 在以太网中部署MSTP协议后可实现如下功能：
>
> - 形成多棵无环路的树，解决广播风暴并实现冗余备份。
> - 多棵生成树在VLAN间实现负载均衡，不同VLAN的流量按照不同的路径转发。

## 二、MSTP原理描述

### 1、STP/RSTP的缺陷

> RSTP在STP基础上进行了改进，实现了网络拓扑快速收敛。但RSTP和STP还存在同一个缺陷：由于局域网内所有的VLAN共享一棵生成树，因此无法在VLAN间实现数据流量的负载均衡，链路被阻塞后将不承载任何流量，还有可能造成部分VLAN的报文无法转发。
>

### 2、MSTP对STP和RSTP的改进

> - 为了弥补STP和RSTP的缺陷，IEEE于2002年发布的802.1S标准定义了MSTP。MSTP兼容STP和RSTP，既可以快速收敛，又提供了数据转发的多个冗余路径，在数据转发过程中实现VLAN数据的负载均衡。
> - MSTP把一个交换网络划分成多个域，每个域内形成多棵生成树，生成树之间彼此独立。每棵生成树叫做一个多生成树实例MSTI（Multiple Spanning Tree Instance），每个域叫做一个MST域（MST Region：Multiple Spanning Tree Region）。
> - 所谓生成树实例就是多个VLAN的一个集合。通过将多个VLAN捆绑到一个实例，可以节省通信开销和资源占用率。MSTP各个实例拓扑的计算相互独立，在这些实例上可以实现负载均衡。可以把多个相同拓扑结构的VLAN映射到一个实例里，这些VLAN在端口上的转发状态取决于端口在对应MSTP实例的状态。
>

## 三、MSTP基本概念：

### 1、MST域（MST Region）

- 都启动了MSTP。
- 具有相同的域名。

  - 具有相同的VLAN到生成树实例映射配置。
  - 具有相同的MSTP修订级别配置。

> 一个局域网可以存在多个MST域，各MST域之间在物理上直接或间接相连。用户可以通过MSTP配置命令把多台交换设备划分在同一个MST域内。

### 2、VLAN映射表

VLAN映射表是MST域的属性，它描述了VLAN和MSTI之间的映射关系。

**CST**

> 公共生成树CST（Common Spanning Tree）是连接交换网络内所有MST域的一棵生成树。
>
> 如果把每个MST域看作是一个节点，CST就是这些节点通过STP或RSTP协议计算生成的一棵生成树。
>

**IST**

> 内部生成树IST（Internal Spanning Tree）是各MST域内的一棵生成树。
>
> IST是一个特殊的MSTI，MSTI的ID为0，通常称为MSTI0。
>
> IST是CIST在MST域中的一个片段。

**SST**

> 运行STP或RSTP的交换设备只能属于一个生成树。
>
> MST域中只有一个交换设备，这个交换设备构成单生成树。
>

CIST

> 公共和内部生成树CIST（Common and Internal Spanning Tree）是通过STP或RSTP协议计算生成的，连接一个交换网络内所有交换设备的单生成树。

### 3、域根

  域根（Regional Root）分为IST域根和MSTI域根。一个MST域内可以生成多棵生成树，每棵生成树都称为一个MSTI。MSTI域根是每个多生成树实例的树根。

- **总根：**总根是CIST（Common and Internal Spanning Tree）的根桥。

- **主桥**：主桥（Master Bridge）也就是IST Master，它是域内距离总根最近的交换设备。

- **端口角色**：

  根端口、指定端口、Alternate端口、Backup端口和边缘端口的作用同RSTP协议中定义。

  除边缘端口外，其他端口角色都参与MSTP的计算过程。

  同一端口在不同的生成树实例中可以担任不同的角色。

### 4、端口角色

| 端口角色      | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| 根端口        | 在非根桥上，离根桥最近的端口是本交换设备的根端口。根交换设备没有根端口。根端口负责向树根方向转发数据。 |
| 指定端口      | 对一台交换设备而言，它的指定端口是向下游交换设备转发BPDU报文的端口。 |
| Alternate端口 | 从配置BPDU报文发送角度来看，Alternate端口就是由于学习到其它网桥发送的配置BPDU报文而阻塞的端口。 从用户流量角度来看，Alternate端口提供了从指定桥到根的另一条可切换路径，作为根端口的备份端口。 |
| Backup端口    | 从配置BPDU报文发送角度来看，Backup端口就是由于学习到自己发送的配置BPDU报文而阻塞的端口。 从用户流量角度来看，Backup端口作为指定端口的备份，提供了另外一条从根节点到叶节点的备份通路。 |
| Master端口    | 1、 Master端口是MST域和总根相连的所有路径中最短路径上的端口，它是交换设备上连接MST域到总根的端口。 2、 Master端口是域中的报文去往总根的必经之路。 3、 Master端口是特殊域边缘端口，Master端口在CIST上的角色是Root Port，在其它各实例上的角色都是Master端口。 |
| 域边缘端口    | 域边缘端口是指位于MST域的边缘并连接其它MST域或SST的端口。    |
| 边缘端口      | 1、如果指定端口位于整个域的边缘，不再与任何交换设备连接，这种端口叫做边缘端口。2、 边缘端口一般与用户终端设备直接连接。 3、 端口使能MSTP功能后，会默认启用边缘端口自动探测功能，当端口在（2 × Hello Timer + 1）秒的时间内收不到BPDU报文，自动将端口设置为边缘端口，否则设置为非边缘端口。 |

### 5、端口状态

MSTP定义的端口状态与RSTP协议中定义相同。

> 注意：
>
> 根端口、Master端口、指定端口和域边缘端口支持Forwarding、Learning和Discarding状态
>
> Alternate端口和Backup端口仅支持Discarding状态。

## 四、MSTP实验

### 1、实验拓扑

附件为实验文件

[mstp.zip](mstp-20250619195123-bormijy.zip)


![在这里插入图片描述](./11、MSTP.assets/15683a34193dfa03c2d6f42b6060fd7b.png)

### 2、现状分析

某公司的总部包含4个部门，为了增加网络的可靠性，需要所在的交换机上配置MSTP，确保网络不会出现环路问题，同时实现负载均衡。

### 3、网络设计

- 搭建网络拓扑，配置VLAN，Trunk，链路聚合。
- 在4台交换机上配置MSTP，在交换机SW1创建两个实例，将vlan10，vlan20划分到实例1中，将vlan30，vlan40划分到实列2中。
- 通过配置MSTP，使实实例1和2的MSTI具有不同的根桥。SW1是实例1的根桥（优先级为4096），是实例2的次根桥（优先级为8192）；SW2是实例2的根桥（优先级为4096），是实例1的次根桥（优先级为8192）。- 对以上配置逐项进行测试，确保局域网中没有环路。

### 4、项目实施

### 5、MSTP的配置

SW1-SW4，配置STP模式为MSTP，配置MSTP域（SW1-SW4执行相同的命令）
```bash
[sw1]vlan batch 10 20 30 40   //创建VLAN
[sw1]stp mode mstp		//STP的模式改为MSTP
[sw1]stp region-configuration   //进入MST域视图
[sw1-mst-region]region-name pokes01   //MSTP域的名称pokes01
[sw1-mst-region]revision-level 1   //域的修订级别，默认MST域的修订级别为0
[sw1-mst-region]instance 1 vlan 10 20   //SMST实列和vlan映射关系
[sw1-mst-region]instance 2 vlan 30 40
[sw1-mst-region]active region-configuration   //激活MSTP域配置
```
纯净版便于复制

```bash
vlan batch 10 20 30 40
stp mode mstp
stp region-configuration
region-name pokes01
revision-level 1
instance 1 vlan 10 20
instance 1 vlan 30 40
active region-configuration
```

### 6、链路聚合

```bash
[sw1]int Eth-Trunk 1
[sw1-Eth-Trunk1]trunkport GigabitEthernet 0/0/1 to 0/0/2
[sw1-Eth-Trunk1]port link-type trunk
[sw1-Eth-Trunk1]port trunk allow-pass vlan 10 20 30 40

[sw2]int Eth-Trunk 1
[sw2-Eth-Trunk1]trunkport GigabitEthernet 0/0/1 to 0/0/2
[sw2-Eth-Trunk1]port link-type trunk
[sw2-Eth-Trunk1]port trunk allow-pass vlan 10 20 30 40
```

### 7、接入层和核心层的trunk配置

```bash
[sw1-GigabitEthernet0/0/3]dis th
interface GigabitEthernet0/0/3
 port link-type trunk
 port trunk allow-pass vlan 10 20

[sw1-GigabitEthernet0/0/4]dis th
interface GigabitEthernet0/0/4
 port link-type trunk
 port trunk allow-pass vlan 30 40

[sw2-GigabitEthernet0/0/3]dis th
#
interface GigabitEthernet0/0/3
 port link-type trunk
 port trunk allow-pass vlan 30 40

[sw1-GigabitEthernet0/0/3]dis th
#
interface GigabitEthernet0/0/4
 port link-type trunk
 port trunk allow-pass vlan 10 20
 
[sw3-GigabitEthernet0/0/1]dis th
#
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 10 20

[sw3-GigabitEthernet0/0/2]dis th
#
interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 10 20

[sw4-GigabitEthernet0/0/1]dis th
#
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 30 40

[sw4-GigabitEthernet0/0/2]dis th
#
interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan 30 40
```

### 8、接入层的vlan配置
sw3

```bash
interface GigabitEthernet0/0/12
 port link-type access
 port default vlan 10
#
interface GigabitEthernet0/0/13
 port link-type access
 port default vlan 20
```

sw4

```bash
interface GigabitEthernet0/0/14
 port link-type access
 port default vlan 30
#
interface GigabitEthernet0/0/15
 port link-type access
 port default vlan 40
```
至此已经基本配置完毕了，接下来我们需要调试SMTP的优先级

### 9、调试SMTP的优先级
```bash
[SW1]stp instance 0 priority 4096
[sw1]stp instance 1 priority 4096
[sw1]stp instance 2 priority 8192

[sw2]stp instance 0 priority 8192
[sw2]stp instance 1 priority 8192
[sw2]stp instance 2 priority 4096
```
### 10、查看信息

```bash
[sw1]dis stp region-configuration 
 Oper configuration
   Format selector    :0     	  #格式选择器
   Region name        :pokes01    #配置名称
   Revision level     :1	 	  #修订级别

   Instance   VLANs Mapped		#实列和VLAN映射表
      0       1 to 9, 11 to 19, 21 to 29, 31 to 39, 41 to 4094
      1       10, 20
      2       30, 40



[sw1]dis stp topology-change 
 CIST topology change information     #CIST拓扑变化信息
   Number of topology changes             :42	#从MSTP初始化开始，发送拓扑变化的总计次数
   Time since last topology change        :0 days 0h:0m:48s	#距离最近一次变化时间
   Topology change initiator(notified)    :Eth-Trunk1		#收到报文而触发的端口
   Topology change last received from     :4c1f-cce1-3e13	#拓扑变化报文来源的桥MAC地址
   Number of generated topologychange traps :   21	#产生的告警次数
   Number of suppressed topologychange traps:   2	#抑制的告警次数

 MSTI 1 topology change information
   Number of topology changes             :25
   Time since last topology change        :0 days 0h:0m:48s
   Topology change initiator(notified)    :Eth-Trunk1
   Topology change last received from     :4c1f-cce1-3e13
   Number of generated topologychange traps :   21
   Number of suppressed topologychange traps:   2

 MSTI 2 topology change information
   Number of topology changes             :2
   Time since last topology change        :0 days 0h:0m:16s
   Topology change initiator(detected)    :GigabitEthernet0/0/4
   Number of generated topologychange traps :   21
   Number of suppressed topologychange traps:   2

```
