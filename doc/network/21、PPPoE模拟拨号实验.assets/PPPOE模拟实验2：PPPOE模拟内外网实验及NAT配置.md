## 二、PPPOE模拟实验2：PPPOE模拟内外网实验及NAT配置

### 1、实验环境

![在这里插入图片描述](./PPPOE模拟实验2：PPPOE模拟内外网实验及NAT配置.assets/3439af8e48327bc54e4dfae03d2423a9-1766983389699-3.png)
pppoe-client上面的接口信息

```bash
[AR1]dis ip interface brief 
*down: administratively down
^down: standby
(l): loopback
(s): spoofing
The number of interface that is UP in Physical is 2
The number of interface that is DOWN in Physical is 1
The number of interface that is UP in Protocol is 1
The number of interface that is DOWN in Protocol is 2

Interface                         IP Address/Mask      Physical   Protocol  
GigabitEthernet0/0/0              unassigned           up         down      
GigabitEthernet0/0/1              192.168.1.254/24     down       down      
NULL0                             unassigned           up         up(s)     

```
配置了基于接口的DHCP

```bash
interface GigabitEthernet0/0/1
 ip address 192.168.1.254 255.255.255.0 
 dhcp select interface
 dhcp server dns-list 8.8.8.8 
 dhcp server domain-name pokes.com
```
<font color='red'>注意事项：AR1、AR2的物理接口g0/0/0不配地址.</font>

### 2、pppoe-server的配置

#### 2.1、pppoe-server配置地址池

```bash
[pppoe-server]ip pool pokes            #创建名为pokes的地址池，名字可以随便起，后面要调用
Info: It's successful to create an IP address pool.
[pppoe-server-ip-pool-pokes]network 10.1.12.0 mask 24   #地址池为10.1.12.0/24
[pppoe-server-ip-pool-pokes]dis th
[V200R003C00]
#
ip pool pokes
 network 10.1.12.0 mask 255.255.255.0 
#
return
[pppoe-server-ip-pool-pokes]q
```

#### 2.2、配置虚拟口关联地址池

配置虚拟口关联地址池，即创建Virtual-Template 1模版。

```bash
[pppoe-server]interface Virtual-Template 1    #创建虚拟接口1
[pppoe-server-Virtual-Template1]ip add 10.1.12.2 24	           #虚拟接口1的地址
[pppoe-server-Virtual-Template1]ppp authentication-mode chap   #认证类型
[pppoe-server-Virtual-Template1]remote address pool pokes      #客户端的地址池pokes
[pppoe-server-Virtual-Template1]dis th
interface Virtual-Template1
 ppp authentication-mode chap 
 remote address pool pokes
 ip address 10.1.12.2 255.255.255.0
 
[pppoe-server]int g0/0/0	
[pppoe-server-GigabitEthernet0/0/0]pppoe-server bind virtual-template 1   #将虚拟接口1关联到g0/0/0接口
[pppoe-server-GigabitEthernet0/0/0]dis th
[V200R003C00]
#
interface GigabitEthernet0/0/0
 pppoe-server bind Virtual-Template 1
#
return
[pppoe-server-GigabitEthernet0/0/0]
```

#### 2.3、创建pppoe拨号的账号

按理我们应该创建pppoe拨号的账号。
这里为了演示拨号失败，我们这里先不新建账号，后面再新建。

### 3、pppoe-client的配置

```bash
[pppoe-client]dialer-rule   
[pppoe-client-dialer-rule]dialer-rule 1 ?
  acl   Permit or deny based on access-list   
  ip    Ip
  ipv6  Ipv6	
[pppoe-client-dialer-rule]dialer-rule 1 ip permit   #创建拨号规则，允许ip流量触发拨号
```



