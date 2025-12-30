# 07.给予接口的DHCP

‍

## 适用场景

> - 基于接口的DHCP，仅支持DHCP服务器与DHCP客户端在同一网段。
> - DHCP服务器与客户端不在同一网段时，就需要DHCP中继。

## 基本配置

> 重点：
>
> - 三层交换机上开启全局`dhcp enable`
> - 进入vlanif接口配置

```python
interface Vlanif10
 ip address 10.5.1.1 255.255.255.0
 dhcp select interface
 dhcp server static-bind ip-address 10.5.1.100 mac-address 5489-98b7-7378
 dhcp server excluded-ip-address 10.5.1.200 10.5.1.254
 dhcp server lease day 0 hour 0 minute 5
 dhcp server dns-list 114.114.114.114
```


> 注释：
> - 绑定MAC静态IP：dhcp server static-bind ip-address 10.5.1.100 mac-address 5489-98b7-7378
> - 排除保留的地址：dhcp server excluded-ip-address 10.5.1.200 10.5.1.254
> - 设置租约：dhcp server lease day 0 hour 0 minute 5
> - #配置DNS：dhcp server dns-list 114.114.114.114  



## 实验部分

###  1、实验环境

要求：PC2、PC1能正常获取到IP地址

![在这里插入图片描述](./07、给予接口的DHCP.assets/c08460bafc0c7616a5668134b4c4533b.png)



注意：<font color='red'>以下操作全部是在核心交换机LSW1上配置</font>

### 2、全局开启dhcp

```bash
dhcp enable 
```

### 3、划分vlan10、vlan20

```bash
vlan batch 10 20

interface GigabitEthernet0/0/2
 port link-type access
 port default vlan 10
 
interface GigabitEthernet0/0/3
 port link-type access
 port default vlan 20
 q
```

## 4、接口DHCP的配置

这一步是在vlan虚接口里面配置的。

```bash
interface Vlanif10
 ip address 10.5.1.1 255.255.255.0
 dhcp select interface
 dhcp server static-bind ip-address 10.5.1.100 mac-address 5489-98b7-7378
 dhcp server excluded-ip-address 10.5.1.200 10.5.1.254
 dhcp server lease day 0 hour 0 minute 5
 dhcp server dns-list 114.114.114.114

 
interface Vlanif20
 ip address 10.5.2.1 255.255.255.0
 dhcp select interface
 dhcp server static-bind ip-address 10.5.2.100 mac-address 5489-98FC-793A
 dhcp server excluded-ip-address 10.5.2.200 10.5.2.254
 dhcp server lease day 0 hour 0 minute 5
 dhcp server dns-list 114.114.114.114
```

注释：

> interface Vlanif10
>
> #vlan地址
>
> ip address 10.5.1.1 255.255.255.0
>
> #选择基于接口的dhcp类型
>
> dhcp select interface
>
> #绑定MAC静态IP
>
> dhcp server static-bind ip-address 10.5.1.100 mac-address 5489-98b7-7378
>
> #排除保留的地址
>
> dhcp server excluded-ip-address 10.5.1.200 10.5.1.254
>
> #设置租约
>
> dhcp server lease day 0 hour 0 minute 5
>
> #配置DNS
>
> dhcp server dns-list 114.114.114.114

## 5、相关查询验证

查询vlan10的IP分配情况

```bash
<hexin-swh>dis ip pool interface vlanif10 
  Pool-name      : vlanif10
  Pool-No        : 0
  Lease          : 0 Days 0 Hours 5 Minutes
  Domain-name    : -
  DNS-server0    : 114.114.114.114 
  NBNS-server0   : -               
  Netbios-type   : -               
  Position       : Interface       Status           : Unlocked
  Gateway-0      : 10.5.1.1        
  Mask           : 255.255.255.0
  VPN instance   : --
 -----------------------------------------------------------------------------
         Start           End     Total  Used  Idle(Expired)  Conflict  Disable
 -----------------------------------------------------------------------------
        10.5.1.1      10.5.1.254   253     1        197(0)         0       55
 -----------------------------------------------------------------------------


<hexin-swh>dis ip pool interface vlanif20 
  Pool-name      : vlanif20
  Pool-No        : 1
  Lease          : 0 Days 0 Hours 5 Minutes
  Domain-name    : -
  DNS-server0    : 114.114.114.114 
  NBNS-server0   : -               
  Netbios-type   : -               
  Position       : Interface       Status           : Unlocked
  Gateway-0      : 10.5.2.1        
  Mask           : 255.255.255.0
  VPN instance   : --
 -----------------------------------------------------------------------------
         Start           End     Total  Used  Idle(Expired)  Conflict  Disable
 -----------------------------------------------------------------------------
        10.5.2.1      10.5.2.254   253     1        197(0)         0       55
 -----------------------------------------------------------------------------

```


### MAC绑定查看

```bash
<hexin-swh>dis ip pool interface vlanif20 all 
  Pool-name      : vlanif20
  Pool-No        : 1
  Lease          : 0 Days 0 Hours 5 Minutes
  Domain-name    : -
  DNS-server0    : 114.114.114.114 
  NBNS-server0   : -               
  Netbios-type   : -               
  Position       : Interface       Status           : Unlocked
  Gateway-0      : 10.5.2.1        
  Mask           : 255.255.255.0
  VPN instance   : --
 -----------------------------------------------------------------------------
         Start           End     Total  Used  Idle(Expired)  Conflict  Disable
 -----------------------------------------------------------------------------
        10.5.2.1      10.5.2.254   253     1        197(0)         0       55
 -----------------------------------------------------------------------------

  Network section : 
  --------------------------------------------------------------------------
  Index              IP               MAC      Lease   Status  
  --------------------------------------------------------------------------
      1        10.5.2.2                 -          -   Idle       
      2        10.5.2.3                 -          -   Idle       
      3        10.5.2.4                 -          -   Idle       
............................................................................
     97       10.5.2.98                 -          -   Idle       
     98       10.5.2.99                 -          -   Idle       
     99      10.5.2.100    5489-98fc-793a          -   Static-bind
    100      10.5.2.101                 -          -   Idle       
    101      10.5.2.102                 -          -   Idle       
    102      10.5.2.103                 -          -   Idle       
............................................................................
```





