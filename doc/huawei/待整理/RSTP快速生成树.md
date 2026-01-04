# RSTP快速生成树

## 基本概述

> RSTP（<font color='red'>Rapid Spanning Tree Protocol</font>，<font color='orange'>快速生成树协议</font>）是一种用于局域网中的链接层协议，旨在防止数据链路层的环路问题，确保网络的稳定性和可靠性。它通过一定的算法，<font color='green'>将网络中的环形结构修剪成无环路的树型结构</font>，从而避免报文在环路中的无限循环和广播风暴。

## 工作原理

> - 核心算法：<font color='orange'>RSTP的核心是生成树算法</font>，该算法能够动态地发现并维护一个无环路的树型拓扑结构。在网络结构发生变化时，如链路故障或恢复，RSTP能够迅速重新计算并更新网络拓扑，以保持网络的稳定性。
> 
> - 端口角色：RSTP定义了多种端口角色，包括根端口、指定端口、替代端口和备份端口等。这些端口角色根据网络拓扑的变化而动态调整，以确保网络中不存在环路，并且能够提供冗余路径以提高网络的可靠性。
> 
> - 状态迁移：RSTP的端口状态包括<font color='red'>丢弃、学习和转发</font>三种。端口状态的迁移是根据接收到的配置消息和其他桥接器的信息来确定的。这种状态迁移机制使得RSTP能够在网络结构发生变化时迅速做出响应。

## 收敛机制

> - P/A协商机制：RSTP采用了一种称为<font color='red'>P/A（Proposal/Agreement）</font>的协商机制来加速端口状态的收敛。当网络结构发生变化时，RSTP交换机之间通过<font color='orange'>发送提议和同意的配置消息来快速确定新的端口角色和状态</font>，从而避免了传统STP中长时间的等待和延迟。
> 
> - 边缘端口特性：RSTP还引入了边缘端口的概念。边缘端口是指直接与终端设备连接的端口，它们不参与生成树计算，可以立即进入转发状态。这大大减少了网络收敛所需的时间，并提高了网络的整体性能。

## 兼容性与配置

> - 向下兼容：<font color='red'>RSTP完全向下兼容传统的STP协议，这意味着在混合运行STP和RSTP的网络环境中，两者可以无缝协作。</font>
> - 配置方法：RSTP的配置相对简单，可以通过命令行界面或图形用户界面进行配置。配置内容包括启用RSTP模式、设置端口角色和状态、调整定时器参数等。

## RSTP的出现解决了什么问题？

STP协议虽然解决了链路闭合引起的死循环问题，但是在端口从阻塞状态到转发状态间经过了一个只学习MAC地址但不参与转发的过程，产生了转发延时(<font color='red'>**默认15秒**</font>)，从而使得生成树的收敛过程需要较长的时间，一般是转发延时的两倍。

> **STP的不足和缺点**： 
> 
> - STP没有细致区分端口状态和端口角色，不利于初学者学习及部署。
> - 从用户角度来看，Listening、Learning和Blocking状态并没有区别，都同样不转发用户流量。
> - 从使用和配置角度来讲，端口之间最本质的区别并不在于端口状态，而是在于端口扮演的角色。 
> - STP算法是被动的算法，依赖定时器等待的方式判断拓扑变化，收敛速度慢。
> - STP算法要求在稳定的拓扑中，根桥主动发出配置BPDU报文，而其他设备再进行处理，最终传遍整个STP网络

为了解决STP收敛时间过长的缺点，IEEE又推出了802.1w标准，定义了<font color='orange'>RSTP(快速生成树)协议</font>。RSTP协议在网络配置参数发生变化时，能够显著的<font color='red'>减少网络的收敛时间（秒级）</font>。

由于RSTP是从STP发展而来的,其<font color='red'>与STP协议保持高度的兼容性</font>。<font color='orange'>这意味着在混合运行STP和RSTP的网络环境中，两者可以无缝协作。</font>

> - 提高收敛速度（秒级）
> - 与STP协议保持高度的兼容性

## 为什么收敛速度快？

STP收敛过程：【阻塞->侦听->学习->转发】

<font color='red'>RSTP协议规定，在某些情况下，处于阻塞状态的端口不必经历：

```python
【阻塞->侦听->学习->转发】
```
这一个过程，就可以直接进入转发状态.</font>

RSTP协议只有以下三种:
>1.丢弃(Discarding)：RSTP将STP中的<font color='red'>阻塞、禁用、侦听</font>统称为丢弃模式。
>2.学习(Learning)：拓扑有所变动情况下，端口处于学习状态并学习MAC地址,将其添加到MAC地址表。
>3.转发(Forwarding)：在网络拓扑稳定后，端口处于转发状态，并开始转发数据包。

对比后会发现RSTP协议收敛过程：【丢弃->学习->转发】，解决了数据同步过慢的问题所在。

### RSTP与STP的关键区别