```bash
[pppoe-client]interface Dialer 1
Jul 15 2021 18:55:22-08:00 pppoe-client %%01IFPDT/4/IF_STATE(l)[0]:Interface Dia
ler1 has turned into UP state.
[pppoe-client-Dialer1]ip add	
[pppoe-client-Dialer1]ip address ppp	
[pppoe-client-Dialer1]ip address ppp-negotiate  #地址采用ppp协商

[pppoe-client]interface Dialer 1                #创建接口拨号组1
[pppoe-client-Dialer1]ip address ppp-negotiate  #ip地址采用ppp协商
[pppoe-client-Dialer1]dialer user zhprny        #此用户不用于认证，是标识作用以及和dialer绑定
[pppoe-client-Dialer1]dialer bundle 1           #设备通过Dialer bundle将物理接口与拨号接口关联起来。
[pppoe-client-Dialer1]dialer-group 1             #放到一个拨号访问组1中
[pppoe-client-Dialer1]ppp chap user pokes        #指定dialer1接口的编号，拨号账号
[pppoe-client-Dialer1]ppp chap password 123456   #拨号的密码


[pppoe-client-Dialer1]dis th
[V200R003C00]
#
interface Dialer1
 link-protocol ppp
 ppp chap user pokes
 ppp chap password cipher %$%$I/!'WCyd<7p[~8;,>51L,$sl%$%$
 ip address ppp-negotiate
 dialer user zhprny
 dialer bundle 1
 dialer-group 1
 
[pppoe-client-GigabitEthernet0/0/0]
Jul 15 2021 19:07:54-08:00 pppoe-client %%01IFNET/4/LINK_STATE(l)[0]:The line pr
otocol PPP on the interface Dialer1:0 has entered the UP state.  #PPP已进入启动状态
[pppoe-client-GigabitEthernet0/0/0]
Jul 15 2021 19:07:54-08:00 pppoe-client %%01IFNET/4/LINK_STATE(l)[1]:The line pr
otocol PPP on the interface Dialer1:0 has entered the DOWN state. #PPP已进入关闭状态

#不停的循环。。。。
```
#原因是没有认证成功，因为我们在PPPOE-server上面还没有创建认证用户和密码

### 4、pppoe服务器上新建认证用户
我们到服务器上直接新建认证用户：
```bash
[pppoe-server]aaa
[pppoe-server-aaa]local-user pokes password cipher 123456
Info: Add a new user.
[pppoe-server-aaa]local-user pokes service-type ppp    #类型为ppp
```

### 5、客户端验证结果
#### 5.1、认证成功信息
然后客户端就会出现认证成功的提示：
```bash
[pppoe-client-GigabitEthernet0/0/0]
Jul 15 2021 19:09:23-08:00 pppoe-client %%01IFNET/4/LINK_STATE(l)[10]:The line p
rotocol PPP on the interface Dialer1:0 has entered the UP state. 
[pppoe-client-GigabitEthernet0/0/0]
Jul 15 2021 19:09:23-08:00 pppoe-client %%01IFNET/4/LINK_STATE(l)[11]:The line p
rotocol PPP IPCP on the interface Dialer1:0 has entered the UP state. 
[pppoe-client-GigabitEthernet0/0/0]q
[pppoe-client]dis ip in b
*down: administratively down
^down: standby
(l): loopback
(s): spoofing
The number of interface that is UP in Physical is 4
The number of interface that is DOWN in Physical is 0
The number of interface that is UP in Protocol is 3
The number of interface that is DOWN in Protocol is 1

Interface                         IP Address/Mask      Physical   Protocol  
Dialer1                           10.1.12.254/32       up         up(s)     #拿到了PPPOE服务器上的地址
GigabitEthernet0/0/0              unassigned           up         down      
GigabitEthernet0/0/1              192.168.1.254/24     up         up        
NULL0                             unassigned           up         up(s) 
```

#### 5.2、pppoe-server 信息
```bash
<pppoe-server>dis interface Virtual-Template 1
Virtual-Template1 current state : UP
Line protocol current state : UP
Last line protocol up time : 2021-07-15 19:09:22 UTC-08:00
Description:HUAWEI, AR Series, Virtual-Template1 Interface
Route Port,The Maximum Transmit Unit is 1492, Hold timer is 10(sec)
Internet Address is 10.1.12.2/24
Link layer protocol is PPP
LCP initial
Physical is None
Current system time: 2021-07-15 20:27:28-08:00
    Last 300 seconds input rate 0 bits/sec, 0 packets/sec
    Last 300 seconds output rate 0 bits/sec, 0 packets/sec
    Realtime 0 seconds input rate 0 bits/sec, 0 packets/sec
    Realtime 0 seconds output rate 0 bits/sec, 0 packets/sec
    Input: 0 bytes
    Output:0 bytes
    Input bandwidth utilization  :    0%
    Output bandwidth utilization :    0%

<pppoe-server>

```

#### 5.3、pppoe-client信息

