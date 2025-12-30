# 企业内部DHCP中继实验

# 企业内部DHCP中继实验

## 一、实验拓扑

![1652193685790](1652193685790-20250619201141-2w79du9.png)

## 二、配置全网互通

### AR1配置

```
[Huawei]sy AR1
[AR1]interface GigabitEthernet0/0/0
[AR1-GigabitEthernet0/0/0]
[AR1-GigabitEthernet0/0/0] ip address 192.168.30.1 255.255.255.0
[AR1-GigabitEthernet0/0/0]

##回执路由
ip route-static 192.168.0.0 255.255.0.0 192.168.30.254
```

### SW1配置

```
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan all


interface GigabitEthernet0/0/2
 port link-type trunk
 port trunk allow-pass vlan all
 
interface GigabitEthernet0/0/3
 port link-type trunk
 port trunk allow-pass vlan all
 

vlan batch 10 20 30 60

interface Vlanif10
 ip address 192.168.10.254 255.255.255.0
interface Vlanif20
 ip address 192.168.20.254 255.255.255.0
interface Vlanif30
 ip address 192.168.30.254 255.255.255.0
interface Vlanif60
 ip address 192.168.60.254 255.255.255.0
 
```

### SW2配置

```
vlan 10
q

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan all

interface Ethernet0/0/1
 port link-type access
 port default vlan 10

```

### SW3配置

```
vlan 20
q

interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan 2 to 4094

interface Ethernet0/0/1
 port link-type access
 port default vlan 20
```

### SW5

```
interface GigabitEthernet0/0/1
 port link-type trunk
 port trunk allow-pass vlan all

interface Ethernet0/0/1
 port link-type access
 port default vlan 60
 
interface Ethernet0/0/2
 port link-type access
 port default vlan 60
```

## 三、接入DHCP服务器

### 利用cloud链接VM虚拟机

利用cloud链接VM虚拟机的server2008服务器，cloud增加两个端口1和2：

- 1用来链接交换机SW5
- 2用来桥接server2008

![1652191247763](1652191247763-20250619201141-azbb9qj.png)

- Server2008单网卡，设置到vmnet1网络
- Server2008的IP地址设置为192.168.60.100/24，网关：192.168.60.254

![1652191197283](1652191197283-20250619201141-fk8f6j4.png)

### 搭建DHCP服务器

在server2008服务器上搭建DHCP服务：添加角色—勾选DHCP，下一步直到完成。

配置三个作用域：分别是vlan10、vlan20、vlan60(服务器)

![1652191586002](1652191586002-20250619201141-qt4ym4k.png)

## 四、配置DHCP中继

在SW1上面配置DHCP中继

```
[SW1]dhcp enable

[SW1-Vlanif10] dhcp select relay 
[SW1-Vlanif10] dhcp relay server-ip 192.168.60.100
[SW1-Vlanif10]q

[SW1]int vlan20
[SW1-Vlanif20] dhcp select relay
[SW1-Vlanif20] dhcp relay server-ip 192.168.60.100
[SW1-Vlanif20] q

[SW1]int vlan60
[SW1-Vlanif20] dhcp select relay
[SW1-Vlanif20] dhcp relay server-ip 192.168.60.100
[SW1-Vlanif20] q
```

## 五、验证结果

![1652194190179](1652194190179-20250619201141-rixamtn.png)

![1652194206659](1652194206659-20250619201141-rx9mf7n.png)

![1652194222450](1652194222450-20250619201141-ijxlafj.png)