> - **更快的收敛速度**：
>   - 端口角色和状态简化，通过**Proposal/Agreement机制**（P/A机制）实现快速收敛（秒级）。
>   - 取消了STP的**Listening**和**Learning**状态，仅保留**Discarding**、**Learning**、**Forwarding**三种状态。
> - **端口角色扩展**：
>   - **Root Port**（根端口）：最优路径到根桥的端口。
>   - **Designated Port**（指定端口）：每个网段转发流量的最佳端口。
>   - **Alternate Port**（替代端口）：根端口的备份（阻塞状态）。
>   - **Backup Port**（备份端口）：指定端口的备份（华为私有实现可能支持）。

### 华为RSTP配置命令

```bash
# 启用RSTP（华为交换机默认模式可能是MSTP，需切换）
system-view
stp mode rstp      # 设置模式为RSTP
stp enable         # 全局开启生成树

# 配置根桥（可选）
stp root primary   # 强制当前交换机为根桥
stp root secondary # 设置为备用根桥

# 调整端口开销和优先级（影响拓扑计算）
interface GigabitEthernet0/0/1
 stp cost 2000     # 修改端口开销（值越小优先级越高）
 stp port priority 64  # 修改端口优先级（0-240，步长16）

# 边缘端口配置（连接终端时避免触发拓扑变更）
interface GigabitEthernet0/0/2
 stp edged-port enable  # 启用边缘端口（类似PortFast）

# 可选：调整Hello Time、Forward Delay等计时器
stp timer hello 2      # Hello时间（默认2秒）
stp timer forward-delay 15  # Forward Delay（建议保持默认）
```

### **华为RSTP特性**

1、**BPDU保护**：防止边缘端口收到BPDU导致网络震荡。

```bash
stp bpdu-protection
```

2、**根保护**：防止非法设备成为根桥。

```bash
interface GigabitEthernet0/0/1
 stp root-protection
```

3、**环路保护**：针对Alternate端口，防止单向链路故障导致环路。

```bash
interface GigabitEthernet0/0/3
 stp loop-protection
```

## RSTP实验
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f63141a2983c4e6ea58c8ae6b32587fc.png)

### 设置根桥

```bash
[sw1]stp mode rstp   	#stp模式切换为rstp
[sw1]stp root primary	#配置为根桥
```

### 设置备用根桥

```bash
[sw2]stp mode rstp 
[sw2]stp root secondary 

[sw2]display stp brief   #查看
 MSTID  Port                        Role  STP State     Protection
   0    GigabitEthernet0/0/1        DESI  FORWARDING      NONE
   0    GigabitEthernet0/0/2        ROOT  FORWARDING      NONE
```

### 配置边缘端口

```bash
[sw3]interface g0/0/2
[sw3-GigabitEthernet0/0/2]stp edged-port enable 

[sw4]int g0/0/2
[sw4-GigabitEthernet0/0/2]stp edged-port enable
```

### 设置bpdu保护

```bash
[sw3]stp bpdu-protection
[sw4]stp bpdu-protection
```

>  **BPDU保护的作用**
>
>  - **防御场景**：<font color='red'>防止边缘端口（如连接PC、服务器的端口）意外接入交换机或Hub</font>，导致生成树拓扑异常震荡。
>  - **触发条件**：当<font color='red'>启用BPDU保护的边缘端口收到任何BPDU报文时，交换机将立即关闭该端口</font>（或将其置为Error-Down状态）。
>  - **典型应用**：用于接入层交换机的用户端口，确保终端设备不会干扰生成树计算。

### 设置根保护

```bash
[sw1]int g0/0/1
[sw1-GigabitEthernet0/0/1]stp root-protection

[sw1]int g0/0/2
[sw1-GigabitEthernet0/0/2]stp root-protection
```

>  **根保护的作用**
>
> - **防御场景**：防止网络中接入<font color='red'>非法交换机</font>通过发送更优的BPDU（如更高的优先级）抢占合法根桥（Root Bridge）的角色，导致网络拓扑异常震荡。
> - **触发条件**：当启用根保护的端口收到<font color='red'>更优BPDU</font>（即声称自己是根桥）时，该端口会立即进入<font color='red'>Discarding状态</font>，阻断流量并记录告警。
> - **恢复机制**：当停止接收更优BPDU后，端口会自动恢复为正常状态（需等待2倍的Forward Delay时间）。

### 故障排查

```bash
display stp brief          # 查看端口角色和状态
display stp interface GigabitEthernet0/0/1  # 检查指定端口详情
display stp root           # 显示根桥信息
display stp abnormal-port  # 查看异常端口（如BPDU保护触发）
```

### 注意事项

> - **与STP兼容性**：RSTP可兼容传统STP设备，但会回退到STP的慢收敛模式。
> - **MSTP模式**：华为交换机默认可能运行MSTP（多实例生成树），需明确切换为RSTP。
> - **拓扑变更机制**：RSTP通过**TCN（拓扑变更通知）**直接刷新MAC表，无需等待计时器超时。



通过合理配置RSTP，可以显著提升华为交换机网络的收敛速度和抗环路能力，尤其适合对延迟敏感的应用环境。实际部署时建议结合具体拓扑调整优先级和开销参数。