```bash
<pppoe-client>dis interface Dialer 1
Dialer1 current state : UP
Line protocol current state : UP (spoofing)
Description:HUAWEI, AR Series, Dialer1 Interface
Route Port,The Maximum Transmit Unit is 1500, Hold timer is 10(sec)
Internet Address is negotiated, 10.1.12.254/32
Link layer protocol is PPP
LCP initial
Physical is Dialer
Current system time: 2021-07-15 20:23:56-08:00
    Last 300 seconds input rate 0 bits/sec, 0 packets/sec
    Last 300 seconds output rate 0 bits/sec, 0 packets/sec
    Realtime 0 seconds input rate 0 bits/sec, 0 packets/sec
    Realtime 0 seconds output rate 0 bits/sec, 0 packets/sec
    Input: 0 bytes
    Output:0 bytes
    Input bandwidth utilization  :    0%
    Output bandwidth utilization :    0%
Bound to Dialer1:0:
Dialer1:0 current state : UP ,
Line protocol current state : UP

Link layer protocol is PPP
LCP opened, IPCP opened
Packets statistics:
  Input packets:0,  0 bytes
  Output packets:4, 336 bytes
  FCS error packets:0
  Address error packets:0
  Control field control error packets:0


<pppoe-client>
```
### 6、NAT的配置

用PC2直接ping 10.1.12.254是可以通的。10.1.12.254是AR1的g0/0/0口获取到的地址，其实就是我们常说的WAN口地址。
```bash
PC2>ping 10.1.12.254

Ping 10.1.12.254: 32 data bytes, Press Ctrl_C to break
From 10.1.12.254: bytes=32 seq=1 ttl=255 time=63 ms
From 10.1.12.254: bytes=32 seq=2 ttl=255 time=31 ms
From 10.1.12.254: bytes=32 seq=3 ttl=255 time=47 ms
From 10.1.12.254: bytes=32 seq=4 ttl=255 time=31 ms
From 10.1.12.254: bytes=32 seq=5 ttl=255 time=47 ms

--- 10.1.12.254 ping statistics ---
  5 packet(s) transmitted
  5 packet(s) received
  0.00% packet loss
  round-trip min/avg/max = 31/43/63 ms

PC2>ping 10.1.12.2

Ping 10.1.12.2: 32 data bytes, Press Ctrl_C to break
Request timeout!
Request timeout!
Request timeout!
Request timeout!
Request timeout!

--- 10.1.12.2 ping statistics ---
  5 packet(s) transmitted
  0 packet(s) received
  100.00% packet loss
#但是无法ping通10.1.12.2
```
无法ping通10.1.12.2的原因是：我们没有做NAT .接下来我们在pppoe-client上面做NAT


#### 6.1、这里配置规则2000
```bash
[pppoe-client]acl number 2000	
[pppoe-client-acl-basic-2000]rule permit source 192.168.1.0 0.0.0.255
```
#### 6.2、将规则2000绑定到接口
如下接口信息，<font color='red'>需要注意的是pppoe的接口是Dialer1，并不是GigabitEthernet0/0/0口。我们必须将规则绑定在Dialer1口，最容易犯错的就是直接绑定在g0/0/0口。</font>

```bash
[pppoe-client]dis ip int b
*down: administratively down
^down: standby
(l): loopback
(s): spoofing
The number of interface that is UP in Physical is 4
The number of interface that is DOWN in Physical is 0
The number of interface that is UP in Protocol is 3
The number of interface that is DOWN in Protocol is 1

Interface                         IP Address/Mask      Physical   Protocol  
Dialer1                           10.1.12.254/32       up         up(s)     
GigabitEthernet0/0/0              unassigned           up         down      
GigabitEthernet0/0/1              192.168.1.254/24     up         up        
NULL0                             unassigned           up         up(s)     
[pppoe-client]
```

```bash
[pppoe-client]int Dialer 1	
[pppoe-client-Dialer1]nat outbound 2000
[pppoe-client-Dialer1]dis th
[V200R003C00]
#
interface Dialer1
 link-protocol ppp
 ppp chap user pokes
 ppp chap password cipher %$%$I/!'WCyd<7p[~8;,>51L,$sl%$%$
 ip address ppp-negotiate
 dialer user zhprny
 dialer bundle 1
 dialer-group 1
 nat outbound 2000
#
return
[pppoe-client-Dialer1]
```
接下来我们就可以ping通10.1.12.2 了。

```bash
PC2>ping 10.1.12.2

Ping 10.1.12.2: 32 data bytes, Press Ctrl_C to break
From 10.1.12.2: bytes=32 seq=1 ttl=254 time=31 ms
From 10.1.12.2: bytes=32 seq=2 ttl=254 time=32 ms
From 10.1.12.2: bytes=32 seq=3 ttl=254 time=46 ms
From 10.1.12.2: bytes=32 seq=4 ttl=254 time=32 ms
From 10.1.12.2: bytes=32 seq=5 ttl=254 time=31 ms

--- 10.1.12.2 ping statistics ---
  5 packet(s) transmitted
  5 packet(s) received
  0.00% packet loss
  round-trip min/avg/max = 31/34/46 ms
```